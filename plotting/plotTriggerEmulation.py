import ROOT
import OfficialAtlasStyle


import optparse
parser = optparse.OptionParser()
parser.add_option('-s', '--signalDir',           dest="signalDir",         default="", help="")
parser.add_option('-o', '--outputDir',           dest="outputDir",         default=".", help="")
parser.add_option('-y', '--year',                dest="year",         default="2016", help="")
o, a = parser.parse_args()

ROOT.gROOT.SetBatch(True)

import os
if not os.path.isdir(o.outputDir):
    os.mkdir(o.outputDir)


inFiles = {

    300   : o.signalDir+"/RSG300_2016_hists/hists.root",
    400   : o.signalDir+"/RSG400_2016_hists/hists.root",
    500   : o.signalDir+"/RSG500_2016_hists/hists.root",
    600   : o.signalDir+"/RSG600_2016_hists/hists.root",
    700   : o.signalDir+"/RSG700_2016_hists/hists.root",
    800   : o.signalDir+"/RSG800_2016_hists/hists.root",
    900   : o.signalDir+"/RSG900_2016_hists/hists.root",
    1000  : o.signalDir+"/RSG1000_2016_hists/hists.root",
    1100  : o.signalDir+"/RSG1100_2016_hists/hists.root",
    1200  : o.signalDir+"/RSG1200_2016_hists/hists.root",
}


def getGraph(mass_pts, color, style=ROOT.kSolid):
    gr = ROOT.TGraph(len(mass_pts))
    gr.SetLineWidth(3)
    gr.SetLineColor(color)
    gr.SetMarkerColor(color)
    gr.SetLineStyle(style)
    return gr

def makeCan(name, trigs, grs, ymin=0, ymax=1, yTitle="Efficiency"):
    axis = ROOT.TH1F("axis","axis",1,300,1200)
    axis.GetYaxis().SetRangeUser(ymin,ymax)
    axis.GetYaxis().SetTitle(yTitle)
    axis.GetXaxis().SetTitle("Resonant Mass [GeV]")

    leg = ROOT.TLegend(0,0,1.0,1.0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    can = ROOT.TCanvas(name,name)
    can.cd()
    axis.Draw()

    for t in trigs:
        grs[t].Draw("PL")
        leg.AddEntry(grs[t] , t, "PL")

    can.Update()
    can.SaveAs(o.outputDir+"/"+name+".pdf")


    canLeg = ROOT.TCanvas(name+"_Leg",name+"_Leg")    
    canLeg.cd()
    leg.Draw()
    canLeg.Update()
    canLeg.SaveAs(o.outputDir+"/"+name+"_Leg.pdf")


def doDir(dirName, mass_pts, do2016=True):

    trigs = []

    if do2016:
        trigs = [
            "HLT_j175_bmv2c2085_split",
            "HLT_j175_bmv2c2077_split",
            "HLT_j65_bmv2c2070_split_3j65_L14J15.0ETA25",
            "HLT_j65_bmv2c2070_split_3j65_L13J25.0ETA23",
            "HLT_j70_bmv2c2070_split_3j70_L13J25.0ETA23",
            "HLT_j70_bmv2c2077_split_3j70_L14J15.0ETA25",
            "HLT_j75_bmv2c2077_split_3j75_L13J25.0ETA23",
            "HLT_2j65_bmv2c2070_split_j65",
            "HLT_2j70_bmv2c2077_split_j70",
            "HLT_2j70_bmv2c2070_split_j70",
            "HLT_2j75_bmv2c2077_split_j75",
            "HLT_2j35_bmv2c2070_split_2j35_L14J15.0ETA25",
            "HLT_2j45_bmv2c2070_split_2j45_L13J25.0ETA23",
            "HLT_2j45_bmv2c2077_split_2j45_L14J15.0ETA25",
            "HLT_2j55_bmv2c2077_split_2j55_L13J25.0ETA23",
            ]

    else:
        trigs = [
            "HLT_2j45_bmedium_split_2j45_L14J15.0ETA25",
            "HLT_j175_bmedium_split_j60_bmedium_split",
            "HLT_2j55_bmedium_split_2j55_L13J25.0ETA23",
            "HLT_2j35_btight_split_2j35_L14J15.0ETA25",
            "HLT_2j45_btight_split_2j45_L13J25.0ETA23",
            "HLT_j225_bloose_split",
            "HLT_j300_bloose_split",
            ]
            


    

    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray+1, ROOT.kPink+10 ,ROOT.kGreen+3, 
              ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray+1, ROOT.kPink+10 ,ROOT.kGreen+3, 
              #ROOT.kViolet-1,ROOT.kYellow,ROOT.kRed+2,ROOT.kOrange-8,
              #ROOT.kRed+1, ROOT.kRed+2,  ROOT.kRed+3, ROOT.kRed+4, 
              ]    

    lineStyles = []
    for c in colors:
        lineStyles.append((c,ROOT.kSolid))
        lineStyles.append((c,ROOT.kDashed))

    
    gSMTrigs = {}
    for it in range(len(trigs)):
        gSMTrigs[trigs[it]] = getGraph(mass_pts, lineStyles[it][0], lineStyles[it][1])

    gSMTrigsMCEMulation = {}
    for it in range(len(trigs)):
        gSMTrigsMCEMulation[trigs[it]] = getGraph(mass_pts, lineStyles[it][0],lineStyles[it][1])

    gSMTrigsNonClosure = {}
    for it in range(len(trigs)):
        gSMTrigsNonClosure[trigs[it]] = getGraph(mass_pts, lineStyles[it][0],lineStyles[it][1])


    binNum = 0

    for i in mass_pts:

        print inFiles[i]
        thisFile = ROOT.TFile(inFiles[i],"READ")

        hist_cutflow           = thisFile.Get(dirName+"/cutflow")
        hist_passTrig          = thisFile.Get(dirName+"/passTrig_cutflow")
        hist_passTrigEmulation = thisFile.Get(dirName+"/passTrigEmu_cutflow")

        passSignal = hist_cutflow.GetBinContent(hist_cutflow.GetXaxis().FindBin("passSignal"))

        if not passSignal: continue
        
        print hist_passTrigEmulation

        for t in trigs:
            thisTrig = hist_passTrig.GetBinContent(hist_passTrig.GetXaxis().FindBin(t))
            thisEffTrig   = float(thisTrig)/passSignal
            gSMTrigs[t].SetPoint(binNum, i , thisEffTrig)

            thisTrig_Em = hist_passTrigEmulation.GetBinContent(hist_passTrigEmulation.GetXaxis().FindBin(t))
            thisEffTrigMCEm   = float(thisTrig_Em)/passSignal
            gSMTrigsMCEMulation[t].SetPoint(binNum, i , thisEffTrigMCEm)

            if thisEffTrig:
                gSMTrigsNonClosure[t].SetPoint(binNum, i, (thisEffTrigMCEm-thisEffTrig))
            else:
                gSMTrigsNonClosure[t].SetPoint(binNum, i, 0)


        thisFile.Close()
        binNum += 1
    

    if do2016:
        makeCan(dirName+"_trigDec",    trigs, gSMTrigs)
        makeCan(dirName+"_trigEmu",    trigs, gSMTrigsMCEMulation)
        makeCan(dirName+"_nonClosure", trigs, gSMTrigsNonClosure, -0.1, 0.1, "Efficiency Difference")
    else:
        makeCan(dirName+"_trigDec_2015",    trigs, gSMTrigs)
        makeCan(dirName+"_trigEmu_2015",    trigs, gSMTrigsMCEMulation)
        makeCan(dirName+"_nonClosure_2015", trigs, gSMTrigsNonClosure, -0.5, 0.5, "Efficiency Difference")



AllMassPts = [300,400,500,600,700,800,900,1000,1100,1200]

doDir("TrigStudy",     AllMassPts)
doDir("TrigStudy",     AllMassPts, do2016 = False)
