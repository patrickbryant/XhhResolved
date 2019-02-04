import ROOT

import copy, sys

import optparse

parser = optparse.OptionParser()

parser.add_option('-i', '--iter',
                  dest="iteration",
                  default="0"
                  )

parser.add_option('-n', '--name',
                  dest="name",
                  default=""
                  )

parser.add_option('-d', '--nTupleDir',
                  dest="dir",
                  default="reWeightData"
                  )

#parser.add_option('-s', '--selection',
#                  dest='selection',
#                  default='trig'
#                  )

parser.add_option('-t', '--ttbarDir',
                 dest='ttbarDir',
                 default=""
                 )

parser.add_option('--ttbarShape',
                 dest='ttbarShape',
                 default=""
                 )

parser.add_option('-o', '--outputDir',
                  dest='outputDir',
                  default="XhhResolved/data/"
                  )

parser.add_option('-q', '--qcdFile',
                  dest="qcdFile",
                  default="testQCD.root",
                  )

parser.add_option('--threeTag',  dest="threeTag",  action="store_true", default=False)

o, a = parser.parse_args()

from math import sqrt
import math
from array import array
import os
if not os.path.isdir(o.outputDir):
    os.mkdir(o.outputDir)
ROOT.gROOT.SetBatch(True)




print "Making weights for iteration:",o.iteration

inFileName = o.dir
inFile = ROOT.TFile(inFileName,"READ")
print "Input file:",inFileName

if o.ttbarShape:
    ttbarShape = ROOT.TFile(o.ttbarShape,"READ")#btag f factor set to get 2b->4b shape right, but not 2b yield or 2b shape
    ttbarFile  = ROOT.TFile(o.ttbarDir,  "READ")#same btag f factor as in data processing. should get right 2b yield
    allhadShape = ROOT.TFile(o.ttbarShape.replace("ttbar","allhad"),"READ")
    allhadFile = ROOT.TFile(o.ttbarDir.replace("ttbar","allhad"),"READ")
    nonallhadShape = ROOT.TFile(o.ttbarShape.replace("ttbar","nonallhad"),"READ")
    nonallhadFile = ROOT.TFile(o.ttbarDir.replace("ttbar","nonallhad"),"READ")

if o.threeTag: 
    tag = "Three"
else: 
    tag = "Four"

outFile = ROOT.TFile(o.outputDir+"/weights2bto"+("3" if o.threeTag else "4")+"b"+o.name+str(int(o.iteration)+1)+".root","RECREATE")
outFile.cd()





# variables = []
def get(rootFile, path):
    obj = rootFile.Get(path)
    if str(obj) == "<ROOT.TObject object at 0x(nil)>": 
        rootFile.ls()
        print 
        print "ERROR: Object not found -", rootFile, path
        sys.exit()

    else: return obj


def do_variable_rebinning(hist,bins):
    a=hist.GetXaxis()
    newhist=ROOT.TH1F(hist.GetName(),
                      hist.GetTitle()+";"+hist.GetXaxis().GetTitle()+";"+hist.GetYaxis().GetTitle(),
                      len(bins)-1,
                      array('d',bins))

    #histErrorOption = hist.GetBinErrorOption()
    #newhist.SetBinErrorOption(histErrorOption)
    newhist.Sumw2()
    newa=newhist.GetXaxis()

    for b in range(1, hist.GetNbinsX()+1):
        newb             = newa.FindBin(a.GetBinCenter(b))

        # Get existing new content (if any)
        val              = newhist.GetBinContent(newb)
        err              = newhist.GetBinError(newb)

        # Get content to add
        ratio_bin_widths = newa.GetBinWidth(newb)/a.GetBinWidth(b)
        val              = val+hist.GetBinContent(b)/ratio_bin_widths
        err              = math.sqrt(err*err+hist.GetBinError(b)/ratio_bin_widths*hist.GetBinError(b)/ratio_bin_widths)
        newhist.SetBinContent(newb,val)
        newhist.SetBinError(newb,err)

    return newhist



def getNormHist(varPathName, rebin, x_min, x_max):
    print "getNormHist:",varPathName, rebin, x_min, x_max
    hist = ROOT.TH1F(get(inFile,varPathName))
    hist.Sumw2()
    if o.ttbarDir:##actually dont do this. Going to weight ttbar also because that is what actually happens since ttbar is really in the data...
        print "subtract ttbar before making ratio"
        hist_ttbar = ttbarFile.Get(varPathName)
        hist_ttbar.SetName("ttbarForRatio")
        hist_ttbar.Sumw2()
        hist_ttbar.Scale(-1)
        hist.Add(hist_ttbar)

    integral = hist.Integral()
    print hist,"integral",integral
    hist.Scale(1/integral)    

    if isinstance(rebin,list): 
        hist = do_variable_rebinning(hist, rebin)
    else:
        hist.Rebin(rebin)
    
    if not (x_min == None) and not (x_max == None):
        hist.GetXaxis().SetRangeUser(x_min, x_max)            
    
    return hist

def makePositive(hist):
    for bin in range(1,hist.GetNbinsX()+1):
        x   = hist.GetXaxis().GetBinCenter(bin)
        y   = hist.GetBinContent(bin)
        err = hist.GetBinError(bin)
        hist.SetBinContent(bin, y if y > 0 else 0.0)
        #hist.SetBinError(bin, err if y > 0 else 0.0)

def calcWeights(varName, dirName, rebin, func="pol1", x_min=None,x_max=None):
    print varName
    hist2b = getNormHist(dirName+"_TwoTag_Sideband/"+varName,  rebin, x_min, x_max)
    hist2b.SetName(hist2b.GetName()+"_2b")
    makePositive(hist2b)
    
    histXb = getNormHist(dirName+"_"+tag+"Tag_Sideband/"+varName, rebin, x_min, x_max)
    histXb.SetName(histXb.GetName()+("_3b" if o.threeTag else "_4b"))
    makePositive(histXb)

    histXb.Write()
    hist2b.Write()

    can = ROOT.TCanvas(histXb.GetName()+"_ratio",histXb.GetName()+"_ratio")
    ratio = ROOT.TH1F(histXb)
    ratio.GetYaxis().SetRangeUser(0,2.5)
    ratio.SetName(histXb.GetName()+"_ratio")
    ratio.Divide(hist2b)
    makePositive(ratio)
    ratio.Fit(func,"")
    ratio.Write()

    ratio_TGraph  = ROOT.TGraph(ratio.GetSize()-2)
    #ratio_TGraph.SetPoint(1,xf,yf)
    #get first and last non-empty bin
    yf = ROOT.Double(1)
    yl = ROOT.Double(1)
    found_first = False
    for bin in range(1,ratio.GetSize()-1):
        c = ratio.GetBinContent(bin)
        if c > 0:
            yl = ROOT.Double(c)
            if found_first: continue
            found_first = True
            yf = ROOT.Double(c)

    found_first = False
    for bin in range(1,ratio.GetSize()-1):
        x = ROOT.Double(ratio.GetBinCenter(bin))
        c = ratio.GetBinContent(bin)
        if c <= 0 and not found_first:
            y = yf
        elif c > 0:
            found_first = True
            y = ROOT.Double(c)
        elif not found_first:
            y = yf
        else:
            y = yl
        ratio_TGraph.SetPoint(bin-1,x,y if "trigBit" not in varName else ROOT.Double(c))
            

    #ratio_TGraph.SetPoint(ratio_TGraph.GetN(),xl,yl)

    if type(func)==type("string"):
        fitResult = ratio.GetFunction(func)
    else:
        fitResult = ratio.GetFunction(func.GetName())
    fitResult.SetName("fit_"+varName)
    fitResult.Write()

    ratio_TSpline = ROOT.TSpline3("spline_"+varName, ratio_TGraph)
    ratio_TSpline.SetName("spline_"+varName)

    ratio_TSpline.Write()
    ratio_TSpline.SetLineColor(ROOT.kGreen)
    ratio_TSpline.Draw("SAME")

    can.SaveAs(histXb.GetName()+"_iter"+o.iteration+"_ratio.pdf")
    return 

# calcWeights("sublHC_Pt_l","PassHCdEta",4)
# calcWeights("dR_hh"       ,"PassHCdEta",4)
# calcWeights("nJetOther"     ,"PassHCdEta",1)
# calcWeights("leadHC_Pt_l",  "PassHCdEta",[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,225,250,275,300,350,400,500], 0, 500)
# calcWeights("sublHC_dRjj","PassHCdEta",4)
# calcWeights("dPhi_hh"     ,"PassHCdEta",4)
# calcWeights("sublHC_leadJet_Pt_m","PassHCdEta",[0,30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,220,240,300,350,400,500],0,500)
# calcWeights("sublHC_leadJet_Pt_m","PassHCdEta",[0,30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,220,240,300],0,300)
# calcWeights("sublHC_Mass","PassHCdEta",1)

# calcWeights("abs_dEta_hh","PassHCdEta",2)
# calcWeights("abs_dEta_gg","PassHCdEta",2)
# calcWeights("leadGC_dRjj","PassHCdEta",4)
# calcWeights("sublGC_dRjj","PassHCdEta",4,"pol2")
# calcWeights("sublGC_sublJet_Pt_m","PassHCdEta",4,"pol2")

def pol2pol1(x,par):
    xx = x[0]
    pol2 = par[0] + xx * par[1] + xx**2 * par[2]

    y1 = par[0] + par[3] * par[1] + par[3]**2 * par[2]
    m  = par[1] + 2*par[2]*par[3] #[3] is x value where we switch to line
    b = y1 - m * par[3]

    pol1 = m*xx + b

    if xx > par[3]: return pol1
    else          : return pol2

def flatPol1(x,par):
    xx = x[0]
    x1 = par[2]
    pol0 = par[0] + x1*par[1]
    pol1 = par[0] + xx*par[1]

    if xx < x1: return pol0
    else:       return pol1


def pol2flat(x,par):
    xx = x[0]
    a  = par[0]
    b  = par[1]
    x1 = par[2]
    c  = -b/(2*x1)
    y1 = a + b*x1 + c*x1**2
    y  = a + b*xx + c*xx**2

    if xx < x1: return y
    return y1

def expPol2pol1(x,par):
    xx = x[0]
    pol2 = par[0] + xx * par[1] + xx**2 * par[2]

    y1 = par[0] + par[3] * par[1] + par[3]**2 * par[2]
    m  = par[1] + 2*par[2]*par[3] #[3] is x value where we switch to line
    b = y1 - m * par[3]

    pol1 = m*xx + b

    exp = par[4]*math.exp(-(xx-35)/par[5])

    if xx > par[3]: return pol1+exp
    else          : return pol2+exp

def pol2pol2(x,par):
    xx = x[0]
    pol2l = par[0] + xx * par[1] + xx**2 * par[2]

    y1 = par[0] + par[3] * par[1] + par[3]**2 * par[2]
    m  = par[1] + 2*par[2]*par[3] #[3] is x value where we switch to line

    #dPol2h = b+2*c*par[3] = m => b = m-2*c*par[3]
    b = m - 2*par[4]*par[3]
    a = y1 - b*par[3] - par[4]*par[3]**2
    #y1 = a + par[3] * (b) + par[3]**2 * c => a = y1 - par[3]*b - par[3]**2 * c
    
    pol2h = a + b*xx + par[4]*xx**2

    if xx > par[3]: return pol2h
    else          : return pol2l



func_HCJet1_Pt = ROOT.TF1("fit_HCJet1_Pt",flatPol1,35,1000,3)

func_HCJet1_Pt.SetParameter(0,1)
func_HCJet1_Pt.SetParameter(1,0)
func_HCJet1_Pt.FixParameter(2,200)
calcWeights("HCJet1_Pt","PassHCdEta",[0,10,20,30,40,70,100,130,160,200,250,400,600,610,620,630,1000],func_HCJet1_Pt)

func_HCJet2_Pt = ROOT.TF1("fit_HCJet2_Pt",flatPol1,35,1000,3)

func_HCJet2_Pt.SetParameter(0,1)
func_HCJet2_Pt.SetParameter(1,0)
func_HCJet2_Pt.FixParameter(2,200)
calcWeights("HCJet2_Pt","PassHCdEta",[0,10,20,30,40,70,100,130,160,200,250,400,600,610,620,630,1000],func_HCJet2_Pt)

func_HCJet3_Pt = ROOT.TF1("fit_HCJet3_Pt",pol2flat,35,200,3)

func_HCJet3_Pt.SetParameter(0,1)
func_HCJet3_Pt.SetParameter(1,0)
func_HCJet3_Pt.FixParameter(2,100)
calcWeights("HCJet3_Pt_s","PassHCdEta",[0,35,36,37,38,39,40,42,44,47,50,55,60,75,100,190,191,192,193,200],func_HCJet3_Pt)

func_HCJet4_Pt = ROOT.TF1("fit_HCJet4_Pt",pol2flat,35,200,3)

func_HCJet4_Pt.SetParameter(0,1)
func_HCJet4_Pt.SetParameter(1,0)
func_HCJet4_Pt.FixParameter(2,100)
#calcWeights("HCJet4_Pt_s","PassHCdEta",[0,35,36,37,38,39,40,42,44,47,50,55,60,75,100,190,191,192,193,200],func_HCJet4_Pt)
calcWeights("HCJet4_Pt_s","PassHCdEta",[0,35,36,37,38,39,40,43,47,52,58,75,190,191,192,193,200],func_HCJet4_Pt)



# func_HC_jets_Pt = ROOT.TF1("fit_HC_jets_Pt",pol2pol1,0,500,4)

# func_HC_jets_Pt.SetParameter(0,1)
# func_HC_jets_Pt.SetParameter(1,0)
# func_HC_jets_Pt.SetParameter(2,0)
# func_HC_jets_Pt.SetParameter(3,200)
# calcWeights("HC_jets_Pt_m","PassHCdEta",4,func_HC_jets_Pt)
# calcWeights("HC_jets_AbsEta","PassHCdEta",2,"pol2")
#calcWeights("HCJetAbsEta","PassHCdEta",[0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.4,2.5,2.6,2.7,4],"pol1")
calcWeights("HCJetAbsEta","PassHCdEta",[-0.2,-0.1,0,0.5,0.8,1.0,1.2,1.4,1.8,2.4,2.5,2.6,2.7,4],"pol1")
calcWeights("trigBits","PassHCdEta",1,"pol1")

# func_sublHC_Ht = ROOT.TF1("fit_sublHC_Ht",pol2pol1,0,500,4)

# func_sublHC_Ht.SetParameter(0,1)
# func_sublHC_Ht.SetParameter(1,0)
# func_sublHC_Ht.SetParameter(2,0)
# func_sublHC_Ht.SetParameter(3,250)
# calcWeights("sublHC_Ht","PassHCdEta",2,func_sublHC_Ht)

# #func_HCJetBottomTwoMV2_Pt = ROOT.TF1("fit_HCJetBottomTwoMV2_Pt",pol2pol1,0,500,4)
# func_HCJetBottomTwoMV2_Pt = ROOT.TF1("fit_HCJetBottomTwoMV2_Pt",pol2pol2,35,500,5)

# func_HCJetBottomTwoMV2_Pt.SetParameter(0,1)
# func_HCJetBottomTwoMV2_Pt.SetParameter(1,0)
# func_HCJetBottomTwoMV2_Pt.SetParameter(2,0)
# func_HCJetBottomTwoMV2_Pt.SetParameter(3,200)
# func_HCJetBottomTwoMV2_Pt.SetParameter(4,0)
# calcWeights("HCJetBottomTwoMV2_Pt_m",  "PassHCdEta",2,func_HCJetBottomTwoMV2_Pt)
# calcWeights("HCJetBottomTwoMV2_AbsEta","PassHCdEta",2,"pol2")



# #func_HCJetTopTwoMV2 = ROOT.TF1("fit_HCJetTopTwoMV2_Pt",expPol2pol1,35,500,6)
# #func_HCJetTopTwoMV2 = ROOT.TF1("fit_HCJetTopTwoMV2_Pt",pol2pol1,35,500,4)
# func_HCJetTopTwoMV2 = ROOT.TF1("fit_HCJetTopTwoMV2_Pt",pol2pol2,35,500,5)
# func_HCJetTopTwoMV2.SetParameter(0,1)
# func_HCJetTopTwoMV2.SetParameter(1,0)
# func_HCJetTopTwoMV2.SetParameter(2,0)
# func_HCJetTopTwoMV2.SetParameter(3,200)
# func_HCJetTopTwoMV2.SetParameter(4,0)
# #func_HCJetTopTwoMV2.SetParameter(5,5)
# #func_HCJetTopTwoMV2.SetParLimits(5,1,50)
# calcWeights("HCJetTopTwoMV2_Pt_m",  "PassHCdEta",1,func_HCJetTopTwoMV2)
# calcWeights("HCJetTopTwoMV2_AbsEta","PassHCdEta",2,"pol2")


# calcWeights("R_dRdR","PassHCdEta",4,"pol2")
# calcWeights("R_dRdR_gg","PassHCdEta",4,"pol2")
calcWeights("GCdR_diff","PassHCdEta",[-0.5,-0.4,-0.3,-0.2,-0.1,0,0.4,0.8,1.2,1.6,2.0,2.4,2.8,4,4.1,4.2,4.3,5],"pol2")
calcWeights("GCdR_sum", "PassHCdEta",[0.5,0.7,1.4,1.8,2.2,2.6,3.0,3.4,3.8,4.2,5.0,6.2,6.3,6.4,6.5,7],"pol2")
# calcWeights("HCdR_diff","PassHCdEta",2,"pol2")
# calcWeights("HCdR_sum", "PassHCdEta",2,"pol2")
# calcWeights("Pt_hh","PassHCdEta",2,"pol2")

# calcWeights("HCJetAR","PassHCdEta",1,"pol1")

# calcWeights("HCJetPtE1","PassHCdEta",1,"pol1")
# calcWeights("HCJetPtE2","PassHCdEta",1,"pol1")

# calcWeights("leadGC_Pt","PassHCdEta",4,"pol1")
# calcWeights("hhJetEtaSum2","PassHCdEta",1,"pol2")

#
# Get Normalization #2b/#4b
#
mu_qcd = {}
mu_qcd_err = {}
mu_qcd_0j = {}
mu_qcd_err_0j = {}
mu_ttbar = {}
mu_ttbar_err = {}
mu_allhad = {}
mu_allhad_err = {}
mu_nonallhad = {}
mu_nonallhad_err = {}


#numer = ROOT.TH1F("weight_4bTo2b", "weight_4bTo2b", 1, 0, 1)
#denom = ROOT.TH1F("denom", "denom", 1, 0, 1)
muFile = open(o.outputDir+"/mu_qcd_"+tag+"Tag"+o.name+o.iteration+".txt","w")
f_qcd  = ROOT.TFile(o.qcdFile,"RECREATE")

def subtractTwoTag(data, ttbar, qcd):
    for dName in data.GetListOfKeys():
        if "TwoTag" not in dName.GetName(): continue
        print dName,dName.GetClassName()
        thisDirName = dName.GetName()
        dataDir  = data .Get(thisDirName)
        ttbarDir = ttbar.Get(thisDirName)
        qcd.mkdir(thisDirName)
        qcd.cd(thisDirName)
        for histKey in dataDir.GetListOfKeys():
            # only store TH1Fs for QCD root file
            if "TH1F" not in histKey.GetClassName(): continue
            histName = histKey.GetName()
            # print "Making qcd:",thisDirName+"/"+histName
            h_data  = data .Get(thisDirName+"/"+histName)
            h_ttbar = ttbar.Get(thisDirName+"/"+histName)

            h_qcd   = ROOT.TH1F(h_data)
            h_qcd.Add(h_ttbar,-1)
            h_qcd.Write()

dirNames = ["PassHCdEta"]
for dirName in dirNames:

    dataXb = inFile.Get(dirName+"_"+tag+"Tag_Sideband/sublHC_Pt_l")
    print dirName+"_"+tag+"Tag_Sideband/sublHC_Pt_l",dataXb
    ndataXb = dataXb.Integral(0,dataXb.GetNbinsX())
    print "nXb:",ndataXb,"+/-",sqrt(ndataXb)

    dataXb_nJetOther = inFile.Get(dirName+"_"+tag+"Tag_Sideband/nJetOther")
    print dirName+"_"+tag+"Tag_Sideband/nJetOther",dataXb_nJetOther
    ndataXb_0j = dataXb_nJetOther.Integral(1,1)
    print "nXb_0j:",ndataXb_0j,"+/-",sqrt(ndataXb_0j)

    data2b = inFile.Get(dirName+"_TwoTag_Sideband/sublHC_Pt_l")
    ndata2b = data2b.Integral(0,data2b.GetNbinsX())
    print "n2b:",ndata2b,"+/-",sqrt(ndata2b)

    data2b_nJetOther = inFile.Get(dirName+"_TwoTag_Sideband/nJetOther")
    ndata2b_0j = data2b_nJetOther.Integral(1,1)
    print "n2b_0j:",ndata2b_0j,"+/-",sqrt(ndata2b_0j)

    
    # print "Subtracting 2b ttbar MC from 2b data to make qcd hists (not yet scaled by mu_qcd)"
    # print " data:",inFile
    # print "ttbar:",ttbarFile
    # print "  qcd:",f_qcd
    # subtractTwoTag(inFile, ttbarFile, f_qcd)
    # f_qcd.Close()

    nttbarXb = 0
    nttbar2b = 0
    nallhadXb = 0
    nallhad2b = 0
    nnonallhadXb = 0
    nnonallhad2b = 0

    if o.ttbarDir:
        ttbarXb = ttbarFile.Get(dirName+"_"+tag+"Tag_Sideband/sublHC_Pt_l")
        print dirName+"_"+tag+"Tag_Sideband/sublHC_Pt_l",ttbarXb
        nttbarXb = ttbarXb.Integral(0,ttbarXb.GetNbinsX())
        print "nttbarXb:",nttbarXb,"+/-",sqrt(nttbarXb)

        ttbarXb_nJetOther = ttbarFile.Get(dirName+"_"+tag+"Tag_Sideband/nJetOther")
        nttbarXb_0j = ttbarXb_nJetOther.Integral(1,1)
        print "nttbarXb_0j:",nttbarXb_0j,"+/-",sqrt(nttbarXb_0j)

        ttbar2b = ttbarFile.Get(dirName+"_TwoTag_Sideband/sublHC_Pt_l")
        nttbar2b = ttbar2b.Integral(0,ttbar2b.GetNbinsX())
        print "nttbar2b:",nttbar2b,"+/-",sqrt(nttbar2b)

        ttbar2b_nJetOther = ttbarFile.Get(dirName+"_TwoTag_Sideband/nJetOther")
        nttbar2b_0j = ttbar2b_nJetOther.Integral(1,1)
        print "nttbar2b_0j:",nttbar2b_0j,"+/-",sqrt(nttbar2b_0j)

        allhadXb = allhadFile.Get(dirName+"_"+tag+"Tag_Sideband/sublHC_Pt_l")
        print dirName+"_"+tag+"Tag_Sideband/sublHC_Pt_l",allhadXb
        nallhadXb = allhadXb.Integral(0,allhadXb.GetNbinsX())
        print "nallhadXb:",nallhadXb,"+/-",sqrt(nallhadXb)

        allhadXb_nJetOther = allhadFile.Get(dirName+"_"+tag+"Tag_Sideband/nJetOther")
        nallhadXb_0j = allhadXb_nJetOther.Integral(1,1)
        print "nallhadXb_0j:",nallhadXb_0j,"+/-",sqrt(nallhadXb_0j)

        allhad2b = allhadFile.Get(dirName+"_TwoTag_Sideband/sublHC_Pt_l")
        nallhad2b = allhad2b.Integral(0,allhad2b.GetNbinsX())
        print "nallhad2b:",nallhad2b,"+/-",sqrt(nallhad2b)

        allhad2b_nJetOther = allhadFile.Get(dirName+"_TwoTag_Sideband/nJetOther")
        nallhad2b_0j = allhad2b_nJetOther.Integral(1,1)
        print "nallhad2b_0j:",nallhad2b_0j,"+/-",sqrt(nallhad2b_0j)

        nonallhadXb = nonallhadFile.Get(dirName+"_"+tag+"Tag_Sideband/sublHC_Pt_l")
        print dirName+"_"+tag+"Tag_Sideband/sublHC_Pt_l",nonallhadXb
        nnonallhadXb = nonallhadXb.Integral(0,nonallhadXb.GetNbinsX())
        print "nnonallhadXb:",nnonallhadXb,"+/-",sqrt(nnonallhadXb)

        nonallhadXb_nJetOther = nonallhadFile.Get(dirName+"_"+tag+"Tag_Sideband/nJetOther")
        nnonallhadXb_0j = nonallhadXb_nJetOther.Integral(1,1)
        print "nnonallhadXb_0j:",nnonallhadXb_0j,"+/-",sqrt(nnonallhadXb_0j)

        nonallhad2b = nonallhadFile.Get(dirName+"_TwoTag_Sideband/sublHC_Pt_l")
        nnonallhad2b = nonallhad2b.Integral(0,nonallhad2b.GetNbinsX())
        print "nnonallhad2b:",nnonallhad2b,"+/-",sqrt(nnonallhad2b)

        nonallhad2b_nJetOther = nonallhadFile.Get(dirName+"_TwoTag_Sideband/nJetOther")
        nnonallhad2b_0j = nonallhad2b_nJetOther.Integral(1,1)
        print "nnonallhad2b_0j:",nnonallhad2b_0j,"+/-",sqrt(nnonallhad2b_0j)


    nXb_qcd = ndataXb - nttbarXb
    n2b_qcd = ndata2b - nttbar2b

    mu_qcd[dirName] = nXb_qcd / n2b_qcd if n2b_qcd else "NaN"

    nXb_qcd_0j = ndataXb_0j - nttbarXb_0j
    n2b_qcd_0j = ndata2b_0j - nttbar2b_0j
    mu_qcd_0j[dirName] = nXb_qcd_0j / n2b_qcd_0j if n2b_qcd_0j else "NaN"

    print nXb_qcd
    print ndataXb
    print nttbarXb


    mu_qcd_err_t1    = 1./n2b_qcd*sqrt(nXb_qcd) if n2b_qcd else "NaN"
    mu_qcd_err_t2    = nXb_qcd/(n2b_qcd*n2b_qcd)*sqrt(n2b_qcd) if n2b_qcd else "NaN"
    mu_qcd_err[dirName] = sqrt(mu_qcd_err_t1*mu_qcd_err_t1 + mu_qcd_err_t2*mu_qcd_err_t2 ) if n2b_qcd else "NaN"
    print "mu_qcd_"+dirName+":",mu_qcd[dirName],"+/-",mu_qcd_err[dirName]

    mu_qcd_err_0j_t1    = 1./n2b_qcd_0j*sqrt(nXb_qcd_0j) if n2b_qcd_0j else "NaN"
    mu_qcd_err_0j_t2    = nXb_qcd_0j/(n2b_qcd_0j*n2b_qcd_0j)*sqrt(n2b_qcd_0j) if n2b_qcd_0j else "NaN"
    mu_qcd_err_0j[dirName] = sqrt(mu_qcd_err_0j_t1*mu_qcd_err_0j_t1 + mu_qcd_err_0j_t2*mu_qcd_err_0j_t2 ) if n2b_qcd_0j else "NaN"

    if o.ttbarDir:
        del ttbar2b #use shape dir to get scaling from 2b->Xb for the ttbar that was made with the correct btag f factor
        ttbar2b = ttbarShape.Get(dirName+"_TwoTag_Sideband/sublHC_Pt_l")
        nttbar2b = ttbar2b.Integral(0,ttbar2b.GetNbinsX())
        print "nttbar2b:",nttbar2b,"+/-",sqrt(nttbar2b)

        del ttbar2b_nJetOther
        ttbar2b_nJetOther = ttbarShape.Get(dirName+"_TwoTag_Sideband/nJetOther")
        nttbar2b_0j = ttbar2b_nJetOther.Integral(1,1)
        print "nttbar2b_0j:",nttbar2b_0j,"+/-",sqrt(nttbar2b_0j)

        mu_ttbar_err_t1    = 1./nttbar2b*sqrt(nttbarXb) if nttbar2b else "NaN"
        mu_ttbar_err_t2    = nttbarXb/(nttbar2b*nttbar2b)*sqrt(nttbar2b) if nttbar2b else "NaN"

        mu_ttbar[dirName] = nttbarXb  / nttbar2b
        mu_ttbar_err[dirName] = sqrt(mu_ttbar_err_t1*mu_ttbar_err_t1 + mu_ttbar_err_t2*mu_ttbar_err_t2 ) if nttbar2b else "NaN"
        print "mu_ttbar_"+dirName+":",mu_ttbar[dirName],"+/-",mu_ttbar_err[dirName]

        allhad2b = allhadShape.Get(dirName+"_TwoTag_Sideband/sublHC_Pt_l")
        nallhad2b = allhad2b.Integral(0,allhad2b.GetNbinsX())
        print "nallhad2b:",nallhad2b,"+/-",sqrt(nallhad2b)

        del allhad2b_nJetOther
        allhad2b_nJetOther = allhadShape.Get(dirName+"_TwoTag_Sideband/nJetOther")
        nallhad2b_0j = allhad2b_nJetOther.Integral(1,1)
        print "nallhad2b_0j:",nallhad2b_0j,"+/-",sqrt(nallhad2b_0j)

        mu_allhad_err_t1    = 1./nallhad2b*sqrt(nallhadXb) if nallhad2b else "NaN"
        mu_allhad_err_t2    = nallhadXb/(nallhad2b*nallhad2b)*sqrt(nallhad2b) if nallhad2b else "NaN"

        mu_allhad[dirName] = nallhadXb  / nallhad2b
        mu_allhad_err[dirName] = sqrt(mu_allhad_err_t1*mu_allhad_err_t1 + mu_allhad_err_t2*mu_allhad_err_t2 ) if nallhad2b else "NaN"
        print "mu_allhad_"+dirName+":",mu_allhad[dirName],"+/-",mu_allhad_err[dirName]

        nonallhad2b = nonallhadShape.Get(dirName+"_TwoTag_Sideband/sublHC_Pt_l")
        nnonallhad2b = nonallhad2b.Integral(0,nonallhad2b.GetNbinsX())
        print "nnonallhad2b:",nnonallhad2b,"+/-",sqrt(nnonallhad2b)

        del nonallhad2b_nJetOther
        nonallhad2b_nJetOther = nonallhadShape.Get(dirName+"_TwoTag_Sideband/nJetOther")
        nnonallhad2b_0j = nonallhad2b_nJetOther.Integral(1,1)
        print "nnonallhad2b_0j:",nnonallhad2b_0j,"+/-",sqrt(nnonallhad2b_0j)

        mu_nonallhad_err_t1    = 1./nnonallhad2b*sqrt(nnonallhadXb) if nnonallhad2b else "NaN"
        mu_nonallhad_err_t2    = nnonallhadXb/(nnonallhad2b*nnonallhad2b)*sqrt(nnonallhad2b) if nnonallhad2b else "NaN"

        mu_nonallhad[dirName] = nnonallhadXb  / nnonallhad2b
        mu_nonallhad_err[dirName] = sqrt(mu_nonallhad_err_t1*mu_nonallhad_err_t1 + mu_nonallhad_err_t2*mu_nonallhad_err_t2 ) if nnonallhad2b else "NaN"
        print "mu_nonallhad_"+dirName+":",mu_nonallhad[dirName],"+/-",mu_nonallhad_err[dirName]



    #
    # Store mu_XXX info in text file
    #
    muFile.write("mu_qcd_"+dirName+"       "+str(mu_qcd[dirName])+"\n")
    muFile.write("mu_qcd_"+dirName+"_err   "+str(mu_qcd_err[dirName])+"\n")
    if o.ttbarDir:
        muFile.write("mu_ttbar_"+dirName+"     "+str(mu_ttbar[dirName])+"\n")
        muFile.write("mu_ttbar_"+dirName+"_err "+str(mu_ttbar_err[dirName])+"\n")
        muFile.write("mu_allhad_"+dirName+"     "+str(mu_allhad[dirName])+"\n")
        muFile.write("mu_allhad_"+dirName+"_err "+str(mu_allhad_err[dirName])+"\n")
        muFile.write("mu_nonallhad_"+dirName+"     "+str(mu_nonallhad[dirName])+"\n")
        muFile.write("mu_nonallhad_"+dirName+"_err "+str(mu_nonallhad_err[dirName])+"\n")
        muFile.write("mu_qcd_"+dirName+"_0j    "+str(mu_qcd_0j[dirName])+"\n")
        muFile.write("mu_qcd_"+dirName+"_err_0j "+str(mu_qcd_err_0j[dirName])+"\n")

muFile.close()




print "Subtracting 2b ttbar MC from 2b data to make qcd hists (not yet scaled by mu_qcd)"
print " data:",inFile
print "ttbar:",ttbarFile
print "  qcd:",f_qcd
subtractTwoTag(inFile, ttbarFile, f_qcd)
f_qcd.Close()
