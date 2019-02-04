from plotTools import plot, read_mu_qcd_file
import ROOT
import collections
import sys
sys.path.insert(0, 'XhhResolved/scripts/')
from setupConfig import setGRL, setLumi, setRegions, setTagger
import rootFiles
import os

###########
## Setup ##
###########
nTuple     = "02-03-04"
status  = ""
weights="redo"
pbryant = "/share/home/pbryant/public/4b_batch/"
outDir = "finalPlots/"
lumi = {"2015":  "3.2 fb^{-1}",
        "2016": "24.3 fb^{-1}"}

#years = ["2015","2016"]
years = ["2016"]

#iterations = ["0","7"]
iterations = ["7"]

HC_plane = [
    # "Sideband","Control","Signal",
    # "LMVR","HMVR",
    # "FullMassPlane",
    "Inclusive",
    ]

regionName = {"hh":"Signal",
              "SB":"Sideband",
              "CR":"Control",
              "LM":"LMV",
              "HM":"HMV",
              "FullMassPlane"  : "",
              "Inclusive": "SB+CR+SR",
              }

#dirNames = ["Inclusive","PassHCdEta","PassAllhadVeto"]
#dirNames = ["Inclusive","PassAllhadVeto"]
dirNames = ["PassAllhadVeto"]
#dirNames = ["PassAllhadVeto","Pass_ggVeto"]
blind = False

#
# Define rebin if any for all plotted variables
#
rebins = {}
rebins["m4j_l"] = [100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,
                   500,520,540,560,580,600,640,680,720,820,900,1000,1200]
rebins["m4j_cor_l"] = rebins["m4j_l"]

rebins["leadHC_Pt_m"] = "smart"
rebins["sublHC_Pt_m"] = "smart"
rebins["leadHC_Pt"] = "smart"
rebins["sublHC_Pt"] = "smart"

rebins["leadGC_Pt_m"] = "smart"
rebins["sublGC_Pt_m"] = "smart"
rebins["leadGC_Pt"] = "smart"
rebins["sublGC_Pt"] = "smart"

rebins["otherJets_Pt"] = "smart"
rebins["otherJets_Phi"] = 4

rebins["HCJet2_Eta"]   = 4
rebins["HCJet2_Phi"]   = 4
rebins["HCJet2_Pt"]    = "smart"
rebins["HCJet2_Pt_s"]  = 2
rebins["HCJet2_Pt_m"]  = "smart"
rebins["HCJet4_Eta"]   = 4
rebins["HCJet4_Phi"]   = 4
rebins["HCJet4_Pt"]    = "smart"
rebins["HCJet4_Pt_s"]  = 2
rebins["HCJet4_Pt_m"]  = "smart"

rebins["HC_jets_Pt_m"] = "smart"
rebins["HC_jets_Pt"]   = "smart"
rebins["HC_jets_Phi"]  = 4

rebins["dR_hh"] = 2
rebins["leadHC_dRjj"]        = 5
rebins["sublHC_dRjj"]        = 5
rebins["leadHC_Eta"] = 4
rebins["sublHC_Eta"] = 4
rebins["leadHC_Phi"] = 2
rebins["sublHC_Phi"] = 2
rebins["leadHC_JVC"] = 2
rebins["sublHC_JVC"] = 2

rebins["leadGC_dRjj"]        = 5
rebins["sublGC_dRjj"]        = 5
rebins["leadGC_Eta"] = 4
rebins["sublGC_Eta"] = 4
rebins["leadGC_Phi"] = 2
rebins["sublGC_Phi"] = 2

rebins["Pt_hh"] = "smart"
rebins["Pt_gg"] = "smart"

xMax = {}
xMax["leadHC_Mass"] = 250
xMax["sublHC_Mass"] = 250

xMin = {}
xMin["leadHC_Mass"] = 0
xMin["sublHC_Mass"] = 0

xMin["leadGC_Mass"] = 0
xMin["sublGC_Mass"] = 0

#
# Define variables to be plotted and their axis label
#

varLabels = {"m4j_cor_v"              : "m_{HH} [GeV]",
             "m4j_cor_v_logy"         : "m_{HH} [GeV]",
             "m4j_cor_l"              : "m_{HH} [GeV]",
             "m4j_cor_l_logy"         : "m_{HH} [GeV]",
             "m4j_cor_f"              : "m_{HH} Bin",
             "m4j_cor_f_logy"         : "m_{HH} Bin",
             "m4j_cor_Z_v"            : "m_{ZZ} [GeV]",
             "m4j_cor_Z_v_logy"       : "m_{ZZ} [GeV]",
             "m4j_cor_H_v"            : "m_{XX} [GeV]",
             "m4j_cor_H_v_logy"       : "m_{XX} [GeV]",
             "m4j_l"                  : "m_{4j} [GeV]",
             "m4j_l_logy"             : "m_{4j} [GeV]",
             "dR_hh"                  : "#DeltaR_{HH}",
             "Pt_hh"                  : "p_{T,HH}",
             "xhh"                      : "X_{HH}",
             "xwt"                      : "X_{Wt}",
             "dhh"                      : "D_{HH} [GeV]",
             "HCJetAbsEta"              : "<|#eta_{i}|>",
             "leadHC_dRjj"           : "#DeltaR_{jj}^{lead}",
             "leadHC_Eta"            : "#eta_{H}^{lead}",
             "leadHC_Phi"            : "#phi_{H}^{lead}",
             "leadHC_Mass"           : "m_{2j}^{lead} [GeV]",
             "leadHC_Ht"             : "H_{T}^{lead} [GeV]",
             "leadHC_Pt"             : "p_{T}^{lead} [GeV]",
             "sublHC_dRjj"           : "#DeltaR_{jj}^{subl}",
             "sublHC_Eta"            : "#eta_{H}^{subl}",
             "sublHC_Phi"            : "#phi_{H}^{subl}",
             "sublHC_Mass"           : "m_{2j}^{subl} [GeV]",
             "sublHC_Pt"             : "p_{T}^{subl} [GeV]",
             "HC_jets_Pt"             : "p_{T,i} [GeV]",
             "HC_jets_Pt_m"           : "p_{T,i} [GeV]",
             "HC_jets_Pt_s"           : "p_{T,i} [GeV]",
             "HC_jets_Phi"            : "#phi_{i}",
             "HC_jets_Eta"            : "#eta_{i}",
             "HC_jets_MV2c10"         : "MV2c10_{i}",
             "otherJets_Pt"             : "p_{T} of additional jets [GeV]",
             "otherJets_Pt_s"             : "p_{T} of additional jets [GeV]",
             "otherJets_Phi"            : "#phi of additional jets",
             "otherJets_Eta"            : "#eta of additional jets",
             "nJetOther"                : "# of additional jets",
             "nJetOther_u"              : "(unweighted) # of additional jets",
             "leadGC_dRjj"           : "#DeltaR_{jj}^{close}",
             "leadGC_Eta"            : "#eta_{2j}^{close}",
             "leadGC_Phi"            : "#phi_{2j}^{close}",
             "leadGC_Mass"           : "m_{2j}^{close} [GeV]",
             "leadGC_Pt"             : "p_{T,2j}^{close} [GeV]",
             "sublGC_dRjj"           : "#DeltaR_{jj}^{other}",
             "sublGC_Eta"            : "#eta_{2j}^{other}",
             "sublGC_Phi"            : "#phi_{2j}^{other}",
             "sublGC_Mass"           : "m_{2j}^{other} [GeV]",
             "sublGC_Pt"             : "p_{T,2j}^{other} [GeV]",
             "HCJet2_Eta"    : "#eta_{2}",
             "HCJet2_Phi"    : "#phi_{2}",
             "HCJet2_Pt"     : "p_{T,2} [GeV]",
             "HCJet2_Pt_s"   : "p_{T,2} [GeV]",
             "HCJet2_Pt_m"   : "p_{T,2} [GeV]",
             "HCJet4_Eta"    : "#eta_{4}",
             "HCJet4_Phi"    : "#phi_{4}",
             "HCJet4_Pt"     : "p_{T,4} [GeV]",
             "HCJet4_Pt_s"   : "p_{T,4} [GeV]",
             "HCJet4_Pt_m"   : "p_{T,4} [GeV]",
             "nPromptMuons_logy" : "# of Muons",
             "NPV":"NPV",
             }


#
# plot variable with given plot parameters and sample dictionary
#
def plotVariable(sample,parameters,variable,outputName):
    parameters["xTitle"]     = varLabels[variable]

    if "_logy" in variable: 
        parameters["logY"]   = True
        variable = variable.replace("_logy","")
    if "_logy" in outputName:
        outputName = outputName.replace("_logy","")

    parameters["rebin"]      = rebins[variable] if variable in rebins else 1
    if variable in xMax:
        parameters["xMax"]      = xMax[variable]
        parameters["xMin"]      = xMin[variable]

    parameters["outputName"] = outputName
    for f in sample:
        for p in sample[f]:
            sample[f][p]["TObject"] = variable
            
    plot(sample,parameters)





#
# Plot data 
#
for year in years:
    if True:
        for iteration in iterations:
            inDir = pbryant+"hists_"+year+"_"+weights
            files = rootFiles.getFiles(iteration,nTuple, inDir, year)

            muFile = pbryant+"XhhResolved/data/mu_qcd_FourTag_"+weights+"_"+year+"_Nominal_"+iteration+".txt"
            mu_qcd_dict = read_mu_qcd_file(muFile)

            for dirName in dirNames:
                for region in HC_plane:
                    print "Main Plots:",year,iteration,dirName,region
                    for var in varLabels:
                        #continue
                        samples = {files["data"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Data",
                                                                                   "legend"   : 1,
                                                                                   "ratio"    : "numer A",
                                                                                   "isData"   : True,
                                                                                   "color"    : "ROOT.kBlack",
                                                                                   "weight"   : 0 if blind and region == "Signal" else 1,
                                                                                   },
                                                  },
                                   files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"label"    : "Multijet",
                                                                                  "legend"   : 2,
                                                                                  "ratio"    : "denom A",
                                                                                  "stack"    : 3,
                                                                                  "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"] if var[-2:]!="_u" 
                                                                                  else mu_qcd_dict["mu_qcd_no_nJetWeight_PassHCdEta"],
                                                                                  "color"    : "ROOT.kYellow",
                                                                                  },
                                                  },
                                   files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"label"    : "Hadronic t#bar{t}",
                                                                                         "legend"   : 3,
                                                                                         "ratio"    : "denom A",
                                                                                         "stack"    : 2,
                                                                                         "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"] if var[-2:]!="_u" 
                                                                                         else mu_qcd_dict["mu_allhad_no_nJetWeight_PassHCdEta"],
                                                                                         "color"    : "ROOT.kAzure-9",
                                                                                         },
                                                         },
                                   files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Semi-leptonic t#bar{t}",
                                                                                        "legend"   : 4,
                                                                                        "ratio"    : "denom A",
                                                                                        "stack"    : 1,
                                                                                        "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                                                                                        "color"    : "ROOT.kAzure-4",
                                                                                        },
                                                       },
                                   }
                        samples[files["H280"]] = {dirName+"_FourTag_"+region+"/": {"label"    : "Scalar (280 GeV)",
                                                                                   "legend"   : 5,
                                                                                   "weight"   : 0.04,
                                                                                   "color"    : "ROOT.kRed",
                                                                                   "lineWidth": 3,
                                                                                   "lineStyle": 7,
                                                                                   },
                                                  }
                        samples[files["SMNR_MhhWeight"]] = {dirName+"_FourTag_"+region+"/": {"label"    : "SM HH #times100",
                                                                                             "legend"   : 6,
                                                                                             "weight"   : 100,
                                                                                             "color"    : "ROOT.kTeal+3",
                                                                                             "lineWidth": 3,
                                                                                             "lineStyle": 2,
                                                                                             },
                                                            }
                
                        parameters = {"ratio"     : True,
                                      "atlas"      : "Thesis",
                                      "rTitle"    : "Data / Bkgd",
                                      "yTitle"    : "Events / Bin",
                                      "yleg"      : [0.55, 0.920],
                                      "title"     : "",
                                      "status"    : status,
                                      "lumi"      : [year,lumi[year]],
                                      "region"    : region,
                                      "outputDir" : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/",
                                      "rebin"     : 1,
                                      "rMax"      : 1.5,
                                      "rMin"      : 0.5,
                                      "xatlas"    : 0.22,
                                      "yatlas"    : 0.85,
                                      "xleg"      : [0.68,0.93]
                                      }

                        #parameters["chi2"] = True
                        if "_v"    in var: 
                            parameters["divideByBinWidth"] = True
                            parameters["xMax"] = 1400
                        if "m4j_cor_Z_v_logy" in var:
                            parameters["xMax"] = 1228
                            parameters["yMax"] = 8e4 if year == "2016" else 8e3
                            parameters["yMin"] = 0.2
                        if "m4j_cor_H_v_logy" in var:
                            parameters["xMax"] = 1306
                            parameters["yMax"] = 8e5 if year == "2016" else 8e4
                            parameters["yMin"] = 0.2
                        if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                        if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
                        plotVariable(samples, parameters, var, var)

                        #
                        # 2b data
                        #
                        #continue
                        samples = {files["data"]:{dirName+"_TwoTag_"+region+"/": {"label"    : "Data (2b)",
                                                                                  "legend"   : 1,
                                                                                  "ratio"    : "numer A",
                                                                                  "isData"   : True,
                                                                                  "color"    : "ROOT.kBlack",
                                                                                  "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                                  },
                                                  },
                                   files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"label"    : "Multijet (2b)",
                                                                                  "legend"   : 2,
                                                                                  "ratio"    : "denom A",
                                                                                  "stack"    : 3,
                                                                                  "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                                  "color"    : "ROOT.kYellow",
                                                                                  },
                                                  },
                                   files["allhad"]:{dirName+"_TwoTag_"+region+"/": {"label"    : "Hadronic t#bar{t} (2b)",
                                                                                    "legend"   : 3,
                                                                                    "ratio"    : "denom A",
                                                                                    "stack"    : 2,
                                                                                    "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                                    "color"    : "ROOT.kAzure-9",
                                                                                    },
                                                    },
                                   files["nonallhad"]:{dirName+"_TwoTag_"+region+"/": {"label"    : "Semi-leptonic t#bar{t} (2b)",
                                                                                        "legend"   : 4,
                                                                                        "ratio"    : "denom A",
                                                                                        "stack"    : 1,
                                                                                        "weight"   : mu_qcd_dict["mu_nonallhad2b_PassHCdEta"]*mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                                        "color"    : "ROOT.kAzure-4",
                                                                                        },
                                                       },
                                   }
                        # samples[files["H280"]] = {dirName+"_FourTag_"+region+"/": {"label"    : "Scalar (280 GeV)",
                        #                                                            "legend"   : 5,
                        #                                                            "weight"   : 0.04,
                        #                                                            "color"    : "ROOT.kRed",
                        #                                                            "lineWidth": 3,
                        #                                                            "lineStyle": 7,
                        #                                                            },
                        #                           }
                        # samples[files["SMNR_MhhWeight"]] = {dirName+"_FourTag_"+region+"/": {"label"    : "SM HH #times100",
                        #                                                                      "legend"   : 6,
                        #                                                                      "weight"   : 100,
                        #                                                                      "color"    : "ROOT.kTeal+3",
                        #                                                                      "lineWidth": 3,
                        #                                                                      "lineStyle": 2,
                        #                                                                      },
                        #                                     }
                
                        parameters = {"ratio"     : True,
                                      "atlas"      : "Thesis",
                                      "rTitle"    : "Data / Bkgd",
                                      "yTitle"    : "Events / Bin",
                                      "yleg"      : [0.55, 0.920],
                                      "title"     : "",
                                      "status"    : status,
                                      "lumi"      : [year,lumi[year]],
                                      "region"    : region,
                                      "outputDir" : outDir+year+"/"+weights+"_2b_iter"+iteration+"/"+dirName+"/"+region+"/",
                                      "rebin"     : 1,
                                      "rMax"      : 1.5,
                                      "rMin"      : 0.5,
                                      "xatlas"    : 0.22,
                                      "yatlas"    : 0.85,
                                      "xleg"      : [0.68,0.93]
                                      }

                        #parameters["chi2"] = True
                        if "_v"    in var: 
                            parameters["divideByBinWidth"] = True
                            parameters["xMax"] = 1400
                        if "m4j_cor_Z_v_logy" in var:
                            parameters["xMax"] = 1228
                            parameters["yMax"] = 8e4 if year == "2016" else 8e3
                            parameters["yMin"] = 0.2
                        if "m4j_cor_H_v_logy" in var:
                            parameters["xMax"] = 1306
                            parameters["yMax"] = 8e5 if year == "2016" else 8e4
                            parameters["yMin"] = 0.2
                        if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                        if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
                        plotVariable(samples, parameters, var, var)

                        # ttbar 2b->4b shape
                        samples = {files["allhadShape"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Hadronic t#bar{t} (4b)",
                                                                                          "legend"   : 1,
                                                                                          "isData"   : True,
                                                                                          "normalize": 1,
                                                                                          "ratio"    : "numer A",
                                                                                          "color"    : "ROOT.kBlack",
                                                                                          },
                                                         dirName+"_TwoTag_"+region+"/": {"label"    : "Hadronic t#bar{t} (2b)",
                                                                                         "legend"   : 2,
                                                                                         "ratio"    : "denom A",
                                                                                         "stack"    : 0,
                                                                                         #"weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                                                                                         "normalize": 1,
                                                                                         "color"    : "ROOT.kAzure-9",
                                                                                         },
                                                         },
                                   }

                        parameters = {"ratio"     : True,
                                      "atlas"     : "Thesis",
                                      "rTitle"    : "4b / 2b",
                                      "yTitle"    : "Events / Bin",
                                      "title"     : "",
                                      "status"    : "Simulation",
                                      "lumi"      : [year,lumi[year]],
                                      "yleg"      : [0.10, 0.35],
                                      "region"    : regionName[region],
                                      "outputDir" : outDir+year+"/"+weights+"_allhadShape_iter"+iteration+"/"+dirName+"/"+region+"/",
                                      "rebin"     : 1,
                                      #"chi2"      : True,
                                      }
                        if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                        if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
    
                        plotVariable(samples, parameters, var, var)

                    #
                    # 2d plots
                    # 
                    samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                            "TObject"    : "m12m34",
                                                                            "weight"     : 1,
                                                                            },
                                          },
                           }
                
                    parameters = {"title"       : "",
                                  "atlas"      : "Thesis",
                                  "status"      : status,
                                  "yTitle"      : "m_{2j}^{subl} [GeV]",
                                  "xTitle"      : "m_{2j}^{lead} [GeV]",
                                  "zTitle"      : "Events / 25 GeV^{2}",
                                  "zTitleOffset": 1.4,
                                  "xMin"        : 45,
                                  "xMax"        : 210,
                                  "yMin"        : 45,
                                  "yMax"        : 210,
                                  "zMin"        : 0,
                                  "maxDigits"   : 3,
                                  "satlas"      : 0.04,
                                  "xatlas"      : 0.15,
                                  "rMargin"     : 0.15,
                                  "rebin"       : 1, 
                                  "canvasSize"  : [720,660],
                                  "lumi"        : [year,lumi[year]],
                                  "region"      : region if region != "FullMassPlane" else "",
                                  "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/",
                                  "functions"   : [[" ((x-120*1.03)**2     + (y-110*1.03)**2)",     0,300,0,300,[30.0**2],ROOT.kOrange+7,1],
                                                   [ "((x-120*1.05)**2     + (y-110*1.05)**2)",     0,300,0,300,[45.0**2],ROOT.kYellow,  1],
                                                   ["(((x-120)/(0.1*x))**2 +((y-110)/(0.1*y))**2)", 0,300,0,300,[ 1.6**2],ROOT.kRed,     7]],
                                  "outputName"  : "m12m34_4b",
                                  }
                    if region == "FullMassPlane": 
                        if status=="Internal":
                            parameters["box"] = [52,177,127,205]
                        if status=="":
                            parameters["box"] = [52,177,112,205]
                    plot(samples, parameters)

                    samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                            "TObject"    : "m12m34",
                                                                            "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                            },
                                          },
                           }
                    parameters["outputName"] = "m12m34_2b"
                    plot(samples, parameters)

                    samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                      "TObject"    : "m12m34",
                                                                                      "weight"     : 1,
                                                                                      },
                                          },
                           }
                    parameters["outputName"] = "m12m34_4b"
                    parameters["status"]     = "Simulation "+status
                    if region == "FullMassPlane": 
                        if status=="Internal":
                            parameters["box"] = [52,177,165,205]
                        if status=="":
                            parameters["box"] = [52,177,124,205]
                    parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    plot(samples, parameters)

                    samples = {files["data"]:{dirName+"_FourTag_"+region+"/": {"drawOptions":"COLZ",
                                                                                  "TObject":"m12m34",
                                                                                  "ratio"    : "numer A",
                                                                                  },
                                              },
                               files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                              "TObject":"m12m34",
                                                                              "ratio"    : "denom A",
                                                                              "stack"    : 2,
                                                                              "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"], 
                                                                              },
                                              },
                               files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                                     "TObject":"m12m34",
                                                                                     "ratio"    : "denom A",
                                                                                     "stack"    : 1,
                                                                                     "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                                                                                     },
                                                     },
                               files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                                    "TObject":"m12m34",
                                                                                    "ratio"    : "denom A",
                                                                                    "stack"    : 0,
                                                                                    "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                                                                                    },
                                                   },
                               }
                    
                    if region == "FullMassPlane": 
                        if status=="Internal":
                            parameters["box"] = [52,177,127,205]
                        if status=="":
                            parameters["box"] = [52,177,112,205]
                    parameters["status"]     = status
                    parameters["outputName"] = "m12m34_ratio"
                    parameters["outputDir"]  = outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/"
                    parameters["rebin"]      = 3
                    parameters["ratio"]      = "2d ratio"
                    parameters["zTitle"]     = "Data / Bkgd"
                    parameters["zMin"]       = 0.5
                    parameters["zMax"]       = 1.5
                    if region != "FullMassPlane": del parameters["functions"]
                    plot(samples, parameters)

                    # samples = {files["data"]:{dirName+"_FourTag_"+region+"/": {"drawOptions":"COLZ",
                    #                                                               "TObject":"lowHt_m12m34",
                    #                                                               "ratio"    : "numer A",
                    #                                                               },
                    #                           },
                    #            files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                    #                                                           "TObject":"lowHt_m12m34",
                    #                                                           "ratio"    : "denom A",
                    #                                                           "stack"    : 2,
                    #                                                           "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"], 
                    #                                                           },
                    #                           },
                    #            files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                    #                                                                  "TObject":"lowHt_m12m34",
                    #                                                                  "ratio"    : "denom A",
                    #                                                                  "stack"    : 1,
                    #                                                                  "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                    #                                                                  },
                    #                                  },
                    #            files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"drawOptions"    : "COLZ",
                    #                                                                 "TObject":"lowHt_m12m34",
                    #                                                                 "ratio"    : "denom A",
                    #                                                                 "stack"    : 0,
                    #                                                                 "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                    #                                                                 },
                    #                                },
                    #            }
                    
                    # parameters["outputName"] = "lowHt_m12m34_ratio"
                    # parameters["rebin"]      = 3
                    # plot(samples, parameters)

                    # samples = {files["data"]:{dirName+"_FourTag_"+region+"/": {"drawOptions":"COLZ",
                    #                                                               "TObject":"highHt_m12m34",
                    #                                                               "ratio"    : "numer A",
                    #                                                               },
                    #                           },
                    #            files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                    #                                                           "TObject":"highHt_m12m34",
                    #                                                           "ratio"    : "denom A",
                    #                                                           "stack"    : 2,
                    #                                                           "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"], 
                    #                                                           },
                    #                           },
                    #            files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                    #                                                                  "TObject":"highHt_m12m34",
                    #                                                                  "ratio"    : "denom A",
                    #                                                                  "stack"    : 1,
                    #                                                                  "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                    #                                                                  },
                    #                                  },
                    #            files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"drawOptions"    : "COLZ",
                    #                                                                 "TObject":"highHt_m12m34",
                    #                                                                 "ratio"    : "denom A",
                    #                                                                 "stack"    : 0,
                    #                                                                 "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                    #                                                                 },
                    #                                },
                    #            }
                    
                    # parameters["outputName"] = "highHt_m12m34_ratio"
                    # parameters["rebin"]      = 3
                    # plot(samples, parameters)

                    #
                    # Mass Dependent Requirements
                    #

                    # lead HC dRjj req
                    samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                           "TObject"    : "m4jLeadHCdRjj",
                                                                           "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                           },
                                          },
                           }
                
                    parameters = {"yTitle"      : "#DeltaR_{j,j}^{lead}",
                                  "atlas"      : "Thesis",
                                  "xTitle"      : "m_{4j} [GeV]",
                                  "zTitle"      : "Events / Bin",
                                  "zTitleOffset": 1.7,
                                  "status"      : status,
                                  "satlas"      : 0.04,
                                  "zMin"        : 0,
                                  "yMin"        : 0.1,
                                  "canvasSize"  : [720,660],
                                  "maxDigits"   : 4,
                                  "rMargin"     : 0.19,
                                  "lumi"        : [year,lumi[year]],
                                  "region"      : region,
                                  "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/",
                                  "outputName"  : "m4jLeadHCdRjj_2b",
                                  "functions"   : [["(360.000/x-0.5000000 - y)",100,1100,0,4,[0],ROOT.kRed,1],
                                                   ["(652.863/x+0.4744490 - y)",100,1100,0,4,[0],ROOT.kRed,1]],
                                  }
            
                    plot(samples, parameters)

                    samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                            "TObject"    : "m4jLeadHCdRjj",
                                                                            "weight"     : 1,
                                                                            },
                                          },
                           }
                    parameters["outputName"] = "m4jLeadHCdRjj_4b"
                    plot(samples, parameters)

                    samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                      "TObject"    : "m4jLeadHCdRjj",
                                                                                      "weight"     : 1,
                                                                                      },
                                                    },
                           }
                    parameters["outputName"] = "m4jLeadHCdRjj_4b"
                    parameters["status"]     = "Simulation "+status
                    parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    plot(samples, parameters)

                    # subl HC dRjj req
                    samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                           "TObject"    : "m4jSublHCdRjj",
                                                                           "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                           },
                                          },
                           }
                
                    parameters = {"yTitle"      : "#DeltaR_{j,j}^{subl}",
                                  "xTitle"      : "m_{4j} [GeV]",
                                  "zTitle"      : "Events / Bin",
                                  "atlas"      : "Thesis",
                                  "status"      : status,
                                  "satlas"      : 0.04,
                                  "zTitleOffset": 1.7,
                                  "zMin"        : 0,
                                  "yMin"        : 0.1,
                                  "canvasSize"  : [720,660],
                                  "maxDigits"   : 4,
                                  "rMargin"     : 0.19,
                                  "lumi"        : [year,lumi[year]],
                                  "region"      : region,
                                  "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/" ,
                                  "outputName"  : "m4jSublHCdRjj_2b",
                                  "functions"   : [["(235.242/x+0.0162996 - y)",100,1100,0,4,[0],ROOT.kRed,1],
                                                   ["(874.890/x+0.3471370 - y)",100,1100,0,4,[0],ROOT.kRed,1]],
                                  }
            
                    plot(samples, parameters)

                    samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                "TObject"    : "m4jSublHCdRjj",
                                                                                "weight"     : 1,
                                                                                },
                                              },
                               }
                    parameters["outputName"] = "m4jSublHCdRjj_4b"
                    plot(samples, parameters)

                    samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                      "TObject"    : "m4jSublHCdRjj",
                                                                                      "weight"     : 1,
                                                                                      },
                                                    },
                           }
                    parameters["outputName"] = "m4jSublHCdRjj_4b"
                    parameters["status"]     = "Simulation "+status
                    parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    plot(samples, parameters)

                    # lead GC dRjj req
                    # samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                        "TObject"    : "m4jLeadGCdRjj",
                    #                                                        "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                    #                                                        },
                    #                       },
                    #        }
                
                    # parameters = {"yTitle"      : "#DeltaR_{j,j}^{close}",
                    #               "xTitle"      : "m_{4j} [GeV]",
                    #               "zTitle"      : "Events / Bin",
                    #               "zTitleOffset": 1.7,
                    #               "atlas"      : "Thesis",
                    #               "status"      : status,
                    #               "satlas"      : 0.04,
                    #               "zMin"        : 0,
                    #               "yMin"        : 0.1,
                    #               "canvasSize"  : [720,660],
                    #               "maxDigits"   : 4,
                    #               "rMargin"     : 0.19,
                    #               "lumi"        : [year,lumi[year]],
                    #               "region"      : region,
                    #               "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/",
                    #               "outputName"  : "m4jLeadGCdRjj_2b",
                    #               "functions"   : [["(360.000/x-0.5000000 - y)",100,1100,0,4,[0],ROOT.kRed,1],
                    #                                ["(652.863/x+0.4744490 - y)",100,1100,0,4,[0],ROOT.kRed,1]],
                    #               }
            
                    # plot(samples, parameters)

                    # samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                         "TObject"    : "m4jLeadGCdRjj",
                    #                                                         "weight"     : 1,
                    #                                                         },
                    #                       },
                    #        }
                    # parameters["outputName"] = "m4jLeadGCdRjj_4b"
                    # plot(samples, parameters)

                    # samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                                   "TObject"    : "m4jLeadGCdRjj",
                    #                                                                   "weight"     : 1,
                    #                                                                   },
                    #                                 },
                    #        }
                    # parameters["outputName"] = "m4jLeadGCdRjj_4b"
                    # parameters["status"]     = "Simulation "+status
                    # parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    # plot(samples, parameters)

                    # samples = {files["H280"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                             "TObject"    : "m4jLeadGCdRjj",
                    #                                                             "weight"     : 0.04,
                    #                                                             },
                    #                           },
                    #            }
                    # parameters["outputName"] = "m4jLeadGCdRjj_4b"
                    # parameters["status"]     = "Simulation "+status
                    # parameters["outputDir"]  = outDir+year+"/NWS_m280/"+dirName+"/"+region+"/"
                    # plot(samples, parameters)

                    # samples = {files["H260"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                             "TObject"    : "m4jLeadGCdRjj",
                    #                                                             "weight"     : 0.04,
                    #                                                             },
                    #                           },
                    #            }
                    # parameters["outputName"] = "m4jLeadGCdRjj_4b"
                    # parameters["status"]     = "Simulation "+status
                    # parameters["outputDir"]  = outDir+year+"/NWS_m260/"+dirName+"/"+region+"/"
                    # plot(samples, parameters)

                    # # subl GC dRjj req
                    # samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                        "TObject"    : "m4jSublGCdRjj",
                    #                                                        "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                    #                                                        },
                    #                       },
                    #        }
                
                    # parameters = {"yTitle"      : "#DeltaR_{j,j}^{other}",
                    #               "xTitle"      : "m_{4j} [GeV]",
                    #               "zTitle"      : "Events / Bin",
                    #               "atlas"      : "Thesis",
                    #               "status"      : status,
                    #               "satlas"      : 0.04,
                    #               "zTitleOffset": 1.7,
                    #               "zMin"        : 0,
                    #               "yMin"        : 0.1,
                    #               "canvasSize"  : [720,660],
                    #               "maxDigits"   : 4,
                    #               "rMargin"     : 0.19,
                    #               "lumi"        : [year,lumi[year]],
                    #               "region"      : region,
                    #               "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/" ,
                    #               "outputName"  : "m4jSublGCdRjj_2b",
                    #               "functions"   : [["(235.242/(x+70)+0.1162996 - y)",100,1100,0,4,[0],ROOT.kGreen,1],
                    #                                ["(235.242/x+0.0162996 - y)",100,1100,0,4,[0],ROOT.kRed,1],
                    #                                ["(874.890/x+0.3471370 - y)",100,1100,0,4,[0],ROOT.kRed,1]],
                    #               }
            
                    # plot(samples, parameters)

                    # samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                             "TObject"    : "m4jSublGCdRjj",
                    #                                                             "weight"     : 1,
                    #                                                             },
                    #                           },
                    #            }
                    # parameters["outputName"] = "m4jSublGCdRjj_4b"
                    # plot(samples, parameters)

                    # samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                                   "TObject"    : "m4jSublGCdRjj",
                    #                                                                   "weight"     : 1,
                    #                                                                   },
                    #                                 },
                    #        }
                    # parameters["outputName"] = "m4jSublGCdRjj_4b"
                    # parameters["status"]     = "Simulation "+status
                    # parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    # plot(samples, parameters)

                    # samples = {files["H280"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                             "TObject"    : "m4jSublGCdRjj",
                    #                                                             "weight"     : 0.04,
                    #                                                             },
                    #                           },
                    #            }
                    # parameters["outputName"] = "m4jSublGCdRjj_4b"
                    # parameters["status"]     = "Simulation "+status
                    # parameters["outputDir"]  = outDir+year+"/NWS_m280/"+dirName+"/"+region+"/"
                    # plot(samples, parameters)

                    # samples = {files["H260"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                    #                                                             "TObject"    : "m4jSublGCdRjj",
                    #                                                             "weight"     : 0.04,
                    #                                                             },
                    #                           },
                    #            }
                    # parameters["outputName"] = "m4jSublGCdRjj_4b"
                    # parameters["status"]     = "Simulation "+status
                    # parameters["outputDir"]  = outDir+year+"/NWS_m260/"+dirName+"/"+region+"/"
                    # plot(samples, parameters)


                    # m4jLeadPtHCandPt
                    samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jLeadPtHCandPt",
                                                                               "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                               },
                                              },
                               }
                
                    parameters = {"yTitle"      : "p_{T}^{lead} [GeV]",
                                  "xTitle"      : "m_{4j} [GeV]",
                                  "zTitle"      : "Events / Bin",
                                  "atlas"      : "Thesis",
                                  "status"      : status,
                                  "satlas"      : 0.04,
                                  "xatlas"      : 0.42,
                                  "yatlas"      : 0.23,
                                  "zTitleOffset": 1.7,
                                  "zMin"        : 0,
                                  "canvasSize"  : [720,660],
                                  "maxDigits"   : 4,
                                  "rMargin"     : 0.19,
                                  "lumi"        : [year,lumi[year]],
                                  "region"      : region,
                                  "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/" ,
                                  "outputName"  : "m4jLeadPtHCandPt_2b",
                                  "functions"  : [["(0.513333*x - 103.333 - y)",100,1100,0,440,[0],ROOT.kRed,1]],
                                  }
            
                    plot(samples, parameters)

                    samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                "TObject"    : "m4jLeadPtHCandPt",
                                                                                "weight"     : 1,
                                                                                },
                                              },
                               }
                    parameters["outputName"] = "m4jLeadPtHCandPt_4b"
                    plot(samples, parameters)

                    samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                      "TObject"    : "m4jLeadPtHCandPt",
                                                                                      "weight"     : 1,
                                                                                      },
                                                    },
                           }
                    parameters["outputName"] = "m4jLeadPtHCandPt_4b"
                    parameters["status"]     = "Simulation "+status
                    parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    plot(samples, parameters)

                    # m4jSublPtHCandPt
                    samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jSublPtHCandPt",
                                                                               "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                               },
                                              },
                               }
                
                    parameters = {"yTitle"      : "p_{T}^{subl} [GeV]",
                                  "xTitle"      : "m_{4j} [GeV]",
                                  "zTitle"      : "Events / Bin",
                                  "atlas"      : "Thesis",
                                  "status"      : status,
                                  "satlas"      : 0.04,
                                  "xatlas"      : 0.42,
                                  "yatlas"      : 0.23,
                                  "zTitleOffset": 1.7,
                                  "zMin"        : 0,
                                  "canvasSize"  : [720,660],
                                  "maxDigits"   : 4,
                                  "rMargin"     : 0.19,
                                  "lumi"        : [year,lumi[year]],
                                  "region"      : region,
                                  "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/" ,
                                  "outputName"  : "m4jSublPtHCandPt_2b",
                                  "functions"  : [["(0.333333*x - 73.3333 - y)",100,1100,0,440,[0],ROOT.kRed,1]],
                                  }
            
                    plot(samples, parameters)

                    samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                "TObject"    : "m4jSublPtHCandPt",
                                                                                "weight"     : 1,
                                                                                },
                                              },
                               }
                    parameters["outputName"] = "m4jSublPtHCandPt_4b"
                    plot(samples, parameters)

                    samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                      "TObject"    : "m4jSublPtHCandPt",
                                                                                      "weight"     : 1,
                                                                                      },
                                                    },
                           }
                    parameters["outputName"] = "m4jSublPtHCandPt_4b"
                    parameters["status"]     = "Simulation "+status
                    parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    plot(samples, parameters)

                    # m4j_nViews
                    samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4j_nViews",
                                                                               "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                               },
                                              },
                               }
                
                    parameters = {"yTitle"      : "Jet Pairings",
                                  "xTitle"      : "m_{4j} [GeV]",
                                  "zTitle"      : "Events / Bin",
                                  "atlas"      : "Thesis",
                                  "satlas"      : 0.04,
                                  #"box"         : [370,2.9,930,3.4],
                                  "xatlas"      : 0.43,
                                  "status"      : status,
                                  "zTitleOffset": 1.7,
                                  "zMin"        : 0,
                                  "canvasSize"  : [720,660],
                                  "maxDigits"   : 4,
                                  "rMargin"     : 0.19,
                                  "lumi"        : [year,lumi[year]],
                                  "region"      : region,
                                  "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/" ,
                                  "outputName"  : "m4j_nViews_2b",
                                  }
            
                    plot(samples, parameters)

                    samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                "TObject"    : "m4j_nViews",
                                                                                "weight"     : 1,
                                                                                },
                                              },
                               }
                    parameters["outputName"] = "m4j_nViews_4b"
                    plot(samples, parameters)

                    samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                      "TObject"    : "m4j_nViews",
                                                                                      "weight"     : 1,
                                                                                      },
                                                    },
                           }
                    parameters["outputName"] = "m4j_nViews_4b"
                    parameters["status"]     = "Simulation "+status
                    parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    plot(samples, parameters)

                    # m4jnJetOther
                    samples = {files["data"]:{dirName+"_TwoTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jnJetOther",
                                                                               "weight"     : mu_qcd_dict["mu_qcd_PassHCdEta"],
                                                                               },
                                              },
                               }
                
                    parameters = {"yTitle"      : "# of Additional Jets",
                                  "xTitle"      : "m_{4j} [GeV]",
                                  "zTitle"      : "Events / Bin",
                                  "atlas"      : "Thesis",
                                  "status"      : status,
                                  "satlas"      : 0.04,
                                  "zTitleOffset": 1.7,
                                  "zMin"        : 0,
                                  "canvasSize"  : [720,660],
                                  "maxDigits"   : 4,
                                  "rMargin"     : 0.19,
                                  "lumi"        : [year,lumi[year]],
                                  "region"      : region,
                                  "outputDir"   : outDir+year+"/"+weights+"_iter"+iteration+"/"+dirName+"/"+region+"/" ,
                                  "outputName"  : "m4jnJetOther_2b",
                                  }
            
                    plot(samples, parameters)

                    samples = {files["data"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                "TObject"    : "m4jnJetOther",
                                                                                "weight"     : 1,
                                                                                },
                                              },
                               }
                    parameters["outputName"] = "m4jnJetOther_4b"
                    plot(samples, parameters)

                    samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/" : {"drawOptions": "COLZ",
                                                                                      "TObject"    : "m4jnJetOther",
                                                                                      "weight"     : 1,
                                                                                      },
                                                    },
                           }
                    parameters["outputName"] = "m4jnJetOther_4b"
                    parameters["status"]     = "Simulation "+status
                    parameters["outputDir"]  = outDir+year+"/SMNR/"+dirName+"/"+region+"/"
                    plot(samples, parameters)


    labels = {"qcd"      :"Multijet",
              "allhad"   :"Hadronic t#bar{t}",
              "nonallhad":"Semileptonic t#bar{t}",
              "ttbar"    :"t#bar{t}",
              "total"    :"Total Background"}

    if True:
        for suffix in ["","_v","_l"]:
            for region in ["hh","CR","LM","HM"]:
                #regionScaled = {"hh":"HH", "CR":"HH", "LM":"ZZ", "HM":"XX"}
                print "Limit Inputs:",suffix,region
                systematics = ["_NP0_up","_NP0_down",
                               "_NP1_up","_NP1_down",
                               "_NP2_up","_NP2_down",
                               "_LowHtCRw","_LowHtCRi",
                               "_HighHtCRw","_HighHtCRi",
                               ]
                samples = {pbryant+"LimitSettingInputs_redo_iter7/resolved_4bSR_"+year+".root":{
                        "data_"+region+suffix: {"label"    : "Data",
                                                "ratio"    : "numer A",
                                                "isData"   : True,
                                                "color"    : "ROOT.kBlack",
                                                "TObject"  : "",
                                                "legend"   : 1,
                                                "weight"   : 0 if blind and region == "Signal" else 1,
                                                },
                        "total_"+region+suffix: {"label"    : "Stat+Syst Uncertainty",
                                                 "ratio"    : "denom A",
                                                 #"stack"    : 2,
                                                 "fillColor"    : "ROOT.kGray+2",
                                                 "fillStyle": 3245,
                                                 "lineColor": "ROOT.kWhite",
                                                 "lineStyle": 1,
                                                 "lineWidth": 0,
                                                 "drawOptions": "e2",
                                                 "systematics":["total_"+region+syst+suffix for syst in systematics],
                                                 "legend"   : 5,
                                                 "legendMark": "f",
                                                 },
                        "qcd_"+region+suffix: {"label"    : "Multijet",
                                               #"ratio"    : "denom A",
                                               "stack"    : 2,
                                               "color"    : "ROOT.kYellow",
                                               #"systematics":["qcd_"+region+syst+suffix for syst in systematics],
                                               "TObject"  : "",
                                               "legend"   : 2,
                                               },
                        "allhad_"+region+suffix: {"label"    : "Hadronic t#bar{t}",
                                                  #"ratio"    : "denom A",
                                                  "stack"    : 1,
                                                  "color"    : "ROOT.kAzure-9",
                                                  #"systematics":["allhad_"+region+syst+suffix for syst in systematics],
                                                  "TObject"  : "",
                                                  "legend"   : 3,
                                                  },
                        "nonallhad_"+region+suffix: {"label"    : "Semi-leptonic t#bar{t}",
                                                     #"ratio"    : "denom A",
                                                     "stack"    : 0,
                                                     "color"    : "ROOT.kAzure-4",
                                                     #"systematics":["nonallhad_"+region+syst+suffix for syst in systematics],
                                                     "TObject"  : "",
                                                     "legend"   : 4,
                                                     },
                        }
                           }
            
                samples[pbryant+"LimitSettingInputs_redo_iter7/resolved_4bSR_"+year+".root"].update({
                        "smrwMhh_"+region+suffix: {"label"    : "SM HH #times100",
                                                   "lineWidth": 3,
                                                   "lineStyle": 2,
                                                   "color"    : "ROOT.kTeal+3",
                                                   "weight"   : 100,
                                                   "TObject"  : "",
                                                   "legend"   : 7,
                                                   },
                        "g_"+region+"_m800_c10"+suffix: {"label"    : "G_{KK} (800 GeV, k/#bar{M}_{Pl}=1)",
                                                         "lineWidth": 3,
                                                         "lineStyle": 3,
                                                         "color"    : "ROOT.kViolet",
                                                         "weight"   : (1.77e+02)/(0.10549*1e3),#updated xs/ami xs
                                                         "TObject"  : "",
                                                         "legend"   : 8,
                                                         },
                        "g_"+region+"_m1200_c20"+suffix: {"label"    : "G_{KK} (1200 GeV, k/#bar{M}_{Pl}=2)",
                                                          "lineWidth": 3,
                                                          "lineStyle": 9,
                                                          "color"    : "ROOT.kViolet-6",
                                                          "weight"   : (2.24e+01*4)/(0.045461*1e3),#updated xs * c^2/ami xs
                                                          "TObject"  : "",
                                                          "legend"   : 9,
                                                          },
                        "s_"+region+"_m280"+suffix: {"label"    : "Scalar (280 GeV)",#times 0.04
                                                     "lineWidth": 3,
                                                     "lineStyle": 7,
                                                     "color"    : "ROOT.kRed",
                                                     "weight"   : 0.04,
                                                     "TObject"  : "",
                                                     "legend"   : 6,
                                                     },
                        })
            
                parameters = {"ratio"     : True,
                              "atlas"      : "Thesis",
                              "title"     : "",
                              "status"    : status,
                              "rTitle"    : "Data / Bkgd",
                              "xTitle"    : "m_{HH} [GeV]" if suffix else "Bin",
                              "yTitle"    : "Events / Bin",
                              "maxDigits": 4,
                              #"stackErrors": True,
                              "errors"    : False,
                              "xMin"      : 150,
                              "xatlas"    : 0.20,
                              "yatlas"    : 0.85,
                              "xleg"      : [0.59, 0.92],
                              "yleg"      : [0.35, 0.92],
                              "lumi"      : [year,lumi[year]],
                              "region"    : regionName[region],
                              "outputDir" : outDir+year+"/results/",
                              "outputName": "data_"+region+suffix,
                              "rMax"      : 1.5,
                              "rMin"      : 0.5,
                              }

                if region == "hh" or region == "CR":
                    parameters["yMax"] = 185 if year == "2015" else 1400

                if suffix == "_v": 
                    parameters["xMin"] = 200
                    parameters["xMax"] = 1479
                    parameters["divideByBinWidth"] = True
                    if region == "hh" or region == "CR":
                        parameters["yMax"] = 1850 if year == "2015" else 14000
                    if region == "LM" or region == "HM":
                        maxMinDict = {"2015":{"LM":[0.5,  6000],
                                              "HM":[0.5, 30000]},
                                      "2016":{"LM":[0.5,200000],
                                              "HM":[0.5,200000]}}
                        parameters["yMin"] = maxMinDict[year][region][0]
                        parameters["yMax"] = maxMinDict[year][region][1]


                plot(samples, parameters)

                parameters["logY"] = True
                if region == "hh" or region == "CR": parameters["yMax"] = parameters["yMax"]*800
                if region == "LM" and suffix == "_v": parameters["yMax"]= parameters["yMax"]*10
                if region == "hh" or region == "CR": parameters["yMin"] = 0.02 if year == "2015" else 0.05
                if suffix == "_v": parameters["yMin"] = parameters["yMin"]*1.5
                plot(samples, parameters)


                # sytematics
                for bkg in ["qcd","allhad","nonallhad","total"]:
                    samples = {pbryant+"LimitSettingInputs_redo_iter7/resolved_4bSR_"+year+".root":
                               {bkg+"_"+region+suffix:  {"label"    : labels[bkg],
                                                         "ratio"    : "denom A",
                                                         "color"    : "ROOT.kBlack",
                                                         "TObject"  : "",
                                                         "legend"   : 1,
                                                         },
                                bkg+"_"+region+"_LowHtCRw"+suffix: {"label"    : "Low H_{T}^{4j} CR Weighted",
                                                                    "ratio"    : "numer A",
                                                                    "color"    : "ROOT.kRed",
                                                                    "TObject"  : "",
                                                                    "legend"   : 2,
                                                                    },
                                bkg+"_"+region+"_LowHtCRi"+suffix: {"label"    : "Low H_{T}^{4j} CR Inverted",
                                                                    "ratio"    : "numer A",
                                                                    "color"    : "ROOT.kBlue",
                                                                    "TObject"  : "",
                                                                    "legend"   : 3,
                                                                    },
                                },
                           }

                    parameters = {"ratio"     : True,
                                  "atlas"      : "Thesis",
                                  "title"     : "",
                                  "rTitle"    : "Var. / Nom.",
                                  "xTitle"    : "m_{HH} [GeV]" if suffix else "Bin",
                                  "yTitle"    : "Events / Bin",
                                  "status"    : status,
                                  "xMin"      : 150,
                                  "yMax"      : (185 if year == "2015" else 1400),
                                  "xatlas"    : 0.25,
                                  "yatlas"    : 0.85,
                                  "xleg"      : [0.61, 0.91],
                                  "yleg"      : [0.43, 0.92],
                                  "lumi"      : [year,lumi[year]],
                                  "region"    : regionName[region],
                                  "outputDir" : outDir+year+"/results/",
                                  "outputName": bkg+"_LowHtCR_"+region+suffix,
                                  "rMax"      : 1.06,
                                  "rMin"      : 0.94,
                                  #"rebin"     : bins,
                                  }
                    if suffix == "_v": 
                        parameters["xMin"] = 200
                        parameters["xMax"] = 1479
                        parameters["divideByBinWidth"] = True
                        if region == "hh" or region == "CR":
                            parameters["yMax"] = 1850 if year == "2015" else 9000

                    plot(samples, parameters)

                    parameters["logY"] = True
                    parameters["yMax"] = parameters["yMax"]*100
                    parameters["yMin"] = 0.2 if year == "2015" else 0.05
                    plot(samples, parameters)

                    samples = {pbryant+"LimitSettingInputs_redo_iter7/resolved_4bSR_"+year+".root":
                                   {bkg+"_"+region+suffix:  {"label"    : labels[bkg],
                                                             "ratio"    : "denom A",
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             "legend"   : 1,
                                                             },
                                    bkg+"_"+region+"_HighHtCRw"+suffix: {"label"    : "High H_{T}^{4j} CR Weighted",
                                                                         "ratio"    : "numer A",
                                                                         "color"    : "ROOT.kRed",
                                                                         "TObject"  : "",
                                                                         "legend"   : 2,
                                                                         },
                                    bkg+"_"+region+"_HighHtCRi"+suffix: {"label"    : "High H_{T}^{4j} CR Inverted",
                                                                         "ratio"    : "numer A",
                                                                         "color"    : "ROOT.kBlue",
                                                                         "TObject"  : "",
                                                                         "legend"   : 3,
                                                                         },
                                    },
                               }

                    parameters = {"ratio"     : True,
                                  "atlas"      : "Thesis",
                                  "title"     : "",
                                  "status"    : status,
                                  "rTitle"    : "Var. / Nom.",
                                  "xTitle"    : "m_{HH} [GeV]" if suffix else "Bin",
                                  "yTitle"    : "Events / Bin",
                                  "xMin"      : 150,
                                  "yMax"      : (185 if year == "2015" else 1400),
                                  "xatlas"    : 0.25,
                                  "yatlas"    : 0.85,
                                  "xleg"      : [0.61, 0.91],
                                  "yleg"      : [0.43, 0.92],
                                  "lumi"      : [year,lumi[year]],
                                  "region"    : regionName[region],
                                  "outputDir" : outDir+year+"/results/",
                                  "outputName": bkg+"_HighHtCR_"+region+suffix,
                                  "rMax"      : 2.0,
                                  "rMin"      : 0.0,
                                  #"rebin"     : bins,
                                  }
                    
                    if suffix == "_v": 
                        parameters["xMin"] = 200
                        parameters["xMax"] = 1479
                        parameters["divideByBinWidth"] = True
                        if region == "hh" or region == "CR":
                            parameters["yMax"] = 1850 if year == "2015" else 9000

                    plot(samples, parameters)

                    parameters["logY"] = True
                    parameters["yMax"] = parameters["yMax"]*100
                    parameters["yMin"] = 0.2 if year == "2015" else 0.05
                    plot(samples, parameters)


            for mass in ["280","300","400","500"]:
                region = "hh"
                samples = {}
                samples[pbryant+"LimitSettingInputs_redo_iter7/resolved_4bSR_"+year+".root"] = collections.OrderedDict()
                samples[pbryant+"LimitSettingInputs_redo_iter7/resolved_4bSR_"+year+".root"]["s_"+region+"_m"+mass+""+suffix] = {
                    "label"    : "Scalar ("+mass+" GeV)",
                    "color"    : "ROOT.kRed",
                    "normalize": 1,
                    "TObject"  : "",
                    "legend"   : 1,
                    }
                samples[pbryant+"LimitSettingInputs_redo_iter7/resolved_4bSR_"+year+".root"]["g_"+region+"_m"+mass+"_c20"+suffix] = {
                    "label"    : "G_{KK} ("+mass+" GeV, k/#bar{M}_{Pl}=2)",
                    "color"    : "ROOT.kBlack",
                    "normalize": 1,
                    "TObject"  : "",
                    "legend"   : 3,
                    }
                samples[pbryant+"LimitSettingInputs_redo_iter7/resolved_4bSR_"+year+".root"]["g_"+region+"_m"+mass+"_c10"+suffix] = {
                    "label"    : "G_{KK} ("+mass+" GeV, k/#bar{M}_{Pl}=1)",
                    "color"    : "ROOT.kBlue",
                    "lineStyle" : 2,
                    "normalize": 1,
                    "TObject"  : "",
                    "legend"   : 2,
                    }
            
                parameters = {"title"     : "",
                              "atlas"      : "Thesis",
                              "xTitle"    : "m_{HH} [GeV]" if suffix else "Bin",
                              "xTitleOffset" : 0.92,
                              "yTitle"    : "Arb. Units",
                              "status"    : "Simulation "+status,
                              "xMin"      : 150,
                              "yMax"      : 0.8,
                              "xatlas"    : 0.22,
                              "yatlas"    : 0.85,
                              "xleg"      : [0.6, 0.89],
                              "yleg"      : [0.7, 0.9],
                              "lumi"      : [year,lumi[year]],
                              "region"    : regionName[region],
                              "outputDir" : outDir+year+"/results/",
                              "outputName": "signalShape_m"+mass+"_"+region+suffix,
                              }

                if suffix == "_v": 
                    parameters["xMin"] = 200
                    parameters["xMax"] = 1479
                    parameters["divideByBinWidth"] = True

                plot(samples, parameters)


#Detector Systematics
NPs = ["Resolved_JET_GroupedNP_1__1up",
       "Resolved_JET_GroupedNP_1__1down",
       "Resolved_JET_GroupedNP_2__1up",
       "Resolved_JET_GroupedNP_2__1down",
       "Resolved_JET_GroupedNP_3__1up",
       "Resolved_JET_GroupedNP_3__1down",
       "Resolved_JET_EtaIntercalibration_NonClosure__1up",
       "Resolved_JET_EtaIntercalibration_NonClosure__1down",
       "Resolved_JET_JER_SINGLE_NP__1up"]
NPNames = {"Resolved_JET_GroupedNP_1__1up"  : "JES NP 1 up",
           "Resolved_JET_GroupedNP_1__1down": "JES NP 1 down",
           "Resolved_JET_GroupedNP_2__1up"  : "JES NP 2 up",
           "Resolved_JET_GroupedNP_2__1down": "JES NP 2 down",
           "Resolved_JET_GroupedNP_3__1up"  : "JES NP 3 up",
           "Resolved_JET_GroupedNP_3__1down": "JES NP 3 down",
           "Resolved_JET_EtaIntercalibration_NonClosure__1up"  : "JES #eta Intercal. up",
           "Resolved_JET_EtaIntercalibration_NonClosure__1down": "JES #eta Intercal. down",
           "Resolved_JET_JER_SINGLE_NP__1up": "JER up",
           }
if True:
    for year in years:
        inDir = pbryant+"hists_"+year+"_"+weights
        files = rootFiles.getFiles("7",nTuple, inDir, year)

        muFile = pbryant+"XhhResolved/data/mu_qcd_FourTag_"+weights+"_"+year+"_Nominal_"+"7"+".txt"
        mu_qcd_dict = read_mu_qcd_file(muFile)

        filesNPs={}
        for NP in NPs:
            inDir  = pbryant+"hists_"+year+"_"+weights
            filesNPs[NP] = rootFiles.getFiles("7",nTuple, inDir, year,"_"+NP)
    
        for dirName in ["PassAllhadVeto"]:
            for region in ["Signal"]:
                for var in ["m4j_cor_v"]:
                    samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : "With Correction",
                                                                                             "legend"   : 1,
                                                                                             "isData"   : True,
                                                                                             "ratio"    : "numer A",
                                                                                             "color"    : "ROOT.kBlack",
                                                                                             },
                                                        },
                               files["SMNR"]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : "Without Correction",
                                                                                   "legend"   : 2,
                                                                                   "ratio"    : "denom A",
                                                                                   "color"    : "ROOT.kTeal+3",
                                                                                   },
                                              },
                               }
                
                    parameters = {"ratio"     : True,
                                  "atlas"      : "Thesis",
                                  "divideByBinWidth" : True,
                                  "rTitle"    : "With / Without",
                                  "xTitle"    : varLabels[var],
                                  "yTitle"    : "Events / Bin",
                                  "title"     : "",
                                  "status"    : "Simulation "+status,
                                  "lumi"      : [year,lumi[year]],
                                  "region"    : region if region != "FullMassPlane" else "",
                                  "outputDir" : outDir+year+"/SMNR/"+dirName+"/"+region+"/",
                                  "outputName": var+"_finiteTopMassCorrection",
                                  "xMin" : 200,
                                  "xMax" : 1479,
                                  "rMax" : 1.5,
                                  "rMin" : 0.5,
                                  "rebin"     : 1,
                                  #"chi2"      : True,
                                  }
                    
                    plot(samples, parameters)

                    sampleNames = {"SMNR_MhhWeight":"SM HH"}
                    for sample in ["SMNR_MhhWeight"]:
                        for i in range(5):
                            samples = {files[sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sampleNames[sample],
                                                                                           "legend"   : 1,
                                                                                           "isData"   : True,
                                                                                           #"normalize": 1,
                                                                                           "ratio"    : "denom A",
                                                                                           "color"    : "ROOT.kBlack",
                                                                                           "TObject"  : "",
                                                                                           },
                                                      dirName+"_FourTag_"+region+"/"+var+"_bSF"+str(2*i+2): {"label"    : "B"+str(i)+" up",
                                                                                                             "legend"   : 2,
                                                                                                             "ratio"    : "numer A",
                                                                                                             #"normalize": 1,
                                                                                                             "color"    : "ROOT.kRed",
                                                                                                             "TObject"  : "",
                                                                                                             },
                                                      dirName+"_FourTag_"+region+"/"+var+"_bSF"+str(2*i+1): {"label"    : "B"+str(i)+" down",
                                                                                                             "legend"   : 3,
                                                                                                             "ratio"    : "numer A",
                                                                                                             #"normalize": 1,
                                                                                                             "color"    : "ROOT.kBlue",
                                                                                                             "TObject"  : "",
                                                                                                             },
                                                      },
                                       }
                
                            parameters = {"ratio"     : True,
                                          "atlas"      : "Thesis",
                                          "status"     : "Simulation "+status,
                                          "rTitle"    : "Syst. / Nom.",
                                          "yTitle"    : "Events / Bin",
                                          "xTitle"    : varLabels[var],
                                          "title"     : "",
                                          "lumi"      : [year,lumi[year]],
                                          "region"    : region if region != "FullMassPlane" else "",
                                          "outputDir" : outDir+year+"/SMNR/"+dirName+"/"+region+"/",
                                          "outputName": var+"_bSF_B"+str(i),
                                          "xleg" : [0.67, 0.94],
                                          "rebin"     : 1,
                                          "divideByBinWidth": True,
                                          "xMin" : 200,
                                          "xMax" : 1479,
                                          "rMax" : 1.05 if i > 1 else 1.2,
                                          "rMin" : 0.95 if i > 1 else 0.8,
                                          "ratioErrors" : False,
                                          #"chi2"      : True,
                                          }
                
                            plot(samples,parameters)

                        samples = {files[sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sampleNames[sample],
                                                                                       "legend"   : 1,
                                                                                       "isData"   : True,
                                                                                       #"normalize": 1,
                                                                                       "ratio"    : "denom A",
                                                                                       "color"    : "ROOT.kBlack",
                                                                                       "TObject"  : "",
                                                                                       },
                                                  dirName+"_FourTag_"+region+"/"+var+"_bSF48"  : {"label"    : "Eff. extrap. up",
                                                                                                  "legend"   : 2,
                                                                                                  "ratio"    : "numer A",
                                                                                                  #"normalize": 1,
                                                                                                  "color"    : "ROOT.kRed",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                                  dirName+"_FourTag_"+region+"/"+var+"_bSF47": {"label"    : "Eff. extrap. down",
                                                                                                "legend"   : 3,
                                                                                                "ratio"    : "numer A",
                                                                                                #"normalize": 1,
                                                                                                "color"    : "ROOT.kBlue",
                                                                                                "TObject"  : "",
                                                                                                },
                                                  },
                                   }
                
                        parameters = {"ratio"     : True,
                                      "atlas"      : "Thesis",
                                      "status"     : "Simulation "+status,
                                      "rTitle"    : "Syst. / Nom.",
                                      "yTitle"    : "Events / Bin",
                                      "xTitle"    : varLabels[var],
                                      "title"     : "",
                                      "lumi"      : [year,lumi[year]],
                                      "region"    : region if region != "FullMassPlane" else "",
                                      "outputDir" : outDir+year+"/SMNR/"+dirName+"/"+region+"/",
                                      "outputName": var+"_B_FT_EFF_extrap",
                                      "xleg" : [0.67, 0.94],
                                      "rebin"     : 1,
                                      "divideByBinWidth": True,
                                      "xMin" : 200,
                                      "xMax" : 1479,
                                      "rMax" : 1.01,
                                      "rMin" : 0.99,
                                      "ratioErrors" : False,
                                      #"chi2"      : True,
                                      }
                
                        plot(samples,parameters)

                        samples = {files[sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sampleNames[sample],
                                                                                       "legend"   : 1,
                                                                                       "isData"   : True,
                                                                                       #"normalize": 1,
                                                                                       "ratio"    : "denom A",
                                                                                       "color"    : "ROOT.kBlack",
                                                                                       "TObject"  : "",
                                                                                       },
                                                  dirName+"_FourTag_"+region+"/"+var+"_tSF_up"  : {"label"    : "Trig. SF up",
                                                                                                   "legend"   : 2,
                                                                                                   "ratio"    : "numer A",
                                                                                                   #"normalize": 1,
                                                                                                   "color"    : "ROOT.kRed",
                                                                                                   "TObject"  : "",
                                                                                                   },
                                                  dirName+"_FourTag_"+region+"/"+var+"_tSF_down": {"label"    : "Trig. SF down",
                                                                                                   "legend"   : 3,
                                                                                                   "ratio"    : "numer A",
                                                                                                   #"normalize": 1,
                                                                                                   "color"    : "ROOT.kBlue",
                                                                                                   "TObject"  : "",
                                                                                                   },
                                                  },
                                   }
                
                        parameters = {"ratio"     : True,
                                      "atlas"      : "Thesis",
                                      "status"     : "Simulation "+status,
                                      "rTitle"    : "Syst. / Nom.",
                                      "yTitle"    : "Events / Bin",
                                      "xTitle"    : varLabels[var],
                                      "title"     : "",
                                      "lumi"      : [year,lumi[year]],
                                      "region"    : region if region != "FullMassPlane" else "",
                                      "outputDir" : outDir+year+"/SMNR/"+dirName+"/"+region+"/",
                                      "outputName": var+"_tSF",
                                      "xleg" : [0.67, 0.94],
                                      "rebin"     : 1,
                                      "divideByBinWidth": True,
                                      "xMin" : 200,
                                      "xMax" : 1479,
                                      "rMax" : 1.05,
                                      "rMin" : 0.95,
                                      "ratioErrors" : False,
                                      #"chi2"      : True,
                                      }
                
                        plot(samples,parameters)
                    
                        for NP in NPs:
                            if "1down" in NP: continue
                            samples = {files[sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sampleNames[sample],
                                                                                           "legend"   : 1,
                                                                                           "isData"   : True,
                                                                                           #"normalize": 1,
                                                                                           "ratio"    : "denom A",
                                                                                           "color"    : "ROOT.kBlack",
                                                                                           "TObject"  : "",
                                                                                           },
                                                      },
                                       filesNPs[NP][sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : NPNames[NP],
                                                                                                  "legend"   : 2,
                                                                                                  "ratio"    : "numer A",
                                                                                                  #"normalize": 1,
                                                                                                  "color"    : "ROOT.kRed",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                                             },
                                       }
                            if "SINGLE" not in NP:
                                NPdown = NP.replace("1up","1down")
                                samples[filesNPs[NPdown][sample]] = {dirName+"_FourTag_"+region+"/"+var: {"label"    : NPNames[NPdown],
                                                                                                          "legend"   : 3,
                                                                                                          "ratio"    : "numer A",
                                                                                                          #"normalize": 1,
                                                                                                          "color"    : "ROOT.kBlue",
                                                                                                          "TObject"  : "",
                                                                                                          },
                                                                     }
                
                            parameters = {"ratio"     : True,
                                          "atlas"      : "Thesis",
                                          "status"     : "Simulation "+status,
                                          "rTitle"    : "Syst. / Nom.",
                                          "yTitle"    : "Events / Bin",
                                          "xTitle"    : varLabels[var],
                                          "title"     : "",
                                          "lumi"      : [year,lumi[year]],
                                          "region"    : region if region != "FullMassPlane" else "",
                                          "outputDir" : outDir+year+"/SMNR/"+dirName+"/"+region+"/",
                                          "outputName": var+"_"+NP.replace("__1up",""),
                                          "rebin"     : 1,
                                          "xleg" : [0.67, 0.94],
                                          "divideByBinWidth": True,
                                          "xMin" : 200,
                                          "xMax" : 1479,
                                          "rMax" : 1.05 if "SINGLE" not in NP else 1.2,
                                          "rMin" : 0.95 if "SINGLE" not in NP else 0.8,
                                          "ratioErrors" : False,
                                          #"chi2"      : True,
                                          }

                            plot(samples,parameters)


if True:
    for region in ["hh"]:
        for bkg in ["qcd","allhad","nonallhad","total"]:
            basePath = "LimitSettingInputs_optimizedXwtFit"
            samples = {basePath+"_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_v":  {"label"    : labels[bkg],
                                                                                         "ratio"    : "denom A",
                                                                                         "color"    : "ROOT.kBlack",
                                                                                         "isData"   : True,
                                                                                         "TObject"  : "",
                                                                                         "legend"   : 1,
                                                                                         },
                                                                  },
                       basePath+"_ttbar_hard_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_v": {"label"    : "t#bar{t} hardened",
                                                                                                   "ratio"    : "numer A",
                                                                                                   "color"    : "ROOT.kRed",
                                                                                                   "TObject"  : "",
                                                                                                   "legend"   : 2,
                                                                                                   },
                                                                             },
                       basePath+"_ttbar_soft_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_v": {"label"    : "t#bar{t} softened",
                                                                                                   "ratio"    : "numer A",
                                                                                                   "color"    : "ROOT.kBlue",
                                                                                                   "TObject"  : "",
                                                                                                   "legend"   : 3,
                                                                                                   },
                                                                             },
                       }

            parameters = {"ratio"     : True,
                          "atlas"      : "Thesis",
                          "title"     : "",
                          "rTitle"    : "Var. / Nom.",
                          "xTitle"    : "m_{HH} [GeV]",
                          "yTitle"    : "Events / Bin",
                          "xMin"      : 200,
                          "xMax"      : 1479,
                          "xatlas"    : 0.27,
                          "yatlas"    : 0.85,
                          "yleg"      : [0.5, 0.9],
                          "xleg"      : [0.67, 0.92],
                          "divideByBinWidth": True,
                          "lumi"      : ["2016",lumi["2016"]],
                          "region"    : regionName[region],
                          "outputDir" : outDir+"/2016/results/",
                          "outputName": bkg+"_ttbar_var_m4j_"+region+"_v",
                          "rMax"      : 1.5 if "had" in bkg else 1.2,
                          "rMin"      : 0.5 if "had" in bkg else 0.8,
                          "ratioErrors" : False if bkg != "total" else True,
                          "logY"      : True,
                          "yMin"      : 0.2,
                          "yMax"      : 8e5,
                          }

            plot(samples, parameters)

            samples = {basePath+"_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_v":  {"label"    : labels[bkg],
                                                                                         "ratio"    : "denom A",
                                                                                         "color"    : "ROOT.kBlack",
                                                                                         "isData"   : True,
                                                                                         "TObject"  : "",
                                                                                         "legend"   : 1,
                                                                                         },
                                                                  },
                       basePath+"_ttbar_hard_xwt_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_v": {"label"    : "t#bar{t} X_{Wt} up",
                                                                                                   "ratio"    : "numer A",
                                                                                                   "color"    : "ROOT.kRed",
                                                                                                   "TObject"  : "",
                                                                                                   "legend"   : 2,
                                                                                                   },
                                                                             },
                       basePath+"_ttbar_soft_xwt_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_v": {"label"    : "t#bar{t} X_{Wt} down",
                                                                                                   "ratio"    : "numer A",
                                                                                                   "color"    : "ROOT.kBlue",
                                                                                                   "TObject"  : "",
                                                                                                   "legend"   : 3,
                                                                                                   },
                                                                             },
                       }

            parameters = {"ratio"     : True,
                          "atlas"      : "Thesis",
                          "title"     : "",
                          "rTitle"    : "Var. / Nom.",
                          "xTitle"    : "m_{HH} [GeV]",
                          "yTitle"    : "Events / Bin",
                          "xMin"      : 200,
                          "xMax"      : 1479,
                          "xatlas"    : 0.27,
                          "yatlas"    : 0.85,
                          "yleg"      : [0.5, 0.9],
                          "xleg"      : [0.67, 0.92],
                          "divideByBinWidth": True,
                          "lumi"      : ["2016",lumi["2016"]],
                          "region"    : regionName[region],
                          "outputDir" : outDir+"/2016/results/",
                          "outputName": bkg+"_ttbar_var_xwt_"+region+"_v",
                          "rMax"      : 2.0 if "had" in bkg else 1.2,
                          "rMin"      : 0.0 if "had" in bkg else 0.8,
                          "ratioErrors" : False if bkg != "total" else True,
                          "logY"      : True,
                          "yMin"      : 0.2,
                          "yMax"      : 8e5,
                          }

            plot(samples, parameters)

            samples = {basePath+"_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_xwt":  {"label"    : labels[bkg],
                                                                                         "ratio"    : "denom A",
                                                                                         "color"    : "ROOT.kBlack",
                                                                                         "isData"   : True,
                                                                                         "TObject"  : "",
                                                                                         "legend"   : 1,
                                                                                         },
                                                                  },
                       basePath+"_ttbar_hard_xwt_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_xwt": {"label"    : "t#bar{t} X_{Wt} up",
                                                                                                   "ratio"    : "numer A",
                                                                                                   "color"    : "ROOT.kRed",
                                                                                                   "TObject"  : "",
                                                                                                   "legend"   : 2,
                                                                                                   },
                                                                             },
                       basePath+"_ttbar_soft_xwt_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_xwt": {"label"    : "t#bar{t} X_{Wt} down",
                                                                                                   "ratio"    : "numer A",
                                                                                                   "color"    : "ROOT.kBlue",
                                                                                                   "TObject"  : "",
                                                                                                   "legend"   : 3,
                                                                                                   },
                                                                             },
                       }

            parameters = {"ratio"     : True,
                          "atlas"      : "Thesis",
                          "title"     : "",
                          "rTitle"    : "Var. / Nom.",
                          "xTitle"    : "X_{Wt}",
                          "yTitle"    : "Events / Bin",
                          #"xMin"      : 200,
                          #"xMax"      : 1479,
                          "xatlas"    : 0.27,
                          "yatlas"    : 0.85,
                          "yleg"      : [0.5, 0.9],
                          "xleg"      : [0.67, 0.92],
                          #"divideByBinWidth": True,
                          "lumi"      : ["2016",lumi["2016"]],
                          "region"    : regionName[region],
                          "outputDir" : outDir+"/2016/results/",
                          "outputName": bkg+"_ttbar_var_xwt_"+region+"_xwt",
                          "rMax"      : 2.0 if "had" in bkg else 1.2,
                          "rMin"      : 0.0 if "had" in bkg else 0.8,
                          "ratioErrors" : False if bkg != "total" else True,
                          #"logY"      : True,
                          #"yMin"      : 0.2,
                          #"yMax"      : 8e5,
                          }

            plot(samples, parameters)


            samples = {basePath+"_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_v":  {"label"    : labels[bkg],
                                                                                         "ratio"    : "denom A",
                                                                                         "color"    : "ROOT.kBlack",
                                                                                         "isData"   : True,
                                                                                         "TObject"  : "",
                                                                                         "legend"   : 1,
                                                                                         },
                                                                  },
                       basePath+"_amcnlo_iter7/resolved_4bSR_2016.root":{bkg+"_"+region+"_v": {"label"    : "t#bar{t} AMC@NLO+Herwig",
                                                                                               "ratio"    : "numer A",
                                                                                               "color"    : "ROOT.kRed",
                                                                                               "TObject"  : "",
                                                                                               "legend"   : 2,
                                                                                               },
                                                                         },
                       }
            
            parameters = {"ratio"     : True,
                          "atlas"      : "Thesis",
                          "title"     : "",
                          "rTitle"    : "Var. / Nom.",
                          "xTitle"    : "m_{HH} [GeV]",
                          "yTitle"    : "Events / Bin",
                          "xMin"      : 200,
                          "xMax"      : 1479,
                          "xatlas"    : 0.27,
                          "yatlas"    : 0.85,
                          "yleg"      : [0.5, 0.9],
                          "xleg"      : [0.67, 0.92],
                          "divideByBinWidth": True,
                          "lumi"      : ["2016",lumi["2016"]],
                          "region"    : regionName[region],
                          "outputDir" : outDir+"/2016/results/",
                          "outputName": bkg+"_amcnlo_"+region+"_v",
                          "rMax"      : 2.0 if "had" in bkg else 1.2,
                          "rMin"      : 0.0 if "had" in bkg else 0.8,
                          "ratioErrors" : False if bkg != "total" else True,
                          "logY"      : True,
                          "yMin"      : 0.2,
                          "yMax"      : 8e5,
                          }

            plot(samples, parameters)

