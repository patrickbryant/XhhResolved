import ROOT
import math

inputFile75NoSys = ROOT.TFile("../Xhh_ICHEP/hists_2016_75GeV-01-02-06/LimitSettingInputs/resolved_4bSR_2016.root","READ")
shapeFile        = ROOT.TFile("./resolved_4bSR_2016_withSys.root", "READ")
signalFile       = ROOT.TFile("./signal_75GeV/hist-01-02-06.root","READ")

outputFile       = ROOT.TFile("./resolved_4bSR_2016_75GeV_wSys.root","RECREATE")


def copyHist(hName, inFile, outFile, outName=None, scale=None, rebin=None):
    h = inFile.Get(hName)
    outFile.cd()
    if outName: 
        h.SetName(outName)
    if scale: 
        h.Scale(scale)
    if rebin:
        h.Rebin(rebin)
    h.Write()

def applyNormSys(hName, normErr, inFile, outFile):
    h = inFile.Get(hName)    
    h_Up = h.Clone(hName+"_Up")
    h_Up.Scale( (1+qcdNormErr))
    outFile.cd()
    h_Up.Write()

    h_Down = h.Clone(hName+"_Down")
    h_Down.Scale((1-qcdNormErr))
    outFile.cd()
    h_Down.Write()

def applyShapeSys(hName, hShapeName, inFile, outFile, shapeFile):
    h_ratio    = ROOT.TH1F(shapeFile.Get(hShapeName))
    h_ratio.SetName(hShapeName+"_ratio_temp")
    h_in_nom = shapeFile.Get(hName)    
    h_ratio.Divide(h_in_nom)


    h = inFile.Get(hName)
    h_out_shape = h.Clone(hShapeName)    


    for i in range(h.GetNbinsX()+1):
        thisRatio = h_ratio.GetBinContent(i)
        oldValue  = h_out_shape.GetBinContent(i)
        newValue  = oldValue * thisRatio
        h_out_shape.SetBinContent(i, newValue)

    outFile.cd()
    h_out_shape.Write()
    h_ratio.Write()


# 
#  Data/ Nominal Bkg
#
copyHists = ["data_hh",  "data_hh_50",
             "qcd_hh",   "qcd_hh_50",
             "ttbar_hh", "ttbar_hh_50", 
             "sm_hh",    "sm_hh_50",    
            ]

for h in copyHists:
    copyHist(h, inputFile75NoSys, outputFile)



#
# QCD 
#

# Norm
qcdNormErr = math.sqrt(0.05*0.05 + 0.05*0.05)
applyNormSys("qcd_hh",    qcdNormErr, inputFile75NoSys, outputFile)
applyNormSys("qcd_hh_50", qcdNormErr, inputFile75NoSys, outputFile)

# Shape
applyShapeSys("qcd_hh",    "qcd_hh_ShapeHighUp",      inputFile75NoSys, outputFile, shapeFile)
applyShapeSys("qcd_hh_50", "qcd_hh_ShapeHighUp_50",   inputFile75NoSys, outputFile, shapeFile)
applyShapeSys("qcd_hh",    "qcd_hh_ShapeHighDown",    inputFile75NoSys, outputFile, shapeFile)
applyShapeSys("qcd_hh_50", "qcd_hh_ShapeHighDown_50", inputFile75NoSys, outputFile, shapeFile)

#
# ttbar
#
ttbarNormErr = 0.58
applyNormSys("ttbar_hh",    ttbarNormErr, inputFile75NoSys, outputFile)
applyNormSys("ttbar_hh_50", ttbarNormErr, inputFile75NoSys, outputFile)

# Shape
applyShapeSys("ttbar_hh",    "ttbar_hh_ShapeHighUp",        inputFile75NoSys, outputFile, shapeFile)
applyShapeSys("ttbar_hh_50", "ttbar_hh_ShapeHighUp_50",     inputFile75NoSys, outputFile, shapeFile)
applyShapeSys("ttbar_hh",    "ttbar_hh_ShapeHighDown",      inputFile75NoSys, outputFile, shapeFile)
applyShapeSys("ttbar_hh_50", "ttbar_hh_ShapeHighDown_50",   inputFile75NoSys, outputFile, shapeFile)

#
#  SM hh 
#
bTagSysMap = [
    ("1",  "sm_hh_FT_EFF_Eigen_B_0__1down"),
    ("2",  "sm_hh_FT_EFF_Eigen_B_0__1up"  ),
    ("3",  "sm_hh_FT_EFF_Eigen_B_1__1down"),
    ("4",  "sm_hh_FT_EFF_Eigen_B_1__1up"  ),
    ("5",  "sm_hh_FT_EFF_Eigen_B_2__1down"),
    ("6",  "sm_hh_FT_EFF_Eigen_B_2__1up"  ),
    ("7",  "sm_hh_FT_EFF_Eigen_B_3__1down"),
    ("8",  "sm_hh_FT_EFF_Eigen_B_3__1up"  ),
    ("9",  "sm_hh_FT_EFF_Eigen_B_4__1down"),
    ("10", "sm_hh_FT_EFF_Eigen_B_4__1up"  ) ,
    ("47", "sm_hh_FT_EFF_extrapolation__1down"),
    ("48", "sm_hh_FT_EFF_extrapolation__1up"),
    ]

for b in bTagSysMap:
    inHistName  = "PassHCdEta_FourTag_Signal/m4j_l_BTagVar"+b[0]
    outHistName = b[1]
    copyHist(inHistName, signalFile, outputFile, outHistName, scale=0.332929)


    outHistName = b[1]+"_50"
    copyHist(inHistName, signalFile, outputFile, outHistName, scale=0.332929, rebin=5)


sm_hh_sysList = [
    "signal_75GeV_JET_EtaIntercalibration_NonClosure__1down",
    "signal_75GeV_JET_EtaIntercalibration_NonClosure__1up",
    "signal_75GeV_JET_GroupedNP_1__1down",
    "signal_75GeV_JET_GroupedNP_1__1up",
    "signal_75GeV_JET_GroupedNP_2__1down",
    "signal_75GeV_JET_GroupedNP_2__1up",
    "signal_75GeV_JET_GroupedNP_3__1down",
    "signal_75GeV_JET_GroupedNP_3__1up",
    "signal_75GeV_JET_JER_SINGLE_NP__1up",
    ]

for d in sm_hh_sysList:
    thisFile = ROOT.TFile(d+"/hist-01-02-06.root","READ")
    inHistName  = "PassHCdEta_FourTag_Signal/m4j_l"

    outHistName = d.replace("signal_75GeV","sm_hh")
    copyHist(inHistName, thisFile, outputFile, outHistName, scale=0.332929)

    outHistName = d.replace("signal_75GeV","sm_hh")+"_50"
    copyHist(inHistName, thisFile, outputFile, outHistName, scale=0.332929, rebin=5)

    thisFile.Close()
