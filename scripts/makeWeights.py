import ROOT
import operator as op
def ncr(n, r):
    r = min(r, n-r)
    if r == 0: return 1
    numer = reduce(op.mul, xrange(n, n-r, -1))
    denom = reduce(op.mul, xrange(1, r+1))
    return numer//denom

def getCombinatoricWeight(f,nj):#number of jets beyond the two required b-jets, ie a 5jet event has nj=3 and w = 3f^2(1-f)+f^3.
    # All terms have f^2 so divide it out because we only care about ratio of combinatoric weights.
    w = 0
    for i in range(2,nj+1):
        w += ncr(nj,nj-i) * (f**(i-2) if (i-2) else 1) * ((1-f)**(nj-i))
    return w

import copy, sys

import optparse

sys.path.insert(0, 'XhhResolved/plotting/')
from plotTools import read_mu_qcd_file

parser = optparse.OptionParser()

parser.add_option('-i', '--iter',
                  dest="iteration",
                  default="0"
                  )

parser.add_option('--noFitWeight',
                 dest='noFitWeight',
                 default=""
                 )

parser.add_option('-w', '--weightSet',
                  dest="weightSet",
                  default=None
                  )

parser.add_option('-r',
                  dest="weightRegion",
                  default=None
                  )

parser.add_option('-d', '--data',
                  dest="data",
                  default="data_iter0/hists.root"
                  )

parser.add_option('-a', '--allhad',
                 dest='allhad',
                 default=""
                 )

parser.add_option('-n', '--nonallhad',
                 dest='nonallhad',
                 default=""
                 )

parser.add_option('-s','--allhadShape',
                 dest='allhadShape',
                 default=""
                 )

parser.add_option('-o', '--outputDir',
                  dest='outputDir',
                  default=""
                  )

parser.add_option('-q', '--qcdFile',
                  dest="qcdFile",
                  default="testQCD.root",
                  )

parser.add_option('--injectFile',
                  dest="injectFile",
                  default="",
                  )

parser.add_option('--injectMu',
                  dest="injectMu",
                  default="",
                  )

parser.add_option('--threeTag',  dest="threeTag",  action="store_true", default=False)

o, a = parser.parse_args()

import math
from array import array
import os
if not os.path.isdir(o.outputDir):
    os.mkdir(o.outputDir)
ROOT.gROOT.SetBatch(True)




print "Making weights for iteration:",o.iteration

inFileName = o.data
inFile = ROOT.TFile(inFileName,"READ")
print "Input file:",inFileName

allhadShape    = ROOT.TFile(o.allhadShape, "READ")
allhadFile     = ROOT.TFile(o.allhad     , "READ")
nonallhadFile  = ROOT.TFile(o.nonallhad  , "READ")
injectFile     = None
if o.injectFile: injectFile = ROOT.TFile(o.injectFile, "READ")

if o.threeTag: 
    tag = "Three"
else: 
    tag = "Four"


useAllhad2bShape = True


# variables = []
def get(rootFile, path):
    obj = rootFile.Get(path)
    if str(obj) == "<ROOT.TObject object at 0x(nil)>": 
        rootFile.ls()
        print 
        print "ERROR: Object not found -", rootFile, path
        sys.exit()

    else: return obj

def makePositive(hist):
    for bin in range(1,hist.GetNbinsX()+1):
        x   = hist.GetXaxis().GetBinCenter(bin)
        y   = hist.GetBinContent(bin)
        err = hist.GetBinError(bin)
        hist.SetBinContent(bin, y if y > 0 else 0.0)
        hist.SetBinError(bin, err if y>0 else 0.0)

def do_variable_rebinning(hist,bins,divide=True):
    a=hist.GetXaxis()
    newhist=ROOT.TH1F(hist.GetName()+"_variableBins",
                      hist.GetTitle()+";"+hist.GetXaxis().GetTitle()+";"+hist.GetYaxis().GetTitle(),
                      len(bins)-1,
                      array('d',bins))

    newhist.Sumw2()
    newa=newhist.GetXaxis()

    for b in range(1, hist.GetNbinsX()+1):
        newb             = newa.FindBin(a.GetBinCenter(b))

        # Get existing new content (if any)
        val              = newhist.GetBinContent(newb)
        err              = newhist.GetBinError(newb)

        # Get content to add
        ratio_bin_widths = newa.GetBinWidth(newb)/a.GetBinWidth(b) if divide else 1.0
        val              = val+hist.GetBinContent(b)/ratio_bin_widths
        err              = math.sqrt(err**2+(hist.GetBinError(b)/ratio_bin_widths)**2)
        newhist.SetBinContent(newb,val)
        newhist.SetBinError(newb,err)

    return newhist


#
# Get Normalization #2b/#4b
#
mu_qcd = {}
mu_qcd_err = {}
mu_allhad = {}
mu_allhad_err = {}
mu_nonallhad2b = {}
mu_nonallhad2b_err = {}
mu_nonallhad4b = {}
mu_nonallhad4b_err = {}


muFile = open("XhhResolved/data/mu_qcd_"+tag+"Tag"+o.weightSet+o.iteration+".txt","w")

singleTagProbDict    = read_mu_qcd_file("XhhResolved/data/singleTagProb_"+tag+"Tag"+o.weightSet+        o.iteration    +".txt")
newSingleTagProbFile =             open("XhhResolved/data/singleTagProb_"+tag+"Tag"+o.weightSet+str(int(o.iteration)+1)+".txt","w")
newSingleTagProb_qcd = {}
newSingleTagProb_qcd_err = {}
newSingleTagProb_allhad = {}
newSingleTagProb_allhad_err = {}

def getHists(cut,region,var,mu_cut=""):#allow for different cut for mu calculation
    baseName = cut+"_"+region+"_"+var+("_use_mu" if mu_cut else "")
    data4b        = inFile       .Get(cut+"_"+tag+"Tag_"+region+"/"+var)
    data4b        .SetName("data4b_"+baseName)
    data2b        = inFile       .Get(cut+    "_TwoTag_"+region+"/"+var)
    data2b        .SetName("data2b_"+baseName)
    allhad2b      = allhadFile   .Get(cut+    "_TwoTag_"+region+"/"+var)#Uses same f as data to correctly subtract 2b ttbar to make qcd estimate
    allhad2b      .SetName("allhad2b_"+baseName)
    allhad4b      = allhadFile   .Get(cut+"_"+tag+"Tag_"+region+"/"+var)
    allhad4b      .SetName("allhad4b_"+baseName)
    allhad2bShape = allhadShape  .Get(cut+    "_TwoTag_"+region+"/"+var)#Uses f to get 2b to 4b normalization right for ttbar
    allhad2bShape .SetName("allhad2bShape_"+baseName)
    nonallhad2b   = nonallhadFile.Get(cut+    "_TwoTag_"+region+"/"+var)#Uses same f as data to correctly subtract 2b ttbar to make qcd estimate
    nonallhad2b   .SetName("nonallhad2b_"+baseName)
    nonallhad4b   = nonallhadFile.Get(cut+"_"+tag+"Tag_"+region+"/"+var)
    nonallhad4b   .SetName("nonallhad4b_"+baseName)

    inject4b = None
    #inject2b = None
    if o.injectFile:
        inject4b = injectFile.Get(cut+"_"+tag+"Tag_"+region+"/"+var)
        inject4b.SetName("inject4b_"+baseName)
        inject4b.Scale(float(o.injectMu))

        #inject2b = injectFile.Get(cut+"_TwoTag_"+region+"/"+var)
        #inject2b.SetName("inject2b_"+baseName)
        #inject2b.Scale(float(o.injectMu))

    if mu_cut: 
        if useAllhad2bShape: allhad2bShape.Scale(mu_allhad[mu_cut])
        else:                allhad4b     .Scale(mu_allhad[mu_cut])
        nonallhad2b.Scale(mu_nonallhad2b[mu_cut])
        nonallhad4b.Scale(mu_nonallhad4b[mu_cut])

    #
    # Make qcd histogram by subtacting 2b ttbar from 2b data
    #
    if "TH1" in str(data2b):
        qcd = ROOT.TH1F(data2b)
    elif "TH2" in str(data2b):
        qcd = ROOT.TH2F(data2b)
    qcd.SetName("qcd_"+baseName)
    qcd.Add(   allhad2b,-1)
    qcd.Add(nonallhad2b,-1)

    if mu_cut: qcd.Scale(mu_qcd[mu_cut])

    if "TH1" in str(data2b):
        bkgd = ROOT.TH1F(qcd)
    elif "TH2" in str(data2b):
        bkgd = ROOT.TH2F(data2b)
    bkgd.SetName("bkgd_"+baseName)
    if useAllhad2bShape: bkgd.Add(allhad2bShape)
    else:                bkgd.Add(allhad4b)
    bkgd.Add(nonallhad4b)

    if o.injectFile:
        data4b.Add(inject4b)
        inject4b.SetLineColor(ROOT.kRed)

    data4b.SetLineColor(ROOT.kBlack)
    qcd.SetFillColor(ROOT.kYellow)
    qcd.SetLineColor(ROOT.kBlack)
    allhad2bShape.SetFillColor(ROOT.kAzure-9)
    allhad2bShape.SetLineColor(ROOT.kBlack)
    allhad4b.SetFillColor(ROOT.kAzure-9)
    allhad4b.SetLineColor(ROOT.kBlack)
    nonallhad4b.SetFillColor(ROOT.kAzure-4)
    nonallhad4b.SetLineColor(ROOT.kBlack)
        
    if mu_cut:
        c=ROOT.TCanvas(var+"_"+cut+"_postfit","Post-fit")
        data4b.Draw("PE")
        stack = ROOT.THStack("stack","stack")
        stack.Add(nonallhad4b,"hist")
        stack.Add(allhad2bShape if useAllhad2bShape else allhad4b,"hist")
        stack.Add(qcd,"hist")
        stack.Draw("HIST SAME")
        data4b.Draw("PE SAME axis")
        data4b.Draw("PE SAME")
        if o.injectFile:
            inject4b.Draw("PE SAME")
        c.SaveAs(o.outputDir+"/"+var+"_"+cut+"_postfit_iter"+str(o.iteration)+".pdf")
        del stack

    return (data4b, data2b, allhad2b, allhad4b, allhad2bShape, nonallhad2b, nonallhad4b, qcd, bkgd)


def getNonAllHadMuErr(data,nonallhad):
    nd = data.GetBinContent(2)+data.GetBinContent(3)
    nn = nonallhad.GetBinContent(2)+nonallhad.GetBinContent(3)
    nde = (data.GetBinError(2)**2+data.GetBinError(3)**2)**0.5
    nne = (nonallhad.GetBinError(2)**2+nonallhad.GetBinError(3)**2)**0.5
    mu = nd/nn if nn>0 else 0
    mue = ((nde/nn)**2+(nne*nd/nn**2)**2)**0.5 if nn>0 else 0
    return (mu,mue)

cuts = ["PassHCdEta"]
for cut in cuts:
    #
    # get nonallhad scale factors from number of events with 1 or 2 prompt muons
    #
    (data4b, data2b, allhad2b, allhad4b, allhad2bShape, nonallhad2b, nonallhad4b, qcd, bkgd) = getHists(cut,o.weightRegion,"nPromptMuons")
    (mu2b,mue2b) = getNonAllHadMuErr(data2b,nonallhad2b)
    (mu4b,mue4b) = getNonAllHadMuErr(data4b,nonallhad4b)
    mu_nonallhad2b[cut] = mu2b
    mu_nonallhad2b_err[cut] = mue2b
    mu_nonallhad4b[cut] = mu4b
    mu_nonallhad4b_err[cut] = mue4b
    print "mu_nonallhad2b    ", mu_nonallhad2b[cut],"+/-",mu_nonallhad2b_err[cut]
    print "mu_nonallhad4b    ", mu_nonallhad4b[cut],"+/-",mu_nonallhad4b_err[cut]

    # nonallhad enriched
    q_bin3 = 0
    a_bin3 = 0
    n_bin3 = nonallhad4b.GetBinContent(2) + nonallhad4b.GetBinContent(3)
    d_bin3 = data4b     .GetBinContent(2) + data4b     .GetBinContent(3)


    #
    # Get scale factors for hists without nJetWeight
    #
    (data4b, data2b, allhad2b, allhad4b, allhad2bShape, nonallhad2b, nonallhad4b, qcd, bkgd) = getHists(cut,o.weightRegion,"nJetOther_u")
    mu_qcd_no_nJetWeight    = (data4b.Integral()-allhad4b.Integral()-nonallhad4b.Integral()*mu4b)/(data2b.Integral()-allhad2b.Integral()-nonallhad2b.Integral()*mu2b)
    mu_allhad_no_nJetWeight = allhad4b.Integral()/allhad2bShape.Integral() if useAllhad2bShape else 1.0

    muFile.write("mu_qcd_no_nJetWeight_"+cut+"       "+str(mu_qcd_no_nJetWeight)+"\n")
    muFile.write("mu_allhad_no_nJetWeight_"+cut+"     "+str(mu_allhad_no_nJetWeight)+"\n")
    

    (data4b, data2b, allhad2b, allhad4b, allhad2bShape, nonallhad2b, nonallhad4b, qcd, bkgd) = getHists(cut,o.weightRegion,"xwt")
    del bkgd
    #
    # Get prefit 2b->4b scale factors
    #
    nonallhad2b.Scale(mu_nonallhad2b[cut])
    #nonallhad4b.Scale(mu_nonallhad4b[cut])

    nd4b = data4b.Integral()
    nd2b = data2b.Integral()
    na4b = allhad4b.Integral()
    na2b = allhad2b.Integral()
    ns2b = allhad2bShape.Integral()
    naTT = ns2b if useAllhad2bShape else na4b
    nn4b = nonallhad4b.Integral()*mu_nonallhad4b[cut]
    nn2b = nonallhad2b.Integral()
    
    mu_allhad[cut] = na4b/naTT
    mu_qcd   [cut] = (nd4b - naTT*mu_allhad[cut] - nn4b)/(nd2b - na2b - nn2b)
    print "mu_qcd    (prefit)", mu_qcd[cut]
    print "mu_allhad (prefit)", mu_allhad[cut]
    muFile.write("mu_qcd_prefit_"+cut+"       "+str(mu_qcd[cut])+"\n")
    muFile.write("mu_allhad_prefit_"+cut+"     "+str(mu_allhad[cut])+"\n")
    if o.noFitWeight: 
        mu_allhad[cut] = float(o.noFitWeight)
        mu_qcd   [cut] = (nd4b - naTT*mu_allhad[cut] - nn4b)/(nd2b - na2b - nn2b)

    #
    # Rebin to reduce shape bias in fit
    #
    xwt_bins = [0,0.75,12]
    #qcd           = do_variable_rebinning(qcd          ,xwt_bins,False)
    allhad2b      = do_variable_rebinning(allhad2b     ,xwt_bins,False)
    allhad2bShape = do_variable_rebinning(allhad2bShape,xwt_bins,False)
    allhad4b      = do_variable_rebinning(allhad4b     ,xwt_bins,False)
    nonallhad2b   = do_variable_rebinning(nonallhad2b  ,xwt_bins,False)
    nonallhad4b   = do_variable_rebinning(nonallhad4b  ,xwt_bins,False)
    data2b        = do_variable_rebinning(data2b       ,xwt_bins,False)
    data4b        = do_variable_rebinning(data4b       ,xwt_bins,False)

    #S = allhad2bShape.GetBinContent(1)
    #B = qcd          .GetBinContent(1)
    #print "allhad sensitivity: S/root(B) =",S,"/root(",B,") = ",S/B**0.5

    # allhad enriched
    q_bin2 = data2b.GetBinContent(1) - allhad2b.GetBinContent(1) - nonallhad2b.GetBinContent(1)*mu_nonallhad2b[cut]
    a_bin2 = allhad2bShape.GetBinContent(1)
    n_bin2 = nonallhad4b.GetBinContent(1)
    d_bin2 = data4b.GetBinContent(1)

    # qcd enriched
    q_bin1 = data2b.GetBinContent(2) - allhad2b.GetBinContent(2) - nonallhad2b.GetBinContent(2)*mu_nonallhad2b[cut]
    a_bin1 = allhad2bShape.GetBinContent(2)
    n_bin1 = nonallhad4b.GetBinContent(2)
    d_bin1 = data4b.GetBinContent(2)

    print "prefit allhad purity"
    print "a_bin2*mu_allhad[cut]/(q_bin2*mu_qcd[cut]+a_bin2*mu_allhad[cut]+n_bin2*mu_nonallhad4b[cut]) =",a_bin2*mu_allhad[cut]/(q_bin2*mu_qcd[cut]+a_bin2*mu_allhad[cut]+n_bin2*mu_nonallhad4b[cut])
    print "S/root(B) =",a_bin2*mu_allhad[cut]/(q_bin2*mu_qcd[cut]+n_bin2*mu_nonallhad4b[cut])**0.5

    # To ensure proper error treatment, make a 3 bin hist for fitting. 1 bin for qcd enriched, 1 for allhad enriched, 1 for nonallhad enriched. 
    # Then the fit result will have the full 3d covariance matrix
    q_3bin = ROOT.TH1F("qcd_3bin","",3,0,3)
    q_3bin.SetBinContent(1,q_bin1)
    q_3bin.SetBinContent(2,q_bin2)
    q_3bin.SetBinContent(3,q_bin3)
    print "qcd:       qcd enriched = ",q_bin1
    print "qcd:    allhad enriched = ",q_bin2
    print "qcd: nonallhad enriched = ",q_bin3

    a_3bin = ROOT.TH1F("allhad_3bin","",3,0,3)
    a_3bin.SetBinContent(1,a_bin1)
    a_3bin.SetBinContent(2,a_bin2)
    a_3bin.SetBinContent(3,a_bin3)
    print "allhad:       qcd enriched = ",a_bin1
    print "allhad:    allhad enriched = ",a_bin2
    print "allhad: nonallhad enriched = ",a_bin3

    n_3bin = ROOT.TH1F("nonallhad_3bin","",3,0,3)
    n_3bin.SetBinContent(1,n_bin1)
    n_3bin.SetBinContent(2,n_bin2)
    n_3bin.SetBinContent(3,n_bin3)
    print "nonallhad:       qcd enriched = ",n_bin1
    print "nonallhad:    allhad enriched = ",n_bin2
    print "nonallhad: nonallhad enriched = ",n_bin3

    d_3bin = ROOT.TH1F("data_3bin","",3,0,3)
    d_3bin.SetBinContent(1,d_bin1)
    d_3bin.SetBinContent(2,d_bin2)
    d_3bin.SetBinContent(3,d_bin3)
    print "data:       qcd enriched = ",a_bin1
    print "data:    allhad enriched = ",a_bin2
    print "data: nonallhad enriched = ",a_bin3

    # define background fit function from hists
    # def bkgd_func(x,par):
    #     xx = x[0]
    #     b  = qcd.GetXaxis().FindBin(xx)
    #     #k_qcd = (nd4b - par[0]*naTT - nn4b)/(nd2b - na2b - nn2b)
    #     k_qcd = par[1]
    #     return k_qcd*qcd.GetBinContent(b) + par[0]*(allhad2bShape if useAllhad2bShape else allhad4b).GetBinContent(b) + nonallhad4b.GetBinContent(b)

    def bkgd_func(x,par):
        xx = x[0]
        b  = q_3bin.GetXaxis().FindBin(xx)
        return par[0]*q_3bin.GetBinContent(b) + par[1]*a_3bin.GetBinContent(b) + par[2]*n_3bin.GetBinContent(b)

    # set to prefit scale factor
    # tf1_bkgd = ROOT.TF1("tf1_bkgd",bkgd_func,0,12,2)
    # tf1_bkgd.SetParameter(0,mu_allhad[cut])
    # tf1_bkgd.SetParameter(1,mu_qcd[cut])

    tf1_bkgd = ROOT.TF1("tf1_bkgd",bkgd_func,0,3,3)
    tf1_bkgd.SetParameter(0,mu_qcd[cut])
    tf1_bkgd.SetParameter(1,mu_allhad[cut])
    tf1_bkgd.SetParameter(2,mu_nonallhad4b[cut])

    if o.noFitWeight: tf1_bkgd.FixParameter(1,mu_allhad[cut])
    fitResult = d_3bin.Fit(tf1_bkgd,"0 S")


    ele_cov = array("d",[0 for x in range(9)])
    ele_cor = array("d",[0 for x in range(9)])
    for i in range(3):
        for j in range(3):
            ele_cov[3*i+j] = fitResult.CovMatrix(i,j)
            ele_cor[3*i+j] = fitResult.Correlation(i,j)
    cov = ROOT.TMatrixD(3,3,ele_cov)
    cor = ROOT.TMatrixD(3,3,ele_cor)

    print "Covariance Matrix:"
    cov.Print()
    print "Correlation Matrix:"
    cor.Print()

    eigenVal = ROOT.TVectorD(3)
    eigenVec = cov.EigenVectors(eigenVal)
    print "Eigenvectors"
    eigenVec.Print()
    print "Eigenvalues"
    eigenVal.Print()
    
    errorVec = []
    for j in range(3):
        for i in range(3):
            errorVec.append(eigenVec[i][j]*eigenVal[j]**0.5)

    mu_qcd        [cut] = tf1_bkgd.GetParameter(0)
    mu_allhad     [cut] = tf1_bkgd.GetParameter(1)
    mu_nonallhad4b[cut] = tf1_bkgd.GetParameter(2)

    mu_qcd_err        [cut] = tf1_bkgd.GetParError(0)
    mu_allhad_err     [cut] = tf1_bkgd.GetParError(1)
    mu_nonallhad4b_err[cut] = tf1_bkgd.GetParError(2)

    print "Post-fit ----------------------------------"
    print "mu_qcd         ", mu_qcd        [cut],"+/-",mu_qcd_err        [cut]
    print "mu_allhad      ", mu_allhad     [cut],"+/-",mu_allhad_err     [cut]
    print "mu_nonallhad4b ", mu_nonallhad4b[cut],"+/-",mu_nonallhad4b_err[cut]

    c=ROOT.TCanvas("combinedBackgroundFit_"+cut,"Post-fit")

    d_3bin.SetLineColor(ROOT.kBlack)
    d_3bin.SetMinimum(0)
    d_3bin.Draw("PE")

    q_3bin.SetLineColor(ROOT.kBlack)
    q_3bin.SetFillColor(ROOT.kYellow)
    q_3bin.Scale(mu_qcd[cut])

    a_3bin.SetLineColor(ROOT.kBlack)
    a_3bin.SetFillColor(ROOT.kAzure-9)
    a_3bin.Scale(mu_allhad[cut])

    n_3bin.SetLineColor(ROOT.kBlack)
    n_3bin.SetFillColor(ROOT.kAzure-4)
    n_3bin.Scale(mu_nonallhad4b[cut])

    stack = ROOT.THStack("stack","stack")
    stack.Add(n_3bin,"hist")
    stack.Add(a_3bin,"hist")
    stack.Add(q_3bin,"hist")
    stack.Draw("HIST SAME")
    d_3bin.Draw("PE SAME axis")
    d_3bin.Draw("PE SAME")
    c.SaveAs(o.outputDir+"/"+"combinedBackgroundFit_"+cut+"_iter"+o.iteration+".pdf")

    #post-fit plots
    getHists(cut,o.weightRegion,"xwt","PassHCdEta")
    getHists(cut,o.weightRegion,"nPromptMuons","PassHCdEta")
    getHists(cut,o.weightRegion,"m4j_cor_v","PassHCdEta")

    del data4b
    del data2b
    del allhad2b
    del allhad4b
    del allhad2bShape
    del nonallhad2b
    del nonallhad4b
    del qcd
    del stack

    #
    # Store mu_XXX info in text file
    #
    muFile.write("mu_qcd_"+cut+"       "+str(mu_qcd[cut])+"\n")
    muFile.write("mu_qcd_"+cut+"_err   "+str(mu_qcd_err[cut])+"\n")
    muFile.write("mu_allhad_"+cut+"     "+str(mu_allhad[cut])+"\n")
    muFile.write("mu_allhad_"+cut+"_err "+str(mu_allhad_err[cut])+"\n")
    muFile.write("mu_nonallhad2b_"+cut+"     "+str(mu_nonallhad2b[cut])+"\n")
    muFile.write("mu_nonallhad2b_"+cut+"_err "+str(mu_nonallhad2b_err[cut])+"\n")
    muFile.write("mu_nonallhad4b_"+cut+"     "+str(mu_nonallhad4b[cut])+"\n")
    muFile.write("mu_nonallhad4b_"+cut+"_err "+str(mu_nonallhad4b_err[cut])+"\n")
    for i in range(3):
        for j in range(3):
            muFile.write("mu_err_NP"+str(i)+"_comp"+str(j)+"  "+str(errorVec[3*i+j])+"\n")


    #
    # Compute correction for singleTagProb
    #
for cut in ["PassHCdEta"]:
    (data4b, data2b, allhad2b, allhad4b, allhad2bShape, nonallhad2b, nonallhad4b, qcd, bkgd) = getHists(cut,o.weightRegion,"nJetOther","PassHCdEta")
    singleTagProb_qcd = singleTagProbDict["singleTagProb_qcd_"+cut]

    def bkgd_func_njet(x,par):
        xx = x[0]
        b  = qcd.GetXaxis().FindBin(xx)
        nj = b+1
        k_qcd = par[1]* getCombinatoricWeight(par[0],nj)/getCombinatoricWeight(singleTagProb_qcd,nj)
        return k_qcd*qcd.GetBinContent(b) + allhad2bShape.GetBinContent(b) + nonallhad4b.GetBinContent(b)

    # set to prefit scale factor
    tf1_bkgd_njet = ROOT.TF1("tf1_bkgd",bkgd_func_njet,0,9.5,2)
    tf1_bkgd_njet.SetParameter(0,singleTagProb_qcd)
    tf1_bkgd_njet.SetParameter(1,mu_qcd["PassHCdEta"])

    # perform fit
    data4b.Fit(tf1_bkgd_njet,"0")

    newSingleTagProb_qcd    [cut] = tf1_bkgd_njet.GetParameter(0)
    newSingleTagProb_qcd_err[cut] = tf1_bkgd_njet.GetParError(0)
    temp_mu_qcd = tf1_bkgd_njet.GetParameter(1)

    print "newSingleTagProb_qcd    (postfit)", newSingleTagProb_qcd   [cut],"+/-",newSingleTagProb_qcd_err   [cut]
    newSingleTagProbFile.write("singleTagProb_qcd_"+cut+"       "+str(newSingleTagProb_qcd[cut])+"\n")
    newSingleTagProbFile.write("singleTagProb_qcd_"+cut+"_err   "+str(newSingleTagProb_qcd_err[cut])+"\n")

    c=ROOT.TCanvas("nJetOther_"+cut+"_postfit_tf1","Post-fit")
    #data4b.SetLineColor(ROOT.kBlack)
    data4b.Draw("PE")
    qcdDraw = ROOT.TH1F(qcd)
    qcdDraw.SetName(qcd.GetName()+"draw")

    allhadShapeDraw = ROOT.TH1F(allhad2bShape if useAllhad2bShape else allhad4b)
    allhadShapeDraw.SetName((allhad2bShape if useAllhad2bShape else allhad4b).GetName()+"draw")
    #allhadShapeDraw.Scale(mu_allhad[cut])
    stack = ROOT.THStack("stack","stack")
    stack.Add(nonallhad4b,"hist")
    stack.Add(allhadShapeDraw,"hist")
    stack.Add(qcdDraw,"hist")
    stack.Draw("HIST SAME")
    data4b.Draw("PE SAME axis")
    data4b.Draw("PE SAME")
    tf1_bkgd_njet.SetLineColor(ROOT.kRed)
    tf1_bkgd_njet.Draw("SAME")
    c.SaveAs(o.outputDir+"/"+"nJetOther_"+cut+"_postfit_tf1_iter"+o.iteration+".pdf")

muFile.close()
newSingleTagProbFile.close()


#
#now compute kinematic reweighting functions
#

outFile = ROOT.TFile("XhhResolved/data/weights2bto"+("3" if o.threeTag else "4")+"b"+o.weightSet+str(int(o.iteration)+1)+".root","RECREATE")
outFile.cd()

def getBins(data,bkgd,xMax=None):
    
    firstBin = 1
    for bin in range(1,data.GetNbinsX()+1):
        if data.GetBinContent(bin) > 0: 
            firstBin = bin
            break

    lastBin = 0
    for bin in range(data.GetNbinsX(),0,-1):
        if data.GetBinContent(bin) > 0:
            lastBin = bin
            break

    cMax = 0
    for bin in range(1,data.GetNbinsX()+1):
        c = data.GetBinContent(bin)
        if c > cMax: cMax = c

    bins = [lastBin+1]
    sMin = 50
    s=0
    b=0
    bkgd_err=0
    f=-1
    for bin in range(lastBin,firstBin-1,-1):
        if xMax:
            x  = data.GetXaxis().GetBinLowEdge(bin)
            if x >= xMax: bins.append(bin)

        s += data.GetBinContent(bin)
        b += bkgd.GetBinContent(bin)
        bkgd_err += bkgd.GetBinError(bin)**2
        if s<sMin: continue
        if not b:  continue
        if bkgd_err**0.5/b > 0.05: continue
        bins.append(bin)
        f = s/b
        s = 0
        b = 0
        bkgd_err = 0
        if cMax > sMin: sMin += (cMax-sMin)/2
    if s<sMin: bins.pop()
    if firstBin not in bins: bins.append(firstBin)

    bins.sort()
    #print bins[-1],data.GetXaxis().GetBinLowEdge(bins[-1])
    #raw_input()
    
    if len(bins)>20:
        newbins = []
        for i in range(len(bins)):
            if i == len(bins)-1 or i%2==0: newbins.append(bins[i])
        bins = newbins
    bins = range(1,bins[0]) + bins + range(bins[-1]+1,data.GetNbinsX()+1)

    binsX = []
    for bin in bins:
        binsX.append(data.GetXaxis().GetBinLowEdge(bin))
    binsX.append(binsX[-1]+data.GetXaxis().GetBinWidth(bins[-1]))
    #print bins[-1],data.GetXaxis().GetBinLowEdge(bins[-1])
    #raw_input()

    #compute x-mean of each bin
    meansX = []
    Nx = 0
    Ix = 0
    I0 = 0
    I1 = 0
    i  = 1
    for bin in range(1,bkgd.GetNbinsX()+1):
        c = bkgd.GetBinContent(bin)
        l = bkgd.GetXaxis().GetBinLowEdge(bin)
        w = bkgd.GetXaxis().GetBinWidth(bin)
        u = l+w
        x = bkgd.GetXaxis().GetBinCenter(bin)
        Nx += 1
        Ix += x
        I0 += c
        I1 += c*x
        if abs(u - binsX[i])<0.00001: 
            i+=1
            m = I1/I0 if I0>0 else Ix/Nx
            Nx = 0
            Ix = 0
            I0 = 0 
            I1 = 0
            meansX.append(m)


    # if xMax:
    #     new=[]
    #     for bin in binsX:
    #         if bin < xMax: new.append(bin)
    #     binsX = new
            
    return (binsX, meansX)


def fillEnds(hist):
    # fill ratio bins at ends of distribution to make smooth spline beyond data points
    # find first bin
    firstBin = 1
    for bin in range(1,hist.GetNbinsX()+1):
        if hist.GetBinContent(bin) > 0 and hist.GetBinError(bin) > 0: 
            firstBin = bin
            break

    #find last bin
    lastBin = 0
    for bin in range(hist.GetNbinsX(),0,-1):
        if hist.GetBinContent(bin) > 0 and hist.GetBinError(bin) > 0:
            lastBin = bin
            break

    for bin in range(1,hist.GetNbinsX()+1):
        if bin < firstBin:
            hist.SetBinContent(bin,hist.GetBinContent(firstBin))
            hist.SetBinError  (bin,0)
        if bin > lastBin:
            hist.SetBinContent(bin,hist.GetBinContent(lastBin))
            hist.SetBinError  (bin,0)


def calcWeights(var, cut ,xMax=None):
    titles={"HCJet2_Pt":"p_{T,2} [GeV]",
            "HCJet4_Pt_s":"p_{T,4} [GeV]",
            "HCJetAbsEta":"<|#eta_{i}|>",
            "leadGC_dRjj":"#DeltaR_{jj}^{close}",
            "sublGC_dRjj":"#DeltaR_{jj}^{other}",
            }
    print "Make reweight spline for ",cut,var
    (data4b, data2b, allhad2b, allhad4b, allhad2bShape, nonallhad2b, nonallhad4b, qcd, bkgd) = getHists(cut,o.weightRegion,var,"PassHCdEta")
    data4b.Add(nonallhad4b  ,-1)
    data4b.Add(allhad2bShape,-1)

    (rebin, mean) = getBins(data4b,qcd,xMax)
    mean_double = array("d",mean)

    widths = [rebin[i+1]-rebin[i] for i in range(len(rebin)-1)]
    width = 1e6
    
    data4b        = do_variable_rebinning(data4b, rebin)
    nonallhad4b   = do_variable_rebinning(nonallhad4b,rebin)
    allhad2bShape = do_variable_rebinning(allhad2bShape,rebin)
    qcd           = do_variable_rebinning(qcd,rebin)
    bkgd          = do_variable_rebinning(bkgd,   rebin)
    
    makePositive(bkgd)
    makePositive(data4b)
    makePositive(qcd)

    data4b.Scale(1.0/data4b.Integral())
    bkgd  .Scale(1.0/bkgd  .Integral())
    qcd   .Scale(1.0/qcd   .Integral())
    data4b.Write()
    qcd   .Write()
    bkgd  .Write()

    can = ROOT.TCanvas(data4b.GetName()+"_ratio",data4b.GetName()+"_ratio",800,400)
    can.SetTopMargin(0.05)
    can.SetBottomMargin(0.15)
    can.SetRightMargin(0.025)
    ratio = ROOT.TH1F(data4b)
    ratio.GetYaxis().SetRangeUser(0,2)
    ratio.SetName(data4b.GetName()+"_ratio")
    #ratio.Divide(bkgd)
    ratio.Divide(qcd)

    raw_ratio = ROOT.TH1F(ratio)
    raw_ratio.SetName(ratio.GetName()+"_raw")
    raw_ratio.SetLineColor(ROOT.kBlack)
    raw_ratio.SetTitle("")
    raw_ratio.SetStats(0)
    raw_ratio.GetXaxis().SetTitle(titles[var])
    raw_ratio.GetXaxis().SetLabelFont(43)
    raw_ratio.GetXaxis().SetLabelSize(18)
    raw_ratio.GetXaxis().SetTitleFont(43)
    raw_ratio.GetXaxis().SetTitleSize(21)
    raw_ratio.GetXaxis().SetTitleOffset(1.1)
    raw_ratio.GetYaxis().SetTitle("(Data_{4b} - t#bar{t}_{4b}) / (Data_{2b} - t#bar{t}_{2b})")
    raw_ratio.GetYaxis().SetLabelFont(43)
    raw_ratio.GetYaxis().SetLabelSize(18)
    raw_ratio.GetYaxis().SetLabelOffset(0.008)
    raw_ratio.GetYaxis().SetTitleFont(43)
    raw_ratio.GetYaxis().SetTitleSize(21)
    raw_ratio.GetYaxis().SetTitleOffset(0.85)
    raw_ratio.Draw("SAME PE")

    #fillEnds(ratio)
    #ratio.Smooth()
    #fillEnds(ratio)

    #ratio.SetLineColor(ROOT.kBlue)
    #ratio.Draw("SAME PE")
    ratio.Write()

    ratio_TGraph  = ROOT.TGraphAsymmErrors()
    ratio_TGraph.SetName("ratio_TGraph"+var)

    #get first and last non-empty bin
    yf = ROOT.Double(1)
    yl = ROOT.Double(1)
    z  = ROOT.Double(0)
    found_first = False
    for bin in range(1,ratio.GetSize()-1):
        x = ROOT.Double(ratio.GetBinCenter(bin))
        c = ratio.GetBinContent(bin)
        if c > 0:
            if xMax:
                if x < xMax: yl = ROOT.Double(c)
            else:
                yl = ROOT.Double(c)
            if found_first: continue
            found_first = True
            yf = ROOT.Double(c)
            # ratio_TGraph.SetPoint(0,ROOT.Double(rebin[0]),yf)
            # ratio_TGraph.SetPointError(0,z,z,z,z)
            # ratio_TGraph.SetPoint(1,x+(x-ROOT.Double(rebin[0]))/2,yf)
            # ratio_TGraph.SetPointError(0,z,z,z,z)



    found_first = False
    found_last  = False
    p = 0
    done        = False
    # kde = ROOT.TKDE()
    # kde.SetIteration(ROOT.TKDE.kAdaptive)
    # kde.SetKernelType(ROOT.TKDE.kGaussian)
    # #kde.SetRange(ROOT.Double(rebin[0]),ROOT.Double(rebin[-1]))
    # kde.SetTuneFactor(ROOT.Double(0.1))
    errors=[]
    for bin in range(1,ratio.GetSize()-1):
        l = ROOT.Double(ratio.GetXaxis().GetBinLowEdge(bin))
        x = ROOT.Double(ratio.GetBinCenter(bin))
        u = l+ROOT.Double(ratio.GetXaxis().GetBinWidth(bin))
        #print l,u,bin-1,len(mean)
        m = ROOT.Double(mean[bin-1])
        ey  = ROOT.Double(ratio.GetBinError(bin))
        errors.append(ratio.GetBinError(bin))
        exl = m-l
        exh = u-m

        if x<l or x>u: print "ERROR: mean",m,"not between bin limits",l,u

        c = ratio.GetBinContent(bin)
        if c <= 0 and not found_first:
            y = yf
            ey = z
        elif c > 0:
            found_first = True
            y = ROOT.Double(c)
            if xMax:
                if x >= xMax: 
                    y = yl
                    found_last = True
        elif not found_first:
            y = yf
            ey = z
        else:
            y = yl
            ey = 0
            found_last = True


        if found_first and not found_last and widths[bin-1] < width: width = widths[bin-1]

        #if not found_first: continue
        #if found_last: 
            # ratio_TGraph.SetPoint(p,m + (m-ROOT.Double(rebin[-1])/2),yl)
            # ratio_TGraph.SetPointError(p,z,z,z,z)
            # ratio_TGraph.SetPoint(p,ROOT.Double(rebin[-1]),yl)
            # ratio_TGraph.SetPointError(p,z,z,z,z)
            #break


        ratio_TGraph.SetPoint(p,m,y if "trigBit" not in var else ROOT.Double(c))
        ratio_TGraph.SetPointError(p,exl,exh,ey,ey)
        p+=1
        #kde.Fill(m,y)
        #if found_last: done = True
    width = width*4
    # for p in range(ratio_TGraph.GetN()):
    #     x=ROOT.Double(0)
    #     y=ROOT.Double(0)
    #     ratio_TGraph.GetPoint(p,x,y)
    #     print p,x,y
    # raw_input()
    #ratio_TGraphForSmoothing = ROOT.TGraphAsymmErrors(ratio_TGraph)
    #ratio_TGraphForSmoothing.SetName("ratio_TGraphForSmoothing")

    ratio_TGraph.SetLineColor(ROOT.kBlue)
    ratio_TGraph.Draw("SAME PE")

    ratio_smoother = ROOT.TGraphSmooth("ratio_smoother")
    #ratio_smooth = ratio_smoother.SmoothLowess(ratio_TGraph,"",0.2,100)
    errors = array("d",errors)
    #ratio_smooth = ratio_smoother.SmoothSuper(ratio_TGraph,"",0,0.2,False,errors)
    ratio_smooth = ratio_smoother.SmoothKern(ratio_TGraph,"normal",width,len(mean),mean_double)
    ratio_smooth.SetName("ratio_smooth")
    ratio_smooth.SetLineColor(ROOT.kGreen)
    ratio_smooth.Draw("SAME PE")
    ratio_TSpline = ROOT.TSpline3("spline_"+var, ratio_smooth)
    ratio_TSpline.SetName("spline_"+var)

    ratio_TSpline.Write()
    ratio_TSpline.SetLineColor(ROOT.kRed)
    ratio_TSpline.Draw("SAME")

    # kde.Draw("SAME")
    # graph_kde = kde.GetGraphWithErrors(1000,ROOT.Double(rebin[0]),ROOT.Double(rebin[-1]))
    # graph_kde.Draw("SAME PE")

    can.SaveAs(o.outputDir+"/"+data4b.GetName()+"_iter"+o.iteration+"_ratio.pdf")

    del data4b
    del data2b
    del allhad2b
    del allhad4b
    del allhad2bShape
    del nonallhad2b
    del nonallhad4b
    del qcd
    del bkgd
    del ratio_TGraph
    return 


def calcWeights2D(var, cut, rebinX, rebinY):
    print "Make 2D reweight for ",cut,var
    (data4b, data2b, allhad2b, allhad4b, allhad2bShape, nonallhad2b, nonallhad4b, qcd, bkgd) = getHists(cut,o.weightRegion,var,"PassHCdEta")
    data4b.Add(nonallhad4b  ,-1)
    data4b.Add(allhad2bShape,-1)

    data4b.RebinX(rebinX)
    data4b.RebinY(rebinY)
    nonallhad4b.RebinX(rebinX)
    nonallhad4b.RebinY(rebinY)
    allhad2bShape.RebinX(rebinX)
    allhad2bShape.RebinY(rebinY)
    qcd.RebinX(rebinX)
    qcd.RebinY(rebinY)
    bkgd.RebinX(rebinX)
    bkgd.RebinY(rebinY)
    
    makePositive(bkgd)
    makePositive(data4b)
    makePositive(qcd)

    data4b.Scale(1.0/data4b.Integral())
    bkgd  .Scale(1.0/bkgd  .Integral())
    qcd   .Scale(1.0/qcd   .Integral())
    data4b.Write()
    qcd   .Write()
    bkgd  .Write()

    can = ROOT.TCanvas(data4b.GetName()+"_ratio",data4b.GetName()+"_ratio",800,800)
    ratio = ROOT.TH2F(data4b)
    ratio.SetStats(0)
    ratio.GetZaxis().SetRangeUser(0.5,1.5)
    ratio.SetName(data4b.GetName()+"_ratio")
    ratio.Divide(qcd)
    ratio.Draw("COLZ")

    can.SaveAs(o.outputDir+"/"+data4b.GetName()+"_iter"+o.iteration+"_ratio.pdf")

    del data4b
    del data2b
    del allhad2b
    del allhad4b
    del allhad2bShape
    del nonallhad2b
    del nonallhad4b
    del qcd
    del bkgd
    return 

kinematicWeightsCut="PassHCdEta"
#calcWeights("HCJet1_Pt",  kinematicWeightsCut)
calcWeights("HCJet2_Pt",  kinematicWeightsCut)
#calcWeights("HCJet3_Pt_s",kinematicWeightsCut)
calcWeights("HCJet4_Pt_s",kinematicWeightsCut,80)
calcWeights("HCJetAbsEta",kinematicWeightsCut)
#calcWeights("trigBits",kinematicWeightsCut,1,"pol1")
#calcWeights("GCdR_diff",  kinematicWeightsCut)
#calcWeights("GCdR_sum",   kinematicWeightsCut)
calcWeights("leadGC_dRjj",kinematicWeightsCut)
calcWeights("sublGC_dRjj",kinematicWeightsCut)
#calcWeights("leadGC_Pt_m",kinematicWeightsCut)
#calcWeights("xwt",        kinematicWeightsCut)
#calcWeights("m4j_cor_l",  kinematicWeightsCut)
#calcWeights2D("dR12dR34",kinematicWeightsCut,4,4)
#calcWeights2D("GC_dR12dR34",kinematicWeightsCut,4,4)

#
# Using computed mu_qcd and mu_allhad, make qcd file
#

f_qcd  = ROOT.TFile(o.qcdFile,"RECREATE")

def subtractTwoTag():
    for dName in inFile.GetListOfKeys():
        if "TwoTag" not in dName.GetName(): continue
        print dName,dName.GetClassName()
        thisDirName = dName.GetName()
        dataDir  = inFile.Get(thisDirName)
        f_qcd.mkdir(thisDirName)
        f_qcd.cd(thisDirName)
        for histKey in dataDir.GetListOfKeys():
            # only store TH1Fs for QCD root file
            if "TH1" not in histKey.GetClassName() and "TH2" not in histKey.GetClassName(): continue
            histName = histKey.GetName()
            h_data   = inFile    .Get(thisDirName+"/"+histName)
            h_allhad = allhadFile.Get(thisDirName+"/"+histName)
            h_nonallhad = nonallhadFile.Get(thisDirName+"/"+histName)
            
            if "TH1F" in histKey.GetClassName():
                h_qcd   = ROOT.TH1F(h_data)
            if "TH2F" in histKey.GetClassName():
                h_qcd   = ROOT.TH2F(h_data)
            h_qcd.Add(h_allhad,-1)
            h_nonallhad.Scale(mu_nonallhad2b["PassHCdEta"])
            h_qcd.Add(h_nonallhad,-1)
            h_qcd.Write()

print "Subtracting 2b ttbar MC from 2b data to make qcd hists (not yet scaled by mu_qcd)"
print " data:",inFile
print "  qcd:",f_qcd
subtractTwoTag()
f_qcd.Close()
