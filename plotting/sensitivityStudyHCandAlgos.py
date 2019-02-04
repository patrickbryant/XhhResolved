import ROOT
from ROOT import TH1F, TCanvas, TPad
import sys
import os
import optparse
import rootFiles
from plotTools import read_mu_qcd_file

parser = optparse.OptionParser()

parser.add_option('-l', '--massList',
                  dest="massList",
                  default="",
                  )
parser.add_option('-o', '--outFile',
                  dest="outFile",
                  default="iter0-01-01-01/sensitivity",
                  )
parser.add_option('-u', '--mu',
                  dest="mu",
                  default="XhhResolved/data/mu_qcd_Nominal-0.txt"
                  )
parser.add_option('-i', '--iter',    dest="iteration",     default="0", help="")
parser.add_option('-v', '--nTuple',    dest="nTuple",     default="01-01-01", help="")

o, a = parser.parse_args()
mu_qcd_dict = read_mu_qcd_file(o.mu)
cutflows = ["Loose"]
algos    = ["DhhMin"]

files = rootFiles.getFiles(o.iteration,o.nTuple)

masses=["M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","SMNR"]

variables = ["m4j_cor_l","m4j_l"]

def get(rootFile, path):
    obj = rootFile.Get(path)
    if str(obj) == "<ROOT.TObject object at 0x(nil)>": 
        rootFile.ls()
        print 
        print "ERROR: Object not found -", rootFile, path
        sys.exit()

    else: return obj

def histCleanup(h):
    h.SetStats(0)
    h.GetXaxis().SetLabelFont(43)
    h.GetXaxis().SetLabelSize(16)
    h.GetYaxis().SetLabelFont(43)
    h.GetYaxis().SetLabelSize(16)
    h.GetXaxis().SetTitleFont(43)
    h.GetXaxis().SetTitleSize(20)
    h.GetYaxis().SetTitleFont(43)
    h.GetYaxis().SetTitleSize(20)
    h.GetXaxis().SetTitleOffset(2.8)
    h.GetYaxis().SetTitleOffset(1.6)

def getSensitivity(h_sig,h_bkg,a,plot = False):

    sensitivity2 = 0
    error2       = 0

    #sigMean = h_sig.GetMean()
    #binMean = h_sig.FindBin(sigMean)
    binMean = h_sig.GetMaximumBin()
    if not binMean: binMean = 2
    sigStdDev = h_sig.GetStdDev()

    if plot: 
        h_sens = TH1F(h_sig)
        h_sens.SetName(h_sig.GetName()+"_"+h_bkg.GetName()+"_sensitivity")
        h_sens.GetYaxis().SetTitle("Relative Sensitivity")

    maxSensitivity = 0

    nBins = h_bkg.GetXaxis().GetNbins()
    #find window which maximizes sensitivity
    for width in range(1,nBins):
        for lowBin in range(1,nBins-width):
            S ,B  = 0,0

            for bin in range(lowBin,lowBin+width):
                S += h_sig.GetBinContent(bin)
                B += h_bkg.GetBinContent(bin) if h_bkg.GetBinContent(bin) > 0 else 0

            sensitivity = S / (a/2.0 + B**0.5)
            if sensitivity > maxSensitivity:
                maxSensitivity = sensitivity
                SMax = S
                BMax = B
                windowLowBin = lowBin
                optimalWidth = width


    sensitivity = maxSensitivity
    optimalWidth = optimalWidth*h_sig.GetXaxis().GetBinWidth(windowLowBin)
    windowLowEdge = h_sig.GetXaxis().GetBinLowEdge(windowLowBin)
    S = SMax
    B = BMax

    for bin in range(h_bkg.GetXaxis().GetNbins()):
        sc = h_sig.GetBinContent(bin)
        se = h_sig.GetBinError(bin)
  
        bc = h_bkg.GetBinContent(bin) if h_bkg.GetBinContent(bin) > 0 else 0
        be = h_bkg.GetBinError(bin)
    
        # m = h_bkg.GetXaxis().GetBinCenter(bin)
        # if abs(m-sigMean) < 2*sigStdDev: #inside signal peak
        #     S += sc
        #     B += bc
            
        bin_sens =  sc / ( a/2.0 + bc**0.5 )
        dE_dS    = 1.0 / ( a/2.0 + bc**0.5 )#partial derivative of sensitivity wrt S
        dE_dB    = -sc / ( 2*bc**0.5 * ( a/2.0 + bc**0.5 )**2 ) if bc else 0.0 # '' wrt B
        bin_err  = ((se*dE_dS)**2 + (be*dE_dB)**2)**0.5

        if plot: 
            h_sens.SetBinContent(bin,bin_sens)
            h_sens.SetBinError(bin,bin_err)

        #sensitivity2 += ( bin_sens )**2
        #error2       += bin_err**2

    # error       = error2**0.5
    # sensitivity = sensitivity2**0.5 
    #sensitivity = S / (a/2.0 + B**0.5)

    dE_dS    = 1.0 / ( a/2.0 + B**0.5 )#partial derivative of sensitivity wrt S
    dE_dB    =  -S / ( 2*B**0.5 * ( a/2.0 + B**0.5 )**2 ) if B else 0.0# '' wrt B

    w_sig    = h_sig.Integral()/h_sig.GetEntries() if h_sig.GetEntries() else 0.0 #calculate weight of an event
    N_sig    = S / w_sig if w_sig else 0.0 #calculate number of events in signal peak
    dS       = (1.0+N_sig)**0.5/N_sig * S if N_sig else 0.0 #calculate error on weighted signal peak using fracional error on unweighted peak

    w_bkg    = h_bkg.Integral()/h_bkg.GetEntries() if h_bkg.GetEntries() else 0.0 
    N_bkg    = B / w_bkg if w_bkg else 0.0
    dB       = (1.0+N_bkg)**0.5/N_bkg * B if N_bkg else 0.0

    error    = ( (dS*dE_dS)**2 + (dB*dE_dB)**2 )**0.5

    if plot:
        h_sens.SetTitle("")
        return h_sens
    else:    return (sensitivity, error, optimalWidth, windowLowEdge, S, B)
 
def plotM4jSensitivity(h_sens, h_sig, h_bkg, width, windowLowEdge, name, sensitivity, error, S, rootB):
    c1 = TCanvas("c1","example",600,700)
    h_sens.SetLineColor(2)
    h_sens.SetMaximum(2.0)
    h_sig.SetLineColor(4)
    if "NonRes" in name:
        maximum = 10
    elif "Mass" in name:
        maximum = 250
    else:
        maximum = 150
    # if "_l" in name:
    #     maximum = maximum*1.8
    # if "xhh" in name:
    #     maximum = 
    h_sig.SetMaximum(maximum)

    h_bkg.SetLineColor(1)
    h_bkg.SetMaximum(maximum)
    histCleanup(h_sens)
    histCleanup(h_sig)
    histCleanup(h_bkg)

    p1 = TPad("p1","p1",0,0.3,1,1)
    p1.SetBottomMargin(0.01)
    p1.Draw()
    p1.cd()

    h_bkg.Draw("hist")
    if "SMNR" in name and "Loose" in name:
        h_sig.Scale(1000)
    if "SMNR" in name and "NonRes" in name:
        h_sig.Scale(100)
    h_sig.Draw("hist SAME")
    c1.cd()
    p2 = TPad("p2","p2",0,0,1,0.3)
    p2.SetTopMargin(0.01)
    p2.SetBottomMargin(0.2)
    p2.Draw()
    p2.cd()
    h_sens.Draw("hist")
    l = ROOT.TLine()
    l.DrawLine(windowLowEdge,      0,windowLowEdge,      2.0)
    l.DrawLine(windowLowEdge+width,0,windowLowEdge+width,2.0)
    if "Mass" in name:
        textX = 470
    else:
        textX = 970
    if "_l" in name:
        textX = 1940
    #th1 = ROOT.TText(970,0.67,"Sensitivity = "+sensitivity+" +/- "+error)
    th1 = ROOT.TText(textX,1.7,"S/(1+sqrt(B)) = "+sensitivity+" +/- "+error)
    th1.SetTextAlign(31)
    th1.SetTextSize(0.08)
    th1.Draw()

    th2 = ROOT.TText(textX,1.5,"S = "+S+", sqrt(B) = "+rootB)
    th2.SetTextAlign(31)
    th2.SetTextSize(0.08)
    th2.Draw()

    c1.cd()
    
    if not os.path.exists(o.outFile):
        os.makedirs(o.outFile)
    c1.SaveAs(o.outFile+"/"+name+".pdf")



f_qcd = ROOT.TFile(files["qcd"],"READ")
f_ttbar = ROOT.TFile(files["ttbar"],"READ")


for cutflow in cutflows:
    for algo in algos:

        for var in variables:
            if var == "leadHCand_Mass":
                h_qcd = get(f_qcd, cutflow+"/"+algo+"/TwoTag/SublHCR/"+var)
            else:
                h_qcd = get(f_qcd, cutflow+"/"+algo+"/TwoTag/Signal/"+var)
                h_ttbar = get(f_ttbar, cutflow+"/"+algo+"/TwoTag/Signal/"+var)
            
            h_qcd.Sumw2()
            h_ttbar.Sumw2()
            
            h_qcd.Scale(mu_qcd_dict["mu_qcd_"+cutflow+algo])
            h_ttbar.Scale(mu_qcd_dict["mu_ttbar_"+cutflow+algo])
            h_bkg = ROOT.TH1F(h_qcd)
            h_bkg.SetName("background"+cutflow+algo+var)
            h_bkg.Add(h_ttbar)

            h_sensitivity = ROOT.TH1F()
            h_sensitivity.SetName(cutflow+algo+var+"_sensitivity")
            h_sensitivity.SetDirectory(0)
            h_sensitivity.GetXaxis().SetTitle("Signal Sample")
            h_sensitivity.GetYaxis().SetTitle("S/(1+sqrt(B))")

            for mass in masses:
                f_sig = ROOT.TFile(files[mass],"READ")            
                if var == "leadHCand_Mass":
                    h_sig = get(f_sig, cutflow+"/"+algo+"/FourTag/SublHCR/"+var)
                else:
                    h_sig = get(f_sig, cutflow+"/"+algo+"/FourTag/Signal/"+var)
                h_sig.Sumw2()
                h_sig.Scale(0.577**2)

                (sensitivity, error, optimalWidth, windowLowEdge, S, B) = getSensitivity(h_sig,h_bkg,2.0)

                h_sens = getSensitivity(h_sig,h_bkg,2.0,True)

                if not os.path.exists(o.outFile+"/"+cutflow+"/"+var):
                    os.makedirs(o.outFile+"/"+cutflow+"/"+var)
                
                plotM4jSensitivity(h_sens, h_sig, h_bkg, optimalWidth, windowLowEdge, cutflow+"/"+var+"/"+mass+"_"+algo, str(sensitivity)[:6], str(error)[:6], str(S)[:5], str((B)**0.5)[:5])
            
                h_sensitivity.Fill(mass,sensitivity)
                bin = h_sensitivity.GetXaxis().FindBin(mass)
                h_sensitivity.SetBinError(bin,error)

                print "-------------------------"
                print h_sig,h_bkg
                print mass,cutflow,algo,var
                print "  Sensitivity:",sensitivity,"+/-",error
                print "Optimal Width:",optimalWidth
                print
                f_sig.Close()
            h_sensitivity.SetMaximum(5)
            h_sensitivity.SetStats(0)
            h_sensitivity.LabelsDeflate("X")
            h_sensitivity.Draw("pe")
            ROOT.gPad.SaveAs(o.outFile+"/"+cutflow+algo+var+"_sensitivity.pdf")
