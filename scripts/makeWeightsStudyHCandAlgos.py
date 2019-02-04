import ROOT

import copy

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

parser.add_option('-o', '--outputDir',
                  dest='outputDir',
                  default="../data/"
                  )

parser.add_option('-q', '--qcdFile',
                  dest="qcdFile",
                  default="testQCD.root",
                  )


o, a = parser.parse_args()

from math import sqrt
import math
from array import array
import os
if not os.path.isdir(o.outputDir):
    os.mkdir(o.outputDir)
ROOT.gROOT.SetBatch(True)


iteration = o.iteration


print "Making weights for iteration:",iteration

inFileName = o.dir
inFile = ROOT.TFile(inFileName,"READ")
print "Input file:",inFileName

if o.ttbarDir:
    ttbarFile = ROOT.TFile(o.ttbarDir,"READ")


outFile = ROOT.TFile(o.outputDir+"/weights2bto4b_"+o.name+str(int(o.iteration)+1)+".root","RECREATE")
outFile.cd()

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
    hist = inFile.Get(varPathName)
    print inFile, varPathName
    print hist
    hist.Sumw2()
    if o.ttbarDir:##actually dont do this. Going to weight ttbar also because that is what actually happens since ttbar is really in the data...
        print "subtract ttbar before making ratio"
        if "Four" in varPathName: #use 2b shape for ttbar with 4b normalization
            hist_4b_ttbar = ttbarFile.Get(varPathName)
            hist_4b_ttbar.SetName("fourtagttbar")
            varPathName  = varPathName.replace("Four","Two")
            hist_ttbar = ttbarFile.Get(varPathName)
            hist_ttbar.SetName("ttbarForRatio")
            hist_ttbar.Sumw2()
            hist_ttbar.Scale(hist_4b_ttbar.Integral()/hist_ttbar.Integral())
        else:
            hist_ttbar = ttbarFile.Get(varPathName)
            hist_ttbar.SetName("ttbarForRatio")
            hist_ttbar.Sumw2()

        hist_ttbar.Scale(-1)
        hist.Add(hist_ttbar)

    for bin in range(hist.GetSize()):
        if hist.GetBinContent(bin) < 0: 
            hist.SetBinContent(bin,0.0)
            hist.SetBinError(bin,0.0)

    integral = hist.Integral()
    hist.Scale(1/integral)    

    if isinstance(rebin,list): 
        hist = do_variable_rebinning(hist, rebin)
    else:
        hist.Rebin(rebin)
    
    if not (x_min == None) and not (x_max == None):
        hist.GetXaxis().SetRangeUser(x_min, x_max)            
    
    return hist

def calcWeights(varName, cutflow, algo, func, rebin, x_min=None,x_max=None):
    print varName
    if "m12m34" == varName: region = "Inclusive"
    else: region = "Sideband"
    hist2b = getNormHist(cutflow+"/"+algo+"/TwoTag/"+region+"/"+varName,  rebin, x_min, x_max)
    hist2b.SetName(hist2b.GetName()+"_2b")
    hist4b = getNormHist(cutflow+"/"+algo+"/FourTag/"+region+"/"+varName, rebin, x_min, x_max)
    hist4b.SetName(hist4b.GetName()+"_4b")
    hist2b.Write()
    hist4b.Write()


    if "m12m34" == varName: ratio = ROOT.TH2F(hist4b)
    else: ratio = ROOT.TH1F(hist4b)
    ratio.SetName(hist4b.GetName()+"_ratio")
    ratio.Divide(hist2b)
    if "m12m34" != varName: ratio.Fit(func,"")
    ratio.Write()

    if "m12m34" != varName:
        fitResult = ratio.GetFunction(func)
        fitResult.SetName("fit_"+varName)
        fitResult.Write()

    return 

calcWeights("HCjet4_pt","Loose","DhhMin", "pol2", 2)
calcWeights("HCjet3_pt","Loose","DhhMin", "pol1", 2)
calcWeights("sublHCand_Pt_l","Loose","DhhMin", "pol1", 2)
calcWeights("leadHCand_leadJet_Pt","Loose","DhhMin", "pol2", 1)
calcWeights("leadHCand_sublJet_Pt","Loose","DhhMin", "pol2", 1)
calcWeights("sublHCand_leadJet_Pt","Loose","DhhMin", "pol2", 1)
calcWeights("sublHCand_sublJet_Pt","Loose","DhhMin", "pol2", 1)
calcWeights("sublHCand_AbsEta","Loose","DhhMin", "pol2", 2)
calcWeights("sublHCand_leadJet_E","Loose","DhhMin", "pol1", 1)
calcWeights("sublHCand_sublJet_E","Loose","DhhMin", "pol1", 1)
calcWeights("leadHCand_AbsEta","Loose","DhhMin", "pol2", 2)
calcWeights("hCandDr"     ,"Loose","DhhMin", "pol2", 4)
calcWeights("nJetOther"     ,"Loose","DhhMin", "pol1", 1)
calcWeights("leadHCand_Pt_l","Loose","DhhMin", "pol1", 2)
calcWeights("leadHCand_Ht","Loose","DhhMin", "pol1", 4)
calcWeights("sublHCand_Ht","Loose","DhhMin", "pol2",  4)
calcWeights("sublHCand_dRjj","Loose","DhhMin", "pol2", 4)
calcWeights("leadHCand_dRjj","Loose","DhhMin", "pol2", 4)
calcWeights("hCandDphi"     ,"Loose","DhhMin", "pol2",  4)

calcWeights("m12m34","Loose","DhhMin","",4,None,None)


#
# Get Normalization #2b/#4b
#
cutflows = ["Loose"]
algos = ["DhhMin"]
mu_qcd = {}
mu_qcd_err = {}
mu_ttbar = {}
mu_ttbar_err = {}
for cutflow in cutflows:
    for algo in algos:
        print "Making weights for algo:",algo
        numer = ROOT.TH1F("weight_4bTo2b", "weight_4bTo2b", 1, 0, 1)
        denom = ROOT.TH1F("denom", "denom", 1, 0, 1)
        
        data4b = inFile.Get(cutflow+"/"+algo+"/FourTag/Sideband/sublHCand_Pt_l")
        print cutflow+"/"+algo+"/FourTag/Sideband/sublHCand_Pt_l",data4b
        ndata4b = data4b.Integral(0,data4b.GetNbinsX())
        print "n4b:",ndata4b,"+/-",sqrt(ndata4b)


        data2b = inFile.Get(cutflow+"/"+algo+"/TwoTag/Sideband/sublHCand_Pt_l")
        ndata2b = data2b.Integral(0,data2b.GetNbinsX())
        print "n2b:",ndata2b,"+/-",sqrt(ndata2b)

        nttbar4b = 0
        nttbar2b = 0
        if o.ttbarDir:
            ttbar4b = ttbarFile.Get(cutflow+"/"+algo+"/FourTag/Sideband/sublHCand_Pt_l")
            print cutflow+"/"+algo+"/FourTag/Sideband/sublHCand_Pt_l",ttbar4b
            ettbar4b = ROOT.Double()
            nttbar4b = ttbar4b.IntegralAndError(0,ttbar4b.GetNbinsX(),ettbar4b)
            print "nttbar4b:",nttbar4b,"+/-",ettbar4b, " (entries =",ttbar4b.GetEntries(),")"

            ttbar2b = ttbarFile.Get(cutflow+"/"+algo+"/TwoTag/Sideband/sublHCand_Pt_l")
            ettbar2b = ROOT.Double()
            nttbar2b = ttbar2b.IntegralAndError(0,ttbar2b.GetNbinsX(),ettbar2b)
            print "nttbar2b:",nttbar2b,"+/-",ettbar2b, " (entries =",ttbar2b.GetEntries(),")"
        
        n4b_qcd = ndata4b - nttbar4b
        n2b_qcd = ndata2b - nttbar2b

        mu_qcd[cutflow+algo] = n4b_qcd / n2b_qcd if n2b_qcd else "NaN"

        mu_qcd_err_t1    = 1./n2b_qcd*sqrt(n4b_qcd) if n2b_qcd else "NaN"
        mu_qcd_err_t2    = n4b_qcd/(n2b_qcd*n2b_qcd)*sqrt(n2b_qcd) if n2b_qcd else "NaN"
        mu_qcd_err[cutflow+algo] = sqrt(mu_qcd_err_t1*mu_qcd_err_t1 + mu_qcd_err_t2*mu_qcd_err_t2 ) if n2b_qcd else "NaN"
        print "mu_qcd_"+cutflow+algo+":",mu_qcd[cutflow+algo],"+/-",mu_qcd_err[cutflow+algo]

        if o.ttbarDir:
            mu_ttbar_err_t1    = ettbar4b * 1./nttbar2b if (nttbar2b > 0) else "NaN"
            mu_ttbar_err_t2    = ettbar2b * nttbar4b/nttbar2b**2 if (nttbar2b > 0) else "NaN"
        
            mu_ttbar[cutflow+algo] = nttbar4b  / nttbar2b
            mu_ttbar_err[cutflow+algo] = sqrt(mu_ttbar_err_t1**2 + mu_ttbar_err_t2**2 ) if nttbar2b else "NaN"
            print "mu_ttbar_"+cutflow+algo+":",mu_ttbar[cutflow+algo],"+/-",mu_ttbar_err[cutflow+algo]



#
# Store mu_XXX info in text file
#

muFile = open(o.outputDir+"/mu_qcd_"+o.name+"-"+iteration+".txt","w")
for cutflow in cutflows:
    for algo in algos:
        muFile.write("mu_qcd_"+cutflow+algo+"       "+str(mu_qcd[cutflow+algo])+"\n")
        muFile.write("mu_qcd_"+cutflow+algo+"_err   "+str(mu_qcd_err[cutflow+algo])+"\n")
        if o.ttbarDir:
            muFile.write("mu_ttbar_"+cutflow+algo+"     "+str(mu_ttbar[cutflow+algo])+"\n")
            muFile.write("mu_ttbar_"+cutflow+algo+"_err "+str(mu_ttbar_err[cutflow+algo])+"\n")
muFile.close()


f_qcd  = ROOT.TFile(o.qcdFile,"RECREATE")
#regions = ["SignalZZ","Sideband","Control","Signal","Inclusive","m300","m400","m500","m600","m700","m800","m900","m1000","m1100","m1200"]
regions = ["Excess","SignalZZ","SignalHH","Sideband","Control","Signal","Inclusive","All","m300","m400","m500","m600","m700","m800","m900","m1000","m1100","m1200"]

def subtractTwoTag(data, ttbar, qcd):
    for cutflow in cutflows:
        for algo in algos:
            for region in regions:
                dirName = cutflow+"/"+algo+"/TwoTag/"+region
                print dirName
                dataDir  = data .Get(dirName)
                ttbarDir = ttbar.Get(dirName)
                
                qcd.mkdir(dirName)
                qcd.cd(dirName)
                for histKey in dataDir.GetListOfKeys():
                    # only store TH1Fs for QCD root file
                    if "TH1F" not in histKey.GetClassName(): continue
                    histName = histKey.GetName()
                    # print "Making qcd:",dirName+"/"+histName
                    h_data  = data .Get(dirName+"/"+histName)
                    h_ttbar = ttbar.Get(dirName+"/"+histName)
                    h_qcd   = ROOT.TH1F(h_data)
                    h_qcd.Add(h_ttbar,-1)
                    h_qcd.Write()

print "Subtracting 2b ttbar MC from 2b data to make qcd hists (not yet scaled by mu_qcd)"
print " data:",inFile
print "ttbar:",ttbarFile
print "  qcd:",f_qcd
subtractTwoTag(inFile, ttbarFile, f_qcd)
f_qcd.Close()
