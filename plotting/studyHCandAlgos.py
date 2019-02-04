from plotTools import plot, read_mu_qcd_file
import rootFiles
import os
import optparse
parser = optparse.OptionParser()

parser.add_option('-a','--all',       action="store_true",          dest="doAll",          default=False, help="")
parser.add_option('--doMain',         action="store_true",          dest="doMain",         default=False, help="")
parser.add_option('--doCRvar',        action="store_true",          dest="doCRvar",        default=False, help="")
parser.add_option('--CR',          dest="CR",        default="Nominal", help="")
parser.add_option('--doSignalOnly',   action="store_true",          dest="doSignalOnly",   default=False, help="")
parser.add_option('--doSignalVsBackgroundShape',   action="store_true",          dest="doSignalVsBackgroundShape",   default=False, help="")
parser.add_option('--doLimitSetting', action="store_true",          dest="doLimitSetting", default=False, help="")
parser.add_option('--doSignal2b4b',   action="store_true",          dest="doSignal2b4b",   default=False, help="")
parser.add_option('--doDataOnly',     action="store_true",          dest="doDataOnly",     default=False, help="")
parser.add_option('--doDataTrig',     action="store_true",          dest="doDataTrig",     default=False, help="")
parser.add_option('--do2dData',       action="store_true",          dest="do2dData",       default=False, help="")
parser.add_option('--do2dSignal',     action="store_true",          dest="do2dSignal",     default=False, help="")
parser.add_option('--doDataMC',       action="store_true",          dest="doDataMC",       default=False, help="")
parser.add_option('--doCutFlow',      action="store_true",          dest="doCutFlow",      default=False, help="")
parser.add_option('--doTrigger',      action="store_true",          dest="doTrigger",      default=False, help="")
parser.add_option('--doWeights',      action="store_true",          dest="doWeights",      default=False, help="")
parser.add_option('--doHCMass',       action="store_true",          dest="doHCMass",       default=False, help="")
parser.add_option('--doJZW',          action="store_true",          dest="doJZW",          default=False, help="")
parser.add_option('--outDir',        dest="outDir",        default="Plots-01-01-01/", help="")
parser.add_option('-i', '--iter',    dest="iteration",     default="0", help="")
parser.add_option('-v', '--nTuple',    dest="nTuple",     default="01-01-01", help="")
parser.add_option('-y', '--year',    dest="year",     default="2015", help="")
parser.add_option('-l', '--lumi',    dest="lumi",     default="3.2 fb^{-1}", help="")
parser.add_option('--tagger',        dest="tagger",     default="MV2c20", help="")

o, a = parser.parse_args()

#o.nTuple = o.o.nTuple
outDir = o.outDir

lumi = o.lumi
if o.year == "2016": lumi = "10.1 fb^{-1}"
if o.year == "2015+2016": lumi = "13.3 fb^{-1}"

tagger = o.tagger

iteration = o.iteration

files={}
if o.year != "comb":
    files[o.year] = rootFiles.getFiles(iteration,o.nTuple,"hists",o.year,o.CR)
else:
    files["2015"] = rootFiles.getFiles(iteration,o.nTuple,"hists","2015",o.CR)
    files["2016"] = rootFiles.getFiles(iteration,o.nTuple,"hists","2016",o.CR)

masses=["H260","M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","nonResonant"]
test=False
#Folders
cutflows = ["Loose"]
algos    = ["DhhMin"]
HC_plane = ["Sideband","Control","Signal","Inclusive","All","SignalZZ","SignalHH","Excess"]
CRvars   = ["LowMass","HighMass","Tight","Loose","FarSB","CloseSB"]
#CRvars   = ["Tight"]

if test:
    HC_plane = ["Sideband","All"]
    masses=["M500"]

muFile = "XhhResolved/data/mu_qcd_"+o.year+"_"+o.CR+"-"+iteration+".txt"

if o.year != "2015+2016":
    mu_qcd_dict = read_mu_qcd_file(muFile)
if o.doCRvar:
    mu_qcd_dict_CRvar={}
    for CR in CRvars:
        mu_qcd_dict_CRvar[CR] = read_mu_qcd_file("XhhResolved/data/mu_qcd_"+o.year+"_"+CR+"-"+iteration+".txt")

rebins = {}
#rebins["m4j_l"] = [400,460,520,580,640,700,800,900,1000,1300,2000] # 20GeV bins originally
rebins["m4j_l"] = [100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,
                   500,520,540,560,580,600,620,640,660,680,700,740,780,820,860,900,960,1020,1080,1160,1240,1320,1400,1500]
rebins["m4j_cor_l"] = rebins["m4j_l"]
rebins["m4j_cor_Z_l"] = [x*10+100 for x in range(91)]
rebins["m4j_cor_H_l"] = [x*10+100 for x in range(91)]

rebins["HCmassCorrelation"] = 2

#rebins["m4j"] #9GeV bins originally. ugh
rebins["m_4j"] = [200,250,300,350,400,450,500,550,600,650,700,800,900,1000,1250,2000,3000]
rebins["leadHCand_Pt_m"] = [0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,340,380,420,500,600,700]
rebins["sublHCand_Pt_m"] = rebins["leadHCand_Pt_m"]
rebins["leadHCand_Pt"] = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,225,250,275,300,350,400,500]
rebins["sublHCand_Pt"] = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,225,250,275,300,350,400,500]
rebins["leadHCand_Ht"] = [30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,225,250,275,300,350,400,500]
rebins["sublHCand_Ht"] = [30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,225,250,275,300,350,400,500]
#rebins["leadHCand_leadJet_Pt"] = [0,30,40,60,80,100,120,140,160,180,200,240,280,320,400,500]
#rebins["sublHCand_leadJet_Pt"] = rebins["leadHCand_leadJet_Pt"]
#rebins["leadHCand_sublJet_Pt"] = rebins["leadHCand_leadJet_Pt"]
#rebins["sublHCand_sublJet_Pt"] = rebins["leadHCand_leadJet_Pt"]
rebins["leadHCand_leadJet_Pt"] = 5
rebins["sublHCand_leadJet_Pt"] = 5
rebins["leadHCand_sublJet_Pt"] = [x*2+20 for x in range(66)]
rebins["sublHCand_sublJet_Pt"] = [x*2+20 for x in range(66)]
rebins["HCjet4_pt"] = [x*2+20 for x in range(66)]
rebins["HCjet3_pt"] = [x*2+20 for x in range(66)]
rebins["otherJets_Pt"] = 4

rebins["leadHCand_leadJet_Pt_m"] = [0,40,60,80,100,120,140,160,180,200,240,280,320,400,500,700]
rebins["leadHCand_sublJet_Pt_m"] = [0,40,60,80,100,120,140,160,180,200,240,280,320,400,500,700]
rebins["sublHCand_leadJet_Pt_m"] = rebins["leadHCand_leadJet_Pt_m"] 
rebins["sublHCand_sublJet_Pt_m"] = rebins["leadHCand_sublJet_Pt_m"] 
rebins["leadHCand_leadJet_E"] = 4
rebins["leadHCand_sublJet_E"] = 2
rebins["sublHCand_leadJet_E"] = 4
rebins["sublHCand_sublJet_E"] = 2
rebins["leadHCand_leadJet_Eta"] = 4
rebins["leadHCand_sublJet_Eta"] = 4
rebins["sublHCand_leadJet_Eta"] = 4
rebins["sublHCand_sublJet_Eta"] = 4
rebins["leadHCand_leadJet_Phi"] = 4
rebins["leadHCand_sublJet_Phi"] = 4
rebins["sublHCand_leadJet_Phi"] = 4
rebins["sublHCand_sublJet_Phi"] = 4
rebins["ht_l"] = 2
rebins["hCandDr"] = [0.25*x for x in range(19)]
rebins["hCandDeta"] = 2
rebins["hCandDphi"] = 4
rebins["leadHCand_dRjj"]        = 4
rebins["sublHCand_dRjj"]        = 4
rebins["leadHCand_Eta"] = 2
rebins["sublHCand_Eta"] = 2
rebins["leadHCand_AbsEta"] = 2
rebins["sublHCand_AbsEta"] = 2
rebins["leadHCand_Phi"] = 2
rebins["sublHCand_Phi"] = 2

#logY = [""]

varLabels = {"m4j"                      : "m_{4j} [GeV]",
             "m4j_cor"                  : "m_{4j} (corrected) [GeV]",
             "m4j_l"                    : "m_{4j} [GeV]",
             "m4j_cor_l"                : "m_{4j} (corrected) [GeV]",
             "m4j_cor_Z_l"              : "m_{4j} (corrected) [GeV]",
             "m4j_cor_H_l"              : "m_{4j} (corrected) [GeV]",
             "m4j_logy"                 : "m_{4j} [GeV]",
             "m4j_cor_logy"             : "m_{4j} (corrected) [GeV]",
             "m4j_l_logy"               : "m_{4j} [GeV]",
             "m4j_cor_l_logy"           : "m_{4j} (corrected) [GeV]",
             "m4j_cor_Z_l_logy"         : "m_{4j} (corrected) [GeV]",
             "m4j_cor_H_l_logy"         : "m_{4j} (corrected) [GeV]",
             "hCandDeta"                : "#Delta#eta_{hh}",
             "hCandDphi"                : "#Delta#phi_{hh}",
             "hCandDr"                  : "#DeltaR_{hh}",
             "HCmassCorrelation"        : "(m_{12}-m_{34})/(m_{12}+m_{34})",
             #"ShiftedHCmasses"          : "Shifted HC Masses [GeV]",
             "xhh"                      : "X_{hh}",
             "dhh"                      : "D_{hh} [GeV]",
             "nPassingViews"            : "# of Views Passing Cuts",
             "nbJets"                   : "# of b-jets",
             "nJets"                    : "# of jets",             
             "leadHCand_dRjj"           : "Lead HC #DeltaR_{jj}",
             "leadHCand_Eta"            : "Lead HC #eta",
             "leadHCand_AbsEta"         : "Lead HC |#eta|",
             "leadHCand_Phi"            : "Lead HC #phi",
             "leadHCand_Mass"           : "m_{2j}^{lead} [GeV]",
             "leadHCand_alpha"          : "m_{h}/(m_{2j}^{lead})",
             "leadHCand_Ht"             : "Lead HC Ht [GeV]",
             "leadHCand_Pt"             : "Lead HC Pt [GeV]",
             "leadHCand_Pt_cor"         : "Lead HC Pt (corrected) [GeV]",
             "leadHCand_leadJet_E"      : "Lead HC Lead Jet E [GeV]",
             "leadHCand_leadJet_Eta"    : "Lead HC Lead Jet #eta",
             "leadHCand_leadJet_Phi"    : "Lead HC Lead Jet #phi",
             "leadHCand_leadJet_Pt"     : "Lead HC Lead Jet Pt [GeV]",
             "leadHCand_leadJet_MV2" : "Lead HC Lead Jet "+tagger,
             "leadHCand_leadJet_Jvt"    : "Lead HC Lead Jet JVT",
             "leadHCand_sublJet_E"      : "Lead HC Subl Jet E [GeV]",
             "leadHCand_sublJet_Eta"    : "Lead HC Subl Jet #eta",
             "leadHCand_sublJet_Phi"    : "Lead HC Subl Jet #phi",
             "leadHCand_sublJet_Pt"     : "Lead HC Subl Jet Pt [GeV]",
             "leadHCand_sublJet_MV2" : "Lead HC Subl Jet "+tagger,
             "leadHCand_sublJet_Jvt"    : "Lead HC Subl Jet JVT",
             "sublHCand_dRjj"           : "Subl HC #DeltaR_{jj}",
             "sublHCand_Eta"            : "Subl HC #eta",
             "sublHCand_AbsEta"         : "Subl HC |#eta|",
             "sublHCand_Phi"            : "Subl HC #phi",
             "sublHCand_Mass"           : "m_{2j}^{subl} [GeV]",
             "sublHCand_alpha"          : "m_{h}/(m_{2j}^{subl})",
             "sublHCand_Ht"             : "Subl HC Ht [GeV]",
             "sublHCand_Pt"             : "Subl HC Pt [GeV]",
             "sublHCand_Pt_cor"         : "Subl HC Pt (corrected) [GeV]",
             "sublHCand_leadJet_E"      : "Subl HC Lead Jet E [GeV]",
             "sublHCand_leadJet_Eta"    : "Subl HC Lead Jet #eta",
             "sublHCand_leadJet_Phi"    : "Subl HC Lead Jet #phi",
             "sublHCand_leadJet_Pt"     : "Subl HC Lead Jet Pt [GeV]",
             "sublHCand_leadJet_MV2" : "Subl HC Lead Jet "+tagger,
             "sublHCand_leadJet_Jvt"    : "Subl HC Lead Jet JVT",
             "sublHCand_sublJet_E"      : "Subl HC Subl Jet E [GeV]",
             "sublHCand_sublJet_Eta"    : "Subl HC Subl Jet #eta",
             "sublHCand_sublJet_Phi"    : "Subl HC Subl Jet #phi",
             "sublHCand_sublJet_Pt"     : "Subl HC Subl Jet Pt [GeV]",
             "sublHCand_sublJet_MV2" : "Subl HC Subl Jet "+tagger,
             "sublHCand_sublJet_Jvt"    : "Subl HC Subl Jet JVT",
             "otherJets_Pt"             : "Other Jets Pt [GeV]",
             "otherJets_E"              : "Other Jets E [GeV]",
             "otherJets_Phi"            : "Other Jets #phi",
             "otherJets_Eta"            : "Other Jets #eta",
             "otherJets_MV2"         : "Other Jets "+tagger,
             "nJetOther"                : "# of additional jets",
             "HCjet4_pt"                : "Softest HC Jet Pt [GeV]",
             "HCjet3_pt"                : "Second Softest HC Jet Pt [GeV]",
             #TTVeto
             "leadHCand_mW"             : "Lead HC mW [GeV]",
             "leadHCand_WdRjj"          : "Lead HC W dR(jj)",
             "leadHCand_mTop"           : "Lead HC mTop [GeV]",
             "leadHCand_TdRwb"          : "Lead HC top dR(bW)",
             "leadHCand_Xtt"            : "Lead HC Xtt",
             "sublHCand_mW"             : "Subl HC mW [GeV]",
             "sublHCand_WdRjj"          : "Subl HC W dR(jj)",
             "sublHCand_mTop"           : "Subl HC mTop [GeV]",
             "sublHCand_TdRwb"          : "Subl HC top dR(bW)",
             "sublHCand_Xtt"            : "Subl HC Xtt",
             }

HCtagVars = {
             "Pt"       : "HC Pt [GeV]",
             "dRjj"     : "HC #DeltaR_{jj}",
             "Mass"     : "HC Mass [GeV]",
             }

direction = {"m4j_l"                    : "+",
             "m4j_cor_l"                : "+",
             "hCandDeta"                : "0",
             "hCandDphi"                : "+",
             "xhh"                      : "-",
             "leadHCand_Pt"             : "+",
             "sublHCand_Pt"             : "+",
             #TTVeto
             # "leadHCand_mW"             : "80.4",
             # "leadHCand_WdRjj"          : "-",
             # "leadHCand_mTop"           : "172.5",
             # "leadHCand_TdRwb"          : "-",
             # "leadHCand_Xtt"            : "-",
             # "sublHCand_mW"             : "80.4",
             # "sublHCand_WdRjj"          : "-",
             # "sublHCand_mTop"           : "172.5",
             # "sublHCand_TdRwb"          : "-",
             # "sublHCand_Xtt"            : "-",             
             }


# plot variable with given plot parameters and sample dictionary
def plotVariable(sample,parameters,variable,outputName):
    if "_logy" in variable: 
        parameters["logY"]   = True
        variable = variable.replace("_logy","")
    if "_logy" in outputName:
        outputName = outputName.replace("_logy","")
    parameters["xTitle"]     = varLabels[variable]
    parameters["rebin"]      = rebins[variable] if variable in rebins else 1
    parameters["outputName"] = outputName
    for f in sample:
        for p in sample[f]:
            sample[f][p]["TObject"] = variable
            
    plot(sample,parameters)


#
# Plot truth match vs anti-truth shapes
#
if (o.doAll or o.doSignalOnly):
    for mass in masses:
        for cutflow in cutflows:
            for region in HC_plane:
                for var in varLabels:
                    samples = {files[o.year][mass]:{cutflow+"/Truth/FourTag/"+region+"/":    {"label"    : mass+" Truth",
                                                                                      "ratio"    : "numer A",
                                                                                      "weight"   : (0.577)**2, #h->bb BR squared
                                                                                      "isData"   : True,
                                                                                      "color"    : "ROOT.kBlack",
                                                                                      },
                                              cutflow+"/NotTruth/FourTag/"+region+"/": {"label"    : mass+" !Truth",
                                                                                        "ratio"    : "denom A",
                                                                                        "weight"   : (0.577)**2, #h->bb BR squared
                                                                                        "color"    : "ROOT.kAzure+2",
                                                                                        },
                                              },
                               }
                
                    parameters = {"ratio"     : True,
                                  "rTitle"    : "Truth/!Truth",
                                  "yTitle"    : "Events",
                                  "lumi"      : [o.year,lumi],
                                  "region"    : region,
                                  "outputDir" : outDir+"/"+cutflow+"/TruthVsAntiTruth/"+mass+"/"+region+"/",
                                  "rebin"     : 1,
                                  }
                    
                    plotVariable(samples, parameters, var, var)

#
# Compare algo+cuts with truth matching to algo+cuts with antitruth matching
#
if o.doAll or o.doSignalOnly:
    for mass in masses:
        for cutflow in cutflows:
            for algo in algos:
                for region in HC_plane:
                    for var in varLabels:

                        samples = {files[o.year][mass]:{cutflow+"/Truth/FourTag/"+region+"/":     {"label"    : "Truth",
                                                                                           "ratio"    : "numer A",
                                                                                           "weight"   : (0.577)**2, #h->bb BR squared
                                                                                           "isData"   : True,
                                                                                           "color"    : "ROOT.kBlack",
                                                                                           },
                                                cutflow+"/"+algo+"Right/FourTag/"+region+"/": {"label"    : "Right View",
                                                                                               "ratio"    : "denom A",
                                                                                               "weight"   : (0.577)**2, #h->bb BR squared
                                                                                               "stack"    : 1,
                                                                                               "color"    : "ROOT.kAzure+2",
                                                                                               },
                                                cutflow+"/"+algo+"Wrong/FourTag/"+region+"/": {"label"    : "Wrong View",
                                                                                               "ratio"    : "denom A",
                                                                                               "weight"   : (0.577)**2, #h->bb BR squared
                                                                                               "stack"    : 0,
                                                                                               "color"    : "ROOT.kCyan+3",
                                                                                               },
                                                },
                                   }
                        
                        parameters = {"ratio"     : True,
                                      "rTitle"    : "Truth/"+algo,
                                      "yTitle"    : "Events",
                                      "lumi"      : [o.year,lumi],
                                      "region"    : region,
                                      "outputDir" : outDir+cutflow+"/"+algo+"/"+mass+"/RightVsWrong/"+region+"/",
                                      "rebin"     : 1,
                                      }
                    
                        plotVariable(samples, parameters, var, var)

#
# Compare twotag to fourtag shape in MC
#
if o.doAll or o.doSignal2b4b:
    for mass in masses:
        for cutflow in cutflows:
            for algo in algos:
                for region in HC_plane:
                    for var in varLabels:

                        samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/":     {"label"    : "4b",
                                                                                              "ratio"    : "numer A",
                                                                                              "normalize": 1,
                                                                                              "isData"   : True,
                                                                                              "color"    : "ROOT.kBlack",
                                                                                              },
                                                cutflow+"/"+algo+"/TwoTag/"+region+"/":      {"label"    : "2b",
                                                                                              "ratio"    : "denom A",
                                                                                              "normalize": 1,
                                                                                              "color"    : "ROOT.kYellow",
                                                                                              },
                                                },
                                   }
                    
                        parameters = {"ratio"     : True,
                                      "rTitle"    : "4b/2b",
                                      "yTitle"    : "Arb. Units",
                                      "lumi"      : [o.year,lumi],
                                      "region"    : region,
                                      "outputDir" : outDir+cutflow+"/"+algo+"/"+mass+"/FourVsTwoTag/"+region+"/",
                                      "rebin"     : 1,
                                      }
                    
                        plotVariable(samples, parameters, var, var)


#
# Compare twotag to fourtag shape in MC
#
if o.doAll or o.doJZW:
    # for cutflow in cutflows:
    #     for algo in algos:
    #         for region in HC_plane:
    #             for var in varLabels:

                    # samples = {files[o.year]["JZW"]:{cutflow+"/"+algo+"/FourTag/"+region+"/":     {"label"    : "4b",
                    #                                                                        "ratio"    : "numer A",
                    #                                                                        "normalize": 1,
                    #                                                                        "isData"   : True,
                    #                                                                        "color"    : "ROOT.kBlack",
                    #                                                                        },
                    #                          cutflow+"/"+algo+"/TwoTag/"+region+"/":      {"label"    : "2b",
                    #                                                                        "ratio"    : "denom A",
                    #                                                                        "normalize": 1,
                    #                                                                        "color"    : "ROOT.kYellow",
                    #                                                                        },
                    #                          },
                    #            }
                    
                    # parameters = {"ratio"     : True,
                    #               "rTitle"    : "4b/2b",
                    #               "yTitle"    : "Arb. Units",
                    #               "title"     : "FourTag vs TwoTag Shape",
                    #               "lumi"      : [o.year,lumi],
                    #               "outputDir" : outDir+cutflow+"/"+algo+"/JZW/FourVsTwoTag/"+region+"/",
                    #               "rebin"     : 1,
                    #               }
                    
                    # plotVariable(samples, parameters, var, var)

    samples = {files[o.year]["njPrediction"]:{"nJetOtherPDF":     {"label"    : "nJetOtherPDF",
                                                    "normalize": 1,
                                                    "isData"   : True,
                                                    "color"    : "ROOT.kBlack",
                                                    "TObject"  : "",
                                                    },
                                      },
               }
    
    parameters = {"ratio"     : False,
                  "yTitle"    : "Arb. Units",
                  "xTitle"    : "# of additional Jets",
                  "xTitleOffset": 1,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"Loose/DhhMin/nJetShape/",
                  "outputName": "nJetOther_control",
                  "rebin"     : 1,
                  }
    
    plot(samples, parameters)

    samples = {files[o.year]["njPrediction"]:{"allJetsMV2":     {"label"    : "allJetsMV2",
                                                    "normalize": 1,
                                                    "isData"   : True,
                                                    "color"    : "ROOT.kBlack",
                                                    "TObject"  : "",
                                                    },
                                      },
               }
                    
    parameters = {"ratio"     : False,
                  "yTitle"    : "Arb. Units",
                  "xTitle"    : tagger,
                  "xTitleOffset": 1,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"Loose/DhhMin/nJetShape/",
                  "outputName": "MV2_control",
                  "rebin"     : 1,
                  }
    
    plot(samples, parameters)

    samples = {files[o.year]["njPrediction"]:{"prob4":     {"label"    : "4b Prediction",
                                                    "ratio"    : "numer A",
                                                    "normalize": 1,
                                                    "isData"   : True,
                                                    "color"    : "ROOT.kBlack",
                                                    "TObject"  : "",
                                                    },
                                      "prob2":      {"label"    : "2b Prediction",
                                                     "ratio"    : "denom A",
                                                     "normalize": 1,
                                                     "color"    : "ROOT.kYellow",
                                                     "TObject"  : "",
                                                     },
                                      },
               }
                    
    parameters = {"ratio"     : True,
                  "rTitle"    : "4b/2b",
                  "yTitle"    : "Arb. Units",
                  "xTitle"    : "# of additional Jets",
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"Loose/DhhMin/nJetShape/",
                  "outputName": "predictednJetOther_control",
                  "rebin"     : 1,
                  }
    
    plot(samples, parameters)

    samples = {files[o.year]["njPrediction"]:{"prob2":      {"label"    : "2b Prediction",
                                                     "ratio"    : "denom A",
                                                     "normalize": 1,
                                                     "color"    : "ROOT.kYellow",
                                                     "TObject"  : "",
                                                     },
                                      },
               files[o.year]["data"]:{"Loose/DhhMin/TwoTag/Sideband/nJetOther":{"label": "2b Data",
                                                                        "ratio": "numer A",
                                                                        "normalize": 1,
                                                                        "color": "ROOT.kBlack",
                                                                        "isData": True,
                                                                        "TObject" : "",
                                                                        },
                              },
               }
                    
    parameters = {"ratio"     : True,
                  "rTitle"    : "Data/Pred.",
                  "rMax"      : 1.1,
                  "rMin"      : 0.9,
                  "yTitle"    : "Arb. Units",
                  "xTitle"    : "# of additional Jets",
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"Loose/DhhMin/nJetShape/",
                  "outputName": "2b_prediction_vs_actual_control",
                  "rebin"     : 1,
                  }
    
    plot(samples, parameters)

    samples = {files[o.year]["njPrediction"]:{"prob4":      {"label"    : "4b Prediction",
                                                     "ratio"    : "denom A",
                                                     "normalize": 1,
                                                     "color"    : "ROOT.kYellow",
                                                     "TObject"  : "",
                                                     },
                                      },
               files[o.year]["data"]:{"Loose/DhhMin/FourTag/Sideband/nJetOther":{"label": "4b Data",
                                                                        "ratio": "numer A",
                                                                        "normalize": 1,
                                                                        "color": "ROOT.kBlack",
                                                                        "isData": True,
                                                                        "TObject" : "",
                                                                        },
                              },
               }
                    
    parameters = {"ratio"     : True,
                  "rTitle"    : "Data/Pred.",
                  "rMax"      : 2,
                  "rMin"      : 0,
                  "yTitle"    : "Arb. Units",
                  "xTitle"    : "# of additional Jets",
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"Loose/DhhMin/nJetShape/",
                  "outputName": "4b_prediction_vs_actual_control",
                  "rebin"     : 1,
                  }
    
    plot(samples, parameters)


#
# Compare lead/subl HC mass distributions
#
if o.doAll or o.doSignalOnly or o.doHCMass or o.doMain:
    for mass in masses:
        for cutflow in cutflows:
            for algo in algos:

                samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/Inclusive/leadHCand_Mass":     {"label"    : "m_{2j}^{lead}",
                                                                                                   "normalize": 1,
                                                                                                   "isData"   : True,
                                                                                                   "color"    : "ROOT.kBlack",
                                                                                                   },
                                        cutflow+"/"+algo+"/FourTag/Inclusive/sublHCand_Mass":      {"label"    : "m_{2j}^{subl}",
                                                                                                    "normalize": 1,
                                                                                                    "color"    : "ROOT.kRed-3",
                                                                                                    },
                                        },
                           }
                    
                parameters = {"ratio"     : False,
                              "yTitle"    : "Arb. Units",
                              "lumi"      : [o.year,lumi],
                              "outputDir" : outDir+cutflow+"/"+algo+"/HC_massComparison/",
                              "rebin"     : 1,
                              "outputName": mass
                              }
                    
                plot(samples, parameters)


if (o.doAll or o.doMain or o.doDataMC) and False:
    for mass in ["M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200"]:
        for cutflow in cutflows:
            for algo in algos:
                for var in direction:
                    massWindow = "m"+mass[1:]
                    samples = {
                               files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+massWindow+"/": {"label"    : "Data",
                                                                                    "isData"   : True,
                                                                                    "color"    : "ROOT.kBlack",
                                                                                    },
                                              },
                               files[o.year]["qcd"] :{cutflow+"/"+algo+"/TwoTag/"+massWindow+"/": {"label"    : "Multijet",
                                                                                   "ratio"    : "bkgd"+direction[var],
                                                                                   "stack"    : 1,
                                                                                   "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kYellow",
                                                                                   },
                                              },
                               files[o.year]["ttbar"]:{cutflow+"/"+algo+"/TwoTag/"+massWindow+"/": {"label"    : "t#bar{t}",
                                                                                   "ratio"    : "bkgd"+direction[var],
                                                                                   "stack"    : 0,
                                                                                   "weight"   : mu_qcd_dict["mu_ttbar_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kAzure-9",
                                                                                   },
                                              },
                               files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+massWindow+"/": {"label"    : ("SMNR x1000" if mass == "nonResonant" else mass),
                                                                                  "ratio"    : "signal"+direction[var],
                                                                                  "weight"   : (0.577)**2 * (1000 if mass == "nonResonant" else 1.0), #h->bb BR squared
                                                                                  "color"    : "ROOT.kAzure+2",
                                                                                  },
                                            },
                               }

                    parameters = {"ratio"     : True,
                                  "yTitle"    : "Events",
                                  "rMax"      : 1,
                                  "rMin"      : 0.001,
                                  "rLogY"     : True,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir" : outDir+cutflow+"/"+algo+"/Data_vs_"+mass+"_Signal/",
                                  "rebin"     : 1,
                                  }

                    plotVariable(samples, parameters, var, var)

    
#
# Plot data 
#
if o.doAll or o.doMain or o.doDataOnly:
    for cutflow in cutflows:
        for algo in algos:
            for region in HC_plane:
                for var in varLabels:
                    samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "Data",
                                                                                    "ratio"    : "numer A",
                                                                                    "isData"   : True,
                                                                                    "color"    : "ROOT.kBlack",
                                                                                    },
                                              },
                               files[o.year]["qcd"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "Multijet",
                                                                                   "ratio"    : "denom A",
                                                                                   "stack"    : 1,
                                                                                   "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kYellow",
                                                                                   },
                                              },
                               files[o.year]["ttbar"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "t#bar{t}",
                                                                                   "ratio"    : "denom A",
                                                                                   "stack"    : 0,
                                                                                   "weight"   : mu_qcd_dict["mu_ttbar_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kAzure-9",
                                                                                   },
                                              },
                               files[o.year]["M400"]:{cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "M400",
                                                                                        "weight"   : (0.577)**2, #h->bb BR squared
                                                                                        "color"    : "ROOT.kAzure+2",
                                                                                        },
                                              },
                               files[o.year]["H260"]:{cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "M260 #mu=0.15",
                                                                                        "weight"   : 0.15*(0.577)**2, #h->bb BR squared
                                                                                        "color"    : "ROOT.kGreen",
                                                                                        },
                                              },
                               }

                    parameters = {"ratio"     : True,
                                  "rTitle"    : "Data/Bkgd",
                                  "yTitle"    : "Events",
                                  "lumi"      : [o.year,lumi],
                                  "region"    : region,
                                  "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                                  "rebin"     : 1,
                                  }

                    plotVariable(samples, parameters, var, var)
                for variable in ["Pt","dRjj","Mass"]:
                    samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/taggedLeadHC_"+variable : {"label"    : "Data",
                                                                                                              "ratio"    : "denom A",
                                                                                                              "isData"   : True,
                                                                                                              "normalize": 1,
                                                                                                              "color"    : "ROOT.kBlack",
                                                                                                              "TObject"  : "",
                                                                                                              },
                                              cutflow+"/"+algo+"/TwoTag/"+region+"/taggedLeadHC_"+variable : {"label"    : "Tagged",
                                                                                                              "ratio"    : "numer A",
                                                                                                              "normalize": 1,
                                                                                                              "color"    : "ROOT.kMagenta+2",
                                                                                                              "TObject"  : "",
                                                                                                              },
                                              cutflow+"/"+algo+"/TwoTag/"+region+"/untaggedLeadHC_"+variable : {"label"    : "Untagged",
                                                                                                                "ratio"    : "numer A",
                                                                                                                "normalize": 1,
                                                                                                                "color"    : "ROOT.kRed-3",
                                                                                                                "TObject"  : "",
                                                                                                                },
                                              cutflow+"/"+algo+"/TwoTag/"+region+"/oneTagLeadHC_"+variable : {"label"    : "One Tag",
                                                                                                                "ratio"    : "numer A",
                                                                                                                "normalize": 1,
                                                                                                                "color"    : "ROOT.kBlue",
                                                                                                                "TObject"  : "",
                                                                                                                },
                                              },
                               }

                    parameters = {"ratio"     : True,
                                  "rTitle"    : "[Item]/Data",
                                  "yTitle"    : "Arb. Units",
                                  "xTitle"    : "Lead "+HCtagVars[variable],
                                  "lumi"      : [o.year,lumi],
                                  "region"    : region,
                                  "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                                  "outputName": "tagged_vs_untagged_LeadHC_"+variable,
                                  "rebin"     : 2,
                                  }

                    plot(samples, parameters)

                    samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/taggedSublHC_"+variable : {"label"    : "Data",
                                                                                                              "ratio"    : "denom A",
                                                                                                              "isData"   : True,
                                                                                                              "normalize": 1,
                                                                                                              "color"    : "ROOT.kBlack",
                                                                                                              "TObject"  : "",
                                                                                                              },
                                              cutflow+"/"+algo+"/TwoTag/"+region+"/taggedSublHC_"+variable : {"label"    : "Tagged",
                                                                                                              "ratio"    : "numer A",
                                                                                                              "normalize": 1,
                                                                                                              "color"    : "ROOT.kMagenta+2",
                                                                                                              "TObject"  : "",
                                                                                                              },
                                              cutflow+"/"+algo+"/TwoTag/"+region+"/untaggedSublHC_"+variable : {"label"    : "Untagged",
                                                                                                                "ratio"    : "numer A",
                                                                                                                "normalize": 1,
                                                                                                                "color"    : "ROOT.kRed-3",
                                                                                                                "TObject"  : "",
                                                                                                                },
                                              cutflow+"/"+algo+"/TwoTag/"+region+"/oneTagSublHC_"+variable : {"label"    : "One Tag",
                                                                                                                "ratio"    : "numer A",
                                                                                                                "normalize": 1,
                                                                                                                "color"    : "ROOT.kBlue",
                                                                                                                "TObject"  : "",
                                                                                                                },
                                              },
                               }

                    parameters = {"ratio"     : True,
                                  "rTitle"    : "[Item]/Data",
                                  "yTitle"    : "Arb. Units",
                                  "xTitle"    : "Subl "+HCtagVars[variable],
                                  "lumi"      : [o.year,lumi],
                                  "region"    : region,
                                  "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                                  "outputName": "tagged_vs_untagged_SublHC_"+variable,
                                  "rebin"     : 2,
                                  }

                    plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/m4j_l": {"label"    : "Data",
                                                                                             "ratio"    : "numer A",
                                                                                             "isData"   : True,
                                                                                             "color"    : "ROOT.kBlack",
                                                                                             "TObject"  : "",
                                                                                             },
                                          },
                           files[o.year]["qcd"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/threetagm4j": {"label"    : "Multijet (Three Tag)",
                                                                                              "ratio"    : "denom A",
                                                                                              "stack"    : 1,
                                                                                              "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                              "color"    : "ROOT.kCyan-3",
                                                                                              "TObject"  : "",
                                                                                              },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/taggedLeadHCm4j": {"label"    : "Multijet (Tag Lead HC)",
                                                                                                  "ratio"    : "denom A",
                                                                                                  "stack"    : 2,
                                                                                                  "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                                  "color"    : "ROOT.kYellow",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/taggedSublHCm4j": {"label"    : "Multijet (Tag Subl HC)",
                                                                                                  "ratio"    : "denom A",
                                                                                                  "stack"    : 3,
                                                                                                  "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                                  "color"    : "ROOT.kBlue-3",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/twotagSplitm4j": {"label"    : "Multijet (TwoTag Split)",
                                                                                                 "ratio"    : "denom A",
                                                                                                 "stack"    : 4,
                                                                                                 "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                                 "color"    : "ROOT.kGreen-3",
                                                                                                 "TObject"  : "",
                                                                                                 },
                                          },
                           files[o.year]["ttbar"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/m4j_l": {"label"    : "t#bar{t}",
                                                                                         "ratio"    : "denom A",
                                                                                         "stack"    : 0,
                                                                                         "weight"   : mu_qcd_dict["mu_ttbar_"+cutflow+algo],
                                                                                         "color"    : "ROOT.kAzure-9",
                                                                                         "TObject"  : "",
                                                                                         },
                                           },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "Data/Bkgd",
                              "yTitle"    : "Events",
                              "xTitle"    : varLabels["m4j"],
                              "lumi"      : [o.year,lumi],
                              "region"    : region,
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "tagComposition_m4j",
                              "rebin"     : 2,
                              }

                plot(samples, parameters)
                parameters["logY"] = True
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/m4j_cor_l": {"label"    : "Data",
                                                                                             "ratio"    : "numer A",
                                                                                             "isData"   : True,
                                                                                             "color"    : "ROOT.kBlack",
                                                                                             "TObject"  : "",
                                                                                             },
                                          },
                           files[o.year]["qcd"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/threetagm4j_cor": {"label"    : "Multijet (Three Tag)",
                                                                                                  "ratio"    : "denom A",
                                                                                                  "stack"    : 1,
                                                                                                  "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                                  "color"    : "ROOT.kCyan-3",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/taggedLeadHCm4j_cor": {"label"    : "Multijet (Tag Lead HC)",
                                                                                                  "ratio"    : "denom A",
                                                                                                  "stack"    : 2,
                                                                                                  "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                                  "color"    : "ROOT.kYellow",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/taggedSublHCm4j_cor": {"label"    : "Multijet (Tag Subl HC)",
                                                                                                  "ratio"    : "denom A",
                                                                                                  "stack"    : 3,
                                                                                                  "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                                  "color"    : "ROOT.kBlue-3",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/twotagSplitm4j_cor": {"label"    : "Multijet (TwoTag Split)",
                                                                                                 "ratio"    : "denom A",
                                                                                                 "stack"    : 4,
                                                                                                 "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                                 "color"    : "ROOT.kGreen-3",
                                                                                                 "TObject"  : "",
                                                                                                 },
                                          },
                           files[o.year]["ttbar"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/m4j_cor_l": {"label"    : "t#bar{t}",
                                                                                         "ratio"    : "denom A",
                                                                                         "stack"    : 0,
                                                                                         "weight"   : mu_qcd_dict["mu_ttbar_"+cutflow+algo],
                                                                                         "color"    : "ROOT.kAzure-9",
                                                                                         "TObject"  : "",
                                                                                         },
                                           },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "Data/Bkgd",
                              "yTitle"    : "Events",
                              "xTitle"    : varLabels["m4j_cor"],
                              "lumi"      : [o.year,lumi],
                              "region"    : region,
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "tagComposition_m4j_cor",
                              "rebin"     : 2,
                              }

                plot(samples, parameters)
                parameters["logY"] = True
                plot(samples, parameters)


                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/m4j_l": {"label"    : "Data",
                                                                                         "ratio"    : "denom A",
                                                                                         "isData"   : True,
                                                                                         "normalize": 1,
                                                                                         "color"    : "ROOT.kBlack",
                                                                                         "TObject"  : "",
                                                                                         },
                                          },
                           files[o.year]["qcd"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/threetagm4j": {"label"    : "Multijet (Three Tag)",
                                                                                              "ratio"    : "numer A",
                                                                                              "normalize": 1,
                                                                                              "color"    : "ROOT.kCyan-3",
                                                                                              "TObject"  : "",
                                                                                              },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/taggedLeadHCm4j": {"label"    : "Multijet (Tag Lead HC)",
                                                                                                  "ratio"    : "numer A",
                                                                                                  "normalize": 1,
                                                                                                  "color"    : "ROOT.kYellow",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/taggedSublHCm4j": {"label"    : "Multijet (Tag Subl HC)",
                                                                                                  "ratio"    : "numer A",
                                                                                                  "normalize": 1,
                                                                                                  "color"    : "ROOT.kBlue-3",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/twotagSplitm4j": {"label"    : "Multijet (TwoTag Split)",
                                                                                                 "ratio"    : "numer A",
                                                                                                 "normalize": 1,
                                                                                                 "color"    : "ROOT.kGreen-3",
                                                                                                 "TObject"  : "",
                                                                                                 },
                                          },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "[item]/Data",
                              "yTitle"    : "Events",
                              "xTitle"    : varLabels["m4j"],
                              "lumi"      : [o.year,lumi],
                              "region"    : region,
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "tagCompositionShape_m4j",
                              "rebin"     : 2,
                              }

                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/m4j_cor_l": {"label"    : "Data",
                                                                                         "ratio"    : "denom A",
                                                                                         "isData"   : True,
                                                                                         "normalize": 1,
                                                                                         "color"    : "ROOT.kBlack",
                                                                                         "TObject"  : "",
                                                                                         },
                                          },
                           files[o.year]["qcd"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/threetagm4j_cor": {"label"    : "Multijet (Three Tag)",
                                                                                              "ratio"    : "numer A",
                                                                                              "normalize": 1,
                                                                                              "color"    : "ROOT.kCyan-3",
                                                                                              "TObject"  : "",
                                                                                              },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/taggedLeadHCm4j_cor": {"label"    : "Multijet (Tag Lead HC)",
                                                                                                  "ratio"    : "numer A",
                                                                                                  "normalize": 1,
                                                                                                  "color"    : "ROOT.kYellow",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/taggedSublHCm4j_cor": {"label"    : "Multijet (Tag Subl HC)",
                                                                                                  "ratio"    : "numer A",
                                                                                                  "normalize": 1,
                                                                                                  "color"    : "ROOT.kBlue-3",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                          cutflow+"/"+algo+"/TwoTag/"+region+"/twotagSplitm4j_cor": {"label"    : "Multijet (TwoTag Split)",
                                                                                                 "ratio"    : "numer A",
                                                                                                 "normalize": 1,
                                                                                                 "color"    : "ROOT.kGreen-3",
                                                                                                 "TObject"  : "",
                                                                                                 },
                                          },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "[item]/Data",
                              "yTitle"    : "Events",
                              "xTitle"    : varLabels["m4j_cor"],
                              "lumi"      : [o.year,lumi],
                              "region"    : region,
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "tagCompositionShape_m4j_cor",
                              "rebin"     : 2,
                              }

                plot(samples, parameters)


                samples = {files[o.year]["qcd"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "Multijet",
                                                                                   "ratio"    : "denom A",
                                                                                   #"stack"    : 1,
                                                                                   "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kYellow",
                                                                                   "TObject"  : "qcdweight",
                                                                                   },
                                          },
                           files[o.year]["ttbar"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "t#bar{t}",
                                                                                    "ratio"    : "numer A",
                                                                                    #"stack"    : 0,
                                                                                    "weight"   : mu_qcd_dict["mu_ttbar_"+cutflow+algo],
                                                                                    "color"    : "ROOT.kAzure-9",
                                                                                    "TObject"  : "qcdweight",
                                                                                    },
                                           },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "Stat Error",
                              "yTitle"    : "Events",
                              "xTitle"    : "QCD weight",
                              "lumi"      : [o.year,lumi],
                              "region"    : region,
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "qcdweight",
                              "rebin"     : 1,
                              }

                plot(samples, parameters)

if (o.doAll or o.doMain or o.doDataOnly or o.doDataTrig) and False:
    for cutflow in cutflows:
        for algo in algos:
            for region in HC_plane:

                samples = {files[o.year]["data"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "Two Tag",
                                                                                   "ratio"    : "denom A",
                                                                                   #"stack"    : 1,
                                                                                   "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kYellow",
                                                                                   "TObject"  : "firedHLT",
                                                                                   },
                                           cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "Four Tag",
                                                                                    "ratio"    : "numer A",
                                                                                    #"stack"    : 1,
                                                                                    "isData"   : True,
                                                                                    "color"    : "ROOT.kBlack",
                                                                                    "TObject"  : "firedHLT",
                                                                                    },
                                           },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "4b/2b",
                              "yTitle"    : "Events",
                              "xTitle"    : "",
                              "lumi"      : [o.year,lumi],
                              "region"    : region,
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "firedHLT",
                              "rebin"     : 1,
                              }

                plot(samples, parameters)

                samples = {files[o.year]["data"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "Two Tag",
                                                                                   "ratio"    : "denom A",
                                                                                   #"stack"    : 1,
                                                                                   "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kYellow",
                                                                                   "TObject"  : "firedHLT_unique",
                                                                                   },
                                           cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "Four Tag",
                                                                                    "ratio"    : "numer A",
                                                                                    #"stack"    : 1,
                                                                                    "isData"   : True,
                                                                                    "color"    : "ROOT.kBlack",
                                                                                    "TObject"  : "firedHLT_unique",
                                                                                    },
                                           },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "4b/2b",
                              "yTitle"    : "Events",
                              "xTitle"    : "",
                              "region"     : region,
                              "lumi"      : [o.year,lumi],
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "firedHLT_unique",
                              "rebin"     : 1,
                              }

                plot(samples, parameters)

                samples = {files[o.year]["data"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "Two Tag",
                                                                                   "ratio"    : "denom A",
                                                                                   #"stack"    : 1,
                                                                                   "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kYellow",
                                                                                   "TObject"  : "firedL1",
                                                                                   },
                                           cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "Four Tag",
                                                                                    "ratio"    : "numer A",
                                                                                    #"stack"    : 1,
                                                                                    "isData"   : True,
                                                                                    "color"    : "ROOT.kBlack",
                                                                                    "TObject"  : "firedL1",
                                                                                    },
                                           },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "4b/2b",
                              "yTitle"    : "Events",
                              "xTitle"    : "",
                              "region"     : region,
                              "lumi"      : [o.year,lumi],
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "firedL1",
                              "rebin"     : 1,
                              }

                plot(samples, parameters)

                samples = {files[o.year]["data"] :{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "Two Tag",
                                                                                   "ratio"    : "denom A",
                                                                                   #"stack"    : 1,
                                                                                   "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                   "color"    : "ROOT.kYellow",
                                                                                   "TObject"  : "firedL1_unique",
                                                                                   },
                                           cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "Four Tag",
                                                                                    "ratio"    : "numer A",
                                                                                    #"stack"    : 1,
                                                                                    "isData"   : True,
                                                                                    "color"    : "ROOT.kBlack",
                                                                                    "TObject"  : "firedL1_unique",
                                                                                    },
                                           },
                           }

                parameters = {"ratio"     : True,
                              "rTitle"    : "4b/2b",
                              "yTitle"    : "Events",
                              "xTitle"    : "",
                              "region"     : region,
                              "lumi"      : [o.year,lumi],
                              "outputDir" : outDir+cutflow+"/"+algo+"/Data/"+region+"/",
                              "outputName": "firedL1_unique",
                              "rebin"     : 1,
                              }

                plot(samples, parameters)


#
# signal vs background shape comparison
#
if o.doSignalVsBackgroundShape:
    for cutflow in cutflows:
        for algo in algos:
            for mass in masses:
                for var in varLabels:
                    samples = {files[o.year]["qcd"] :{cutflow+"/"+algo+"/TwoTag/Signal/": {"label"    : "Multijet",
                                                                                           "ratio"    : "denom A",
                                                                                           "normalize": 1,
                                                                                           "color"    : "ROOT.kRed+3",
                                                                                           },
                                                      },
                               files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/Signal/": {"label"    : mass,
                                                                                          "ratio"    : "numer A",
                                                                                          "normalize": 1,
                                                                                          "color"    : "ROOT.kBlue",
                                                                                          },
                                                    },
                               }

                    parameters = {"ratio"     : True,
                                  "rTitle"    : "S/B",
                                  "yTitle"    : "Events",
                                  "lumi"      : [o.year,lumi],
                                  "region"    : "Signal",
                                  "outputDir" : outDir+cutflow+"/"+algo+"/Data/SignalVsBackgroundShape/"+mass+"/",
                                  }

                    plotVariable(samples, parameters, var, var)



#2d hists
if o.doAll or o.doMain or o.do2dSignal or o.doSignalOnly:
    additionalAlgos = []
    for algo in algos:
        additionalAlgos.append(algo)
        additionalAlgos.append(algo+"Right")
        additionalAlgos.append(algo+"Wrong")
    additionalAlgos.append("Truth")
    additionalAlgos.append("NotTruth")
        
    for mass in masses:
        for cutflow in cutflows:
            for algo in additionalAlgos:
                for region in HC_plane:
            
                    samples     = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                           "TObject"    : "m12m34",
                                                                                           },
                                                },
                                   }

                    parameters = {
                                  "box"   : [70,240,210,290],
                                  "yTitle"     : "m_{2j}^{subl} [GeV]",
                                  "xTitle"     : "m_{2j}^{lead} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 3,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/HC_plane/"+mass+"/"+region+"/",
                                  "outputName" : "m12m34_"+algo,
                                  }
                
                    plot(samples,parameters)

                    samples     = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                           "TObject"    : "leadHCand_mWmT",
                                                                                           },
                                                },
                                   }

                    parameters = {
                                  "yTitle"     : "Lead HC m_{t} [GeV]",
                                  "xTitle"     : "Lead HC m_{W} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 3,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/Xtt_plane/"+mass+"/"+region+"/",
                                  "outputName" : "leadHCand_mWmT_"+algo,
                                  }
                
                    plot(samples,parameters)

                    samples     = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                           "TObject"    : "sublHCand_mWmT",
                                                                                           },
                                                },
                                   }

                    parameters = {
                                  "yTitle"     : "Subl HC m_{t} [GeV]",
                                  "xTitle"     : "Subl HC m_{W} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 3,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/Xtt_plane/"+mass+"/"+region+"/",
                                  "outputName" : "sublHCand_mWmT_"+algo,
                                  }
                
                    plot(samples,parameters)

                    samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                       "TObject"    : "m4jLeadHCandPt",
                                                                                       },
                                            },
                               }

                    parameters = {
                                  "yTitle"     : "Lead HC Pt [GeV]",
                                  "xTitle"     : "m_{4j} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 4,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/"+mass+"_MDCs/"+region+"/",
                                  "outputName" : "m4jLeadHCPt_"+algo,
                                  }
            
                    plot(samples, parameters)

                    samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                       "TObject"    : "m4jSublHCandPt",
                                                                                       },
                                            },
                               }

                    parameters = {
                                  "yTitle"     : "Subl HC Pt [GeV]",
                                  "xTitle"     : "m_{4j} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 4,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/"+mass+"_MDCs/"+region+"/",
                                  "outputName" : "m4jSublHCPt_"+algo,
                                  }
            
                    plot(samples, parameters)

                    samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                       "TObject"    : "m4jHCdEta",
                                                                                       },
                                            },
                               }

                    parameters = {
                                  "yTitle"     : "#Delta#eta_{hh}",
                                  "xTitle"     : "m_{4j} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 4,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/"+mass+"_MDCs/"+region+"/",
                                  "outputName" : "m4jHCdEta_"+algo,
                                  }
            
                    plot(samples, parameters)

                    samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                       "TObject"    : "m4jLeadHCdRjj",
                                                                                       },
                                            },
                               }

                    parameters = {
                                  "yTitle"     : "Lead HC #DeltaR_{jj}",
                                  "xTitle"     : "m_{4j} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 4,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/"+mass+"_MDRs/"+region+"/",
                                  "outputName" : "m4jLeadHCdRjj_"+algo,
                                  }
            
                    plot(samples, parameters)

                    samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                       "TObject"    : "m4jSublHCdRjj",
                                                                                       },
                                            },
                               }

                    parameters = {
                                  "yTitle"     : "Subl HC #DeltaR_{jj}",
                                  "xTitle"     : "m_{4j} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 4,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/"+mass+"_MDRs/"+region+"/",
                                  "outputName" : "m4jSublHCdRjj_"+algo,
                                  }
            
                    plot(samples, parameters)

                    samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                       "TObject"    : "m4jHCdPhi",
                                                                                       },
                                            },
                               }

                    parameters = {
                                  "yTitle"     : "#Delta#phi_{hh}",
                                  "xTitle"     : "m_{4j} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 4,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/"+mass+"_MDRs/"+region+"/",
                                  "outputName" : "m4jHCdPhi_"+algo,
                                  }
            
                    plot(samples, parameters)

                    samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                       "TObject"    : "aveMV2",
                                                                                       },
                                            },
                               }

                    parameters = {
                                  "yTitle"     : "Ave MV2",
                                  "xTitle"     : "nJets",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 4,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/"+mass+"_AveMV2/"+region+"/",
                                  "outputName" : "aveMV2_4b_"+algo,
                                  }
            
                    plot(samples, parameters)

                    samples = {files[o.year][mass]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                       "TObject"    : "aveMV2",
                                                                                       },
                                            },
                               }

                    parameters = {
                                  "yTitle"     : "Ave MV2",
                                  "xTitle"     : "nJets",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 4,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir"  : outDir+cutflow+"/"+mass+"_AveMV2/"+region+"/",
                                  "outputName" : "aveMV2_2b_"+algo,
                                  }
            
                    plot(samples, parameters)


if o.doAll or o.doMain or o.do2dData or o.doDataOnly:
    for cutflow in cutflows:
        for algo in algos:
            for region in HC_plane:
            
                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                            "TObject"    : "m12m34",
                                                                                            #"stack"      : 1,
                                                                                            "weight"     : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                            },
                                                  },
                           # files[o.year]["ttbar"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"drawOptions": "COLZ",
                           #                                                                  "TObject"  : "m12m34",
                           #                                                                  "stack"    : 0,
                           #                                                                  "weight"   : mu_qcd_dict["mu_ttbar_"+cutflow+algo],
                           #                                                                  },
                                                   
                           #                         },
                           }
                
                parameters = {"title"      : "",
                              "box"   : [70,240,210,290],
                              "yTitle"     : "m_{2j}^{subl} [GeV]",
                              "xTitle"     : "m_{2j}^{lead} [GeV]",
                              "zTitle"     : "Events/9 GeV^{2}",
                              "zTitleOffset": 1.3,
                              #"yMax"        : 6200 if o.year == "2016" else 1500,
                              "satlas"     : 0.04,
                              "rMargin"    : 0.15,
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 3,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_HC_plane/"+region+"/",
                              # "functions"  : [["((x-120)**2+(y-115)**2)",0,300,0,300,[48**2,88*2]],
                              #                 ["(((x-120)/(0.1*x))**2+((y-115)/(0.1*y))**2)",0,300,0,300,[1.6**2]]],
                              "functions"  : [["((x-120)**2+(y-115)**2)",0,300,0,300,[48**2]],
                                              ["((x-120)**2+(y-115)**2)",0,300,0,300,[88**2]],
                                              ["(((x-120)/(0.1*x))**2+((y-115)/(0.1*y))**2)",0,300,0,300,[1.6**2]]],
                              "outputName" : "m12m34_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "leadHCand_mWmT",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "Subl HC m_{t} [GeV]",
                              "xTitle"     : "Lead HC m_{W} [GeV]",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 3,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_Xtt_plane/"+region+"/",
                              "outputName" : "leadHCand_mWmT_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "sublHCand_mWmT",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "Subl HC m_{t} [GeV]",
                              "xTitle"     : "Subl HC m_{W} [GeV]",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 3,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_Xtt_plane/"+region+"/",
                              "outputName" : "sublHCand_mWmT_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "m4jLeadHCandPt",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "Lead HC Pt [GeV]",
                              "xTitle"     : "m_{4j} [GeV]",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 4,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_MDCs/"+region+"/",
                              "outputName" : "m4jLeadHCPt_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "m4jSublHCandPt",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "Subl HC Pt [GeV]",
                              "xTitle"     : "m_{4j} [GeV]",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 4,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_MDCs/"+region+"/",
                              "outputName" : "m4jSublHCPt_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "m4jHCdEta",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "#Delta#eta_{hh}",
                              "xTitle"     : "m_{4j} [GeV]",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 4,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_MDCs/"+region+"/",
                              "outputName" : "m4jHCdEta_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "m4jLeadHCdRjj",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "Lead HC #DeltaR_{jj}",
                              "xTitle"     : "m_{4j} [GeV]",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 4,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_MDRs/"+region+"/",
                              "outputName" : "m4jLeadHCdRjj_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "m4jSublHCdRjj",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "Subl HC #DeltaR_{jj}",
                              "xTitle"     : "m_{4j} [GeV]",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 4,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_MDRs/"+region+"/",
                              "outputName" : "m4jSublHCdRjj_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "m4jHCdPhi",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "#Delta#phi_{hh}",
                              "xTitle"     : "m_{4j} [GeV]",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 4,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_MDRs/"+region+"/",
                              "outputName" : "m4jHCdPhi_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "aveMV2",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "Ave MV2",
                              "xTitle"     : "nJets",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 4,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_AveMV2/"+region+"/",
                              "outputName" : "aveMV2_2b_"+algo,
                              }
            
                plot(samples, parameters)

                samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                    "TObject"    : "aveMV2",
                                                                                    },
                                          },
                           }

                parameters = {
                              "yTitle"     : "Ave MV2",
                              "xTitle"     : "nJets",
                              "rebin"      : 1, 
                              "canvasSize" : [720,660],
                              "maxDigits"  : 4,
                              "lumi"      : [o.year,lumi],
                              "outputDir"  : outDir+cutflow+"/Data_AveMV2/"+region+"/",
                              "outputName" : "aveMV2_4b_"+algo,
                              }
            
                plot(samples, parameters)


#
# Control region variations/ background cross checks
#
if o.doAll or o.doCRvar:
    for CR in CRvars:
        for cutflow in cutflows:
            for algo in algos:
                for region in HC_plane:
            
                    samples = {files[o.year]["data"+CR]:{cutflow+"/"+algo+"/TwoTag/"+region+"/" : {"drawOptions": "COLZ",
                                                                                           "TObject"    : "m12m34",
                                                                                           },
                                                 },
                               }

                    parameters = {
                                  "yTitle"     : "m_{2j}^{subl} [GeV]",
                                  "xTitle"     : "m_{2j}^{lead} [GeV]",
                                  "rebin"      : 1, 
                                  "canvasSize" : [720,660],
                                  "maxDigits"  : 3,
                                  "outputDir"  : outDir+cutflow+"/Data_HC_plane_CRvar/"+region+"/",
                                  "outputName" : "m12m34_"+CR+"_"+algo,
                                  }
            
                    plot(samples, parameters)

                    samples = {files[o.year]["qcd"+CR]:{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : CR,
                                                                                         "ratio"    : "numer A",
                                                                                         "isData"   : True,
                                                                                         "weight"   : mu_qcd_dict_CRvar[CR]["mu_qcd_"+cutflow+algo],
                                                                                         "color"    : "ROOT.kBlack",
                                                                                         },
                                                },
                               files[o.year]["qcd"]:{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "Nominal",
                                                                                      "ratio"    : "denom A",
                                                                                      "weight"   : mu_qcd_dict["mu_qcd_"+cutflow+algo],
                                                                                      "color"    : "ROOT.kRed+3",
                                                                                      },
                                             },
                               }
                    
                    parameters = {"ratio"     : True,
                                  "rTitle"    : CR+"/Nominal",
                                  "yTitle"    : "Events",
                                  "lumi"      : [o.year,lumi],
                                  "maxDigits" : 5,
                                  "outputDir" : outDir+cutflow+"/"+algo+"/Data_CRvars/"+region+"/",
                                  }
                    
                    plotVariable(samples, parameters, "m4j_l" ,CR+"_m4j_l")
                    plotVariable(samples, parameters, "m4j_cor_l" ,CR+"_m4j_cor_l")
 
                    samples = {files[o.year]["data"]:{cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "Data",
                                                                                        "ratio"    : "numer A",
                                                                                        "isData"   : True,
                                                                                        "color"    : "ROOT.kBlack",
                                                                                        },
                                              },
                               files[o.year]["qcd"+CR] :{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "Multijet",
                                                                                          "ratio"    : "denom A",
                                                                                          "stack"    : 1,
                                                                                          "weight"   : mu_qcd_dict_CRvar[CR]["mu_qcd_"+cutflow+algo],
                                                                                          "color"    : "ROOT.kYellow",
                                                                                          },
                                              },
                               files[o.year]["ttbar"+CR]:{cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "t#bar{t}",
                                                                                           "ratio"    : "denom A",
                                                                                           "stack"    : 0,
                                                                                           "weight"   : mu_qcd_dict_CRvar[CR]["mu_ttbar_"+cutflow+algo],
                                                                                           "color"    : "ROOT.kAzure-9",
                                                                                           },
                                                  },
                               files[o.year]["H260"]:{cutflow+"/"+algo+"/FourTag/"+region+"/": {"label"    : "M260 #mu=0.15",
                                                                                        "weight"   : 0.15*(0.577)**2, #h->bb BR squared
                                                                                        "color"    : "ROOT.kGreen",
                                                                                        },
                                              cutflow+"/"+algo+"/TwoTag/"+region+"/": {"label"    : "M260 #mu=0.15 (2b)",
                                                                                       "weight"   : mu_qcd_dict_CRvar[CR]["mu_qcd_"+cutflow+algo]*0.15*(0.577)**2, 
                                                                                       "color"    : "ROOT.kGreen+2",
                                                                                       },
                                              },
                               }

                    parameters = {"ratio"     : True,
                                  "rTitle"    : "Data/Bkgd",
                                  "yTitle"    : "Events",
                                  "region"     : region,
                                  "lumi"      : [o.year,lumi],
                                  "outputDir" : outDir+cutflow+"/"+algo+"/Data_CRvars/"+region+"/",
                                  "rebin"     : 1,
                                  }

                    plotVariable(samples, parameters, "m4j_l" ,CR+"fullBKGD_m4j_l")
                    plotVariable(samples, parameters, "m4j_cor_l" ,CR+"fullBKGD_m4j_cor_l")


#
# Trigger Efficiencies
#
if (o.doAll or o.doTrigger or o.doMain or o.doSignalOnly) and True:
    for cutflow in cutflows:
        if o.year == "2015":
            samples = {files[o.year]["trigger"]:{cutflow+"_TrigEff_numer_Xhh_passHLT_denom_Xhh": {"label"      : "HLT OR",
                                                                                          "color"      : "ROOT.kBlack",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "21",
                                                                                          "TObject"   : "",
                                                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j70_bmedium_3j70_L14J15.0ETA25_denom_Xhh": {"label"      : "j70_bm_3j70",
                                                                                                                     "color"      : "ROOT.kGreen",
                                                                                                                     "drawOptions" : "P",
                                                                                                                     "marker"      : "22",
                                                                                                                     "TObject"   : "",
                                                                                                                     },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_2j35_btight_2j35_L13J25.0ETA23_denom_Xhh": {"label"      : "2j35_bt_2j35",
                                                                                                                     "color"      : "ROOT.kCyan",
                                                                                                                     "drawOptions" : "P",
                                                                                                                     "marker"      : "24",
                                                                                                                     "TObject"   : "",
                                                                                                                     },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j100_2j55_bmedium_denom_Xhh": {"label"      : "j100_2j55_bm",
                                                                                                        "color"      : "ROOT.kAzure",
                                                                                                        "drawOptions" : "P",
                                                                                                        "marker"      : "26",
                                                                                                        "TObject"   : "",
                                                                                                        },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j225_bloose_denom_Xhh": {"label"      : "j225_bl",
                                                                                                  "color"      : "ROOT.kAzure-9",
                                                                                                  "drawOptions" : "P",
                                                                                                  "marker"      : "27",
                                                                                                  "TObject"   : "",
                                                                                                  },
                                         },
                       }
            
            parameters = {"title"      : "",
                          "yTitle"     : "Efficiency",
                          "xTitle"     : "Signal Sample",
                          "xTitleOffset": 1,
                          "labelSize"  : 16,
                          "lumi"       : [o.year,lumi],
                          "rebin"      : 1, 
                          "yMin"       : 0,
                          "yMax"       : 1.5,
                          "xleg"       : [0.6,0.89],
                          "yleg"       : [0.7,0.92],
                          "xatlas"     : 0.13,
                          "logY"       : False,
                          "ratio"      : False,
                          "outputDir"  : outDir+"/trigger/"+cutflow+"/",
                          "outputName" : "Xhh_HLT_vs_Xhh",
                          "drawLines"  : [[0,1,11,1],[10,0,10,1]]
                          }
        
            plot(samples,parameters)

            samples = {files[o.year]["trigger"]:{cutflow+"_TrigEff_numer_Xhh_passHLT_denom_Xhh": {"label"      : "HLT OR",
                                                                                          "color"      : "ROOT.kBlack",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "21",
                                                                                          "TObject"   : "",
                                                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j70_bmedium_3j70_L14J15.0ETA25only_denom_Xhh": {"label"      : "j70_bm_3j70",
                                                                                                                     "color"      : "ROOT.kGreen",
                                                                                                                     "drawOptions" : "P",
                                                                                                                     "marker"      : "22",
                                                                                                                     "TObject"   : "",
                                                                                                                     },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_2j35_btight_2j35_L14J15.0ETA25only_denom_Xhh": {"label"      : "2j35_bt_2j35",
                                                                                                                     "color"      : "ROOT.kCyan",
                                                                                                                     "drawOptions" : "P",
                                                                                                                     "marker"      : "24",
                                                                                                                     "TObject"   : "",
                                                                                                                     },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j100_2j55_bmediumonly_denom_Xhh": {"label"      : "j100_2j55_bm",
                                                                                                        "color"      : "ROOT.kAzure",
                                                                                                        "drawOptions" : "P",
                                                                                                        "marker"      : "26",
                                                                                                        "TObject"   : "",
                                                                                                        },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j225_blooseonly_denom_Xhh": {"label"      : "j225_bl",
                                                                                                  "color"      : "ROOT.kAzure-9",
                                                                                                  "drawOptions" : "P",
                                                                                                  "marker"      : "27",
                                                                                                  "TObject"   : "",
                                                                                                  },
                                         },
                       }
            
            parameters = {"title"      : "",
                          "yTitle"     : "Efficiency",
                          "xTitle"     : "Signal Sample",
                          "xTitleOffset": 1,
                          "labelSize"  : 16,
                          "lumi"       : [o.year,lumi],
                          "rebin"      : 1, 
                          "yMin"       : 0.0001,
                          "yMax"       : 100,
                          "xleg"       : [0.6,0.89],
                          "yleg"       : [0.7,0.92],
                          "xatlas"     : 0.13,
                          "logY"       : True,
                          "ratio"      : False,
                          "outputDir"  : outDir+"/trigger/"+cutflow+"/",
                          "outputName" : "Xhh_HLT_vs_Xhh_unique",
                          "drawLines"  : [[0,1,11,1],[10,0.0001,10,1]]
                          }
        
            plot(samples,parameters)


            samples = {files[o.year]["trigger"]:{cutflow+"_TrigEff_numer_Xhh_passHLT_denom_Xhh_passL1": {"label"      : "HLT OR",
                                                                                                 "color"      : "ROOT.kBlack",
                                                                                                 "drawOptions" : "P",
                                                                                                 "marker"      : "21",
                                                                                                 "TObject"   : "",
                                                                                                 },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j70_bmedium_3j70_L14J15.0ETA25_denom_Xhh_passL1": {"label"      : "j70_bm_3j70",
                                                                                                                            "color"      : "ROOT.kGreen",
                                                                                                                            "drawOptions" : "P",
                                                                                                                            "marker"      : "22",
                                                                                                                            "TObject"   : "",
                                                                                                                            },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_2j35_btight_2j35_L14J15.0ETA25_denom_Xhh_passL1": {"label"      : "2j35_bt_2j35",
                                                                                                                            "color"      : "ROOT.kCyan",
                                                                                                                            "drawOptions" : "P",
                                                                                                                            "marker"      : "24",
                                                                                                                            "TObject"   : "",
                                                                                                                            },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j100_2j55_bmedium_denom_Xhh_passL1": {"label"      : "j100_2j55_bm",
                                                                                                               "color"      : "ROOT.kAzure",
                                                                                                               "drawOptions" : "P",
                                                                                                               "marker"      : "26",
                                                                                                               "TObject"   : "",
                                                                                                               },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j225_bloose_denom_Xhh_passL1": {"label"      : "j225_bl",
                                                                                                         "color"      : "ROOT.kAzure-9",
                                                                                                         "drawOptions" : "P",
                                                                                                         "marker"      : "27",
                                                                                                         "TObject"   : "",
                                                                                                         },
                                         },
                       }

            parameters = {"title"      : "",
                          "yTitle"     : "Efficiency",
                          "xTitle"     : "Signal Sample",
                          "xTitleOffset": 1,
                          "labelSize"  : 16,
                          "lumi"       : [o.year,lumi],
                          "rebin"      : 1, 
                          "yMin"       : 0,
                          "yMax"       : 1.5,
                          "xleg"       : [0.6,0.89],
                          "yleg"       : [0.7,0.92],
                          "xatlas"     : 0.13,
                          "logY"       : False,
                          "ratio"      : False,
                          "outputDir"  : outDir+"/trigger/"+cutflow+"/",
                          "outputName" : "Xhh_passL1_HLT_vs_Xhh",
                          "drawLines"  : [[0,1,11,1],[10,0,10,1]]
                          }
        
            plot(samples,parameters)


            samples = {files[o.year]["trigger"]:{cutflow+"_TrigEff_numer_Xhh_passL1_denom_Xhh": {"label"      : "L1 OR",
                                                                                         "color"      : "ROOT.kRed",
                                                                                         "drawOptions" : "P",
                                                                                         "marker"      : "20",
                                                                                         "TObject"    : "",
                                                                                         },
                                         cutflow+"_TrigEff_numer_Xhh_L1_J100_denom_Xhh": {"label"      : "L1_J100",
                                                                                          "color"      : "ROOT.kGreen",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "21",
                                                                                          "TObject"    : "",
                                                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_L1_J75_3J20_denom_Xhh": {"label"      : "L1_J75_3J20",
                                                                                          "color"      : "ROOT.kBlue",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "22",
                                                                                          "TObject"    : "",
                                                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_L1_3J25.0ETA23_denom_Xhh": {"label"      : "L1_3J25.0ETA23",
                                                                                                 "color"      : "ROOT.kMagenta",
                                                                                                 "drawOptions" : "P",
                                                                                                 "marker"      : "23",
                                                                                                 "TObject"    : "",
                                                                                                 },
                                         },
                       }

            parameters = {"title"      : "",
                          "yTitle"     : "Efficiency",
                          "xTitle"     : "Signal Sample",
                          "xTitleOffset": 1,
                          "labelSize"  : 16,
                          "lumi"       : [o.year,lumi],
                          "rebin"      : 1, 
                          "yMin"       : 0,
                          "yMax"       : 1.5,
                          "xleg"       : [0.6,0.89],
                          "yleg"       : [0.7,0.92],
                          "xatlas"     : 0.13,
                          "logY"       : False,
                          "ratio"      : False,
                          "outputDir"  : outDir+"/trigger/"+cutflow+"/",
                          "outputName" : "Xhh_L1_vs_Xhh",
                          "drawLines"  : [[0,1,11,1],[10,0,10,1]]
                          }
    
            plot(samples,parameters)
        
        if o.year == "2016":
            samples = {files[o.year]["trigger"]:{cutflow+"_TrigEff_numer_Xhh_passHLT_denom_Xhh": {"label"      : "HLT OR",
                                                                                          "color"      : "ROOT.kBlack",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "21",
                                                                                          "TObject"   : "",
                                                                                          },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_j150_bmv2c2060_split_j50_bmv2c2060_split_denom_Xhh": {"label"      : "j150_b60_j50_b60",
                                         #                                                                       "color"      : "ROOT.kBlue",
                                         #                                                                       "drawOptions" : "P",
                                         #                                                                       "marker"      : "23",
                                         #                                                                       "TObject"   : "",
                                         #                                                                       },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25_denom_Xhh": {"label"      : "2j35_b60_2j35",
                                                                                                                     "color"      : "ROOT.kCyan",
                                                                                                                     "drawOptions" : "P",
                                                                                                                     "marker"      : "24",
                                                                                                                     "TObject"   : "",
                                                                                                                     },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_2j70_bmv2c2050_split_j70_denom_Xhh": {"label"      : "2j70_b50_j70",
                                         #                                                                              "color"      : "ROOT.kOrange",
                                         #                                                                              "drawOptions" : "P",
                                         #                                                                              "marker"      : "25",
                                         #                                                                              "TObject"   : "",
                                         #                                                                              },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_j275_bmv2c2070_split_denom_Xhh": {"label"      : "j275_b70",
                                         #                                                          "color"      : "ROOT.kAzure-9",
                                         #                                                          "drawOptions" : "P",
                                         #                                                          "marker"      : "27",
                                         #                                                          "TObject"   : "",
                                         #                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j225_bmv2c2060_split_denom_Xhh": {"label"      : "j225_b60",
                                                                                                           "color"      : "ROOT.kAzure-9",
                                                                                                           "drawOptions" : "P",
                                                                                                           "marker"      : "27",
                                                                                                           "TObject"   : "",
                                                                                                           },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25_denom_Xhh": {"label"      : "j75_b70_3j75",
                                                                                                                      "color"      : "ROOT.kGreen",
                                                                                                                      "drawOptions" : "P",
                                                                                                                      "marker"      : "22",
                                                                                                                      "TObject"   : "",
                                                                                                                      },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j100_2j55_bmv2c2060_split_denom_Xhh": {"label"      : "j100_2j55_b60",
                                                                                                               "color"      : "ROOT.kAzure",
                                                                                                               "drawOptions" : "P",
                                                                                                               "marker"      : "26",
                                                                                                               "TObject"   : "",
                                                                                                               },
                                         },
                       }

            parameters = {"title"      : "",
                          "yTitle"     : "Efficiency",
                          "xTitle"     : "Signal Sample",
                          "xTitleOffset": 1,
                          "labelSize"  : 16,
                          "lumi"       : [o.year,lumi],
                          "rebin"      : 1, 
                          "yMin"       : 0,
                          "yMax"       : 1.5,
                          "xleg"       : [0.6,0.89],
                          "yleg"       : [0.7,0.92],
                          "xatlas"     : 0.13,
                          "logY"       : False,
                          "ratio"      : False,
                          "outputDir"  : outDir+"/trigger/"+cutflow+"/",
                          "outputName" : "Xhh_HLT_vs_Xhh",
                          "drawLines"  : [[0,1,11,1],[10,0,10,1]]
                          }
        
            plot(samples,parameters)

            samples = {files[o.year]["trigger"]:{cutflow+"_TrigEff_numer_Xhh_passHLT_denom_Xhh_passL1": {"label"      : "HLT OR",
                                                                                          "color"      : "ROOT.kBlack",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "21",
                                                                                          "TObject"   : "",
                                                                                          },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_j150_bmv2c2060_split_j50_bmv2c2060_split_denom_Xhh_passL1": {"label"      : "j150_b60_j50_b60",
                                         #                                                                       "color"      : "ROOT.kBlue",
                                         #                                                                       "drawOptions" : "P",
                                         #                                                                       "marker"      : "23",
                                         #                                                                       "TObject"   : "",
                                         #                                                                       },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25_denom_Xhh_passL1": {"label"      : "2j35_b60_2j35",
                                                                                                                     "color"      : "ROOT.kCyan",
                                                                                                                     "drawOptions" : "P",
                                                                                                                     "marker"      : "24",
                                                                                                                     "TObject"   : "",
                                                                                                                     },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_2j70_bmv2c2050_split_j70_denom_Xhh_passL1": {"label"      : "2j70_b50_j70",
                                         #                                                                              "color"      : "ROOT.kOrange",
                                         #                                                                              "drawOptions" : "P",
                                         #                                                                              "marker"      : "25",
                                         #                                                                              "TObject"   : "",
                                         #                                                                              },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_j275_bmv2c2070_split_denom_Xhh_passL1": {"label"      : "j275_b70",
                                         #                                                          "color"      : "ROOT.kAzure-9",
                                         #                                                          "drawOptions" : "P",
                                         #                                                          "marker"      : "27",
                                         #                                                          "TObject"   : "",
                                         #                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j225_bmv2c2060_split_denom_Xhh_passL1": {"label"      : "j225_b60",
                                                                                                           "color"      : "ROOT.kAzure-9",
                                                                                                           "drawOptions" : "P",
                                                                                                           "marker"      : "27",
                                                                                                           "TObject"   : "",
                                                                                                           },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25_denom_Xhh_passL1": {"label"      : "j75_b70_3j75",
                                                                                                                      "color"      : "ROOT.kGreen",
                                                                                                                      "drawOptions" : "P",
                                                                                                                      "marker"      : "22",
                                                                                                                      "TObject"   : "",
                                                                                                                      },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j100_2j55_bmv2c2060_split_denom_Xhh_passL1": {"label"      : "j100_2j55_b60",
                                                                                                               "color"      : "ROOT.kAzure",
                                                                                                               "drawOptions" : "P",
                                                                                                               "marker"      : "26",
                                                                                                               "TObject"   : "",
                                                                                                               },
                                         },
                       }

            parameters = {"title"      : "",
                          "yTitle"     : "Efficiency",
                          "xTitle"     : "Signal Sample",
                          "xTitleOffset": 1,
                          "labelSize"  : 16,
                          "lumi"       : [o.year,lumi],
                          "rebin"      : 1, 
                          "yMin"       : 0,
                          "yMax"       : 1.5,
                          "xleg"       : [0.6,0.89],
                          "yleg"       : [0.7,0.92],
                          "xatlas"     : 0.13,
                          "logY"       : False,
                          "ratio"      : False,
                          "outputDir"  : outDir+"/trigger/"+cutflow+"/",
                          "outputName" : "Xhh_passL1_HLT_vs_Xhh",
                          "drawLines"  : [[0,1,11,1],[10,0,10,1]]
                          }
        
            plot(samples,parameters)


            samples = {files[o.year]["trigger"]:{cutflow+"_TrigEff_numer_Xhh_passHLT_denom_Xhh": {"label"      : "HLT OR",
                                                                                          "color"      : "ROOT.kBlack",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "21",
                                                                                          "TObject"   : "",
                                                                                          },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_j150_bmv2c2060_split_j50_bmv2c2060_splitonly_denom_Xhh": {"label"      : "j150_b60_j50_b60",
                                         #                                                                       "color"      : "ROOT.kBlue",
                                         #                                                                       "drawOptions" : "P",
                                         #                                                                       "marker"      : "23",
                                         #                                                                       "TObject"   : "",
                                         #                                                                       },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25only_denom_Xhh": {"label"      : "2j35_b60_2j35",
                                                                                                                     "color"      : "ROOT.kCyan",
                                                                                                                     "drawOptions" : "P",
                                                                                                                     "marker"      : "24",
                                                                                                                     "TObject"   : "",
                                                                                                                     },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_2j70_bmv2c2050_split_j70_denom_Xhh": {"label"      : "2j70_b50_j70",
                                         #                                                                              "color"      : "ROOT.kOrange",
                                         #                                                                              "drawOptions" : "P",
                                         #                                                                              "marker"      : "25",
                                         #                                                                              "TObject"   : "",
                                         #                                                                              },
                                         # cutflow+"_TrigEff_numer_Xhh_HLT_j275_bmv2c2070_split_denom_Xhh": {"label"      : "j275_b70",
                                         #                                                          "color"      : "ROOT.kAzure-9",
                                         #                                                          "drawOptions" : "P",
                                         #                                                          "marker"      : "27",
                                         #                                                          "TObject"   : "",
                                         #                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j225_bmv2c2060_splitonly_denom_Xhh": {"label"      : "j225_b60",
                                                                                                           "color"      : "ROOT.kAzure-9",
                                                                                                           "drawOptions" : "P",
                                                                                                           "marker"      : "27",
                                                                                                           "TObject"   : "",
                                                                                                           },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25only_denom_Xhh": {"label"      : "j75_b70_3j75",
                                                                                                                      "color"      : "ROOT.kGreen",
                                                                                                                      "drawOptions" : "P",
                                                                                                                      "marker"      : "22",
                                                                                                                      "TObject"   : "",
                                                                                                                      },
                                         cutflow+"_TrigEff_numer_Xhh_HLT_j100_2j55_bmv2c2060_splitonly_denom_Xhh": {"label"      : "j100_2j55_b60",
                                                                                                               "color"      : "ROOT.kAzure",
                                                                                                               "drawOptions" : "P",
                                                                                                               "marker"      : "26",
                                                                                                               "TObject"   : "",
                                                                                                               },
                                         },
                       }

            parameters = {"title"      : "",
                          "yTitle"     : "Efficiency",
                          "xTitle"     : "Signal Sample",
                          "xTitleOffset": 1,
                          "labelSize"  : 16,
                          "lumi"       : [o.year,lumi],
                          "rebin"      : 1, 
                          "yMin"       : .0001,
                          "yMax"       : 100,
                          "xleg"       : [0.6,0.89],
                          "yleg"       : [0.7,0.92],
                          "xatlas"     : 0.13,
                          "logY"       : True,
                          "ratio"      : False,
                          "outputDir"  : outDir+"/trigger/"+cutflow+"/",
                          "outputName" : "Xhh_HLT_vs_Xhh_unique",
                          "drawLines"  : [[0,1,11,1],[10,0.0001,10,1]]
                          }
        
            plot(samples,parameters)

            samples = {files[o.year]["trigger"]:{cutflow+"_TrigEff_numer_Xhh_passL1_denom_Xhh": {"label"      : "L1 OR",
                                                                                         "color"      : "ROOT.kRed",
                                                                                         "drawOptions" : "P",
                                                                                         "marker"      : "20",
                                                                                         "TObject"    : "",
                                                                                         },
                                         cutflow+"_TrigEff_numer_Xhh_L1_J100_denom_Xhh": {"label"      : "L1_J100",
                                                                                          "color"      : "ROOT.kGreen",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "21",
                                                                                          "TObject"    : "",
                                                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_L1_4J15.0ETA25_denom_Xhh": {"label"      : "L1_4J15.0ETA25",
                                                                                          "color"      : "ROOT.kBlue",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "22",
                                                                                          "TObject"    : "",
                                                                                          },
                                         cutflow+"_TrigEff_numer_Xhh_L1_J75_3J20_denom_Xhh": {"label"      : "L1_J75_3J20",
                                                                                                 "color"      : "ROOT.kMagenta",
                                                                                                 "drawOptions" : "P",
                                                                                                 "marker"      : "23",
                                                                                                 "TObject"    : "",
                                                                                                 },
                                         },
                       }

            parameters = {"title"      : "",
                          "yTitle"     : "Efficiency",
                          "xTitle"     : "Signal Sample",
                          "xTitleOffset": 1,
                          "labelSize"  : 16,
                          "lumi"       : [o.year,lumi],
                          "rebin"      : 1, 
                          "yMin"       : 0,
                          "yMax"       : 1.5,
                          "xleg"       : [0.55,0.95],
                          "yleg"       : [0.7,0.92],
                          "xatlas"     : 0.13,
                          "logY"       : False,
                          "ratio"      : False,
                          "outputDir"  : outDir+"/trigger/"+cutflow+"/",
                          "outputName" : "Xhh_L1_vs_Xhh",
                          "drawLines"  : [[0,1,11,1],[10,0,10,1]]
                          }
    
            plot(samples,parameters)



        ##Acceptance plots
        samples = {files[o.year]["trigger"]:{cutflow+"_Acceptance_numer_Xhh_passHLT_denom_nSample": {"label"      : "Xhh+HLT",
                                                                                             "color"      : "ROOT.kBlack",
                                                                                             "drawOptions" : "P",
                                                                                             "marker"      : "20",
                                                                                             "TObject"    : "",
                                                                                             },
                                     cutflow+"_Acceptance_numer_Xhh_passL1_denom_nSample": {"label"      : "Xhh+L1",
                                                                                            "color"      : "ROOT.kRed",
                                                                                            "drawOptions" : "P",
                                                                                            "marker"      : "21",
                                                                                            "TObject"    : "",
                                                                                            },
                                     cutflow+"_Acceptance_numer_Xhh_denom_nSample": {"label"      : "Xhh",
                                                                                     "color"      : "ROOT.kBlue",
                                                                                     "drawOptions" : "P",
                                                                                     "marker"      : "22",
                                                                                     "TObject"    : "",
                                                                                            },
                                     cutflow+"_Acceptance_numer_PassHCdEta_denom_nSample": {"label"      : "#Delta#eta_{hh}",
                                                                                            "color"      : "ROOT.kMagenta",
                                                                                            "drawOptions" : "P",
                                                                                            "marker"      : "23",
                                                                                            "TObject"    : "",
                                                                                            },
                                     cutflow+"_Acceptance_numer_PassHCdR_denom_nSample": {"label"      : "#DeltaR_{hh}",
                                                                                            "color"      : "ROOT.kGreen",
                                                                                            "drawOptions" : "P",
                                                                                            "marker"      : "23",
                                                                                            "TObject"    : "",
                                                                                            },
                                     cutflow+"_Acceptance_numer_PassHCPt_denom_nSample": {"label"      : "p_{T,h}",
                                                                                          "color"      : "ROOT.kCyan",
                                                                                          "drawOptions" : "P",
                                                                                          "marker"      : "24",
                                                                                          "TObject"    : "",
                                                                                          },
                                     cutflow+"_Acceptance_numer_PassHCJetPt_denom_nSample": {"label"      : "HC jet Pt",
                                                                                             "color"      : "ROOT.kGreen",
                                                                                             "drawOptions" : "P",
                                                                                             "marker"      : "25",
                                                                                             "TObject"    : "",
                                                                                             },
                                     cutflow+"_Acceptance_numer_nBJets_denom_nSample": {"label"      : "4 b-jets",
                                                                                        "color"      : "ROOT.kOrange",
                                                                                        "drawOptions" : "P",
                                                                                        "marker"      : "26",
                                                                                        "TObject"    : "",
                                                                                        },
                                     },
                   }

        parameters = {"title"      : "",
                      "yTitle"     : "Acceptance",
                      "xTitle"     : "Signal Sample",
                      "xTitleOffset": 1,
                      "labelSize"  : 18,
                      "legendTextSize":0.03,
                      "lumi"       : [o.year,lumi],
                      "rebin"      : 1, 
                      "yMin"       : 0,
                      "yMax"       : 0.25,
                      "xleg"       : [0.6,1],
                      "yleg"       : [0.65,0.9],
                      "xatlas"     : 0.13,
                      "yatlas"     : 0.9,
                      "logY"       : False,
                      "ratio"      : False,
                      "outputDir"  : outDir+"/acceptance/"+cutflow+"/",
                      "outputName" : "absoluteAcceptance",
                      "drawLines"  : [[10,0,10,0.25]]
                      }
    
        plot(samples,parameters)

        samples = {files[o.year]["trigger"]:{"RSG_"+cutflow+"_Acceptance_numer_Xhh_passHLT_denom_nSample": {"label"      : "Trigger",
                                                                                                            "legend"     : 7,
                                                                                                            "color"      : "ROOT.kBlack",
                                                                                                            "drawOptions" : "LP",
                                                                                                            "marker"      : "24",
                                                                                                            "TObject"    : "",
                                                                                                            },
                                             "RSG_"+cutflow+"_Acceptance_numer_Xhh_denom_nSample": {"label"      : "X_{hh}",
                                                                                                    "legend"     : 6,
                                                                                                    "color"      : "ROOT.kBlue",
                                                                                                    "marker"      : "26",
                                                                                                    "drawOptions" : "LP",
                                                                                                    "TObject"    : "",
                                                                                                    },
                                             "RSG_"+cutflow+"_Acceptance_numer_PassHCdR_denom_nSample": {"label"      : "#DeltaR_{hh}",
                                                                                                         "legend"     : 5,
                                                                                                         "color"      : "ROOT.kGreen",
                                                                                                         "drawOptions" : "LP",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "RSG_"+cutflow+"_Acceptance_numer_PassHCdEta_denom_nSample": {"label"      : "#Delta#eta_{hh}",
                                                                                                           "legend"     : 4,
                                                                                                           "color"      : "ROOT.kMagenta",
                                                                                                           "drawOptions" : "LP",
                                                                                                           "marker"      : "24",
                                                                                                           "TObject"    : "",
                                                                                                           },
                                             "RSG_"+cutflow+"_Acceptance_numer_PassHCPt_denom_nSample": {"label"      : "p_{T,h}",
                                                                                                         "legend"     : 3,
                                                                                                         "color"      : "ROOT.kCyan",
                                                                                                         "drawOptions" : "LP",
                                                                                                         "marker"      : "26",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "RSG_"+cutflow+"_Acceptance_numer_PassHCdRjj_denom_nSample": {"label"      : "#DeltaR_{jj}",
                                                                                                         "legend"     : 2,
                                                                                                         "color"      : "ROOT.kRed",
                                                                                                         "drawOptions" : "LP",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "RSG_"+cutflow+"_Acceptance_numer_nBJets_denom_nSample": {"label"      : "4 b-tagged jets",
                                                                                                       "legend"     : 1,
                                                                                                       "color"      : "ROOT.kOrange",
                                                                                                       "drawOptions" : "LP",
                                                                                                       "marker"      : "24",
                                                                                                       "TObject"    : "",
                                                                                                       },
                                             },
                   }

        parameters = {"title"      : "",
                      "yTitle"     : "Acceptance #times Efficiency",
                      "xTitle"     : "m_{G*_{KK}} [GeV]",
                      "xTitleOffset": 0.95,
                      "legendTextSize":0.03,
                      "canvasSize" : [600,500],
                      "rMargin"    : 0.05,
                      "lMargin"    : 0.12,
                      "yTitleOffset": 1.1,
                      "lumi"       : [o.year,lumi],
                      "rebin"      : 1, 
                      "yMin"       : 0,
                      "yMax"       : 0.2,
                      "xleg"       : [0.15,0.43],
                      "yleg"       : [0.6,0.92],
                      "labelSize"  : 16,
                      "xatlas"     : 0.52,
                      "yatlas"     : 0.9,
                      "logY"       : False,
                      "ratio"      : False,
                      "outputDir"  : outDir+"/acceptance/"+cutflow+"/",
                      "outputName" : "absoluteAcceptance_RSG_c10",
                      }
    
        plot(samples,parameters)

        samples = {files[o.year]["trigger"]:{"RSG_"+cutflow+"_Acceptance_numer_Xhh_passHLT_denom_nSample": {"label"      : "Trigger",
                                                                                                            "legend"     : 5,
                                                                                                            "color"      : "ROOT.kBlack",
                                                                                                            "drawOptions" : "LP",
                                                                                                            "marker"      : "24",
                                                                                                            "TObject"    : "",
                                                                                                            },
                                             "RSG_"+cutflow+"_Acceptance_numer_Xhh_denom_nSample": {"label"      : "X_{hh}",
                                                                                                    "legend"     : 4,
                                                                                                    "color"      : "ROOT.kBlue",
                                                                                                    "marker"      : "26",
                                                                                                    "drawOptions" : "LP",
                                                                                                    "TObject"    : "",
                                                                                                    },
                                             "RSG_"+cutflow+"_Acceptance_numer_PassHCdR_denom_nSample": {"label"      : "m_{4j} Dependent Cuts, #DeltaR_{hh}",
                                                                                                          "legend"     : 3,
                                                                                                         "color"      : "ROOT.kGreen",
                                                                                                         "drawOptions" : "LP",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "RSG_"+cutflow+"_Acceptance_numer_PassHCdRjj_denom_nSample": {"label"      : "#DeltaR_{jj}",
                                                                                                         "legend"     : 2,
                                                                                                         "color"      : "ROOT.kRed",
                                                                                                         "drawOptions" : "LP",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "RSG_"+cutflow+"_Acceptance_numer_nBJets_denom_nSample": {"label"      : "4 b-tagged jets",
                                                                                                       "legend"     : 1,
                                                                                                       "color"      : "ROOT.kOrange",
                                                                                                       "drawOptions" : "LP",
                                                                                                       "marker"      : "24",
                                                                                                       "TObject"    : "",
                                                                                                       },
                                             },
                   }

        parameters = {"title"      : "",
                      "yTitle"     : "Acceptance #times Efficiency",
                      "xTitle"     : "m_{G*_{KK}} [GeV]",
                      "xTitleOffset": 0.95,
                      "legendTextSize":0.03,
                      "canvasSize" : [600,500],
                      "rMargin"    : 0.05,
                      "lMargin"    : 0.12,
                      "yTitleOffset": 1.1,
                      "lumi"       : [o.year,lumi],
                      "rebin"      : 1, 
                      "yMin"       : 0,
                      "yMax"       : 0.21,
                      "xleg"       : [0.15,0.43],
                      "yleg"       : [0.6,0.92],
                      "labelSize"  : 16,
                      "xatlas"     : 0.52,
                      "yatlas"     : 0.88,
                      "satlas"     : 0.05,
                      "logY"       : False,
                      "ratio"      : False,
                      "outputDir"  : outDir+"/acceptance/"+cutflow+"/",
                      "outputName" : "absoluteAcceptance_RSG_c10_simple",
                      }
    
        plot(samples,parameters)


        samples = {files[o.year]["trigger"]:{"RSG_"+cutflow+"Right_Acceptance_numer_Xhh_passHLT_denom_nSample": {"label"      : "Trigger",
                                                                                                            "legend"     : 7,
                                                                                                            "color"      : "ROOT.kBlack",
                                                                                                            "drawOptions" : "LP",
                                                                                                            "marker"      : "24",
                                                                                                            "TObject"    : "",
                                                                                                            },
                                             "RSG_"+cutflow+"Right_Acceptance_numer_Xhh_denom_nSample": {"label"      : "X_{hh}",
                                                                                                    "legend"     : 6,
                                                                                                    "color"      : "ROOT.kBlue",
                                                                                                    "marker"      : "26",
                                                                                                    "drawOptions" : "LP",
                                                                                                    "TObject"    : "",
                                                                                                    },
                                             "RSG_"+cutflow+"Right_Acceptance_numer_PassHCdR_denom_nSample": {"label"      : "#DeltaR_{hh}",
                                                                                                         "legend"     : 5,
                                                                                                         "color"      : "ROOT.kGreen",
                                                                                                         "drawOptions" : "LP",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "RSG_"+cutflow+"Right_Acceptance_numer_PassHCdEta_denom_nSample": {"label"      : "#Delta#eta_{hh}",
                                                                                                           "legend"     : 4,
                                                                                                           "color"      : "ROOT.kMagenta",
                                                                                                           "drawOptions" : "LP",
                                                                                                           "marker"      : "24",
                                                                                                           "TObject"    : "",
                                                                                                           },
                                             "RSG_"+cutflow+"Right_Acceptance_numer_PassHCPt_denom_nSample": {"label"      : "p_{T,h}",
                                                                                                         "legend"     : 3,
                                                                                                         "color"      : "ROOT.kCyan",
                                                                                                         "drawOptions" : "LP",
                                                                                                         "marker"      : "26",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "RSG_"+cutflow+"Right_Acceptance_numer_PassHCdRjj_denom_nSample": {"label"      : "#DeltaR_{jj}",
                                                                                                         "legend"     : 2,
                                                                                                         "color"      : "ROOT.kRed",
                                                                                                         "drawOptions" : "LP",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "RSG_"+cutflow+"Right_Acceptance_numer_nBJets_denom_nSample": {"label"      : "4 b-tagged jets",
                                                                                                       "legend"     : 1,
                                                                                                       "color"      : "ROOT.kOrange",
                                                                                                       "drawOptions" : "LP",
                                                                                                       "marker"      : "24",
                                                                                                       "TObject"    : "",
                                                                                                       },
                                             },
                   }

        parameters = {"title"      : "",
                      "yTitle"     : "Acceptance #times Efficiency",
                      "xTitle"     : "m_{G*_{KK}} [GeV]",
                      "xTitleOffset": 1,
                      "legendTextSize":0.03,
                      "canvasSize" : [600,500],
                      "rMargin"    : 0.05,
                      "lMargin"    : 0.12,
                      "yTitleOffset": 1.1,
                      "lumi"       : [o.year,lumi],
                      "rebin"      : 1, 
                      "yMin"       : 0,
                      "yMax"       : 0.25,
                      "xleg"       : [0.65,0.95],
                      "yleg"       : [0.6,0.87],
                      "labelSize"  : 18,
                      "xatlas"     : 0.52,
                      "yatlas"     : 0.8,
                      "logY"       : False,
                      "ratio"      : False,
                      "outputDir"  : outDir+"/acceptance/"+cutflow+"/",
                      "outputName" : "absoluteAcceptance_RSG_c10_truthMatch",
                      }
    
        plot(samples,parameters)

        samples = {files[o.year]["trigger"]:{"SMNR_"+cutflow+"_Acceptance_numer_Xhh_passHLT_denom_nSample": {"label"      : "Trigger",
                                                                                                            "legend"     : 7,
                                                                                                            "color"      : "ROOT.kBlack",
                                                                                                            "drawOptions" : "HIST P",
                                                                                                            "marker"      : "24",
                                                                                                            "TObject"    : "",
                                                                                                            },
                                             "SMNR_"+cutflow+"_Acceptance_numer_Xhh_denom_nSample": {"label"      : "X_{hh}",
                                                                                                    "legend"     : 6,
                                                                                                    "color"      : "ROOT.kBlue",
                                                                                                    "marker"      : "26",
                                                                                                    "drawOptions" : "HIST P",
                                                                                                    "TObject"    : "",
                                                                                                    },
                                             "SMNR_"+cutflow+"_Acceptance_numer_PassHCdR_denom_nSample": {"label"      : "#DeltaR_{hh}",
                                                                                                         "legend"     : 5,
                                                                                                         "color"      : "ROOT.kGreen",
                                                                                                         "drawOptions" : "HIST P",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "SMNR_"+cutflow+"_Acceptance_numer_PassHCdEta_denom_nSample": {"label"      : "#Delta#eta_{hh}",
                                                                                                           "legend"     : 4,
                                                                                                           "color"      : "ROOT.kMagenta",
                                                                                                           "drawOptions" : "HIST P",
                                                                                                           "marker"      : "24",
                                                                                                           "TObject"    : "",
                                                                                                           },
                                             "SMNR_"+cutflow+"_Acceptance_numer_PassHCPt_denom_nSample": {"label"      : "p_{T,h}",
                                                                                                         "legend"     : 3,
                                                                                                         "color"      : "ROOT.kCyan",
                                                                                                         "drawOptions" : "HIST P",
                                                                                                         "marker"      : "26",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "SMNR_"+cutflow+"_Acceptance_numer_PassHCdRjj_denom_nSample": {"label"      : "#DeltaR_{jj}",
                                                                                                         "legend"     : 2,
                                                                                                         "color"      : "ROOT.kRed",
                                                                                                         "drawOptions" : "HIST P",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "SMNR_"+cutflow+"_Acceptance_numer_nBJets_denom_nSample": {"label"      : "4 b-tagged jets",
                                                                                                       "legend"     : 1,
                                                                                                       "color"      : "ROOT.kOrange",
                                                                                                       "drawOptions" : "HIST P",
                                                                                                       "marker"      : "24",
                                                                                                       "TObject"    : "",
                                                                                                       },
                                             },
                   }

        parameters = {"title"      : "",
                      "yTitle"     : "",
                      "yTickLength": 0.1,
                      "xTitle"     : "",
                      "xTitleOffset": 1,
                      "legendTextSize":0.03,
                      "canvasSize" : [125,500],
                      "rMargin"    : 0.08,
                      "lMargin"    : 0.4,
                      "yTitleOffset": 2,
                      "lumi"       : [o.year,lumi],
                      "rebin"      : 1, 
                      "yMin"       : 0,
                      "yMax"       : 0.08,
                      "xleg"       : [2,2],
                      "yleg"       : [1,1],
                      "labelSize"  : 18,
                      "xatlas"     : 2.4,
                      "yatlas"     : 0.8,
                      "logY"       : False,
                      "ratio"      : False,
                      "outputDir"  : outDir+"/acceptance/"+cutflow+"/",
                      "outputName" : "absoluteAcceptance_SMNR",
                      }
    
        plot(samples,parameters)

        samples = {files[o.year]["trigger"]:{"SMNR_"+cutflow+"_Acceptance_numer_Xhh_passHLT_denom_nSample": {"label"      : "Trigger",
                                                                                                            "legend"     : 5,
                                                                                                            "color"      : "ROOT.kBlack",
                                                                                                            "drawOptions" : "HIST P",
                                                                                                            "marker"      : "24",
                                                                                                            "TObject"    : "",
                                                                                                            },
                                             "SMNR_"+cutflow+"_Acceptance_numer_Xhh_denom_nSample": {"label"      : "X_{hh}",
                                                                                                    "legend"     : 4,
                                                                                                    "color"      : "ROOT.kBlue",
                                                                                                    "marker"      : "26",
                                                                                                    "drawOptions" : "HIST P",
                                                                                                    "TObject"    : "",
                                                                                                    },
                                             "SMNR_"+cutflow+"_Acceptance_numer_PassHCdR_denom_nSample": {"label"      : "m_{4j} Dependent Cuts, #DeltaR_{hh}",
                                                                                                         "legend"     : 3,
                                                                                                         "color"      : "ROOT.kGreen",
                                                                                                         "drawOptions" : "HIST P",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "SMNR_"+cutflow+"_Acceptance_numer_PassHCdRjj_denom_nSample": {"label"      : "#DeltaR_{jj}",
                                                                                                         "legend"     : 2,
                                                                                                         "color"      : "ROOT.kRed",
                                                                                                         "drawOptions" : "HIST P",
                                                                                                         "marker"      : "25",
                                                                                                         "TObject"    : "",
                                                                                                         },
                                             "SMNR_"+cutflow+"_Acceptance_numer_nBJets_denom_nSample": {"label"      : "4 b-tagged jets",
                                                                                                       "legend"     : 1,
                                                                                                       "color"      : "ROOT.kOrange",
                                                                                                       "drawOptions" : "HIST P",
                                                                                                       "marker"      : "24",
                                                                                                       "TObject"    : "",
                                                                                                       },
                                             },
                   }

        parameters = {"title"      : "",
                      "yTitle"     : "",
                      "yTickLength": 0.1,
                      "xTitle"     : "",
                      "xTitleOffset": 1,
                      "legendTextSize":0.03,
                      "canvasSize" : [125,500],
                      "rMargin"    : 0.08,
                      "lMargin"    : 0.4,
                      "yTitleOffset": 2,
                      "lumi"       : [o.year,lumi],
                      "rebin"      : 1, 
                      "yMin"       : 0,
                      "yMax"       : 0.08,
                      "xleg"       : [2,2],
                      "yleg"       : [1,1],
                      "labelSize"  : 18,
                      "xatlas"     : 2.4,
                      "yatlas"     : 0.8,
                      "logY"       : False,
                      "ratio"      : False,
                      "outputDir"  : outDir+"/acceptance/"+cutflow+"/",
                      "outputName" : "absoluteAcceptance_SMNR_simple",
                      }
    
        plot(samples,parameters)


#
# Kinematic weights
#
if o.doMain or o.doAll or o.doWeights:
    samples     = {files[o.year]["weights"]:{"m12m34_4b_ratio" : {"drawOptions": "COLZ",
                                                          "TObject"    : "",
                                                          "weight"  : 1.0/16,
                                                          },
                                     },
                   }
    
    parameters = {"title"      : "",
                  "yTitle"     : "m_{2j}^{subl} [GeV]",
                  "xTitle"     : "m_{2j}^{lead} [GeV]",
                  "yMax"       : 1.6,
                  "yMin"       : 0.4,
                  "rebin"      : 4,
                  "canvasSize" : [720,660],
                  "maxDigits"  : 3,
                  "outputDir"  : outDir+"/weights/",
                  "outputName" : "m12m34",
                  }
    
    plot(samples,parameters)


    samples = {files[o.year]["weights"]:{"HCjet4_pt_4b_ratio": {"isData"   : True,
                                                                   "color"    : "ROOT.kBlack",
                                                                   "TObject"  : "",
                                                                   },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Softest HC Jet Pt [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "HCjet4_pt",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 150,
                  #"drawLines"  : [[0,0.1,800,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"HCjet3_pt_4b_ratio": {"isData"   : True,
                                                                   "color"    : "ROOT.kBlack",
                                                                   "TObject"  : "",
                                                                   },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Second Softest HC Jet Pt [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "HCjet3_pt",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 150,
                  #"drawLines"  : [[0,0.1,800,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)


    samples = {files[o.year]["weights"]:{"sublHCand_leadJet_Pt_4b_ratio": {"isData"   : True,
                                                                   "color"    : "ROOT.kBlack",
                                                                   "TObject"  : "",
                                                                   },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Subl HC Lead Jet Pt [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "sublHCand_leadJet_Pt",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 250,
                  #"drawLines"  : [[0,0.1,800,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"sublHCand_sublJet_Pt_4b_ratio": {"isData"   : True,
                                                                   "color"    : "ROOT.kBlack",
                                                                   "TObject"  : "",
                                                                   },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Subl HC Subl Jet Pt [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "sublHCand_sublJet_Pt",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 250,
                  #"drawLines"  : [[0,0.1,800,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"sublHCand_leadJet_E_4b_ratio": {"isData"   : True,
                                                                   "color"    : "ROOT.kBlack",
                                                                  "weight"    : 1./4,
                                                                   "TObject"  : "",
                                                                   },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Subl HC Lead Jet E [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "sublHCand_leadJet_E",
                  "rebin"     : 4,
                  "xMax"      : 500,
                  #"drawLines"  : [[0,0.1,800,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters,True)

    samples = {files[o.year]["weights"]:{"sublHCand_sublJet_E_4b_ratio": {"isData"   : True,
                                                                   "color"    : "ROOT.kBlack",
                                                                  "weight"    : 1./4,
                                                                   "TObject"  : "",
                                                                   },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Subl HC Subl Jet E [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "sublHCand_sublJet_E",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  "rebin"     : 4,
                  "xMax"      : 500,
                  #"drawLines"  : [[0,0.1,800,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)


    samples = {files[o.year]["weights"]:{"sublHCand_Pt_l_4b_ratio": {"isData"   : True,
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Subl HC Pt [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "sublHCand_Pt",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 800,
                  "drawLines"  : [[0,0.1,800,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"sublHCand_Ht_4b_ratio": {"isData"   : True,
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Subl HC H_{t} [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "sublHCand_Ht",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 500,
                  "drawLines"  : [[0,0.1,500,0.1],[0,2,500,2]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"leadHCand_Ht_4b_ratio": {"isData"   : True,
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Lead HC H_{t} [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "leadHCand_Ht",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 500,
                  "drawLines"  : [[0,0.1,500,0.1],[0,2,500,2]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)


    samples = {files[o.year]["weights"]:{"sublHCand_AbsEta_4b_ratio": {"isData"   : True,
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Subl HC |#eta|",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "sublHCand_AbsEta",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 3,
                  "drawLines"  : [[0,0.1,3,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"leadHCand_AbsEta_4b_ratio": {"isData"   : True,
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Lead HC |#eta|",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "leadHCand_AbsEta",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 3,
                  "drawLines"  : [[0,0.1,3,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)


    samples = {files[o.year]["weights"]:{"leadHCand_Pt_l_4b_ratio": {"isData"   : True,
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "lead HC Pt [GeV]",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "leadHCand_Pt",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 800,
                  "drawLines"  : [[0,0.1,800,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"sublHCand_dRjj_4b_ratio": {"isData"   : True,
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Subl HC #DeltaR_{jj}",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "sublHCand_dRjj",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  #"xMax"      : 800,
                  "drawLines"  : [[-0.1,0.1,4,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"leadHCand_dRjj_4b_ratio": {"isData"   : True,
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "Lead HC #DeltaR_{jj}",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "leadHCand_dRjj",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  #"xMax"      : 800,
                  "drawLines"  : [[-0.1,0.1,4,0.1]],
                  "fitStats"   : 1111,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"hCandDr_4b_ratio": {"isData"   : True,
                                                      "color"    : "ROOT.kBlack",
                                                      "TObject"  : "",
                                                      },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "#DeltaR(HC_{lead}, HC_{subl})",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "hCandDr",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 4,
                  "drawLines"  : [[0,0.1,4,0.1]]
                  }

    plot(samples, parameters)

    samples = {files[o.year]["weights"]:{"hCandDphi_4b_ratio": {"isData"   : True,
                                                      "color"    : "ROOT.kBlack",
                                                      "TObject"  : "",
                                                      },
                                 },
               }
    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "#Delta#phi(HC_{lead}, HC_{subl})",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "hCandDphi",
                  #"rebin"     : [0,80,160,240,320,400,480,560,640,720,800],
                  #"rebin"     : 1,
                  "xMax"      : 4,
                  "drawLines"  : [[-0.2,0.1,4,0.1]]
                  }

    plot(samples, parameters)


    samples = {files[o.year]["weights"]:{"nJetOther_4b_ratio": {"isData"   : True,
                                                      "color"    : "ROOT.kBlack",
                                                      "TObject"  : "",
                                                      },
                                 },
               }

    parameters = {"ratio"     : False,
                  "yTitle"    : "4b/2b",
                  "xTitle"    : "# of additional Jets",
                  "xTitleOffset":1,
                  "yMin"      : 0,
                  "yMax"      : 2 if iteration != "0" else 7,
                  "xatlas"    : 0.25,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : outDir+"/weights/",
                  "outputName": "nJetOther",
                  "xMax"      : 9.5,
                  "drawLines"  : [[-0.5,0.1,9.5,0.1]]
                  }

    plot(samples, parameters)


#
# Cutflows
#
if (o.doAll or o.doCutFlow) and False:
    for cutflow in cutflows:

        samples = {files[o.year]["data"]:{cutflow+"/DhhMin/TwoTag/":   {"label"      : "DhhMin",
                                                                "weight"     : mu_qcd_dict["mu_qcd_"+cutflow+"DhhMin"],
                                                                "TObject"    : "CutFlow",
                                                                "color"      : "ROOT.kBlue",
                                                                },
                                  },
                   }
        
        parameters = {
                      "yTitle"     : "Events",
                      "xTitle"     : "",
                      "rebin"      : 1, 
                      "logY"       : True,
                      "yMax"       : 2*10e5,
                      "yMin"       : 500,
                      "rMax"       : 2.1,
                      "rMin"       : 1,
                      "ratio"      : False,
                      "canvasSize" : [700,620],
                      "rTitle"     : "Algo/PtMax",
                      "outputDir"  : outDir+cutflow+"/CutFlows/",
                      "outputName" : "Data_FourTag",
                      }
        
        plot(samples,parameters)

#
# Signal cutflows
#
if (o.doAll or o.doCutFlow or o.doSignalOnly) and False:
    for mass in masses:
        for cutflow in cutflows:
            for algo in algos:
                samples = {files[o.year][mass]:{cutflow+"/"+algo+"/FourTag/":      {"label"      : algo,
                                                                            "TObject"    : "CutFlow",
                                                                            "weight"     : (0.577)**2, #h->bb BR squared
                                                                            "ratio"      : "denom A",
                                                                            "color"      : "ROOT.kYellow",
                                                                            },
                                        cutflow+"/"+algo+"Right/FourTag/": {"label"      : algo+" Truth",
                                                                            "TObject"    : "CutFlow",
                                                                            "weight"     : (0.577)**2, #h->bb BR squared
                                                                            "ratio"      : "numer A",
                                                                            "color"      : "ROOT.kBlack",
                                                                            },
                                        cutflow+"/Truth/FourTag/":         {"label"      : "Truth",
                                                                            "TObject"    : "CutFlow",
                                                                            "weight"     : (0.577)**2, #h->bb BR squared
                                                                            "color"      : "ROOT.kBlue",
                                                                            },
                                      },
                       }

                parameters = {
                              "yTitle"     : "Events",
                              "xTitle"     : "",
                              "rebin"      : 1, 
                              "yMin"       : 1,
                              "yMax"       : 10e3,
                              "logY"       : True,
                              "ratio"      : True,
                              "canvasSize" : [700,620],
                              "rTitle"     : "Truth Fraction",
                              "rMax"       : 1,
                              "rMin"       : 0,
                              "outputDir"  : outDir+cutflow+"/CutFlows/"+mass+"/",
                              "outputName" : "FourTag_"+algo,
                              }
            
                plot(samples, parameters )


if o.doLimitSetting and o.year != "comb":
    samples = {files[o.year]["LimitSettingInputs"]:{"data_hh": {"label"    : "Data",
                                                                "ratio"    : "numer A",
                                                                "isData"   : True,
                                                                "color"    : "ROOT.kBlack",
                                                                "TObject"  : "",
                                                                "legend"   : 1,
                                                                },
                                            "qcd_hh": {"label"    : "Multijet",
                                                       "ratio"    : "denom A",
                                                       "stack"    : 1,
                                                       "color"    : "ROOT.kYellow",
                                                       "systematics":["qcd_hh_ShapeHighUp","qcd_hh_ShapeHighDown",
                                                                      "qcd_hh_WidthUp",    "qcd_hh_WidthDown",
                                                                      "qcd_hh_PeakUp",     "qcd_hh_PeakDown",
                                                                      "qcd_hh_Up",         "qcd_hh_Down"],
                                                       "TObject"  : "",
                                                       "legend"   : 2,
                                                       },
                                            "ttbar_hh": {"label"    : "t#bar{t}",
                                                         "ratio"    : "denom A",
                                                         "stack"    : 0,
                                                         "color"    : "ROOT.kAzure-9",
                                                         "systematics":["ttbar_hh_ShapeHighUp","ttbar_hh_ShapeHighDown",
                                                                        "ttbar_hh_WidthUp",    "ttbar_hh_WidthDown",
                                                                        "ttbar_hh_PeakUp",     "ttbar_hh_PeakDown",
                                                                        "ttbar_hh_Up",         "ttbar_hh_Down"],
                                                         "TObject"  : "",
                                                         "legend"   : 3,
                                                         },
                                            # "hdm_hh_m260": {"label"    : "260 GeV NW Scalar",
                                            #                 "color"    : "ROOT.kAzure+2",
                                            #                 "weight"    : 0.1,
                                            #                 "TObject"  : "",
                                            #                   },
                                            "g_hh_m800_c10": {"label"    : "G(800) #times10",
                                                              "color"    : "ROOT.kMagenta+2",
                                                              "weight"   : 10,
                                                              "TObject"  : "",
                                                              "legend"   : 5,
                                                              },
                                            "g_hh_m300_c10": {"label"    : "G(300) #times10",
                                                              "color"    : "ROOT.kBlue+1",
                                                              "weight"   : 10,
                                                              "TObject"  : "",
                                                              "legend"   : 4,
                                                              },
                                            "sm_hh": {"label"    : "SM hh #times500",
                                                      "color"    : "ROOT.kTeal+3",
                                                      "weight"   : 500,
                                                      "TObject"  : "",
                                                      "legend"   : 6,
                                                      },
                                            },
               }
    
    parameters = {"ratio"     : True,
                  "title"     : "",
                  "rTitle"    : "Data/Bkgd",
                  "xTitle"    : "m_{4j} [GeV]",
                  "yTitle"    : "Events",
                  "stackErrors": True,
                  "xMin"      : 150,
                  "xMax"      : 1300,
                  "yMax"      : 135 if o.year == "2015" else 450,
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.85,
                  "xleg"      : [0.63, 0.95],
                  "yleg"      : [0.53, 0.9],
                  "lumi"      : [o.year,lumi],
                  "region"    : "Signal",
                  "outputDir" : o.outDir,
                  "outputName": "data",
                  "rebin"     : 1,
                  }
    if o.year == "2015+2016": 
        parameters["yMax"] = 580
        parameters["xatlas"] = 0.27

    plot(samples, parameters)
    parameters["rebin"] = [150,160,170,180,190,200,220,240,250,260,270,280,290,300,310,320,330,340,360,380,400,420,440,460,480,500,520,540,560,600,640,700,800,900,1000,1150,1300]
    parameters["outputName"] = parameters["outputName"]+"_variableBins"
    parameters["yTitle"] = "Events/10 GeV"
    plot(samples, parameters)
    parameters["logY"] = True
    parameters["yMax"] = parameters["yMax"]*5
    parameters["yMin"] = 0.02 if o.year == "2015" else 0.09
    plot(samples, parameters)
    #parameters["rebin"]=parameters["rebin"].append(2000)
    parameters["rebin"]=parameters["rebin"].append(2000)
    parameters["xMax"]=2000
    parameters["outputName"] = parameters["outputName"]+"_2TeV"
    plot(samples, parameters)

    parameters = {"ratio"     : True,
                  "logY"      : True,
                  "rTitle"    : "Data/Bkgd",
                  "xTitle"    : "m_{4j} [GeV]",
                  "yTitle"    : "Events",
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.81,
                  "xleg"      : [0.62, 0.95],
                  "yleg"      : [0.50, 0.875],
                  "stackErrors": True,
                  "xMin"      : 150,
                  "xMax"      : 1300,
                  "lumi"      : [o.year,lumi],
                  "region"    : "Signal",
                  "outputDir" : o.outDir,
                  "outputName": "data",
                  "rebin"     : 1,
                  }

    plot(samples, parameters)

    parameters = {"ratio"     : True,
                  "rTitle"    : "Data/Bkgd",
                  "xTitle"    : "m_{4j} [GeV]",
                  "yTitle"    : "Events",
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.81,
                  "xleg"      : [0.62, 0.95],
                  "yleg"      : [0.50, 0.875],
                  "stackErrors": True,
                  "xMin"      : 150,
                  "xMax"      : 1300,
                  "lumi"      : [o.year,lumi],
                  "region"    : "Signal",
                  "outputDir" : o.outDir,
                  "outputName": "data_50",
                  "rebin"     : 5,
                  }

    plot(samples, parameters)

    parameters = {"ratio"     : True,
                  "logY"      : True,
                  "region"    :	"Signal",
                  "rTitle"    : "Data/Bkgd",
                  "xTitle"    : "m_{4j} [GeV]",
                  "yTitle"    : "Events",
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.81,
                  "xleg"      : [0.62, 0.95],
                  "yleg"      : [0.50, 0.875],
                  "stackErrors": True,
                  "xMin"      : 150,
                  "xMax"      : 1300,
                  "lumi"      : [o.year,lumi],
                  "outputDir" : o.outDir,
                  "outputName": "data_50",
                  "rebin"     : 5,
                  }

    plot(samples, parameters)

    samples = {files[o.year]["LimitSettingInputs"]:{"data_HH": {"label"    : "Data",
                                                        "ratio"    : "numer A",
                                                        "isData"   : True,
                                                        "color"    : "ROOT.kBlack",
                                                        "TObject"  : "",
                                                        },
                                            "qcd_HH": {"label"    : "Multijet",
                                                       "ratio"    : "denom A",
                                                       "stack"    : 1,
                                                       "color"    : "ROOT.kYellow",
                                                       "systematics":["qcd_HH_WidthUp",    "qcd_HH_WidthDown",
                                                                      "qcd_HH_PeakUp",     "qcd_HH_PeakDown",
                                                                      "qcd_HH_Up",         "qcd_HH_Down"],
                                                       "TObject"  : "",
                                                       },
                                            "ttbar_HH": {"label"    : "t#bar{t}",
                                                         "ratio"    : "denom A",
                                                         "stack"    : 0,
                                                         "color"    : "ROOT.kAzure-9",
                                                         "systematics":["ttbar_HH_WidthUp",    "ttbar_HH_WidthDown",
                                                                        "ttbar_HH_PeakUp",     "ttbar_HH_PeakDown",
                                                                        "ttbar_HH_Up",         "ttbar_HH_Down"],
                                                         "TObject"  : "",
                                                         },
                                            # "hdm_HH_m260": {"label"    : "260 GeV NW Scalar",
                                            #                 "color"    : "ROOT.kAzure+2",
                                            #                 "weight"    : 0.1,
                                            #                 "TObject"  : "",
                                            #                   },
                                            "g_HH_m500_c10": {"label"    : "500 GeV RSG c=1.0",
                                                              "color"    : "ROOT.kBlue",
                                                              "TObject"  : "",
                                                              },
                                            "sm_HH": {"label"    : "SMNRx200",
                                                      "color"    : "ROOT.kGreen",
                                                      "weight"   : 200,
                                                      "TObject"  : "",
                                                      },
                                            },
               }
    
    parameters = {"ratio"     : True,
                  "rTitle"    : "Data/Bkgd",
                  "xTitle"    : "m_{4j} [GeV]",
                  "yTitle"    : "Events",
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.81,
                  "xleg"      : [0.62, 0.95],
                  "yleg"      : [0.50, 0.875],
                  "stackErrors": True,
                  "xMin"      : 150,
                  "xMax"      : 1300,
                  "xleg"      : [0.65, 0.90],
                  "yleg"      : [0.60, 0.875],
                  "lumi"      : [o.year,lumi],
                  "region"    : "HH Signal",
                  "outputDir" : o.outDir,
                  "outputName": "data_HH",
                  "rebin"     : 1,
                  }

    plot(samples, parameters)
    parameters["rebin"] = [150,280,300,320,340,360,380,400,420,440,460,480,500,520,540,580,620,700,800,1300]
    parameters["outputName"] = parameters["outputName"]+"_variableBins"
    parameters["yTitle"] = "Events/10 GeV"
    plot(samples, parameters)
    parameters["logY"] = True
    plot(samples, parameters)
    #parameters["rebin"]=parameters["rebin"].append(2000)
    parameters["rebin"]=[150,280,300,320,340,360,380,400,420,440,460,480,500,520,540,580,620,700,800,1300,2000]
    parameters["xMax"]=2000
    parameters["outputName"] = parameters["outputName"]+"_2TeV"
    plot(samples, parameters)

    parameters = {"ratio"     : True,
                  "logY"      : True,
                  "rTitle"    : "Data/Bkgd",
                  "xTitle"    : "m_{4j} [GeV]",
                  "yTitle"    : "Events",
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.81,
                  "xleg"      : [0.62, 0.95],
                  "yleg"      : [0.50, 0.875],
                  "stackErrors": True,
                  "xMin"      : 150,
                  "xMax"      : 1300,
                  "lumi"      : [o.year,lumi],
                  "region"    : "HH Signal",
                  "outputDir" : o.outDir,
                  "outputName": "data_HH",
                  "rebin"     : 1,
                  }

    plot(samples, parameters)


    samples = {files[o.year]["LimitSettingInputs"]:{"data_ZZ": {"label"    : "Data",
                                                        "ratio"    : "numer A",
                                                        "isData"   : True,
                                                        "color"    : "ROOT.kBlack",
                                                        "TObject"  : "",
                                                        },
                                            "qcd_ZZ": {"label"    : "Multijet",
                                                       "ratio"    : "denom A",
                                                       "stack"    : 1,
                                                       "color"    : "ROOT.kYellow",
                                                       "systematics":["qcd_ZZ_WidthUp",    "qcd_ZZ_WidthDown",
                                                                      "qcd_ZZ_PeakUp",     "qcd_ZZ_PeakDown",
                                                                      "qcd_ZZ_Up",         "qcd_ZZ_Down"],
                                                       "TObject"  : "",
                                                       },
                                            "ttbar_ZZ": {"label"    : "t#bar{t}",
                                                         "ratio"    : "denom A",
                                                         "stack"    : 0,
                                                         "color"    : "ROOT.kAzure-9",
                                                         "systematics":["ttbar_ZZ_WidthUp",    "ttbar_ZZ_WidthDown",
                                                                        "ttbar_ZZ_PeakUp",     "ttbar_ZZ_PeakDown",
                                                                        "ttbar_ZZ_Up",         "ttbar_ZZ_Down"],
                                                         "TObject"  : "",
                                                         },
                                            # "hdm_ZZ_m260": {"label"    : "260 GeV NW Scalar",
                                            #                 "color"    : "ROOT.kAzure+2",
                                            #                 "weight"    : 0.1,
                                            #                 "TObject"  : "",
                                            #                   },
                                            "g_ZZ_m500_c10": {"label"    : "500 GeV RSG c=1.0",
                                                              "color"    : "ROOT.kBlue",
                                                              "TObject"  : "",
                                                              },
                                            "sm_ZZ": {"label"    : "SMNRx200",
                                                      "color"    : "ROOT.kGreen",
                                                      "weight"   : 200,
                                                      "TObject"  : "",
                                                      },
                                            },
               }
    
    parameters = {"ratio"     : True,
                  "rTitle"    : "Data/Bkgd",
                  "xTitle"    : "m_{4j} [GeV]",
                  "yTitle"    : "Events",
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.81,
                  "xleg"      : [0.62, 0.95],
                  "yleg"      : [0.50, 0.875],
                  "stackErrors": True,
                  "xMin"      : 150,
                  "xMax"      : 1300,
                  "xleg"      : [0.65, 0.90],
                  "yleg"      : [0.60, 0.875],
                  "lumi"      : [o.year,lumi],
                  "region"    : "ZZ Signal",
                  "outputDir" : o.outDir,
                  "outputName": "data_ZZ",
                  "rebin"     : 1,
                  }

    plot(samples, parameters)
    parameters["rebin"] = [150,160,180,200,220,240,260,280,300,320,340,360,400,440,480,520,600,700,800,900,1100,1300]
    parameters["outputName"] = parameters["outputName"]+"_variableBins"
    parameters["yTitle"] = "Events/10 GeV"
    plot(samples, parameters)
    parameters["logY"] = True
    plot(samples, parameters)
    #parameters["rebin"]=parameters["rebin"].append(2000)
    parameters["rebin"]= [150,160,180,200,210,220,230,240,250,260,270,280,300,320,340,360,380,400,440,480,520,600,700,1300,2000]
    parameters["xMax"]=2000
    parameters["outputName"] = parameters["outputName"]+"_2TeV"
    plot(samples, parameters)

    parameters = {"ratio"     : True,
                  "logY"      : True,
                  "rTitle"    : "Data/Bkgd",
                  "xTitle"    : "m_{4j} [GeV]",
                  "yTitle"    : "Events",
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.81,
                  "xleg"      : [0.62, 0.95],
                  "yleg"      : [0.50, 0.875],
                  "stackErrors": True,
                  "xMin"      : 150,
                  "xMax"      : 1300,
                  "lumi"      : [o.year,lumi],
                  "region"    : "ZZ Signal", 
                  "outputDir" : o.outDir,
                  "outputName": "data_ZZ",
                  "rebin"     : 1,
                  }

    plot(samples, parameters)


    samples = {files[o.year]["LimitSettingInputs"]:{"qcd_hh" : {"label"    : "Multijet",
                                                  "ratio"    : "denom A",
                                                  "color"    : "ROOT.kBlack",
                                                  "TObject"  : "",
                                                  },
                                            # "fitLandauhh_qcd" : {"label"    : "Landau Fit",
                                            #                      "color"    : "ROOT.kBlack",
                                            #                      "TObject"  : "",
                                            #                      },
                                            "qcd_hh_Up" : {"label"    : "Norm. Up",
                                                           "ratio"    : "numer A",
                                                           "color"    : "ROOT.kRed-3",
                                                           "TObject"  : "",
                                                           },
                                            "qcd_hh_Down" : {"label"    : "Norm. Down",
                                                             "ratio"    : "numer A",
                                                             "color"    : "ROOT.kRed",
                                                             "TObject"  : "",
                                                             },
                                            "qcd_hh_ShapeHighUp" : {"label"    : "Tail Shape Up",
                                                                    "ratio"    : "numer A",
                                                                    "color"    : "ROOT.kBlue",
                                                                    "TObject"  : "",
                                                                    },
                                            "qcd_hh_ShapeHighDown" : {"label"    : "Tail Shape Down",
                                                                      "ratio"    : "numer A",
                                                                      "color"    : "ROOT.kBlue+2",
                                                                      "TObject"  : "",
                                                                      },
                                            "qcd_hh_WidthUp" : {"label"    : "Width Up",
                                                                "ratio"    : "numer A",
                                                                "color"    : "ROOT.kGreen",
                                                                "TObject"  : "",
                                                                },
                                            "qcd_hh_WidthDown" : {"label"    : "Width Down",
                                                                  "ratio"    : "numer A",
                                                                  "color"    : "ROOT.kGreen+2",
                                                                  "TObject"  : "",
                                                                  },
                                            "qcd_hh_PeakUp" : {"label"    : "Peak Up",
                                                                "ratio"    : "numer A",
                                                                "color"    : "ROOT.kMagenta",
                                                                "TObject"  : "",
                                                                },
                                            "qcd_hh_PeakDown" : {"label"    : "Peak Down",
                                                                  "ratio"    : "numer A",
                                                                  "color"    : "ROOT.kMagenta+2",
                                                                  "TObject"  : "",
                                                                  },
                                            },
               }

    parameters = {"ratio"     : True,
                  "ratioErrors":False,
                  "rColor"    : "ROOT.kWhite",
                  "rMin"      : 0,
                  "rMax"      : 2,
                  "rTitle"    : "Variation/Nominal",
                  "yTitle"    : "Events",
                  "xTitle"    : varLabels["m4j"],
                  "xMax"      : 1300.0,
                  "xMin"      : 150.0,
                  "title"     : "",
                  "lumi"      : [o.year,lumi],
                  "region"    : "Signal", 
                  "outputDir" : o.outDir,
                  "outputName": "qcd",
                  }

    plot(samples, parameters)

    parameters = {"ratio"     : True,
                  "ratioErrors":False,
                  "logY"      : True,
                  "yMin"      : 0.1,
                  "rColor"    : "ROOT.kWhite",
                  "rMin"      : 0,
                  "rMax"      : 2,
                  "rTitle"    : "Variation/Nominal",
                  "yTitle"    : "Events",
                  "xTitle"    : varLabels["m4j"],
                  "xMax"      : 1300.0,
                  "xMin"      : 150.0,
                  "title"     : "",
                  "lumi"      : [o.year,lumi],
                  "region"    : "Signal", 
                  "outputDir" : o.outDir,
                  "outputName": "qcd",
                  }

    plot(samples, parameters)


    samples = {files[o.year]["LimitSettingInputs"]:{"ttbar_hh" : {"label"    : "t#bar{t}",
                                                  "ratio"    : "denom A",
                                                  "color"    : "ROOT.kBlack",
                                                  "TObject"  : "",
                                                  },
                                      "ttbar_hh_Up" : {"label"    : "Norm. Up",
                                                     "ratio"    : "numer A",
                                                     "color"    : "ROOT.kRed-3",
                                                     "TObject"  : "",
                                                     },
                                      "ttbar_hh_Down" : {"label"    : "Norm. Down",
                                                       "ratio"    : "numer A",
                                                       "color"    : "ROOT.kRed",
                                                       "TObject"  : "",
                                                       },
                                      "ttbar_hh_ShapeHighUp" : {"label"    : "Tail Shape Up",
                                                          "ratio"    : "numer A",
                                                          "color"    : "ROOT.kBlue",
                                                          "TObject"  : "",
                                                          },
                                      "ttbar_hh_ShapeHighDown" : {"label"    : "Tail Shape Down",
                                                            "ratio"    : "numer A",
                                                            "color"    : "ROOT.kBlue+2",
                                                            "TObject"  : "",
                                                            },
                                      "ttbar_hh_WidthUp" : {"label"    : "Width Up",
                                                          "ratio"    : "numer A",
                                                          "color"    : "ROOT.kGreen",
                                                          "TObject"  : "",
                                                          },
                                      "ttbar_hh_WidthDown" : {"label"    : "Width Down",
                                                            "ratio"    : "numer A",
                                                            "color"    : "ROOT.kGreen+2",
                                                            "TObject"  : "",
                                                            },
                                      "ttbar_hh_PeakUp" : {"label"    : "Peak Up",
                                                          "ratio"    : "numer A",
                                                          "color"    : "ROOT.kMagenta",
                                                          "TObject"  : "",
                                                          },
                                      "ttbar_hh_PeakDown" : {"label"    : "Peak Down",
                                                            "ratio"    : "numer A",
                                                            "color"    : "ROOT.kMagenta+2",
                                                            "TObject"  : "",
                                                            },
                                      },
               }

    parameters = {"ratio"     : True,
                  "ratioErrors":False,
                  "rColor"    : "ROOT.kWhite",
                  "rMin"      : 0,
                  "rMax"      : 2,
                  "rTitle"    : "Variation/Nominal",
                  "yTitle"    : "Events",
                  "xTitle"    : varLabels["m4j"],
                  "xMax"      : 1300.0,
                  "xMin"      : 150.0,
                  "title"     : "",
                  "lumi"      : [o.year,lumi],
                  "region"    : "Signal", 
                  "outputDir" : o.outDir,
                  "outputName": "ttbar",
                  }

    plot(samples, parameters)

    parameters = {"ratio"     : True,
                  "ratioErrors":False,
                  "logY"      : True,
                  "yMin"      : 0.1,
                  "rColor"    : "ROOT.kWhite",
                  "rMin"      : 0,
                  "rMax"      : 2,
                  "rTitle"    : "Variation/Nominal",
                  "yTitle"    : "Events",
                  "xTitle"    : varLabels["m4j"],
                  "xMax"      : 1300.0,
                  "xMin"      : 150.0,
                  "title"     : "",
                  "lumi"      : [o.year,lumi],
                  "region"    : "Signal", 
                  "outputDir" : o.outDir,
                  "outputName": "ttbar",
                  }

    plot(samples, parameters)


    if o.year != "2015+2016":
        samples = {files[o.year]["data"]:{"Loose/DhhMin/FourTag/Control/": {"label"    : "Data",
                                                                            "TObject"  : "m4j_l",
                                                                            "ratio"    : "numer A",
                                                                            "isData"   : True,
                                                                            "color"    : "ROOT.kBlack",
                                                                            "legend"   : 1,
                                                                            },
                                          },
                   files[o.year]["qcd"] :{"Loose/DhhMin/TwoTag/Control/": {"label"    : "Multijet",
                                                                           "TObject"  : "m4j_l",
                                                                           "ratio"    : "denom A",
                                                                           "stack"    : 1,
                                                                           "weight"   : mu_qcd_dict["mu_qcd_LooseDhhMin"],
                                                                           "color"    : "ROOT.kYellow",
                                                                           "legend"   : 2,
                                                                           },
                                          },
                   files[o.year]["ttbar"]:{"Loose/DhhMin/TwoTag/Control/": {"label"    : "t#bar{t}",
                                                                            "TObject"  : "m4j_l",
                                                                            "ratio"    : "denom A",
                                                                            "stack"    : 0,
                                                                            "weight"   : mu_qcd_dict["mu_ttbar_LooseDhhMin"],
                                                                            "color"    : "ROOT.kAzure-9",
                                                                            "legend"   : 3,
                                                                            },
                                           },
                   files[o.year]["LimitSettingInputs"]:{"fitHigh_qcd" : {"label"    : "Fit to Tail",
                                                                         "color"    : "ROOT.kRed",
                                                                         "lineStyle" : 1,
                                                                         "TObject"  : "",
                                                                         "pad"      : "rPad",
                                                                         "legend"   : 4,
                                                                         "xMin"     : 500,
                                                                         "xMax"     : 1500,
                                                                         },
                                                        "fitHighUp_qcd" : {"label"    : "Tail Up",
                                                                           "color"    : "ROOT.kRed",
                                                                           "lineStyle": 2,
                                                                           "TObject"  : "",
                                                                           "pad"      : "rPad",
                                                                           "legend"   : 5,
                                                                           "xMin"     : 500,
                                                                           "xMax"     : 1500,
                                                                           },
                                                        "fitHighDown_qcd" : {"label"    : "Tail Down",
                                                                             "color"    : "ROOT.kRed",
                                                                             "lineStyle": 4,
                                                                             "TObject"  : "",
                                                                             "pad"      : "rPad",
                                                                             "legend"   : 6,
                                                                             "xMin"     : 500,
                                                                             "xMax"     : 1500,
                                                                             },
                                                        # "fitLow_qcd" : {"label"    : "Fit to Bulk",
                                                        #                  "color"    : "ROOT.kGreen",
                                                        #                  "TObject"  : "",
                                                        #                  "pad"      : "rPad",
                                                        #                  },
                                                        # "fitLowUp_qcd" : {"label"    : "Bulk Up",
                                                        #                "color"    : "ROOT.kGreen+2",
                                                        #                "TObject"  : "",
                                                        #                "pad"      : "rPad",
                                                        #                },
                                                        # "fitLowDown_qcd" : {"label"    : "Bulk Down",
                                                        #                "color"    : "ROOT.kGreen-2",
                                                        #                "TObject"  : "",
                                                        #                "pad"      : "rPad",
                                                        #                },
                                                        },
                   }
        
        parameters = {"ratio"     : True,
                      "rTitle"    : "Data/Bkgd",
                      "logY"      : True,
                      "yTitle"    : "Events",
                      "xTitle"    : varLabels["m4j"],
                      "title"     : "",
                      "xMin"      : 150,
                      "xMax"      : 1500,
                      "yMin"      : 0.05,
                      "lumi"      : [o.year,lumi],
                      "region"    : "Control", 
                      "outputDir" : o.outDir,
                      "rMin"      : 0,
                      "rMax"      : 2,
                      "xatlas"    : 0.27,
                      "yatlas"    : 0.85,
                      "xleg"      : [0.63, 0.95],
                      "yleg"      : [0.53, 0.9],
                      "outputName": "m4jControl",
                      "rebin"     : rebins["m4j_l"],
                      }
        
        plot(samples, parameters)


    samples = {files[o.year]["LimitSettingInputs"]:{"qcd_2b_ZZ" : {"label"    : "Multijet (2b)",
                                                           "ratio"    : "denom A",
                                                           "color"    : "ROOT.kBlue",
                                                           "TObject"  : "",
                                                           },
                                            "qcd_4b_ZZ" : {"label"    : "Multijet (4b)",
                                                           "ratio"    : "numer A",
                                                           "isData"   : True,
                                                           "color"    : "ROOT.kBlack",
                                                           "TObject"  : "",
                                                           },
                                            "qcd_ZZ_WidthUp" : {"label"    : "Width Up",
                                                                "ratio"    : "numer A",
                                                                "color"    : "ROOT.kGreen",
                                                                "TObject"  : "",
                                                                },
                                            "qcd_ZZ_WidthDown" : {"label"    : "Width Down",
                                                                  "ratio"    : "numer A",
                                                                  "color"    : "ROOT.kGreen+2",
                                                                  "TObject"  : "",
                                                                  },
                                            "qcd_ZZ_PeakUp" : {"label"    : "Peak Up",
                                                                "ratio"    : "numer A",
                                                                "color"    : "ROOT.kMagenta",
                                                                "TObject"  : "",
                                                                },
                                            "qcd_ZZ_PeakDown" : {"label"    : "Peak Down",
                                                                  "ratio"    : "numer A",
                                                                  "color"    : "ROOT.kMagenta+2",
                                                                  "TObject"  : "",
                                                                  },
                                            },
               }

    parameters = {"ratio"     : True,
                  "ratioErrors":False,
                  "rColor"    : "ROOT.kWhite",
                  "rMin"      : 0,
                  "rMax"      : 2,
                  "rTitle"    : "Variation/Nominal",
                  "yTitle"    : "Events",
                  "xTitle"    : varLabels["m4j"],
                  "xMax"      : 800.0,
                  "xMin"      : 150.0,
                  #"yMax"      : 120,
                  #"yMin"      : 0,
                  "title"     : "",
                  "lumi"      : [o.year,lumi],
                  "region"    : "ZZ Signal", 
                  "outputDir" : o.outDir,
                  "outputName": "qcd_ZZ",
                  }

    plot(samples, parameters)


    samples = {files[o.year]["LimitSettingInputs"]:{"qcd_2b_HH" : {"label"    : "Multijet (2b)",
                                                           "ratio"    : "denom A",
                                                           "color"    : "ROOT.kBlue",
                                                           "TObject"  : "",
                                                           },
                                            "qcd_4b_HH" : {"label"    : "Multijet (4b)",
                                                           "ratio"    : "numer A",
                                                           "isData"   : True,
                                                           "color"    : "ROOT.kBlack",
                                                           "TObject"  : "",
                                                           },
                                            "qcd_HH_WidthUp" : {"label"    : "Width Up",
                                                               "ratio"    : "numer A",
                                                               "color"    : "ROOT.kGreen",
                                                               "TObject"  : "",
                                                               },
                                            "qcd_HH_WidthDown" : {"label"    : "Width Down",
                                                                 "ratio"    : "numer A",
                                                                 "color"    : "ROOT.kGreen+2",
                                                                 "TObject"  : "",
                                                                 },
                                            "qcd_HH_PeakUp" : {"label"    : "Peak Up",
                                                               "ratio"    : "numer A",
                                                               "color"    : "ROOT.kMagenta",
                                                               "TObject"  : "",
                                                               },
                                            "qcd_HH_PeakDown" : {"label"    : "Peak Down",
                                                                 "ratio"    : "numer A",
                                                                 "color"    : "ROOT.kMagenta+2",
                                                                 "TObject"  : "",
                                                                 },
                                            },
               }

    parameters = {"ratio"     : True,
                  "ratioErrors":False,
                  "rColor"    : "ROOT.kWhite",
                  "rMin"      : 0,
                  "rMax"      : 2,
                  "rTitle"    : "Variation/Nominal",
                  "yTitle"    : "Events",
                  "xTitle"    : varLabels["m4j"],
                  "xMax"      : 1000.0,
                  "xMin"      : 250.0,
                  #"yMax"      : 120,
                  #"yMin"      : 0,
                  "title"     : "",
                  "lumi"      : [o.year,lumi],
                  "region"    : "HH Signal", 
                  "outputDir" : o.outDir,
                  "outputName": "qcd_HH",
                  }

    plot(samples, parameters)


