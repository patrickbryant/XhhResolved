from plotTools import plot, read_mu_qcd_file
import ROOT
import collections
import sys
sys.path.insert(0, 'XhhResolved/scripts/')
from setupConfig import setGRL, setLumi, setRegions, setTagger
import rootFiles
import os
import optparse
parser = optparse.OptionParser()

parser.add_option('-a','--all',       action="store_true",          dest="doAll",          default=False, help="")
parser.add_option('--doMain',         action="store_true",          dest="doMain",         default=False, help="")
parser.add_option('--doSyst',         action="store_true",          dest="doSyst",         default=False, help="")
parser.add_option('--CR',          dest="CR",        default="Nominal", help="")
parser.add_option('--doSignalOnly',   action="store_true",          dest="doSignalOnly",   default=False, help="")
parser.add_option('--doLimitInputs',  action="store_true",          dest="doLimitInputs",  default=False, help="")
parser.add_option('--doPostFit',      action="store_true",          dest="doPostFit",      default=False, help="")
parser.add_option('--doSignal2b4b',   action="store_true",          dest="doSignal2b4b",   default=False, help="")
parser.add_option('--doDataOnly',     action="store_true",          dest="doDataOnly",     default=False, help="")
parser.add_option('--do2dData',       action="store_true",          dest="do2dData",       default=False, help="")
parser.add_option('--do2dSignal',     action="store_true",          dest="do2dSignal",     default=False, help="")
parser.add_option('--doDataMC',       action="store_true",          dest="doDataMC",       default=False, help="")
parser.add_option('--doCutFlow',      action="store_true",          dest="doCutFlow",      default=False, help="")
parser.add_option('--doTrigger',      action="store_true",          dest="doTrigger",      default=False, help="")
parser.add_option('--doWeights',      action="store_true",          dest="doWeights",      default=False, help="")
parser.add_option('--doHCMass',       action="store_true",          dest="doHCMass",       default=False, help="")
parser.add_option('--doJZW',          action="store_true",          dest="doJZW",          default=False, help="")
parser.add_option('--outDir',         dest="outDir",                default="Plots-01-01-01/", help="")
parser.add_option('--inDir',          dest="inDir",                 default="hists", help="")
parser.add_option('--variation',     dest="variation",     default="Nominal", help="")
parser.add_option('-i', '--iter',    dest="iteration",     default="0", help="")
parser.add_option('-v', '--nTuple',    dest="nTuple",     default="01-01-01", help="")
parser.add_option('-y', '--year',    dest="year",     default="2015", help="")
parser.add_option('-l', '--lumi',    dest="lumi",     default="3.2 fb^{-1}", help="")
parser.add_option('--weights',   dest="weights",   default="")
parser.add_option('--threeTag',  dest="threeTag",  action="store_true", default=False)

o, a = parser.parse_args()

###########
## Setup ##
###########
(leadMass_SR, sublMass_SR, radius_SR, radius_CR, radius_SB, inner_SB, CR_shift, SB_shift, doTightQCDTag, doLooseQCDTag, leadHCmassCut, sublHCmassCut, DhhCut) = setRegions(o.variation)

blind = False
outDir = o.outDir
if not blind:
    if o.outDir[-1] == "/": outDir = outDir[:-1]+"_UNBLINDED/"
    else: outDir = outDir + "_UNBLINDED/"
lumi = o.lumi
if o.year == "2016": lumi = "24.3 fb^{-1}"

iteration = o.iteration

if o.threeTag: 
    tag = "Three"
else:
    tag = "Four"

files = rootFiles.getFiles(iteration,o.nTuple, o.inDir, o.year)
NPs = ["Resolved_JET_GroupedNP_1__1up",
       "Resolved_JET_GroupedNP_1__1down",
       "Resolved_JET_GroupedNP_2__1up",
       "Resolved_JET_GroupedNP_2__1down",
       "Resolved_JET_GroupedNP_3__1up",
       "Resolved_JET_GroupedNP_3__1down",
       "Resolved_JET_EtaIntercalibration_NonClosure__1up",
       "Resolved_JET_EtaIntercalibration_NonClosure__1down",
       "Resolved_JET_JER_SINGLE_NP__1up"]
NPNames = {"Resolved_JET_GroupedNP_1__1up"  : "JET NP 1 up",
           "Resolved_JET_GroupedNP_1__1down": "JET NP 1 down",
           "Resolved_JET_GroupedNP_2__1up"  : "JET NP 2 up",
           "Resolved_JET_GroupedNP_2__1down": "JET NP 2 down",
           "Resolved_JET_GroupedNP_3__1up"  : "JET NP 3 up",
           "Resolved_JET_GroupedNP_3__1down": "JET NP 3 down",
           "Resolved_JET_EtaIntercalibration_NonClosure__1up"  : "JET #eta Intercal. up",
           "Resolved_JET_EtaIntercalibration_NonClosure__1down": "JET #eta Intercal. down",
           "Resolved_JET_JER_SINGLE_NP__1up": "JER up",
           }
filesNPs={}
for NP in NPs:
    filesNPs[NP] = rootFiles.getFiles(iteration,o.nTuple, o.inDir, o.year,"_"+NP)

status=""
masses=["M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","nonResonant"]
#HC_plane = ["LowDhh","Sideband","Control","Signal","Inclusive","LMVR","HMVR","NoSR"]
#HC_plane = ["Sideband_nJet4","Sideband_nJet5","Control_nJet4","Control_nJet5","Signal_nJet4","Signal_nJet5","Sideband","Control","Signal"]#,"Inclusive","LMVR","HMVR","NoSR"]
HC_plane = [
    #"FullMassPlane_nJet4","FullMassPlane_nJet5",
    #"NoSR_nJet4","NoSR_nJet5",
    "Sideband","Control","Signal",
    "Inclusive","LMVR","HMVR","FullMassPlane",
    #"Sideband_nJet4","Sideband_nJet5",
    #"Control_nJet4","Control_nJet5",
    #"Signal_nJet4","Signal_nJet5",
    ]

regionName = {"hh":"Signal",
              "SB":"Sideband",
              "CR":"Control",
              "LM":"LM Validation",
              "HM":"HM Validation"}

muFile = "XhhResolved/data/mu_qcd_"+tag+"Tag_"+o.weights+"_"+o.year+"_"+o.CR+"_"+iteration+".txt"

mu_qcd_dict={}
if not o.doTrigger: mu_qcd_dict = read_mu_qcd_file(muFile)

#
# Define rebin if any for all plotted variables
#
rebins = {}
rebins["m4j_l"] = [100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,
                   500,520,540,560,580,600,640,680,720,820,900,1000,1200]
rebins["met_trkEt_l"]  = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,240,280,320,400,500]
rebins["met_clusEt_l"] = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,240,280,320,400,500]
rebins["ht"] = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,230,260,300,340,350,400,500,700,1000]
rebins["R_pt_4j_l"] = rebins["ht"]
rebins["ht_l"] = [0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,2000]
rebins["mht"] = 2
rebins["mht_l"] = [0,10,20,30,40,50,60,70,80,90,100,120,140,160,180,200,240,280,320,400,500]

rebins["mindRjj"] = 2
rebins["maxdRjj"] = 2

rebins["m4j_cor_l"] = rebins["m4j_l"]
rebins["lowHt_m4j_cor_l"] = rebins["m4j_l"]
rebins["highHt_m4j_cor_l"] = rebins["m4j_l"]
rebins["Ht4j_l"] = rebins["m4j_l"]

rebins["m4j"]  = "smart"
rebins["m4j_cor"] = "smart"
rebins["m_4j"] = [200,250,300,350,400,450,500,550,600,650,700,800,900,1000,1250,2000,3000]
rebins["leadHC_Pt_m"] = "smart"
rebins["sublHC_Pt_m"] = "smart"
rebins["leadHC_Pt"] = "smart"
rebins["sublHC_Pt"] = "smart"

rebins["leadHC_Pt_cor_m"] = "smart"
rebins["sublHC_Pt_cor_m"] = "smart"
rebins["leadHC_Pt_cor"] = "smart"
rebins["sublHC_Pt_cor"] = "smart"

rebins["leadHC_Ht"] = "smart"
rebins["sublHC_Ht"] = "smart"
#rebins["leadHC_leadJet_Pt"] = [0,30,40,60,80,100,120,140,160,180,200,240,280,320,400,500]
#rebins["sublHC_leadJet_Pt"] = rebins["leadHC_leadJet_Pt"]
#rebins["leadHC_sublJet_Pt"] = rebins["leadHC_leadJet_Pt"]
#rebins["sublHC_sublJet_Pt"] = rebins["leadHC_leadJet_Pt"]
rebins["leadHC_leadJet_Pt"] = [0,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,240,280,320,400,500,700] 
rebins["sublHC_leadJet_Pt"] = [0,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,240,280,320,400,500,700] 
rebins["leadHC_sublJet_Pt"] = [0,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,240,280,320,400,500,700] 
rebins["sublHC_sublJet_Pt"] = [0,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,240,280,320,400,500,700] 

rebins["leadGC_Pt_m"] = "smart"
rebins["sublGC_Pt_m"] = "smart"
rebins["leadGC_Pt"] = "smart"
rebins["sublGC_Pt"] = "smart"

rebins["leadGC_Pt_cor_m"] = "smart"
rebins["sublGC_Pt_cor_m"] = "smart"
rebins["leadGC_Pt_cor"] = "smart"
rebins["sublGC_Pt_cor"] = "smart"

rebins["sublHC_Pt_diff"] = 2
rebins["leadHC_Pt_diff"] = 2

rebins["leadGC_Ht"] = "smart"
rebins["sublGC_Ht"] = "smart"
#rebins["leadGC_leadJet_Pt"] = [0,30,40,60,80,100,120,140,160,180,200,240,280,320,400,500]
#rebins["sublGC_leadJet_Pt"] = rebins["leadGC_leadJet_Pt"]
#rebins["leadGC_sublJet_Pt"] = rebins["leadGC_leadJet_Pt"]
#rebins["sublGC_sublJet_Pt"] = rebins["leadGC_leadJet_Pt"]
rebins["leadGC_leadJet_Pt"] = [0,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,240,280,320,400,500,700] 
rebins["sublGC_leadJet_Pt"] = [0,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,240,280,320,400,500,700] 
rebins["leadGC_sublJet_Pt"] = [0,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,240,280,320,400,500,700] 
rebins["sublGC_sublJet_Pt"] = [0,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,240,280,320,400,500,700] 

rebins["otherJets_Pt"] = "smart"
rebins["otherJets_Phi"] = 4

rebins["preSelJets_Pt"] = "smart"
rebins["preSelJets_Phi"] = 4

rebins["leadHC_leadJet_Pt_m"] = [0,30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,220,240,300,350,400,500]
rebins["leadHC_sublJet_Pt_m"] = [0,30,40,50,60,70,80,90,100,120,150,200,250,300]
rebins["sublHC_leadJet_Pt_m"] = rebins["leadHC_leadJet_Pt_m"] 
rebins["sublHC_sublJet_Pt_m"] = rebins["leadHC_sublJet_Pt_m"] 
rebins["leadHC_leadJet_Pt_s"] = 2
rebins["leadHC_sublJet_Pt_s"] = 2
rebins["sublHC_leadJet_Pt_s"] = 2
rebins["sublHC_sublJet_Pt_s"] = 2



rebins["leadHC_leadJet_E"] = 4
rebins["leadHC_sublJet_E"] = 4
rebins["sublHC_leadJet_E"] = 4
rebins["sublHC_sublJet_E"] = 4
rebins["leadHC_leadJet_Eta"] = 4
rebins["leadHC_sublJet_Eta"] = 4
rebins["sublHC_leadJet_Eta"] = 4
rebins["sublHC_sublJet_Eta"] = 4
rebins["leadHC_leadJet_Phi"] = 4
rebins["leadHC_sublJet_Phi"] = 4
rebins["sublHC_leadJet_Phi"] = 4
rebins["sublHC_sublJet_Phi"] = 4

rebins["leadGC_leadJet_Pt_m"] = [0,30,40,50,60,70,80,90,100,110,120,130,140,150,160,180,200,220,240,300,350,400,500]
rebins["leadGC_sublJet_Pt_m"] = [0,30,40,50,60,70,80,90,100,120,150,200,250,300]
rebins["sublGC_leadJet_Pt_m"] = rebins["leadGC_leadJet_Pt_m"] 
rebins["sublGC_sublJet_Pt_m"] = rebins["leadGC_sublJet_Pt_m"] 
rebins["leadGC_leadJet_Pt_s"] = 2
rebins["leadGC_sublJet_Pt_s"] = 2
rebins["sublGC_leadJet_Pt_s"] = 2
rebins["sublGC_sublJet_Pt_s"] = 2

rebins["leadHC_jetPtAsymmetry"] = "smart"
rebins["sublHC_jetPtAsymmetry"] = "smart"
rebins["leadGC_jetPtAsymmetry"] = "smart"
rebins["sublGC_jetPtAsymmetry"] = "smart"

rebins["leadGC_leadJet_E"] = 4
rebins["leadGC_sublJet_E"] = 4
rebins["sublGC_leadJet_E"] = 4
rebins["sublGC_sublJet_E"] = 4
rebins["leadGC_leadJet_Eta"] = 4
rebins["leadGC_sublJet_Eta"] = 4
rebins["sublGC_leadJet_Eta"] = 4
rebins["sublGC_sublJet_Eta"] = 4
rebins["leadGC_leadJet_Phi"] = 4
rebins["leadGC_sublJet_Phi"] = 4
rebins["sublGC_leadJet_Phi"] = 4
rebins["sublGC_sublJet_Phi"] = 4

rebins["HCJet1_Eta"]   = 4
rebins["HCJet1_Phi"]   = 4
rebins["HCJet1_Pt"]    = "smart"
rebins["HCJet1_Pt_s"]  = 2
rebins["HCJet1_Pt_m"]  = "smart"
rebins["HCJet2_Eta"]   = 4
rebins["HCJet2_Phi"]   = 4
rebins["HCJet2_Pt"]    = "smart"
rebins["HCJet2_Pt_s"]  = 2
rebins["HCJet2_Pt_m"]  = "smart"
rebins["HCJet3_Eta"]   = 4
rebins["HCJet3_Phi"]   = 4
rebins["HCJet3_Pt"]    = "smart"
rebins["HCJet3_Pt_s"]  = 2
rebins["HCJet3_Pt_m"]  = "smart"
rebins["HCJet4_Eta"]   = 4
rebins["HCJet4_Phi"]   = 4
rebins["HCJet4_Pt"]    = "smart"
rebins["HCJet4_Pt_s"]  = 2
rebins["HCJet4_Pt_m"]  = "smart"

rebins["HCJetTopTwoMV2_Eta"]   = 4
rebins["HCJetTopTwoMV2_Phi"]   = 4
rebins["HCJetTopTwoMV2_Pt"]    = "smart"
rebins["HCJetTopTwoMV2_Pt_s"]  = 2
rebins["HCJetTopTwoMV2_Pt_m"]  = "smart"

rebins["HCJetBottomTwoMV2_Eta"]   = 4
rebins["HCJetBottomTwoMV2_Phi"]   = 4
rebins["HCJetBottomTwoMV2_Pt"]    = "smart"
rebins["HCJetBottomTwoMV2_Pt_s"]  = 2
rebins["HCJetBottomTwoMV2_Pt_m"]  = "smart"

#rebins["HC_jets_Energy"] = "smart"
rebins["HC_jets_PtE_ratio"] = 1
rebins["HC_jets_Pt_m"] = "smart"
rebins["HC_jets_Pt"]   = "smart"
rebins["HC_jets_Phi"]  = 4

rebins["ht_l"] = 2
rebins["dR_hh"] = 2
rebins["dEta_hh"] = 2
rebins["dPhi_hh"] = 4
rebins["dR_gg"] = 2
rebins["dEta_gg"] = 2
rebins["dPhi_gg"] = 4
rebins["R_dRdR"] = 4
rebins["R_dRdR_gg"] = 4
rebins["GCdR_diff"] = 4
rebins["GCdR_sum" ] = 4
rebins["HCdR_diff"] = 2
rebins["HCdR_sum" ] = 2
rebins["leadHC_dRjj"]        = 4
rebins["sublHC_dRjj"]        = 4
rebins["leadHC_Eta"] = 4
rebins["sublHC_Eta"] = 4
rebins["leadHC_Phi"] = 4
rebins["sublHC_Phi"] = 4
rebins["leadHC_JVC"] = 2
rebins["sublHC_JVC"] = 2

rebins["leadGC_dRjj"]        = 4
rebins["sublGC_dRjj"]        = 4
rebins["leadGC_Eta"] = 4
rebins["sublGC_Eta"] = 4
rebins["leadGC_Phi"] = 4
rebins["sublGC_Phi"] = 4

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

varLabels = {"m4j"                    : "m_{4j} [GeV]",
             "m4j_logy"               : "m_{4j} [GeV]",
             "m4j_cor"                : "m_{4j} (corrected) [GeV]",
             "m4j_cor_logy"           : "m_{4j} (corrected) [GeV]",
             "m4j_l"                  : "m_{4j} [GeV]",
             "m4j_l_logy"             : "m_{4j} [GeV]",
             "m4j_cor_l"              : "m_{4j} (corrected) [GeV]",
             "m4j_cor_l_logy"         : "m_{4j} (corrected) [GeV]",
             "m4j_cor_v"              : "m_{4j} (corrected) [GeV]",
             #"m4j_cor_v_s"            : "m_{4j} (corrected) [GeV]",
             "m4j_cor_v_logy"         : "m_{4j} (corrected) [GeV]",
             #"m4j_cor_v_s_logy"       : "m_{4j} (corrected) [GeV]",
             "m4j_cor_f"              : "m_{4j} (corrected) Bin",
             #"m4j_cor_f_s"            : "m_{4j} (corrected) Bin",
             "m4j_cor_f_logy"         : "m_{4j} (corrected) Bin",
             #"m4j_cor_f_s_logy"       : "m_{4j} (corrected) Bin",
             "m4j_cor_Z_v"            : "m_{4j} (Z corrected) [GeV]",
             "m4j_cor_Z_v_logy"       : "m_{4j} (Z corrected) [GeV]",
             "m4j_cor_H_v"            : "m_{4j} (H corrected) [GeV]",
             "m4j_cor_H_v_logy"       : "m_{4j} (H corrected) [GeV]",
             "m4j_diff"               : "m_{4j} (corrected diff) [GeV]",
             "Ht4j_l"                 : "Ht_{4j} [GeV]",
             "R_pt_4j_l"              : "#sqrt{#Sigma (pt-40)^2} 4j [GeV]",
             "lowHt_m4j_cor_l"              : "m_{4j} (corrected) [GeV]",
             "lowHt_m4j_cor_l_logy"         : "m_{4j} (corrected) [GeV]",
             "lowHt_m4j_cor_v"              : "m_{4j} (corrected) [GeV]",
             "lowHt_m4j_cor_v_logy"         : "m_{4j} (corrected) [GeV]",
             "lowHt_m4j_cor_f"              : "m_{4j} (corrected) Bin",
             "lowHt_m4j_cor_f_logy"         : "m_{4j} (corrected) Bin",
             "highHt_m4j_cor_l"              : "m_{4j} (corrected) [GeV]",
             "highHt_m4j_cor_l_logy"         : "m_{4j} (corrected) [GeV]",
             "highHt_m4j_cor_v"              : "m_{4j} (corrected) [GeV]",
             "highHt_m4j_cor_v_logy"         : "m_{4j} (corrected) [GeV]",
             "highHt_m4j_cor_f"              : "m_{4j} (corrected) Bin",
             "highHt_m4j_cor_f_logy"         : "m_{4j} (corrected) Bin",
             "dEta_hh"                : "#Delta#eta_{HH}",
             "dPhi_hh"                : "#Delta#phi_{HH}",
             "dR_hh"                  : "#DeltaR_{HH}",
             "Pt_hh"                  : "p_{T}^{HH}",
             "R_dRdR"                 : "R(dR_{h1},dR_{h2})",
             "dEta_gg"                : "#Delta#eta_{gg}",
             "dPhi_gg"                : "#Delta#phi_{gg}",
             "dR_gg"                  : "#DeltaR_{gg}",
             "Pt_gg"                  : "Pt_{gg}",
             "R_dRdR_gg"              : "R(dR_{g1},dR_{g2})",
             "HCdR_diff"              : "#DeltaR_{2}-#DeltaR_{1}",
             "HCdR_sum"               : "#DeltaR_{2}+#DeltaR_{1}",
             "GCdR_diff"              : "#DeltaR_{2}-#DeltaR_{1}",
             "GCdR_sum"               : "#DeltaR_{2}+#DeltaR_{1}",
             "xhh"                      : "X_{HH}",
             "xwt"                      : "X_{Wt}",
             "xwt_ave"                  : "<X_{Wt}>",
             "xtt"                      : "X_{t#bar{t}}",
             "dhh"                      : "D_{HH} [GeV]",
             "lhh"                      : "L_{HH} [GeV]",
             "rhh"                      : "R_{HH} [GeV]",
             "rhhMin"                   : "R_{HH} (Min) [GeV]",
             "hhJetEtaSum2"             : "#Sigma_{HC Jets} #eta^{2}",
             "HCJetAbsEta"              : "<|HC Jet #eta|>",
             #"nPassingViews"            : "# of Views Passing Cuts",
             #"nbJetsOther"                   : "# of additional b-jets",
             "nJets"                    : "# of jets",             
             "trigBits"                 : "Trigger Combination",
             "trigBits_logy"            : "Trigger Combination",
             "leadHC_dRjj"           : "Lead HC #DeltaR_{jj}",
             "leadHC_Eta"            : "Lead HC #eta",
             "leadHC_Phi"            : "Lead HC #phi",
             "leadHC_Mass"           : "Lead HC Mass [GeV]",
             "leadHC_Ht"             : "Lead HC Ht [GeV]",
             "leadHC_Pt"             : "Lead HC Pt [GeV]",
             "leadHC_Pt_cor"         : "Lead HC Pt (corrected) [GeV]",
             "leadHC_Pt_diff"        : "Lead HC Pt Diff [GeV]",
             "leadHC_jetPtAsymmetry" : "Lead HC Pt(j_{1}) - Pt(j_{2})",
             #"leadHC_JVC"            : "Lead HC JVC",
             #"leadHC_leadJet_E"      : "Lead HC Lead Jet E [GeV]",
             "leadHC_leadJet_Eta"    : "Lead HC Lead Jet #eta",
             "leadHC_leadJet_Phi"    : "Lead HC Lead Jet #phi",
             "leadHC_leadJet_Pt"     : "Lead HC Lead Jet Pt [GeV]",
             "leadHC_leadJet_Pt_s"   : "Lead HC Lead Jet Pt [GeV]",
             "leadHC_leadJet_Pt_m"   : "Lead HC Lead Jet Pt [GeV]",
             "leadHC_leadJet_MV2c10" : "Lead HC Lead Jet MV2c10",
             "leadHC_leadJet_MV2c10_logy" : "Lead HC Lead Jet MV2c10",
             #"leadHC_leadJet_Jvt"    : "Lead HC Lead Jet JVT",
             #"leadHC_sublJet_E"      : "Lead HC Subl Jet E [GeV]",
             "leadHC_sublJet_Eta"    : "Lead HC Subl Jet #eta",
             "leadHC_sublJet_Phi"    : "Lead HC Subl Jet #phi",
             "leadHC_sublJet_Pt"     : "Lead HC Subl Jet Pt [GeV]",
             "leadHC_sublJet_Pt_s"   : "Lead HC Subl Jet Pt [GeV]",
             "leadHC_sublJet_Pt_m"   : "Lead HC Subl Jet Pt [GeV]",
             "leadHC_sublJet_MV2c10" : "Lead HC Subl Jet MV2c10",
             #"leadHC_sublJet_Jvt"    : "Lead HC Subl Jet JVT",
             "sublHC_dRjj"           : "Subl HC #DeltaR_{jj}",
             "sublHC_Eta"            : "Subl HC #eta",
             "sublHC_Phi"            : "Subl HC #phi",
             "sublHC_Mass"           : "Subl HC Mass [GeV]",
             "sublHC_Ht"             : "Subl HC Ht [GeV]",
             "sublHC_Pt"             : "Subl HC Pt [GeV]",
             "sublHC_Pt_cor"         : "Subl HC Pt (corrected) [GeV]",
             "sublHC_Pt_diff"        : "Subl HC Pt Diff [GeV]",
             "sublHC_jetPtAsymmetry" : "Subl HC Pt(j_{1}) - Pt(j_{2})",
             #"sublHC_JVC"            : "Subl HC JVC",
             #"sublHC_leadJet_E"      : "Subl HC Lead Jet E [GeV]",
             "sublHC_leadJet_Eta"    : "Subl HC Lead Jet #eta",
             "sublHC_leadJet_Phi"    : "Subl HC Lead Jet #phi",
             "sublHC_leadJet_Pt"     : "Subl HC Lead Jet Pt [GeV]",
             "sublHC_leadJet_Pt_s"   : "Subl HC Lead Jet Pt [GeV]",
             "sublHC_leadJet_Pt_m"   : "Subl HC Lead Jet Pt [GeV]",
             "sublHC_leadJet_MV2c10" : "Subl HC Lead Jet MV2c10",
             #"sublHC_leadJet_Jvt"    : "Subl HC Lead Jet JVT",
             #"sublHC_sublJet_E"      : "Subl HC Subl Jet E [GeV]",
             "sublHC_sublJet_Eta"    : "Subl HC Subl Jet #eta",
             "sublHC_sublJet_Phi"    : "Subl HC Subl Jet #phi",
             "sublHC_sublJet_Pt"     : "Subl HC Subl Jet Pt [GeV]",
             "sublHC_sublJet_Pt_s"   : "Subl HC Subl Jet Pt [GeV]",
             "sublHC_sublJet_Pt_m"   : "Subl HC Subl Jet Pt [GeV]",
             "sublHC_sublJet_MV2c10" : "Subl HC Subl Jet MV2c10",
             #"sublHC_sublJet_Jvt"    : "Subl HC Subl Jet JVT",
             "HC_jets_Pt"             : "HC Jets Pt [GeV]",
             "HC_jets_Pt_m"           : "HC Jets Pt [GeV]",
             "HC_jets_Pt_s"           : "HC Jets Pt [GeV]",
             "HC_jets_Energy"         : "HC Jets E [GeV]",
             #"HC_jets_PtE_ratio"      : "HC Jets Pt/E",
             "HC_jets_Mass"           : "HC Jets M [GeV]",
             "HC_jets_Phi"            : "HC Jets #phi",
             "HC_jets_Eta"            : "HC Jets #eta",
             "HC_jets_MV2c10"         : "HC Jets MV2c10",
             "HCJetAR"                : "HC Jets sqrt( #Sigma ( 1-p_{T}/E )^{2} )/2",
             "otherJets_Pt"             : "Other Jets Pt [GeV]",
             "otherJets_Pt_s"             : "Other Jets Pt [GeV]",
             #"otherJets_E"              : "Other Jets E [GeV]",
             "otherJets_Phi"            : "Other Jets #phi",
             "otherJets_Eta"            : "Other Jets #eta",
             "otherJets_MV2c10"         : "Other Jets MV2c10",
             "otherJets_MV2c10_logy"         : "Other Jets MV2c10",
             #"otherJets_Jvt_logy"       : "Other Jets JVT",
             #"preSelJets_Pt"             : "Preselection Jets Pt [GeV]",
             #"preSelJets_Pt_s"             : "Preselection Jets Pt [GeV]",
             #"preSelJets_E"              : "Preselection Jets E [GeV]",
             #"preSelJets_Phi"            : "Preselection Jets #phi",
             #"preSelJets_Eta"            : "Preselection Jets #eta",
             #"preSelJets_MV2c10"         : "Preselection Jets MV2c10",
             #"preSelJets_MV2c10_logy"         : "Preselection Jets MV2c10",
             #"preSelJets_Jvt_logy"       : "Preselection Jets JVT",
             "nJetOther"                : "# of additional jets",
             "nJetOther_u"              : "(unweighted) # of additional jets",
             "nbJetsOther"              : "# of additional b-jets",
             #TTVeto
             # "leadHC_mW"             : "Lead HC mW [GeV]",
             # "leadHC_WdRjj"          : "Lead HC W dR(jj)",
             # "leadHC_mTop"           : "Lead HC mTop [GeV]",
             # "leadHC_TdRwb"          : "Lead HC top dR(bW)",
             # "leadHC_Xwt"            : "Lead HC Xwt",
             # "sublHC_mW"             : "Subl HC mW [GeV]",
             # "sublHC_WdRjj"          : "Subl HC W dR(jj)",
             # "sublHC_mTop"           : "Subl HC mTop [GeV]",
             # "sublHC_TdRwb"          : "Subl HC top dR(bW)",
             # "sublHC_Xwt"            : "Subl HC Xwt",
             "leadGC_dRjj"           : "Lead GC #DeltaR_{jj}",
             "leadGC_Eta"            : "Lead GC #eta",
             "leadGC_Phi"            : "Lead GC #phi",
             "leadGC_Mass"           : "Lead GC Mass [GeV]",
             "leadGC_Ht"             : "Lead GC Ht [GeV]",
             "leadGC_Pt"             : "Lead GC Pt [GeV]",
             "leadGC_Pt_cor"         : "Lead GC Pt (corrected) [GeV]",
             "leadGC_Pt_diff"        : "Lead GC Pt Diff [GeV]",
             "leadGC_jetPtAsymmetry" : "Lead GC Pt(j_{1}) - Pt(j_{2})",
             #"leadGC_leadJet_E"      : "Lead GC Lead Jet E [GeV]",
             "leadGC_leadJet_Eta"    : "Lead GC Lead Jet #eta",
             "leadGC_leadJet_Phi"    : "Lead GC Lead Jet #phi",
             "leadGC_leadJet_Pt"     : "Lead GC Lead Jet Pt [GeV]",
             "leadGC_leadJet_Pt_s"   : "Lead GC Lead Jet Pt [GeV]",
             "leadGC_leadJet_Pt_m"   : "Lead GC Lead Jet Pt [GeV]",
             "leadGC_leadJet_MV2c10" : "Lead GC Lead Jet MV2c10",
             "leadGC_leadJet_MV2c10_logy" : "Lead GC Lead Jet MV2c10",
             #"leadGC_leadJet_Jvt"    : "Lead GC Lead Jet JVT",
             #"leadGC_sublJet_E"      : "Lead GC Subl Jet E [GeV]",
             "leadGC_sublJet_Eta"    : "Lead GC Subl Jet #eta",
             "leadGC_sublJet_Phi"    : "Lead GC Subl Jet #phi",
             "leadGC_sublJet_Pt"     : "Lead GC Subl Jet Pt [GeV]",
             "leadGC_sublJet_Pt_s"   : "Lead GC Subl Jet Pt [GeV]",
             "leadGC_sublJet_Pt_m"   : "Lead GC Subl Jet Pt [GeV]",
             "leadGC_sublJet_MV2c10" : "Lead GC Subl Jet MV2c10",
             #"leadGC_sublJet_Jvt"    : "Lead GC Subl Jet JVT",
             "sublGC_dRjj"           : "Subl GC #DeltaR_{jj}",
             "sublGC_Eta"            : "Subl GC #eta",
             "sublGC_Phi"            : "Subl GC #phi",
             "sublGC_Mass"           : "Subl GC Mass [GeV]",
             "sublGC_Ht"             : "Subl GC Ht [GeV]",
             "sublGC_Pt"             : "Subl GC Pt [GeV]",
             "sublGC_Pt_cor"         : "Subl GC Pt (corrected) [GeV]",
             "sublGC_Pt_diff"        : "Subl GC Pt Diff [GeV]",
             "sublGC_jetPtAsymmetry" : "Subl GC Pt(j_{1}) - Pt(j_{2})",
             #"sublGC_leadJet_E"      : "Subl GC Lead Jet E [GeV]",
             "sublGC_leadJet_Eta"    : "Subl GC Lead Jet #eta",
             "sublGC_leadJet_Phi"    : "Subl GC Lead Jet #phi",
             "sublGC_leadJet_Pt"     : "Subl GC Lead Jet Pt [GeV]",
             "sublGC_leadJet_Pt_s"   : "Subl GC Lead Jet Pt [GeV]",
             "sublGC_leadJet_Pt_m"   : "Subl GC Lead Jet Pt [GeV]",
             "sublGC_leadJet_MV2c10" : "Subl GC Lead Jet MV2c10",
             #"sublGC_leadJet_Jvt"    : "Subl GC Lead Jet JVT",
             #"sublGC_sublJet_E"      : "Subl GC Subl Jet E [GeV]",
             "sublGC_sublJet_Eta"    : "Subl GC Subl Jet #eta",
             "sublGC_sublJet_Phi"    : "Subl GC Subl Jet #phi",
             "sublGC_sublJet_Pt"     : "Subl GC Subl Jet Pt [GeV]",
             "sublGC_sublJet_Pt_s"   : "Subl GC Subl Jet Pt [GeV]",
             "sublGC_sublJet_Pt_m"   : "Subl GC Subl Jet Pt [GeV]",
             "sublGC_sublJet_MV2c10" : "Subl GC Subl Jet MV2c10",
             #"sublGC_sublJet_Jvt"    : "Subl GC Subl Jet JVT",
             "HCJet1_Eta"    : "HC Jet 1 #eta",
             "HCJet1_Phi"    : "HC Jet 1 #phi",
             "HCJet1_Pt"     : "HC Jet 1 Pt [GeV]",
             "HCJet1_Pt_s"   : "HC Jet 1 Pt [GeV]",
             "HCJet1_Pt_m"   : "HC Jet 1 Pt [GeV]",
             "HCJet1_MV2c10" : "HC Jet 1 MV2c10",
             "HCJet1_MV2c10_logy" : "HC Jet 1 MV2c10",
             "HCJet2_Eta"    : "HC Jet 2 #eta",
             "HCJet2_Phi"    : "HC Jet 2 #phi",
             "HCJet2_Pt"     : "HC Jet 2 Pt [GeV]",
             "HCJet2_Pt_s"   : "HC Jet 2 Pt [GeV]",
             "HCJet2_Pt_m"   : "HC Jet 2 Pt [GeV]",
             "HCJet2_MV2c10" : "HC Jet 2 MV2c10",
             "HCJet2_MV2c10_logy" : "HC Jet 2 MV2c10",
             "HCJet3_Eta"    : "HC Jet 3 #eta",
             "HCJet3_Phi"    : "HC Jet 3 #phi",
             "HCJet3_Pt"     : "HC Jet 3 Pt [GeV]",
             "HCJet3_Pt_s"   : "HC Jet 3 Pt [GeV]",
             "HCJet3_Pt_m"   : "HC Jet 3 Pt [GeV]",
             "HCJet3_MV2c10" : "HC Jet 3 MV2c10",
             "HCJet3_MV2c10_logy" : "HC Jet 3 MV2c10",
             "HCJet4_Eta"    : "HC Jet 4 #eta",
             "HCJet4_Phi"    : "HC Jet 4 #phi",
             "HCJet4_Pt"     : "HC Jet 4 Pt [GeV]",
             "HCJet4_Pt_s"   : "HC Jet 4 Pt [GeV]",
             "HCJet4_Pt_m"   : "HC Jet 4 Pt [GeV]",
             "HCJet4_MV2c10" : "HC Jet 4 MV2c10",
             "HCJet4_MV2c10_logy" : "HC Jet 4 MV2c10",
             "met_clusEt" : "met_clusEt",
             "met_clusEt_l" : "met_clusEt_l",
             "met_clusEt_l_logy" : "met_clusEt_l",
             "met_clusPhi" : "met_clusPhi",
             "met_trkEt" : "met_trkEt",
             "met_trkEt_l" : "met_trkEt_l",
             "met_trkEt_l_logy" : "met_trkEt_l",
             "met_trkPhi" : "met_trkPhi",
             "nMuons_logy" : "# of Muons (Loose)",
             "nPromptMuons_logy" : "# of Muons",
             "nPromptElecs_logy" : "# of Electrons",
             "NPV":"NPV",
             }

HCtagVars = {
             "Pt"       : "HC Pt [GeV]",
             "dRjj"     : "HC #DeltaR_{jj}",
             "Mass"     : "HC Mass [GeV]",
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
#dirNames = ["Inclusive","PassHCdEta","PassXtt"]
#dirNames = ["Excess","Inclusive","PassHCdEta","PassAllhadVeto"]
#dirNames = ["Excess","PassAllhadVeto"]
#dirNames = ["Excess","NotExcess"]
#dirNames = ["PassVbbVeto","PassAllhadVeto","PassHCdEta","Excess","NotExcess"]
dirNames = ["Inclusive","PassHCdEta","PassAllhadVeto"]
#dirNames = ["PassHCdEta","PassAllhadVeto"]
#dirNames = ["Pass_ggVeto"]
if(o.doAll or o.doMain or o.doDataOnly):
    for dirName in dirNames:
        for region in HC_plane:
            print "Main Plots:",dirName, region
            for ratio in ["2d significance","2d difference","2d ratio"]:
                zTitle = {"2d significance":"(D-B)/#sqrt{B+#deltaB^{2}}",
                          "2d difference"  :"D-B",
                          "2d ratio"       :"D/B"}
                if "significance" in ratio: 
                    zMin, zMax = -3, 3
                if "ratio" in ratio: 
                    zMin, zMax = 0.5, 1.5
                if "difference" in ratio:
                    zMin, zMax = None, None

                samples = {files["data"]:{dirName+"_"+tag+"Tag_"+region+"/": {"drawOptions":"COLZ",
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
            
            
                    
                parameters = {"title"       : "",
                          "yTitle"      : "m_{2j}^{subl} [GeV]",
                          "xTitle"      : "m_{2j}^{lead} [GeV]",
                          "zTitle"      : zTitle[ratio],
                          "zTitleOffset": 1.4,
                          "ratio"       : ratio,
                          "xMin"        : 45,
                          "xMax"        : 210,
                          "yMin"        : 45,
                          "yMax"        : 210,
                          "zMin"        : zMin,
                          "zMax"        : zMax,
                          "satlas"      : 0.04,
                          "rMargin"     : 0.15,
                          "rebin"       : 3, 
                          "canvasSize"  : [720,660],
                          "lumi"        : [o.year,lumi],
                          "region"      : region if region != "FullMassPlane" else "",
                          #"box"         : [83,172,150,196],
                          "outputDir"   : outDir+dirName+"/data/"+region+"/",
                          "functions"   : [[" ((x-"+str(leadMass_SR)+"*"+str(CR_shift)+")**2 + (y-"+str(sublMass_SR)+"*"+str(CR_shift)+")**2)", 0,300,0,300,[30**2],ROOT.kOrange+7,1],
                                           [ "((x-"+str(leadMass_SR)+"*"+str(SB_shift)+")**2 + (y-"+str(sublMass_SR)+"*"+str(SB_shift)+")**2)", 0,300,0,300,[45**2],ROOT.kYellow,1],
                                           ["(((x-"+str(leadMass_SR)+")/(0.1*x))**2          +((y-"+str(sublMass_SR)+")/(0.1*y))**2)",          0,300,0,300,[1.6**2],ROOT.kRed,7]],
                              "outputName" : "m12m34_"+ratio.replace("2d ",""),
                              }
            
                if "difference" in ratio: 
                    del parameters["zMin"]
                    del parameters["zMax"]
                plot(samples, parameters)

                samples = {files["data"]:{dirName+"_"+tag+"Tag_"+region+"/": {"drawOptions":"COLZ",
                                                                          "TObject":"GC_m12m34",
                                                                          "ratio"    : "numer A",
                                                                          },
                                      },
                       files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                      "TObject":"GC_m12m34",
                                                                      "ratio"    : "denom A",
                                                                      "stack"    : 2,
                                                                      "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"], 
                                                                      },
                                      },
                       files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                             "TObject":"GC_m12m34",
                                                                             "ratio"    : "denom A",
                                                                             "stack"    : 1,
                                                                             "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                                                                             },
                                             },
                       files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                            "TObject":"GC_m12m34",
                                                                            "ratio"    : "denom A",
                                                                            "stack"    : 0,
                                                                            "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                                                                            },
                                           },
                       }
            
            
                    
                parameters = {"title"       : "",
                          "yTitle"      : "GC m_{2j}^{subl} [GeV]",
                          "xTitle"      : "GC m_{2j}^{lead} [GeV]",
                          "zTitle"      : zTitle[ratio],
                          "zTitleOffset": 1.4,
                          "ratio"       : ratio,
                          "xMin"        : 0,
                          "xMax"        : 300,
                          "yMin"        : 0,
                          "yMax"        : 300,
                          "zMin"        : zMin,
                          "zMax"        : zMax,
                          "satlas"      : 0.04,
                          "rMargin"     : 0.15,
                          "rebin"       : 3, 
                          "canvasSize"  : [720,660],
                          "lumi"        : [o.year,lumi],
                          "region"      : region if region != "FullMassPlane" else "",
                          #"box"         : [83,172,150,196],
                          "outputDir"   : outDir+dirName+"/data/"+region+"/",
                          "functions"   : [[" ((x-"+str(leadMass_SR)+"*"+str(CR_shift)+")**2 + (y-"+str(sublMass_SR)+"*"+str(CR_shift)+")**2)", 0,300,0,300,[30**2],ROOT.kOrange+7,1],
                                           [ "((x-"+str(leadMass_SR)+"*"+str(SB_shift)+")**2 + (y-"+str(sublMass_SR)+"*"+str(SB_shift)+")**2)", 0,300,0,300,[45**2],ROOT.kYellow,1],
                                           ["(((x-"+str(leadMass_SR)+")/(0.1*x))**2          +((y-"+str(sublMass_SR)+")/(0.1*y))**2)",          0,300,0,300,[1.6**2],ROOT.kRed,7]],
                              "outputName" : "GC_m12m34_"+ratio.replace("2d ",""),
                              }
            
                if "difference" in ratio: 
                    del parameters["zMin"]
                    del parameters["zMax"]
                plot(samples, parameters)


                samples = {files["data"]:{dirName+"_"+tag+"Tag_"+region+"/": {"drawOptions":"COLZ",
                                                                          "TObject":"m4jnJetOther",
                                                                          "ratio"    : "numer A",
                                                                          },
                                      },
                       files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                      "TObject":"m4jnJetOther",
                                                                      "ratio"    : "denom A",
                                                                      "stack"    : 2,
                                                                      "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"], 
                                                                      },
                                      },
                       files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                             "TObject":"m4jnJetOther",
                                                                             "ratio"    : "denom A",
                                                                             "stack"    : 1,
                                                                             "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                                                                             },
                                             },
                       files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                            "TObject":"m4jnJetOther",
                                                                            "ratio"    : "denom A",
                                                                            "stack"    : 0,
                                                                            "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                                                                            },
                                           },
                       }
            
            
                parameters = {"title"       : "",
                          "ratio"       : ratio,
                          "yTitle"     : "# of Additional Jets",
                          "xTitle"     : "m_{4j} [GeV]",
                          "zTitle"      : zTitle[ratio],
                          "zTitleOffset": 1.3,
                          "zMin"        : zMin,
                          "zMax"        : zMax,
                          "satlas"      : 0.04,
                          "rMargin"     : 0.15,
                          "rebinX"      : 4, 
                          "canvasSize"  : [720,660],
                          "lumi"        : [o.year,lumi],
                          "region"      : region if region != "FullMassPlane" else "",
                          #"box"         : [83,172,150,196],
                          "outputDir"   : outDir+dirName+"/data/"+region+"/",
                          "outputName" : "m4jnJetOther_"+ratio.replace("2d ",""),
                          }
            
                if "difference" in ratio: 
                    del parameters["zMin"]
                    del parameters["zMax"]
                plot(samples, parameters)

                samples = {files["data"]:{dirName+"_"+tag+"Tag_"+region+"/": {"drawOptions":"COLZ",
                                                                          "TObject":"dR12dR34",
                                                                          "ratio"    : "numer A",
                                                                          },
                                      },
                       files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                      "TObject":"dR12dR34",
                                                                      "ratio"    : "denom A",
                                                                      "stack"    : 2,
                                                                      "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"], 
                                                                      },
                                      },
                       files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                             "TObject":"dR12dR34",
                                                                             "ratio"    : "denom A",
                                                                             "stack"    : 1,
                                                                             "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                                                                             },
                                             },
                       files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                            "TObject":"dR12dR34",
                                                                            "ratio"    : "denom A",
                                                                            "stack"    : 0,
                                                                            "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                                                                            },
                                           },
                       }
            
            
                parameters = {"title"       : "",
                          "ratio"       : ratio,
                          "yTitle"     : "Subl HC #DeltaR_{jj}",
                          "xTitle"     : "Lead HC #DeltaR_{jj}",
                          "zTitle"      : zTitle[ratio],
                          "zTitleOffset": 1.3,
                          "zMin"        : zMin,
                          "zMax"        : zMax,
                          "satlas"      : 0.04,
                          "rMargin"     : 0.15,
                          "rebin"       : 4,
                          "xMax"        : 4,
                          "yMax"        : 4,
                          "xMin"        : 0,
                          "yMin"        : 0,
                          "canvasSize"  : [720,660],
                          "lumi"        : [o.year,lumi],
                          "region"      : region if region != "FullMassPlane" else "",
                          #"box"         : [83,172,150,196],
                          "outputDir"   : outDir+dirName+"/data/"+region+"/",
                          "outputName" : "dR12dR34_"+ratio.replace("2d ",""),
                          }
            
                if "difference" in ratio: 
                    del parameters["zMin"]
                    del parameters["zMax"]
                plot(samples, parameters)

                samples = {files["data"]:{dirName+"_"+tag+"Tag_"+region+"/": {"drawOptions":"COLZ",
                                                                          "TObject":"GC_dR12dR34",
                                                                          "ratio"    : "numer A",
                                                                          },
                                      },
                       files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                      "TObject":"GC_dR12dR34",
                                                                      "ratio"    : "denom A",
                                                                      "stack"    : 2,
                                                                      "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"], 
                                                                      },
                                      },
                       files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                             "TObject":"GC_dR12dR34",
                                                                             "ratio"    : "denom A",
                                                                             "stack"    : 1,
                                                                             "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                                                                             },
                                             },
                       files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                            "TObject":"GC_dR12dR34",
                                                                            "ratio"    : "denom A",
                                                                            "stack"    : 0,
                                                                            "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                                                                            },
                                           },
                       }
            
            
                parameters = {"title"       : "",
                          "ratio"       : ratio,
                          "yTitle"     : "Subl GC #DeltaR_{jj}",
                          "xTitle"     : "Lead GC #DeltaR_{jj}",
                          "zTitle"      : zTitle[ratio],
                          "zTitleOffset": 1.3,
                          "zMin"        : zMin,
                          "zMax"        : zMax,
                          "satlas"      : 0.04,
                          "rMargin"     : 0.15,
                          "rebin"       : 4,
                          "xMax"        : 4,
                          "yMax"        : 4,
                          "xMin"        : 0,
                          "yMin"        : 0,
                          "canvasSize"  : [720,660],
                          "lumi"        : [o.year,lumi],
                          "region"      : region if region != "FullMassPlane" else "",
                          #"box"         : [83,172,150,196],
                          "outputDir"   : outDir+dirName+"/data/"+region+"/",
                          "outputName" : "GC_dR12dR34_"+ratio.replace("2d ",""),
                          }
            
                if "difference" in ratio: 
                    del parameters["zMin"]
                    del parameters["zMax"]
                plot(samples, parameters)


                samples = {files["data"]:{dirName+"_"+tag+"Tag_"+region+"/": {"drawOptions":"COLZ",
                                                                          "TObject":"pt2pt4",
                                                                          "ratio"    : "numer A",
                                                                          },
                                      },
                       files["qcd"] :{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                      "TObject":"pt2pt4",
                                                                      "ratio"    : "denom A",
                                                                      "stack"    : 2,
                                                                      "weight"   : mu_qcd_dict["mu_qcd_PassHCdEta"], 
                                                                      },
                                      },
                       files["allhadShape"]:{dirName+"_TwoTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                             "TObject":"pt2pt4",
                                                                             "ratio"    : "denom A",
                                                                             "stack"    : 1,
                                                                             "weight"   : mu_qcd_dict["mu_allhad_PassHCdEta"],
                                                                             },
                                             },
                       files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"drawOptions"    : "COLZ",
                                                                            "TObject":"pt2pt4",
                                                                            "ratio"    : "denom A",
                                                                            "stack"    : 0,
                                                                            "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                                                                            },
                                           },
                       }
            
            
                parameters = {"title"       : "",
                          "ratio"       : ratio,
                          "yTitle"     : "HC Jet 4 Pt [GeV]",
                          "xTitle"     : "HC Jet 2 Pt [GeV]",
                          "zTitle"      : zTitle[ratio],
                          "zTitleOffset": 1.3,
                          "zMin"        : zMin,
                          "zMax"        : zMax,
                              "yMin"    : 40,
                              "yMax"    : 80,
                              "xMin"    : 40,
                              "xMax"    : 140,
                          "satlas"      : 0.04,
                          "rMargin"     : 0.15,
                          "canvasSize"  : [720,660],
                          "lumi"        : [o.year,lumi],
                          "region"      : region if region != "FullMassPlane" else "",
                          #"box"         : [83,172,150,196],
                          "outputDir"   : outDir+dirName+"/data/"+region+"/",
                          "outputName" : "pt2pt4_"+ratio.replace("2d ",""),
                          }
            
                if "difference" in ratio: 
                    del parameters["zMin"]
                    del parameters["zMax"]
                plot(samples, parameters)


            for var in varLabels:
                samples = {files["data"]:{dirName+"_"+tag+"Tag_"+region+"/": {"label"    : "Data",
                                                                              "legend"   : 1,
                                                                              "ratio"    : "numer A",
                                                                              "isData"   : True,
                                                                              "color"    : "ROOT.kBlack",
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
                           # files["zbb"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Z+b#bar{b}",
                           #                                                "legend"   : 5,
                           #                                                "ratio"    : "denom A",
                           #                                                "stack"    : 0,
                           #                                                "weight"   : 1,
                           #                                                "color"    : "ROOT.kGreen+2",
                           #                                                },
                           #               },
                           }
                samples[files["SMNR_MhhWeight"]] = {dirName+"_"+tag+"Tag_"+region+"/": {"label"    : "SM HH #times 100",
                                                                                        "legend"   : 6,
                                                                                        "weight"   : 100,
                                                                                        "color"    : "ROOT.kTeal+3",
                                                                                        },
                                                    }
                # samples[files["H260"]] = {dirName+"_"+tag+"Tag_"+region+"/": {"label"    : "NWS 260GeV #mu=0.06",
                #                                                               "legend"   : 6,
                #                                                               "weight"   : 0.06,
                #                                                               "color"    : "ROOT.kBlue+1",
                #                                                               },
                #                           }
                samples[files["H280"]] = {dirName+"_"+tag+"Tag_"+region+"/": {"label"    : "Scalar (280 GeV)",
                                                                              "legend"   : 5,
                                                                              "weight"   : 0.04,
                                                                              "color"    : "ROOT.kRed",
                                                                              },
                                          }
                
                parameters = {#"ratio"     : "significance",
                              "ratio"     : True,
                              "rTitle"    : "Data / Bkgd",
                              #"rTitle"    : "(D-B)/#sqrt{B+#deltaB^{2}}",
                              "yTitle"    : "Events / Bin",
                              "status"    : status,
                              "yleg"      : [0.55, 0.920],
                              "title"     : "",
                              "lumi"      : [o.year,lumi],
                              "region"    : region if region != "FullMassPlane" else "",
                              "outputDir" : outDir+dirName+"/data/"+region+"/",
                              "rebin"     : 1,
                              "rMax"      : 1.5,
                              "rMin"      : 0.5,
                              "xatlas"    : 0.22,
                              "yatlas"    : 0.85,
                              "xleg"      : [0.68,0.93]
                              # "rMax"      :  3,
                              # "rMin"      : -3,
                              }

                if "_v" in var: parameters["divideByBinWidth"] = True
                if not (region == "Signal" and blind): parameters["chi2"] = True
                if region == "Signal" and blind: samples[files["data"]][dirName+"_"+tag+"Tag_"+region+"/"]["weight"] = 0
                if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
                plotVariable(samples, parameters, var, var)

                # #2b data and ttbar
                # samples = {files["data"]:{dirName+"_TwoTag_"+region+"/": {"label"    : "Data (2b)",
                #                                                           "legend"   : 1,
                #                                                           "ratio"    : "numer A",
                #                                                           "isData"   : True,
                #                                                           "color"    : "ROOT.kBlack",
                #                                                           },
                #                           },
                #            files["allhad"]:{dirName+"_TwoTag_"+region+"/": {"label"    : "Hadronic t#bar{t} (2b)",
                #                                                             "legend"   : 2,
                #                                                             "ratio"    : "denom A",
                #                                                             "stack"    : 1,
                #                                                             "weight"   : 1,
                #                                                             "color"    : "ROOT.kAzure-9",
                #                                                             },
                #                            },
                #            files["nonallhad"]:{dirName+"_TwoTag_"+region+"/": {"label"    : "Leptonic t#bar{t} (2b)",
                #                                                                "legend"   : 3,
                #                                                                "ratio"    : "denom A",
                #                                                                "stack"    : 0,
                #                                                                "weight"   : mu_qcd_dict["mu_nonallhad2b_PassHCdEta"],
                #                                                                "color"    : "ROOT.kAzure-4",
                #                                                             },
                #                            },
                #            }
                
                # parameters = {"ratio"     : True,
                #               "rTitle"    : "Data / Bkgd",
                #               "yTitle"    : "Events / Bin",
                #               "title"     : "",
                #               "lumi"      : [o.year,lumi],
                #               "region"    : region if region != "FullMassPlane" else "",
                #               "outputDir" : outDir+dirName+"/data_2b/"+region+"/",
                #               "rebin"     : 1,
                #               }
                # if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                # if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
                # plotVariable(samples, parameters, var, var)

                # #4b data and ttbar
                # samples = {files["data"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Data (4b)",
                #                                                            "legend"   : 1,
                #                                                            "ratio"    : "numer A",
                #                                                            "isData"   : True,
                #                                                            "color"    : "ROOT.kBlack",
                #                                                            },
                #                           },
                #            files["allhad"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Hadronic t#bar{t} (4b)",
                #                                                              "legend"   : 2,
                #                                                              "ratio"    : "denom A",
                #                                                              "stack"    : 1,
                #                                                              "weight"   : 1,
                #                                                              "color"    : "ROOT.kAzure-9",
                #                                                              },
                #                             },
                #            files["nonallhad"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Leptonic t#bar{t} (4b)",
                #                                                                 "legend"   : 3,
                #                                                                 "ratio"    : "denom A",
                #                                                                 "stack"    : 0,
                #                                                                 "weight"   : mu_qcd_dict["mu_nonallhad4b_PassHCdEta"],
                #                                                                 "color"    : "ROOT.kAzure-4",
                #                                                                 },
                #                                },
                #            }
                
                # parameters = {"ratio"     : True,
                #               "rTitle"    : "Data / Bkgd",
                #               "yTitle"    : "Events / Bin",
                #               "title"     : "",
                #               "lumi"      : [o.year,lumi],
                #               "region"    : region if region != "FullMassPlane" else "",
                #               "outputDir" : outDir+dirName+"/data_4b/"+region+"/",
                #               "rebin"     : 1,
                #               }
                # if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                # if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
                # plotVariable(samples, parameters, var, var)

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
                              "rTitle"    : "4b/2b",
                              "yTitle"    : "Events / Bin",
                              "title"     : "",
                              "status"    : "Simulation",
                              "lumi"      : [o.year,lumi],
                              "region"    : region if region != "FullMassPlane" else "",
                              "outputDir" : outDir+dirName+"/allhadShape/"+region+"/",
                              "rebin"     : 1,
                              "chi2"      : True,
                              }
                if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
    
                plotVariable(samples, parameters, var, var)

                #weighted vs unweighted SMNR
                samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/": {"label"    : "With Correction",
                                                                                     "legend"   : 1,
                                                                                     "isData"   : True,
                                                                                     "ratio"    : "numer A",
                                                                                     "color"    : "ROOT.kBlack",
                                                                                     },
                                                    },
                           files["SMNR"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Without Correction",
                                                                           "legend"   : 2,
                                                                           "ratio"    : "denom A",
                                                                           "color"    : "ROOT.kTeal+3",
                                                                           },
                                          },
                           }
                
                parameters = {"ratio"     : True,
                              "rTitle"    : "Black/Green",
                              "yTitle"    : "Events / Bin",
                              "title"     : "",
                              "status"    : "Simulation",
                              "lumi"      : [o.year,lumi],
                              "region"    : region if region != "FullMassPlane" else "",
                              "outputDir" : outDir+dirName+"/SMNR_weightedComparison/"+region+"/",
                              "rebin"     : 1,
                              #"chi2"      : True,
                              }
                if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
    
                plotVariable(samples, parameters, var, var)

                #weighted vs unweighted SMNR
                # samples = {files["SMNR_MhhWeight"]:{dirName+"_FourTag_"+region+"/": {"label"    : "Without PU Reweight",
                #                                                                      "legend"   : 1,
                #                                                                      "isData"   : True,
                #                                                                      "ratio"    : "numer A",
                #                                                                      "color"    : "ROOT.kBlack",
                #                                                                      },
                #                                     },
                #            files["SMNR_MhhWeight_PUWeight"]:{dirName+"_FourTag_"+region+"/": {"label"    : "With PU Reweight",
                #                                                                               "legend"   : 2,
                #                                                                               "ratio"    : "denom A",
                #                                                                               "color"    : "ROOT.kTeal+3",
                #                                                                               },
                #                           },
                #            }
                
                # parameters = {"ratio"     : True,
                #               "rTitle"    : "Black/Green",
                #               "yTitle"    : "Events / Bin",
                #               "title"     : "",
                #               "status"    : "Simulation",
                #               "lumi"      : [o.year,lumi],
                #               "region"    : region if region != "FullMassPlane" else "",
                #               "outputDir" : outDir+dirName+"/SMNR_PUWeightComparison/"+region+"/",
                #               "rebin"     : 1,
                #               #"chi2"      : True,
                #               }
                # if "HCJet" in var: parameters["outputDir"] = parameters["outputDir"]+"HCJets/"
                # if "GC"    in var: parameters["outputDir"] = parameters["outputDir"]+"GCs/"
    
                # plotVariable(samples, parameters, var, var)



#
# 2d plots
# 
if o.doAll or o.doMain or o.doDataOnly or o.do2dData:
    for sample in ["data","H280","SMNR"]:#,"SMNR","M300","M800"]:
        for dirName in dirNames:
            for region in HC_plane:
                print "2d plots:",sample,dirName,region
                tag = "Two" if sample in ["data","qcd","ttbar"] else "Four"
                weight = 1
                if sample in ["data","qcd"]: weight = mu_qcd_dict["mu_qcd_PassHCdEta"]
                elif sample == "ttbar":      weight = mu_qcd_dict["mu_ttbar_PassHCdEta"]

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m12m34",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {"title"       : "",
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
                              "rMargin"     : 0.15,
                              "rebin"       : 1, 
                              "canvasSize"  : [720,660],
                              "lumi"        : [o.year,lumi],
                              "status"      : status if sample == "data" else "Simulation",
                              "region"      : region if region != "FullMassPlane" else "",
                              "outputDir"   : outDir+dirName+"/"+sample+"/"+region+"/",
                              "functions"   : [[" ((x-"+str(leadMass_SR)+"*"+str(CR_shift)+")**2 + (y-"+str(sublMass_SR)+"*"+str(CR_shift)+")**2)", 0,300,0,300,[30**2],ROOT.kOrange+7,1],
                                               [ "((x-"+str(leadMass_SR)+"*"+str(SB_shift)+")**2 + (y-"+str(sublMass_SR)+"*"+str(SB_shift)+")**2)", 0,300,0,300,[45**2],ROOT.kYellow,1],
                                               ["(((x-"+str(leadMass_SR)+")/(0.1*x))**2          +((y-"+str(sublMass_SR)+")/(0.1*y))**2)",          0,300,0,300,[1.6**2],ROOT.kRed,7]],
                              "outputName" : "m12m34",
                              }
                if region == "FullMassPlane": parameters["box"] = [83,177,175,205]

                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "GC_m12m34",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {"title"       : "",
                              "yTitle"      : "GC m_{2j}^{subl} [GeV]",
                              "xTitle"      : "GC m_{2j}^{lead} [GeV]",
                              "zTitle"      : "Events / 25 GeV^{2}",
                              "zTitleOffset": 1.4,
                              "xMin"        : 0,
                              "xMax"        : 300,
                              "yMin"        : 0,
                              "yMax"        : 300,
                              "zMin"        : 0,
                              "maxDigits"   : 3,
                              "satlas"      : 0.04,
                              "rMargin"     : 0.15,
                              "rebin"       : 1, 
                              "canvasSize"  : [720,660],
                              "lumi"        : [o.year,lumi],
                              "status"      : status if sample == "data" else "Simulation",
                              "region"      : region if region != "FullMassPlane" else "",
                              #"box"         : [83,177,175,205],
                              "outputDir"   : outDir+dirName+"/"+sample+"/"+region+"/",
                              "functions"   : [[" ((x-"+str(leadMass_SR)+"*"+str(CR_shift)+")**2 + (y-"+str(sublMass_SR)+"*"+str(CR_shift)+")**2)", 0,300,0,300,[30**2],ROOT.kOrange+7,1],
                                               [ "((x-"+str(leadMass_SR)+"*"+str(SB_shift)+")**2 + (y-"+str(sublMass_SR)+"*"+str(SB_shift)+")**2)", 0,300,0,300,[45**2],ROOT.kYellow,1],
                                               ["(((x-"+str(leadMass_SR)+")/(0.1*x))**2          +((y-"+str(sublMass_SR)+")/(0.1*y))**2)",          0,300,0,300,[1.6**2],ROOT.kRed,7]],
                              "outputName" : "GC_m12m34",
                              }

                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "dR12dR34",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {"title"       : "",
                              "yTitle"     : "Subl HC #DeltaR_{jj}",
                              "xTitle"     : "Lead HC #DeltaR_{jj}",
                              "zTitle"      : "Events / Bin",
                              "zTitleOffset": 1.4,
                              "zMin"        : 0,
                              "xMax"        : 4,
                              "yMax"        : 4,
                              "xMin"        : 0,
                              "yMin"        : 0,
                              "maxDigits"   : 3,
                              "satlas"      : 0.04,
                              "rMargin"     : 0.15,
                              "rebin"       : 1, 
                              "canvasSize"  : [720,660],
                              "lumi"        : [o.year,lumi],
                              "status"      : status if sample == "data" else "Simulation",
                              "region"      : region if region != "FullMassPlane" else "",
                              "outputDir"   : outDir+dirName+"/"+sample+"/"+region+"/",
                              "outputName" : "dR12dR34",
                              }

                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "GC_dR12dR34",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {"title"       : "",
                              "yTitle"     : "Subl GC #DeltaR_{jj}",
                              "xTitle"     : "Lead GC #DeltaR_{jj}",
                              "zTitle"      : "Events / Bin",
                              "zTitleOffset": 1.4,
                              "zMin"        : 0,
                              "xMax"        : 4,
                              "yMax"        : 4,
                              "xMin"        : 0,
                              "yMin"        : 0,
                              "maxDigits"   : 3,
                              "satlas"      : 0.04,
                              "rMargin"     : 0.15,
                              "rebin"       : 1, 
                              "canvasSize"  : [720,660],
                              "lumi"        : [o.year,lumi],
                              "region"      : region if region != "FullMassPlane" else "",
                              "status"      : status if sample == "data" else "Simulation",
                              "outputDir"   : outDir+dirName+"/"+sample+"/"+region+"/",
                              "outputName" : "GC_dR12dR34",
                              }

                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jnJetOther",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "# of Additional Jets",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "region"      : region if region != "FullMassPlane" else "",
                    "status"      : status if sample == "data" else "Simulation",
                    "box"         : [83,172,150,196],
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4jnJetOther",
                    }
            
                plot(samples, parameters)
            

                #
                # Mass Dependent Cuts
                #
                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jLeadHCandPt",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "Lead HC Pt [GeV]",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "region"      : region if region != "FullMassPlane" else "",
                    "box"         : [83,172,150,196],
                    "status"      : status if sample == "data" else "Simulation",
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4jLeadHCPt",
                    "functions"  : [["(0.513333*x - 103.333 - y)",100,1100,0,440,[0],ROOT.kRed,1]],
                    }
            
                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                           "TObject"    : "m4jSublHCandPt",
                                                                           "weight"     : weight,
                                                                           },
                                          },
                           }

                parameters = {
                    "yTitle"     : "Subl HC Pt [GeV]",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "region"      : region if region != "FullMassPlane" else "",
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4jSublHCPt",
                    "status"      : status if sample == "data" else "Simulation",
                    "functions"  : [["(0.333333*x - 73.3333 - y)",100,1100,0,440,[0],ROOT.kRed,1]],
                    }
            
                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jLeadPtHCandPt",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "Lead(Pt) HC Pt [GeV]",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "region"      : region if region != "FullMassPlane" else "",
                    "box"         : [320,335,745,425],
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "status"      : status if sample == "data" else "Simulation",
                    "outputName" : "m4jLeadPtHCPt",
                    "functions"  : [["(0.513333*x - 103.333 - y)",100,1100,0,440,[0],ROOT.kRed,1]],
                    }
            
                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                           "TObject"    : "m4jSublPtHCandPt",
                                                                           "weight"     : weight,
                                                                           },
                                          },
                           }

                parameters = {
                    "yTitle"     : "Subl(Pt) HC Pt [GeV]",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "region"      : region if region != "FullMassPlane" else "",
                    "box"         : [320,220,745,280],
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "status"      : status if sample == "data" else "Simulation",
                    "outputName" : "m4jSublPtHCPt",
                    "functions"  : [["(0.333333*x - 73.3333 - y)",100,1100,0,440,[0],ROOT.kRed,1]],
                    }
            
                plot(samples, parameters)

                    
                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jHCdEta",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "#Delta#eta_{HH}",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"       : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "region"      : region if region != "FullMassPlane" else "",
                    "box"         : [320,1.35,745,1.75],
                    "status"      : status if sample == "data" else "Simulation",
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4jHCdEta",
                    #"functions"  : [["(0.00000428571*x*x - 0.00522857*x + 2.94286 - y)",100,1100,1,1.8,[0],ROOT.kRed,1]],
                    # "functions"  : [["(3.5 - 0.006*x - y)",0,410,1.09,1.8,[0],ROOT.kRed,1],
                    #                 ["(1.1 - y)",393,1100,0,1.15,[0],ROOT.kRed,1] ],
                    }
            
                plot(samples, parameters)


                #
                # Mass Dependent Requirements
                #
                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jLeadHCdRjj",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "Lead HC #DeltaR_{j,j}",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "region"      : region if region != "FullMassPlane" else "",
                    "status"      : status if sample == "data" else "Simulation",
                    #"box"         : [320,2.95,745,3.75],
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4jLeadHCdRjj",
                    "functions"  : [["(360.000/x-0.5000000 - y)",100,1100,0,4,[0],ROOT.kRed,1],
                                    ["(652.863/x+0.4744490 - y)",100,1100,0,4,[0],ROOT.kRed,1]],
                    }
            
                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jSublHCdRjj",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "Subl HC #DeltaR_{j,j}",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "region"      : region if region != "FullMassPlane" else "",
                    #"box"         : [320,2.95,745,3.75],
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4jSublHCdRjj",
                    "status"      : status if sample == "data" else "Simulation",
                    "functions"  : [["(235.242/x+0.0162996 - y)",100,1100,0,4,[0],ROOT.kRed,1],
                                    ["(874.890/x+0.3471370 - y)",100,1100,0,4,[0],ROOT.kRed,1]],
                    }
            
                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jLeadPtHCdRjj",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "Lead(Pt) HC #DeltaR_{j,j}",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "status"      : status if sample == "data" else "Simulation",
                    "region"      : region if region != "FullMassPlane" else "",
                    #"box"         : [320,2.95,745,3.75],
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4jLeadPtHCdRjj",
                    "functions"  : [["(360.000/x-0.5000000 - y)",100,1100,0,4,[0],ROOT.kRed,1],
                                    ["(652.863/x+0.4744490 - y)",100,1100,0,4,[0],ROOT.kRed,1]],
                    }
            
                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4jSublPtHCdRjj",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "Subl(Pt) HC #DeltaR_{j,j}",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "status"      : status if sample == "data" else "Simulation",
                    "region"      : region if region != "FullMassPlane" else "",
                    #"box"         : [320,2.95,745,3.75],
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4jSublPtHCdRjj",
                    "functions"  : [["(235.242/x+0.0162996 - y)",100,1100,0,4,[0],ROOT.kRed,1],
                                    ["(874.890/x+0.3471370 - y)",100,1100,0,4,[0],ROOT.kRed,1]],
                    }
            
                plot(samples, parameters)

                #
                # Passing HC jet pairings vs m4j
                #
                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "m4j_nViews",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {
                    "yTitle"     : "Jet Pairings",
                    "xTitle"     : "m_{4j} [GeV]",
                    "zMin"        : 0,
                    "canvasSize" : [720,660],
                    "maxDigits"  : 4,
                    "lumi"       : [o.year,lumi],
                    "status"      : status if sample == "data" else "Simulation",
                    "region"      : region if region != "FullMassPlane" else "",
                    "box"         : [350,2.77,820,3.4],
                    "outputDir"  : outDir+dirName+"/"+sample+"/"+region+"/",
                    "outputName" : "m4j_nViews",
                    }
            
                plot(samples, parameters)

                samples = {files[sample]:{dirName+"_"+tag+"Tag_"+region+"/" : {"drawOptions": "COLZ",
                                                                               "TObject"    : "pt2pt4",
                                                                               "weight"     : weight,
                                                                               },
                                          },
                           }
                
                parameters = {"title"       : "",
                              "yTitle"     : "HC Jet 4 Pt [GeV]",
                              "xTitle"     : "HC Jet 2 Pt [GeV]",
                              "zTitle"      : "Events / Bin",
                              "zTitleOffset": 1.4,
                              "zMin"        : 0,
                              "yMin"    : 40,
                              "yMax"    : 80,
                              "xMin"    : 40,
                              "xMax"    : 140,
                              "maxDigits"   : 3,
                              "satlas"      : 0.04,
                              "rMargin"     : 0.15,
                              "rebin"       : 1, 
                              "canvasSize"  : [720,660],
                              "lumi"        : [o.year,lumi],
                              "region"      : region if region != "FullMassPlane" else "",
                              "outputDir"   : outDir+dirName+"/"+sample+"/"+region+"/",
                              "status"      : status if sample == "data" else "Simulation "+status,
                              "outputName" : "pt2pt4",
                              }

                plot(samples, parameters)


if o.doLimitInputs:

    for suffix in ["","_v","_l"]:#,"_v_s"]:
        for region in ["hh","CR","LM","HM"]:
            print "limit inputs:",suffix,region
            systematics = ["_NP0_up","_NP0_down",
                           "_NP1_up","_NP1_down",
                           "_NP2_up","_NP2_down",
                           "_LowHtCRw","_LowHtCRi",
                           "_HighHtCRw","_HighHtCRi",
                           ]
            samples = {"LimitSettingInputs_redo_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{"data_"+region+suffix: {"label"    : "Data",
                                                                                                                               "ratio"    : "numer A",
                                                                                                                               "isData"   : True,
                                                                                                                               "color"    : "ROOT.kBlack",
                                                                                                                               "TObject"  : "",
                                                                                                                               "legend"   : 1,
                                                                                                                               "weight": 0 if blind and region == "hh" else 1,
                                                                                                                               },
                                                "qcd_"+region+suffix: {"label"    : "Multijet",
                                                                       "ratio"    : "denom A",
                                                                       "stack"    : 2,
                                                                       "color"    : "ROOT.kYellow",
                                                                       "systematics":["qcd_"+region+syst+suffix for syst in systematics] if region == "hh" else [],
                                                                       "TObject"  : "",
                                                                       "legend"   : 2,
                                                                       },
                                                "allhad_"+region+suffix: {"label"    : "Hadronic t#bar{t}",
                                                                          "ratio"    : "denom A",
                                                                          "stack"    : 1,
                                                                          "color"    : "ROOT.kAzure-9",
                                                                          "systematics":["allhad_"+region+syst+suffix for syst in systematics] if region == "hh" else [],
                                                                          "TObject"  : "",
                                                                          "legend"   : 3,
                                                                          },
                                                "nonallhad_"+region+suffix: {"label"    : "Semi-leptonic t#bar{t}",
                                                                             "ratio"    : "denom A",
                                                                             "stack"    : 0,
                                                                             "color"    : "ROOT.kAzure-4",
                                                                             "systematics":["nonallhad_"+region+syst+suffix for syst in systematics] if region == "hh" else [],
                                                                             "TObject"  : "",
                                                                             "legend"   : 4,
                                                                             },
                                                }
                   }

            #if region == "hh": 
            samples["LimitSettingInputs_redo_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root"].update({
                        "smrwMhh_"+region+suffix: {"label"    : "SM HH #times100",
                                                   "color"    : "ROOT.kTeal+3",
                                                   "weight"   : 100,
                                                   "TObject"  : "",
                                                   "legend"   : 6,
                                                   },
                                                         "g_"+region+"_m800_c10"+suffix: {"label"    : "G_{KK} (800 GeV, k/#bar{M}_{Pl}=1)",
                                                                                   "color"    : "ROOT.kViolet",
                                                                                   "weight"   : (1.77e+02)/(0.10549*1e3),#updated xs/ami xs
                                                                                   "TObject"  : "",
                                                                                   "legend"   : 7,
                                                                                   },
                                                         "g_"+region+"_m1200_c20"+suffix: {"label"    : "G_{KK} (1200 GeV, k/#bar{M}_{Pl}=2)",
                                                                                   "color"    : "ROOT.kViolet-6",
                                                                                   "weight"   : (2.24e+01*4)/(0.045461*1e3),#updated xs * c^2/ami xs
                                                                                   "TObject"  : "",
                                                                                   "legend"   : 8,
                                                                                   },
                                                         "s_"+region+"_m280"+suffix: {"label"    : "Scalar (280 GeV)",#times 0.04
                                                                               "color"    : "ROOT.kRed",
                                                                               "weight"   : 0.04,
                                                                               "TObject"  : "",
                                                                               "legend"   : 5,
                                                                               },
                                                         })
                                                        
            parameters = {"ratio"     : True,
                      "title"     : "",
                      "rTitle"    : "Data / Bkgd",
                      "xTitle"    : "m_{4j} [GeV]" if suffix else "Bin",
                      "yTitle"    : "Events / Bin",
                         "stackErrors": True,
                          #"xMin"      : 150,
                      "yMax"      : (185 if o.year == "2015" else 1400)*(0.5 if suffix[-2:]=="_s" else 1),
                      "xatlas"    : 0.22,
                      "yatlas"    : 0.85,
                      "xleg"      : [0.63, 0.92],
                      "yleg"      : [0.4, 0.9],
                      "lumi"      : [o.year,lumi],
                      "region"    : regionName[region],
                      "outputDir" : o.outDir,
                      "outputName": "data_"+region+suffix,
                          "rMax"      : 1.5,
                          "rMin"      : 0.5,
                      #"rebin"     : bins,
                      }
            if suffix == "_v": 
                parameters["xMin"] = 200
                parameters["xMax"] = 1479
                parameters["divideByBinWidth"] = True
                #parameters["ratioLines"] = [[150,1,1479,1]]
                #parameters["yMax"] = parameters["yMax"]*0.07
                #parameters["yTitle"] = "Events/GeV"
            #if not (regionName[region] == "Signal" and blind): parameters["chi2"] = True

            plot(samples, parameters)

            parameters["logY"] = True
            parameters["yMax"] = parameters["yMax"]*100
            parameters["yMin"] = 0.02 if o.year == "2015" else 0.05
            if suffix == "_v": parameters["yMin"] = parameters["yMin"]*0.15
            plot(samples, parameters)

            # sytematics
            for bkg in ["qcd","allhad","nonallhad","total"]:
                labels = {"qcd":"Multijet",
                          "allhad":"All hadronic t#bar{t}",
                          "nonallhad":"Non-all hadronic t#bar{t}",
                          "total":"Background"}
                samples = {"LimitSettingInputs_redo_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix:  {"label"    : labels[bkg],
                                                                    "ratio"    : "denom A",
                                                                    "color"    : "ROOT.kBlack",
                                                                    "TObject"  : "",
                                                                    "legend"   : 1,
                                                                    },
                                                bkg+"_"+region+"_LowHtCRw"+suffix: {"label"    : "Low Ht CR Weighted",
                                                                                    "ratio"    : "numer A",
                                                                                    "color"    : "ROOT.kRed",
                                                                                    "TObject"  : "",
                                                                                    "legend"   : 2,
                                                                                    },
                                                bkg+"_"+region+"_LowHtCRi"+suffix: {"label"    : "Low Ht CR Inverted",
                                                                                    "ratio"    : "numer A",
                                                                                    "color"    : "ROOT.kBlue",
                                                                                    "TObject"  : "",
                                                                                    "legend"   : 3,
                                                                                    },
                                                },
                       }

                parameters = {"ratio"     : True,
                      "title"     : "",
                      "rTitle"    : "Var / Nom",
                      "xTitle"    : "m_{4j} (corrected) [GeV]" if suffix else "Bin",
                      "yTitle"    : "Events / Bin",
                      "xMin"      : 150,
                      "yMax"      : (185 if o.year == "2015" else 1400)*(0.5 if suffix[-2:]=="_s" else 1),
                      "xatlas"    : 0.27,
                      "yatlas"    : 0.85,
                      "xleg"      : [0.63, 0.95],
                      "yleg"      : [0.4, 0.9],
                      "lumi"      : [o.year,lumi],
                      "region"    : regionName[region],
                      "outputDir" : o.outDir,
                      "outputName": bkg+"_LowHtCR_"+region+suffix,
                              "rMax"      : 1.3,
                              "rMin"      : 0.7,
                      #"rebin"     : bins,
                      }

                plot(samples, parameters)

                parameters["logY"] = True
                parameters["yMax"] = parameters["yMax"]*10
                parameters["yMin"] = 0.02 if o.year == "2015" else 0.005
                plot(samples, parameters)

                samples = {"LimitSettingInputs_redo_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix:  {"label"    : labels[bkg],
                                                                    "ratio"    : "denom A",
                                                                    "color"    : "ROOT.kBlack",
                                                                    "TObject"  : "",
                                                                    "legend"   : 1,
                                                                    },
                                                bkg+"_"+region+"_HighHtCRw"+suffix: {"label"    : "High Ht CR Weighted",
                                                                                    "ratio"    : "numer A",
                                                                                    "color"    : "ROOT.kRed",
                                                                                    "TObject"  : "",
                                                                                    "legend"   : 2,
                                                                                    },
                                                bkg+"_"+region+"_HighHtCRi"+suffix: {"label"    : "High Ht CR Inverted",
                                                                                    "ratio"    : "numer A",
                                                                                    "color"    : "ROOT.kBlue",
                                                                                    "TObject"  : "",
                                                                                    "legend"   : 3,
                                                                                    },
                                                },
                       }

                parameters = {"ratio"     : True,
                      "title"     : "",
                      "rTitle"    : "Var / Nom",
                      "xTitle"    : "m_{4j} (corrected) [GeV]" if suffix else "Bin",
                      "yTitle"    : "Events / Bin",
                      "xMin"      : 150,
                      "yMax"      : (185 if o.year == "2015" else 1400)*(0.5 if suffix[-2:]=="_s" else 1),
                      "xatlas"    : 0.27,
                      "yatlas"    : 0.85,
                      "xleg"      : [0.63, 0.95],
                      "yleg"      : [0.4, 0.9],
                      "lumi"      : [o.year,lumi],
                      "region"    : regionName[region],
                      "outputDir" : o.outDir,
                      "outputName": bkg+"_HighHtCR_"+region+suffix,
                              "rMax"      : 1.3,
                              "rMin"      : 0.7,
                      #"rebin"     : bins,
                      }

                plot(samples, parameters)

                parameters["logY"] = True
                parameters["yMax"] = parameters["yMax"]*10
                parameters["yMin"] = 0.02 if o.year == "2015" else 0.005
                plot(samples, parameters)


                samples = {"LimitSettingInputs_redo_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix:  {"label"    : labels[bkg],
                                                                    "ratio"    : "denom A",
                                                                    "color"    : "ROOT.kBlack",
                                                                    "TObject"  : "",
                                                                    "legend"   : 1,
                                                                    },
                                                bkg+"_"+region+"_CRw"+suffix: {"label"    : "CR Weighted",
                                                                                    "ratio"    : "numer A",
                                                                                    "color"    : "ROOT.kRed",
                                                                                    "TObject"  : "",
                                                                                    "legend"   : 2,
                                                                                    },
                                                bkg+"_"+region+"_CRi"+suffix: {"label"    : "CR Inverted",
                                                                                    "ratio"    : "numer A",
                                                                                    "color"    : "ROOT.kBlue",
                                                                                    "TObject"  : "",
                                                                                    "legend"   : 3,
                                                                                    },
                                                },
                       }

                parameters = {"ratio"     : True,
                      "title"     : "",
                      "rTitle"    : "Var / Nom",
                      "xTitle"    : "m_{4j} (corrected) [GeV]" if suffix else "Bin",
                      "yTitle"    : "Events / Bin",
                      "xMin"      : 150,
                      "yMax"      : (185 if o.year == "2015" else 1400)*(0.5 if suffix[-2:]=="_s" else 1),
                      "xatlas"    : 0.27,
                      "yatlas"    : 0.85,
                      "xleg"      : [0.63, 0.95],
                      "yleg"      : [0.4, 0.9],
                      "lumi"      : [o.year,lumi],
                      "region"    : regionName[region],
                      "outputDir" : o.outDir,
                      "outputName": bkg+"_AllHtCR_"+region+suffix,
                              "rMax"      : 1.3,
                              "rMin"      : 0.7,
                      #"rebin"     : bins,
                      }

                plot(samples, parameters)

                parameters["logY"] = True
                parameters["yMax"] = parameters["yMax"]*10
                parameters["yMin"] = 0.02 if o.year == "2015" else 0.005
                plot(samples, parameters)

                for NP in "012":
                    samples = {"LimitSettingInputs_redo_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":
                                   {bkg+"_"+region+suffix:  {"label"    : labels[bkg],
                                                             "ratio"    : "denom A",
                                                             "color"    : "ROOT.kBlack",
                                                             "TObject"  : "",
                                                             "legend"   : 1,
                                                             },
                                    bkg+"_"+region+"_NP"+NP+"_up"+suffix: {"label"    : "Norm. NP"+NP+" up",
                                                                           "ratio"    : "numer A",
                                                                           "color"    : "ROOT.kRed",
                                                                           "TObject"  : "",
                                                                           "legend"   : 2,
                                                                           },
                                    bkg+"_"+region+"_NP"+NP+"_down"+suffix: {"label"    : "Norm. NP"+NP+" down",
                                                                             "ratio"    : "numer A",
                                                                             "color"    : "ROOT.kBlue",
                                                                             "TObject"  : "",
                                                                             "legend"   : 3,
                                                                             },
                                    },
                               }

                    parameters = {"ratio"     : True,
                                  "title"     : "",
                                  "rTitle"    : "Var / Nom",
                                  "xTitle"    : "m_{4j} (corrected) [GeV]" if suffix else "Bin",
                                  "yTitle"    : "Events / Bin",
                                  "xMin"      : 150,
                                  "yMax"      : (185 if o.year == "2015" else 1400)*(0.5 if suffix[-2:]=="_s" else 1),
                                  "xatlas"    : 0.27,
                                  "yatlas"    : 0.85,
                                  "xleg"      : [0.63, 0.95],
                                  "yleg"      : [0.4, 0.9],
                                  "lumi"      : [o.year,lumi],
                                  "region"    : regionName[region],
                                  "outputDir" : o.outDir,
                                  "outputName": bkg+"_norm_NP"+NP+"_"+region+suffix,
                                  "rMax"      : 1.1,
                                  "rMin"      : 0.9,
                                  #"rebin"     : bins,
                                  }

                    plot(samples, parameters)

                    parameters["logY"] = True
                    parameters["yMax"] = parameters["yMax"]*10
                    parameters["yMin"] = 0.02 if o.year == "2015" else 0.005
                    plot(samples, parameters)

    #         for bkg in ["qcd","allhad","nonallhad","total"]:
    #             basePath = "LimitSettingInputs_redo"
    #             samples = {basePath+"_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix:  {"label"    : labels[bkg],
    #                                                                 "ratio"    : "denom A",
    #                                                                 "color"    : "ROOT.kBlack",
    #                                                                 "TObject"  : "",
    #                                                                 "legend"   : 1,
    #                                                                 },
    #                                                     },
    #                        basePath+"_ttbar_hard_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix: {"label"    : "t#bar{t} hardened",
    #                                                                                                                               "ratio"    : "numer A",
    #                                                                                                                               "color"    : "ROOT.kRed",
    #                                                                                                                               "TObject"  : "",
    #                                                                                                                               "legend"   : 2,
    #                                                                                                                               },
    #                                                                                                       },
    #                        basePath+"_ttbar_soft_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix: {"label"    : "t#bar{t} softened",
    #                                                                                                                               "ratio"    : "numer A",
    #                                                                                                                               "color"    : "ROOT.kBlue",
    #                                                                                                                               "TObject"  : "",
    #                                                                                                                               "legend"   : 3,
    #                                                                                                                               },
    #                                                                                                       },
    #                        }

    #             parameters = {"ratio"     : True,
    #                   "title"     : "",
    #                   "rTitle"    : "Var / Nom",
    #                   "xTitle"    : "m_{4j} (corrected) [GeV]" if suffix else "Bin",
    #                   "yTitle"    : "Events / Bin",
    #                   "xMin"      : 150,
    #                   "yMax"      : 135 if o.year == "2015" else 1500,
    #                   "xatlas"    : 0.27,
    #                   "yatlas"    : 0.85,
    #                   "xleg"      : [0.63, 0.95],
    #                   "yleg"      : [0.4, 0.9],
    #                   "lumi"      : [o.year,lumi],
    #                   "region"    : regionName[region],
    #                   "outputDir" : o.outDir,
    #                   "outputName": bkg+"_ttbar_var_m4j_"+region+suffix,
    #                           "rMax"      : 2,
    #                           "rMin"      : 0,
    #                   #"rebin"     : bins,
    #                   }

    #             plot(samples, parameters)

    #             parameters["logY"] = True
    #             parameters["yMax"] = parameters["yMax"]*10
    #             parameters["yMin"] = 0.02 if o.year == "2015" else 0.005
    #             plot(samples, parameters)

    #             samples = {basePath+"_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix:  {"label"    : labels[bkg],
    #                                                                 "ratio"    : "denom A",
    #                                                                 "color"    : "ROOT.kBlack",
    #                                                                 "TObject"  : "",
    #                                                                 "legend"   : 1,
    #                                                                 },
    #                                                     },
    #                        basePath+"_ttbar_hard_xwt_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix: {"label"    : "t#bar{t} X_{wt} Up",
    #                                                                                                                               "ratio"    : "numer A",
    #                                                                                                                               "color"    : "ROOT.kRed",
    #                                                                                                                               "TObject"  : "",
    #                                                                                                                               "legend"   : 2,
    #                                                                                                                               },
    #                                                                                                       },
    #                        basePath+"_ttbar_soft_xwt_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix: {"label"    : "t#bar{t} X_{wt} Down",
    #                                                                                                                               "ratio"    : "numer A",
    #                                                                                                                               "color"    : "ROOT.kBlue",
    #                                                                                                                               "TObject"  : "",
    #                                                                                                                               "legend"   : 3,
    #                                                                                                                               },
    #                                                                                                       },
    #                        }

    #             parameters = {"ratio"     : True,
    #                   "title"     : "",
    #                   "rTitle"    : "Var / Nom",
    #                   "xTitle"    : "m_{4j} (corrected) [GeV]" if suffix else "Bin",
    #                   "yTitle"    : "Events / Bin",
    #                   "xMin"      : 150,
    #                   "yMax"      : 135 if o.year == "2015" else 1500,
    #                   "xatlas"    : 0.27,
    #                   "yatlas"    : 0.85,
    #                   "xleg"      : [0.63, 0.95],
    #                   "yleg"      : [0.4, 0.9],
    #                   "lumi"      : [o.year,lumi],
    #                   "region"    : regionName[region],
    #                   "outputDir" : o.outDir,
    #                   "outputName": bkg+"_ttbar_var_xwt_"+region+suffix,
    #                           "rMax"      : 2,
    #                           "rMin"      : 0,
    #                   #"rebin"     : bins,
    #                   }

    #             plot(samples, parameters)

    #             parameters["logY"] = True
    #             parameters["yMax"] = parameters["yMax"]*10
    #             parameters["yMin"] = 0.02 if o.year == "2015" else 0.005
    #             plot(samples, parameters)

    #             samples = {basePath+"_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix:  {"label"    : labels[bkg]+" (Powheg+Pythia)",
    #                                                                 "ratio"    : "denom A",
    #                                                                 "color"    : "ROOT.kBlack",
    #                                                                 "TObject"  : "",
    #                                                                 "legend"   : 1,
    #                                                                 },
    #                                                     },
    #                        basePath+"_amcnlo_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix: {"label"    : "aMcAtNlo Herwig",
    #                                                                                                                               "ratio"    : "numer A",
    #                                                                                                                               "color"    : "ROOT.kRed",
    #                                                                                                                               "TObject"  : "",
    #                                                                                                                               "legend"   : 2,
    #                                                                                                                               },
    #                                                                                                       },
    #                        }

    #             parameters = {"ratio"     : True,
    #                   "title"     : "",
    #                   "rTitle"    : "Var / Nom",
    #                   "xTitle"    : "m_{4j} (corrected) [GeV]" if suffix else "Bin",
    #                   "yTitle"    : "Events / Bin",
    #                   "xMin"      : 150,
    #                   "yMax"      : 135 if o.year == "2015" else 1500,
    #                   "xatlas"    : 0.27,
    #                   "yatlas"    : 0.85,
    #                   "xleg"      : [0.63, 0.95],
    #                   "yleg"      : [0.4, 0.9],
    #                   "lumi"      : [o.year,lumi],
    #                   "region"    : regionName[region],
    #                   "outputDir" : o.outDir,
    #                   "outputName": bkg+"_amcnlo_"+region+suffix,
    #                           "rMax"      : 2,
    #                           "rMin"      : 0,
    #                   #"rebin"     : bins,
    #                   }

    #             plot(samples, parameters)

    #             parameters["logY"] = True
    #             parameters["yMax"] = parameters["yMax"]*10
    #             parameters["yMin"] = 0.02 if o.year == "2015" else 0.005
    #             plot(samples, parameters)


    # for suffix in ["_xwt"]:
    #     for region in ["hh","CR","LM","HM"]:
    #         for bkg in ["qcd","allhad","nonallhad","total"]:

    #             samples = {basePath+"_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix:  {"label"    : labels[bkg],
    #                                                                 "ratio"    : "denom A",
    #                                                                 "color"    : "ROOT.kBlack",
    #                                                                 "TObject"  : "",
    #                                                                 "legend"   : 1,
    #                                                                 },
    #                                                     },
    #                        basePath+"_ttbar_hard_xwt_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix: {"label"    : "t#bar{t} X_{wt} Up",
    #                                                                                                                               "ratio"    : "numer A",
    #                                                                                                                               "color"    : "ROOT.kRed",
    #                                                                                                                               "TObject"  : "",
    #                                                                                                                               "legend"   : 2,
    #                                                                                                                               },
    #                                                                                                       },
    #                        basePath+"_ttbar_soft_xwt_iter"+str(iteration)+"/resolved_4bSR_"+o.year+".root":{bkg+"_"+region+suffix: {"label"    : "t#bar{t} X_{wt} Down",
    #                                                                                                                               "ratio"    : "numer A",
    #                                                                                                                               "color"    : "ROOT.kBlue",
    #                                                                                                                               "TObject"  : "",
    #                                                                                                                               "legend"   : 3,
    #                                                                                                                               },
    #                                                                                                       },
    #                        }

    #             parameters = {"ratio"     : True,
    #                   "title"     : "",
    #                   "rTitle"    : "Var / Nom",
    #                   "xTitle"    : "X_{wt}",
    #                   "yTitle"    : "Events / Bin",
    #                   "xatlas"    : 0.27,
    #                   "yatlas"    : 0.85,
    #                   "xleg"      : [0.63, 0.95],
    #                   "yleg"      : [0.4, 0.9],
    #                   "lumi"      : [o.year,lumi],
    #                   "region"    : regionName[region],
    #                   "outputDir" : o.outDir,
    #                   "outputName": bkg+"_ttbar_var_xwt_"+region+suffix,
    #                           "rMax"      : 2,
    #                           "rMin"      : 0,
    #                   #"rebin"     : bins,
    #                   }

    #             plot(samples, parameters)
                

if o.doPostFit:
    region = "CR"
    fits = ["prefit","postfit"]

    bins = [150,250]
    lastBin = bins[-1]
    while lastBin <= 1500:
        lastBin = lastBin+int(lastBin*0.005)*10
        bins.append(lastBin)

    for fit in fits: 
        samples = {files["fitCrossChecks"]:{"m4j_cor_l_data": {"label"    : "Data",
                                                               "ratio"    : "numer A",
                                                           "isData"   : True,
                                                           "color"    : "ROOT.kBlack",
                                                           "TObject"  : "",
                                                           "legend"   : 1,
                                                           },
                                        "m4j_cor_l_qcd_"+fit: {"label"    : "Multijet",
                                                                 "ratio"    : "denom A",
                                                                 "stack"    : 2,
                                                                 "color"    : "ROOT.kYellow",
                                                                 "TObject"  : "",
                                                                 "legend"   : 2,
                                                                 },
                                        "m4j_cor_l_allhad_"+fit: {"label"    : "Hadronic t#bar{t}",
                                                                    "ratio"    : "denom A",
                                                                    "stack"    : 1,
                                                                    "color"    : "ROOT.kAzure-9",
                                                                    "TObject"  : "",
                                                                    "legend"   : 3,
                                                                    },
                                        "m4j_cor_l_nonallhad_"+fit: {"label"    : "Leptonic t#bar{t}",
                                                                       "ratio"    : "denom A",
                                                                       "stack"    : 0,
                                                                       "color"    : "ROOT.kAzure-4",
                                                                       "TObject"  : "",
                                                                       "legend"   : 4,
                                                                       },
                                        }
                   }
                                                        

        parameters = {"ratio"     : True,
                  "title"     : "",
                  "rTitle"    : "Data / Bkgd",
                  "xTitle"    : "m_{4j} (corrected) [GeV]",
                  "yTitle"    : "Events / Bin",
                  "xMin"      : 150,
                  "yMax"      : 1500,
                  "xatlas"    : 0.27,
                  "yatlas"    : 0.85,
                  "xleg"      : [0.63, 0.95],
                  "yleg"      : [0.4, 0.9],
                  "lumi"      : [o.year,lumi],
                  "region"    : regionName[region],
                  "outputDir" : o.outDir,
                  "outputName": "data_"+fit+"_"+region,
                      "rMax"      : 1.5,
                      "rMin"      : 0.5,
                      #"rebin"     : bins,
                      #"rebin"     : 1,
                      }
        if region == "CR": parameters["yMax"] = 800
        if not (regionName[region] == "Signal" and blind): parameters["chi2"] = True
    
        plot(samples, parameters)

        parameters["logY"] = True
        parameters["yMax"] = parameters["yMax"]*17
        parameters["yMin"] = 0.05

        plot(samples,parameters)


if o.doTrigger:
    triggers={
              "2015":[["HLT_2j35_btight_2j35_L14J15.0ETA25","2j35_btight_2j35"],
                      ["HLT_j100_2j55_bmedium",             "j100_2j55_bmedium"],
                      ["HLT_j225_bloose",                   "j225_bloose"],
                      ["L1_4J15.0ETA25", "4J15 |#eta|<2.5"],
                      ["L1_J75_3J20",    "J75_3J20"],
                      ["L1_J100",        "J100"]],
              "2016":[["HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25","2j35_b60_2j35"],
                      ["HLT_j100_2j55_bmv2c2060_split",              "j100_2j55_b60"],
                      ["HLT_j225_bmv2c2060_split",                   "j225_b60"],
                      ["L1_4J15.0ETA25", "4J15 |#eta|<2.5"],
                      ["L1_J75_3J20",    "J75_3J20"],
                      ["L1_J100",        "J100"]],
              }
    samples = {files["trigger"]:collections.OrderedDict()}
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_HLT_SF_up"] = {"color"      : "ROOT.kWhite",
                                                                     "fillColor"  : "ROOT.kGray+2",
                                                                     #"lineStyle"  : 2,
                                                                     "lineWidth"  : 0,
                                                                     "fillStyle"  : 3245,
                                                                     "drawOptions" : "C",
                                                                     "label" : "Systematic Uncertainty",
                                                                     "legendMark" : "f",
                                                                     "legend" : 2,
                                                                     }
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_HLT_SF_down"] = {#"color"      : "ROOT.kWhite",
                                                                       "fillColor"  : "10",
                                                                       #"lineStyle"  : 2,
                                                                       "lineWidth"  : 0,
                                                                       "fillStyle"  : 1001,
                                                                       "drawOptions" : "C",
                                                                       }
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_HLT"] = {"label"      : "HLT OR",
                                                                   "legend"     : 1,
                                                                   "color"      : "ROOT.kBlack",
                                                                   "drawOptions" : "PC",
                                                                   "marker"      : "20",
                                                                   "TObject"   : "",
                                                                   }
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_"+triggers[o.year][0][0]] = {"label"      : triggers[o.year][0][1],
                                                                                  "legend"     : 3,
                                                                                  "color"      : "ROOT.kGreen",
                                                                                  "lineStyle"  : 2,
                                                                                  "drawOptions" : "PC",
                                                                                  "marker"      : "20",
                                                                                  "TObject"   : "",
                                                                                  }
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_"+triggers[o.year][1][0]] = {"label"      : triggers[o.year][1][1],
                                                                                   "legend"     : 4,
                                                                                   "color"      : "ROOT.kBlue",
                                                                                   "lineStyle"  : 7,
                                                                                   "drawOptions" : "PC",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_"+triggers[o.year][2][0]] = {"label"      : triggers[o.year][2][1],
                                                                                   "legend"     : 5,
                                                                                   "color"      : "ROOT.kRed",
                                                                                   "lineStyle"  : 9,
                                                                                   "drawOptions" : "PC",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }

    parameters = {"title"      : "",
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Efficiency",
                  "xTitle"     : "m(G_{KK}) [GeV]",
                  "xTitleOffset": 1,
                  "labelSize"  : 16,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1.5,
                  "xleg"       : [0.6,0.89],
                  "yleg"       : [0.68,0.92],
                  "xatlas"     : 0.15,
                  "yatlas"     : 0.85,
                  "satlas"     : 0.05,
                  "statusOffset": 0.13,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "trigEff_RSG_c10_passSignal_HLT",
                  "drawLines"  : [[250,1,1270,1]]
                  }
        
    plot(samples,parameters,True)


    samples = {files["trigger"]:collections.OrderedDict()}
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_L1"] = {"label"      : "L1 OR",
                                                                  "legend"     : 1,
                                                                  "color"      : "ROOT.kBlack",
                                                                  "drawOptions" : "HIST PC",
                                                                  "marker"      : "20",
                                                                  "TObject"   : "",
                                                                  }
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_"+triggers[o.year][3][0]] = {"label"      : triggers[o.year][3][1],
                                                                                  "legend"     : 2,
                                                                                  "color"      : "ROOT.kGreen",
                                                                                  "lineStyle"  : 2,
                                                                                  "drawOptions" : "HIST PC",
                                                                                  "marker"      : "20",
                                                                                  "TObject"   : "",
                                                                                  }
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_"+triggers[o.year][4][0]] = {"label"      : triggers[o.year][4][1],
                                                                                   "legend"     : 3,
                                                                                   "color"      : "ROOT.kBlue",
                                                                                   "lineStyle"  : 7,
                                                                                   "drawOptions" : "HIST PC",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }
    samples[files["trigger"]]["trigEff_RSG_c10_passSignal_"+triggers[o.year][5][0]] = {"label"      : triggers[o.year][5][1],
                                                                                   "legend"     : 4,
                                                                                   "color"      : "ROOT.kRed",
                                                                                   "lineStyle"  : 9,
                                                                                   "drawOptions" : "HIST PC",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }

    parameters = {"title"      : "",
                  "atlas"      : "Thesis",
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Efficiency",
                  "xTitle"     : "m(G_{KK}) [GeV]",
                  "xTitleOffset": 1,
                  "labelSize"  : 16,
                  "lumi"       : ["",""],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1.5,
                  "xleg"       : [0.6,0.89],
                  "yleg"       : [0.68,0.92],
                  "xatlas"     : 0.15,
                  "yatlas"     : 0.85,
                  "satlas"     : 0.05,
                  "statusOffset": 0.13,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "trigEff_RSG_c10_passSignal_L1",
                  "drawLines"  : [[250,1,1270,1]]
                  }
        
    if o.year == "2016": plot(samples,parameters,False)


    samples = {files["trigger"]:collections.OrderedDict()}
    samples[files["trigger"]]["trigEff_NWS_passSignal_HLT_SF_up"] = {"color"      : "ROOT.kWhite",
                                                                     "fillColor"  : "ROOT.kGray+2",
                                                                     #"lineStyle"  : 2,
                                                                     "lineWidth"  : 0,
                                                                     "fillStyle"  : 3245,
                                                                     "drawOptions" : "HIST C",
                                                                     "label" : "Systematic Uncertainty",
                                                                     "legendMark" : "f",
                                                                     "legend" : 2,
                                                                     }
    samples[files["trigger"]]["trigEff_NWS_passSignal_HLT_SF_down"] = {#"color"      : "ROOT.kWhite",
                                                                       "fillColor"  : "10",
                                                                       #"lineStyle"  : 2,
                                                                       "lineWidth"  : 0,
                                                                       "fillStyle"  : 1001,
                                                                       "drawOptions" : "HIST C",
                                                                       }
    samples[files["trigger"]]["trigEff_NWS_passSignal_HLT"] = {"label"      : "HLT OR",
                                                               "legend"     : 1,
                                                               "color"      : "ROOT.kBlack",
                                                               "drawOptions" : "HIST PC",
                                                               "marker"      : "20",
                                                               "TObject"   : "",
                                                               }
    samples[files["trigger"]]["trigEff_NWS_passSignal_"+triggers[o.year][0][0]] = {"label"      : triggers[o.year][0][1],
                                                                                  "legend"     : 3,
                                                                                  "color"      : "ROOT.kGreen",
                                                                                  "lineStyle"  : 2,
                                                                                  "drawOptions" : "HIST PC",
                                                                                  "marker"      : "20",
                                                                                  "TObject"   : "",
                                                                                  }
    samples[files["trigger"]]["trigEff_NWS_passSignal_"+triggers[o.year][1][0]] = {"label"      : triggers[o.year][1][1],
                                                                                   "legend"     : 4,
                                                                                   "color"      : "ROOT.kBlue",
                                                                                   "lineStyle"  : 7,
                                                                                   "drawOptions" : "HIST PC",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }
    samples[files["trigger"]]["trigEff_NWS_passSignal_"+triggers[o.year][2][0]] = {"label"      : triggers[o.year][2][1],
                                                                                   "legend"     : 5,
                                                                                   "color"      : "ROOT.kRed",
                                                                                   "lineStyle"  : 9,
                                                                                   "drawOptions" : "HIST PC",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }

    parameters = {"title"      : "",
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Efficiency",
                  "xTitle"     : "m(Scalar) [GeV]",
                  "xTitleOffset": 1,
                  "labelSize"  : 16,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1.5,
                  "xleg"       : [0.6,0.89],
                  "yleg"       : [0.68,0.92],
                  "xatlas"     : 0.15,
                  "yatlas"     : 0.85,
                  "satlas"     : 0.05,
                  "statusOffset": 0.13,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "trigEff_NWS_passSignal_HLT",
                  "drawLines"  : [[250,1,1270,1]]
                  }
        
    plot(samples,parameters)

    samples = {files["trigger"]:collections.OrderedDict()}
    samples[files["trigger"]]["trigEff_NWS_passSignal_L1"] = {"label"      : "L1 OR",
                                                                  "legend"     : 1,
                                                                  "color"      : "ROOT.kBlack",
                                                                  "drawOptions" : "PC",
                                                                  "marker"      : "20",
                                                                  "TObject"   : "",
                                                                  }
    samples[files["trigger"]]["trigEff_NWS_passSignal_"+triggers[o.year][3][0]] = {"label"      : triggers[o.year][3][1],
                                                                                  "legend"     : 2,
                                                                                  "color"      : "ROOT.kGreen",
                                                                                  "lineStyle"  : 2,
                                                                                  "drawOptions" : "PC",
                                                                                  "marker"      : "20",
                                                                                  "TObject"   : "",
                                                                                  }
    samples[files["trigger"]]["trigEff_NWS_passSignal_"+triggers[o.year][4][0]] = {"label"      : triggers[o.year][4][1],
                                                                                   "legend"     : 3,
                                                                                   "color"      : "ROOT.kBlue",
                                                                                   "lineStyle"  : 7,
                                                                                   "drawOptions" : "PC",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }
    samples[files["trigger"]]["trigEff_NWS_passSignal_"+triggers[o.year][5][0]] = {"label"      : triggers[o.year][5][1],
                                                                                   "legend"     : 4,
                                                                                   "color"      : "ROOT.kRed",
                                                                                   "lineStyle"  : 9,
                                                                                   "drawOptions" : "PC",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }

    parameters = {"title"      : "",
                  "atlas"      : "Thesis",
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Efficiency",
                  "xTitle"     : "m(Scalar) [GeV]",
                  "xTitleOffset": 1,
                  "labelSize"  : 16,
                  "lumi"       : ["",""],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1.5,
                  "xleg"       : [0.6,0.89],
                  "yleg"       : [0.68,0.92],
                  "xatlas"     : 0.15,
                  "yatlas"     : 0.85,
                  "satlas"     : 0.05,
                  "statusOffset": 0.13,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "trigEff_NWS_passSignal_L1",
                  "drawLines"  : [[250,1,1270,1]]
                  }
        
    if o.year == "2016":     plot(samples,parameters,True)

    samples = {files["trigger"]:{"trigEffMC_NWS_passSignal_HLT": {"label"      : "HLT OR",
                                                                "legend"     : 1,
                                                                "color"      : "ROOT.kBlack",
                                                                "drawOptions" : "PC",
                                                                "marker"      : "20",
                                                                "TObject"   : "",
                                                                },
                                 "trigEffMC_NWS_passSignal_"+triggers[o.year][0][0]: {"label"      : triggers[o.year][0][1],
                                                                                    "legend"     : 2,
                                                                                    "color"      : "ROOT.kGreen",
                                                                                    "lineStyle"  : 2,
                                                                                    "drawOptions" : "PC",
                                                                                    "marker"      : "20",
                                                                                    "TObject"   : "",
                                                                                    },
                                 "trigEffMC_NWS_passSignal_"+triggers[o.year][1][0]: {"label"      : triggers[o.year][1][1],
                                                                                    "legend"     : 3,
                                                                                    "color"      : "ROOT.kBlue",
                                                                                    "lineStyle"  : 7,
                                                                                    "drawOptions" : "PC",
                                                                                    "marker"      : "20",
                                                                                    "TObject"   : "",
                                                                                    },
                                 "trigEffMC_NWS_passSignal_"+triggers[o.year][2][0]: {"label"      : triggers[o.year][2][1],
                                                                                    "legend"     : 4,
                                                                                    "color"      : "ROOT.kRed",
                                                                                    "lineStyle"  : 9,
                                                                                    "drawOptions" : "PC",
                                                                                    "marker"      : "20",
                                                                                    "TObject"   : "",
                                                                                    },
                                 },
               }

    parameters = {"title"      : "",
                  "atlas"      : "Thesis",                  
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Efficiency",
                  "xTitle"     : "m(Scalar) [GeV]",
                  "xTitleOffset": 1,
                  "labelSize"  : 16,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1.5,
                  "xleg"       : [0.6,0.89],
                  "yleg"       : [0.68,0.92],
                  "xatlas"     : 0.15,
                  "yatlas"     : 0.85,
                  "satlas"     : 0.05,
                  "statusOffset": 0.13,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "trigEffMC_NWS_passSignal_HLT",
                  "drawLines"  : [[250,1,1270,1]]
                  }
        
    plot(samples,parameters,True)


    samples = {files["trigger"]:collections.OrderedDict()}
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_HLT_SF_up"] = {"color"      : "ROOT.kWhite",
                                                                     "fillColor"  : "ROOT.kGray+2",
                                                                     #"lineStyle"  : 2,
                                                                     "lineWidth"  : 0,
                                                                     "fillStyle"  : 3245,
                                                                     "drawOptions" : "HIST",
                                                                     "label" : "Systematic Uncertainty",
                                                                     "legendMark" : "f",
                                                                     "legend" : 2,
                                                                     }
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_HLT_SF_down"] = {#"color"      : "ROOT.kWhite",
                                                                       "fillColor"  : "10",
                                                                       #"lineStyle"  : 2,
                                                                       "lineWidth"  : 0,
                                                                       "fillStyle"  : 1001,
                                                                       "drawOptions" : "HIST",
                                                                       }
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_HLT"] = {"label"      : "HLT OR",
                                                               "legend"     : 1,
                                                               "color"      : "ROOT.kBlack",
                                                               "drawOptions" : "HIST P",
                                                               "marker"      : "20",
                                                               "TObject"   : "",
                                                               }
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_"+triggers[o.year][0][0]] = {"label"      : triggers[o.year][0][1],
                                                                                  "legend"     : 3,
                                                                                  "color"      : "ROOT.kGreen",
                                                                                  "lineStyle"  : 2,
                                                                                  "drawOptions" : "HIST P",
                                                                                  "marker"      : "20",
                                                                                  "TObject"   : "",
                                                                                  }
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_"+triggers[o.year][1][0]] = {"label"      : triggers[o.year][1][1],
                                                                                   "legend"     : 4,
                                                                                   "color"      : "ROOT.kBlue",
                                                                                   "lineStyle"  : 7,
                                                                                   "drawOptions" : "HIST P",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_"+triggers[o.year][2][0]] = {"label"      : triggers[o.year][2][1],
                                                                                   "legend"     : 5,
                                                                                   "color"      : "ROOT.kRed",
                                                                                   "lineStyle"  : 9,
                                                                                   "drawOptions" : "HIST P",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }

    parameters = {"title"      : "",
                  #"status"     : "Simulation "+status,
                  "yTitle"     : "",
                  "yTickLength": 0.1,
                  "xTitle"     : "",
                  "xTitleOffset": 1,
                  "legendTextSize":0.04,
                  "canvasSize" : [125,500],
                  "rMargin"    : 0.08,
                  "lMargin"    : 0.4,
                  "yTitleOffset": 2,
                  #"lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1.5,
                  "xleg"       : [2,2],
                  "yleg"       : [1,1],
                  "labelSize"  : 18,
                  "xatlas"     : 0.455,
                  "yatlas"     : 0.92,
                  "atlasSize"  : 12,
                  "statusSize" : 12,
                  "satlas"     : 0.025,
                  "smallStatus": "Simulation "+status,
                  "statusOffset": 10,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "trigEff_SMNR_passSignal_HLT",
                  "drawLines"  : [[0,1,1,1]]
                  }
    
    plot(samples,parameters)

    samples = {files["trigger"]:collections.OrderedDict()}
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_L1"] = {"label"      : "L1 OR",
                                                                  "legend"     : 1,
                                                                  "color"      : "ROOT.kBlack",
                                                                  "drawOptions" : "P HIST",
                                                                  "marker"      : "20",
                                                                  "TObject"   : "",
                                                                  }
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_"+triggers[o.year][3][0]] = {"label"      : triggers[o.year][3][1],
                                                                                  "legend"     : 2,
                                                                                  "color"      : "ROOT.kGreen",
                                                                                  "lineStyle"  : 2,
                                                                                  "drawOptions" : "P HIST",
                                                                                  "marker"      : "20",
                                                                                  "TObject"   : "",
                                                                                  }
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_"+triggers[o.year][4][0]] = {"label"      : triggers[o.year][4][1],
                                                                                   "legend"     : 3,
                                                                                   "color"      : "ROOT.kBlue",
                                                                                   "lineStyle"  : 7,
                                                                                   "drawOptions" : "HIST P",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }
    samples[files["trigger"]]["trigEff_SMNR_MhhWeight_passSignal_"+triggers[o.year][5][0]] = {"label"      : triggers[o.year][5][1],
                                                                                   "legend"     : 4,
                                                                                   "color"      : "ROOT.kRed",
                                                                                   "lineStyle"  : 9,
                                                                                   "drawOptions" : "HIST P",
                                                                                   "marker"      : "20",
                                                                                   "TObject"   : "",
                                                                                   }

    parameters = {"title"      : "",
                  "atlas"      : "Thesis",
                  #"status"     : "Simulation "+status,
                  "yTitle"     : "",
                  "yTickLength": 0.1,
                  "xTitle"     : "",
                  "xTitleOffset": 1,
                  "legendTextSize":0.04,
                  "canvasSize" : [125,500],
                  "rMargin"    : 0.08,
                  "lMargin"    : 0.4,
                  "yTitleOffset": 2,
                  #"lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1.5,
                  "xleg"       : [2,2],
                  "yleg"       : [1,1],
                  "labelSize"  : 18,
                  "xatlas"     : 0.455,
                  "yatlas"     : 0.92,
                  "atlasSize"  : 12,
                  "statusSize" : 12,
                  "satlas"     : 0.025,
                  "smallStatus": "Simulation "+status,
                  "statusOffset": 10,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "trigEff_SMNR_passSignal_L1",
                  "drawLines"  : [[0,1,1,1]]
                  }
 
    if o.year == "2016":     plot(samples,parameters,False)


    ##Acceptance plots
    samples = {files["trigger"]:{"acceptance_RSG_c10_passSignal_HLT_over_all": {"label"      : "Trigger",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST PC",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_RSG_c10_passSignal_over_all": {"label"      : "X_{Wt}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST PC",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_RSG_c10_passSignalBeforeAllhadVeto_over_all": {"label"      : "X_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST PC",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_RSG_c10_passHCdEta_over_all": {"label"      : "#Delta#eta_{HH}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST PC",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_RSG_c10_passHCPt_over_all": {"label"      : "H p_{T}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST PC",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_RSG_c10_passHCJetPairing_over_all": {"label"      : "#DeltaR_{jj}",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST PC",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 "acceptance_RSG_c10_passHCJetSelection_over_all": {"label"      : "4 b-jets",
                                                                                "legend"     : 1,
                                                                                "color"      : "ROOT.kMagenta",
                                                                                "drawOptions" : "HIST PC",
                                                                                "marker"      : "20",
                                                                                "TObject"    : "",
                                                                                },
                                 },
               }

    parameters = {"title"      : "",
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Acceptance #times Efficiency",
                  "xTitle"     : "m(G_{KK}) [GeV]",
                  "xTitleOffset": 0.95,
                  "legendTextSize":0.04,
                  "canvasSize" : [600,500],
                  "rMargin"    : 0.05,
                  "lMargin"    : 0.12,
                  "yTitleOffset": 1.1,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 0.21,
                  "xleg"       : [0.15,0.43],
                  "yleg"       : [0.55,0.92],
                  "labelSize"  : 16,
                  "xatlas"     : 0.57,
                  "yatlas"     : 0.875,
                  "xlumi"      : 0.57,
                  "ylumi"      : 0.82,
                  "satlas"     : 0.05,
                  "statusOffset": 0.15,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "absoluteAcceptance_RSG_c10",
                  }
    
    plot(samples,parameters)


    samples = {files["trigger"]:{"acceptance_RSG_c10_passSignal_HLT_over_passSignal": {"label"      : "Trigger / X_{Wt}",
                                                                                       "legend"     : 6,
                                                                                       "color"      : "ROOT.kBlack",
                                                                                       "drawOptions" : "PC",
                                                                                       "marker"      : "20",
                                                                                       "TObject"    : "",
                                                                                       },
                                 "acceptance_RSG_c10_passSignal_over_passSignalBeforeAllhadVeto": {"label"      : "X_{Wt} / X_{HH}",
                                                                                                   "legend"     : 5,
                                                                                                   "color"      : "ROOT.kBlue",
                                                                                                   "marker"      : "20",
                                                                                                   "drawOptions" : "PC",
                                                                                                   "TObject"    : "",
                                                                                                   },
                                 "acceptance_RSG_c10_passSignalBeforeAllhadVeto_over_passHCdEta": {"label"      : "X_{HH} / #Delta#eta_{HH}",
                                                                                                   "legend"     : 4,
                                                                                                   "color"      : "ROOT.kGreen",
                                                                                                   "drawOptions" : "PC",
                                                                                                   "marker"      : "20",
                                                                                                   "TObject"    : "",
                                                                                                   },
                                 "acceptance_RSG_c10_passHCdEta_over_passHCPt": {"label"      : "#Delta#eta_{HH} / H p_{T}",
                                                                                 "legend"     : 3,
                                                                                 "color"      : "ROOT.kRed",
                                                                                 "drawOptions" : "PC",
                                                                                 "marker"      : "20",
                                                                                 "TObject"    : "",
                                                                                 },
                                 "acceptance_RSG_c10_passHCPt_over_passHCJetPairing": {"label"      : "H p_{T} / #DeltaR_{jj}",
                                                                                       "legend"     : 2,
                                                                                       "color"      : "ROOT.kOrange",
                                                                                       "drawOptions" : "PC",
                                                                                       "marker"      : "20",
                                                                                       "TObject"    : "",
                                                                                       },
                                 "acceptance_RSG_c10_passHCJetPairing_over_passHCJetSelection": {"label"      : "#DeltaR_{jj} / 4 b-jets",
                                                                                                 "legend"     : 1,
                                                                                                 "color"      : "ROOT.kAzure+2",
                                                                                                 "drawOptions" : "PC",
                                                                                                 "marker"      : "20",
                                                                                                 "TObject"    : "",
                                                                                                 },
                                 },
               }

    parameters = {"title"      : "",
                  "atlas"      : "Thesis",                  
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Acceptance #times Efficiency",
                  "xTitle"     : "m(G_{KK}) [GeV]",
                  "xTitleOffset": 0.95,
                  "legendTextSize":0.04,
                  "canvasSize" : [600,500],
                  "rMargin"    : 0.05,
                  "lMargin"    : 0.12,
                  "yTitleOffset": 1.1,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0.4,
                  "yMax"       : 1.5,
                  "xleg"       : [0.15,0.43],
                  "yleg"       : [0.6,0.92],
                  "labelSize"  : 16,
                  "xatlas"     : 0.57,
                  "yatlas"     : 0.875,
                  "xlumi"      : 0.57,
                  "ylumi"      : 0.82,
                  "satlas"     : 0.05,
                  "statusOffset": 0.15,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "relativeAcceptance_RSG_c10",
                  "drawLines"  : [[250,1,1270,1]]
                  }
    
    plot(samples,parameters)


    samples = {files["trigger"]:{"acceptance_RSG_c20_passSignal_HLT_over_all": {"label"      : "Trigger",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST PC",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_RSG_c20_passSignal_over_all": {"label"      : "X_{Wt}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST PC",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_RSG_c20_passSignalBeforeAllhadVeto_over_all": {"label"      : "X_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST PC",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_RSG_c20_passHCdEta_over_all": {"label"      : "#Delta#eta_{HH}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST PC",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_RSG_c20_passHCPt_over_all": {"label"      : "H p_{T}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST PC",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_RSG_c20_passHCJetPairing_over_all": {"label"      : "#DeltaR_{jj}",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST PC",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 "acceptance_RSG_c20_passHCJetSelection_over_all": {"label"      : "4 b-jets",
                                                                                "legend"     : 1,
                                                                                "color"      : "ROOT.kMagenta",
                                                                                "drawOptions" : "HIST PC",
                                                                                "marker"      : "20",
                                                                                "TObject"    : "",
                                                                                },
                                 },
               }

    parameters = {"title"      : "",
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Acceptance #times Efficiency",
                  "xTitle"     : "m(G_{KK}) [GeV]",
                  "xTitleOffset": 0.95,
                  "legendTextSize":0.04,
                  "canvasSize" : [600,500],
                  "rMargin"    : 0.05,
                  "lMargin"    : 0.12,
                  "yTitleOffset": 1.1,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 0.21,
                  "xleg"       : [0.15,0.43],
                  "yleg"       : [0.55,0.92],
                  "labelSize"  : 16,
                  "xatlas"     : 0.57,
                  "yatlas"     : 0.875,
                  "xlumi"      : 0.57,
                  "ylumi"      : 0.82,
                  "satlas"     : 0.05,
                  "statusOffset": 0.15,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "absoluteAcceptance_RSG_c20",
                  }
    
    plot(samples,parameters)


    samples = {files["trigger"]:{"acceptance_RSG_c20_passSignal_HLT_over_passSignal": {"label"      : "Trigger / X_{Wt}",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST PC",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_RSG_c20_passSignal_over_passSignalBeforeAllhadVeto": {"label"      : "X_{Wt} / X_{HH}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST PC",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_RSG_c20_passSignalBeforeAllhadVeto_over_passHCdEta": {"label"      : "X_{HH} / #Delta#eta_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST PC",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_RSG_c20_passHCdEta_over_passHCPt": {"label"      : "#Delta#eta_{HH} / H p_{T}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST PC",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_RSG_c20_passHCPt_over_passHCJetPairing": {"label"      : "H p_{T} / #DeltaR_{jj}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST PC",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_RSG_c20_passHCJetPairing_over_passHCJetSelection": {"label"      : "#DeltaR_{jj} / 4 b-jets",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST PC",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 },
               }

    parameters = {"title"      : "",
                  "atlas"      : "Thesis",                  
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Acceptance #times Efficiency",
                  "xTitle"     : "m(G_{KK}) [GeV]",
                  "xTitleOffset": 0.95,
                  "legendTextSize":0.04,
                  "canvasSize" : [600,500],
                  "rMargin"    : 0.05,
                  "lMargin"    : 0.12,
                  "yTitleOffset": 1.1,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0.4,
                  "yMax"       : 1.5,
                  "xleg"       : [0.15,0.43],
                  "yleg"       : [0.6,0.92],
                  "labelSize"  : 16,
                  "xatlas"     : 0.57,
                  "yatlas"     : 0.875,
                  "xlumi"      : 0.57,
                  "ylumi"      : 0.82,
                  "satlas"     : 0.05,
                  "statusOffset": 0.15,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "relativeAcceptance_RSG_c20",
                  "drawLines"  : [[250,1,1270,1]]
                  }
    
    plot(samples,parameters)



    samples = {files["trigger"]:{"acceptance_NWS_passSignal_HLT_over_all": {"label"      : "Trigger",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST PC",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_NWS_passSignal_over_all": {"label"      : "X_{Wt}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST PC",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_NWS_passSignalBeforeAllhadVeto_over_all": {"label"      : "X_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST PC",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_NWS_passHCdEta_over_all": {"label"      : "#Delta#eta_{HH}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST PC",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_NWS_passHCPt_over_all": {"label"      : "H p_{T}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST PC",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_NWS_passHCJetPairing_over_all": {"label"      : "#DeltaR_{jj}",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST PC",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 "acceptance_NWS_passHCJetSelection_over_all": {"label"      : "4 b-jets",
                                                                                "legend"     : 1,
                                                                                "color"      : "ROOT.kMagenta",
                                                                                "drawOptions" : "HIST PC",
                                                                                "marker"      : "20",
                                                                                "TObject"    : "",
                                                                                },
                                 },
               }

    parameters = {"title"      : "",
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Acceptance #times Efficiency",
                  "xTitle"     : "m(Scalar) [GeV]",
                  "xTitleOffset": 0.95,
                  "legendTextSize":0.04,
                  "canvasSize" : [600,500],
                  "rMargin"    : 0.05,
                  "lMargin"    : 0.12,
                  "yTitleOffset": 1.1,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 0.21,
                  "xleg"       : [0.15,0.43],
                  "yleg"       : [0.55,0.92],
                  "labelSize"  : 16,
                  "xatlas"     : 0.57,
                  "yatlas"     : 0.875,
                  "xlumi"      : 0.57,
                  "ylumi"      : 0.82,
                  "satlas"     : 0.05,
                  "statusOffset": 0.15,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "absoluteAcceptance_NWS",
                  }
    
    plot(samples,parameters)

    samples = {files["trigger"]:{"acceptance_NWS_passSignal_HLT_over_passSignal": {"label"      : "Trigger / X_{Wt}",
                                                                                       "legend"     : 7,
                                                                                       "color"      : "ROOT.kBlack",
                                                                                       "drawOptions" : "HIST PC",
                                                                                       "marker"      : "20",
                                                                                       "TObject"    : "",
                                                                                       },
                                 "acceptance_NWS_passSignal_over_passSignalBeforeAllhadVeto": {"label"      : "X_{Wt} / X_{HH}",
                                                                                                   "legend"     : 6,
                                                                                                   "color"      : "ROOT.kBlue",
                                                                                                   "marker"      : "20",
                                                                                                   "drawOptions" : "HIST PC",
                                                                                                   "TObject"    : "",
                                                                                                   },
                                 "acceptance_NWS_passSignalBeforeAllhadVeto_over_passHCdEta": {"label"      : "X_{HH} / #Delta#eta_{HH}",
                                                                                                   "legend"     : 5,
                                                                                                   "color"      : "ROOT.kGreen",
                                                                                                   "drawOptions" : "HIST PC",
                                                                                                   "marker"      : "20",
                                                                                                   "TObject"    : "",
                                                                                                   },
                                 "acceptance_NWS_passHCdEta_over_passHCPt": {"label"      : "#Delta#eta_{HH} / H p_{T}",
                                                                                 "legend"     : 4,
                                                                                 "color"      : "ROOT.kRed",
                                                                                 "drawOptions" : "HIST PC",
                                                                                 "marker"      : "20",
                                                                                 "TObject"    : "",
                                                                                 },
                                 "acceptance_NWS_passHCPt_over_passHCJetPairing": {"label"      : "H p_{T} / #DeltaR_{jj}",
                                                                                       "legend"     : 3,
                                                                                       "color"      : "ROOT.kOrange",
                                                                                       "drawOptions" : "HIST PC",
                                                                                       "marker"      : "20",
                                                                                       "TObject"    : "",
                                                                                       },
                                 "acceptance_NWS_passHCJetPairing_over_passHCJetSelection": {"label"      : "#DeltaR_{jj} / 4 b-jets",
                                                                                                 "legend"     : 2,
                                                                                                 "color"      : "ROOT.kAzure+2",
                                                                                                 "drawOptions" : "HIST PC",
                                                                                                 "marker"      : "20",
                                                                                                 "TObject"    : "",
                                                                                                 },
                                 },
               }

    parameters = {"title"      : "",
                  "atlas"      : "Thesis",                  
                  "status"     : "Simulation "+status,
                  "yTitle"     : "Acceptance #times Efficiency",
                  "xTitle"     : "m(Scalar) [GeV]",
                  "xTitleOffset": 0.95,
                  "legendTextSize":0.04,
                  "canvasSize" : [600,500],
                  "rMargin"    : 0.05,
                  "lMargin"    : 0.12,
                  "yTitleOffset": 1.1,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0.4,
                  "yMax"       : 1.5,
                  "xleg"       : [0.15,0.43],
                  "yleg"       : [0.6,0.92],
                  "labelSize"  : 16,
                  "xatlas"     : 0.57,
                  "yatlas"     : 0.875,
                  "xlumi"      : 0.57,
                  "ylumi"      : 0.82,
                  "satlas"     : 0.05,
                  "statusOffset": 0.15,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "relativeAcceptance_NWS",
                  "drawLines"  : [[250,1,1270,1]]
                  }
    
    plot(samples,parameters)

    # samples = {files["trigger"]:{"acceptance_NWS_NLO_passSignal_HLT_over_all": {"label"      : "Trigger",
    #                                                                         "legend"     : 7,
    #                                                                         "color"      : "ROOT.kBlack",
    #                                                                         "drawOptions" : "HIST PC",
    #                                                                         "marker"      : "20",
    #                                                                         "TObject"    : "",
    #                                                                         },
    #                              "acceptance_NWS_NLO_passSignal_over_all": {"label"      : "X_{Wt} < 1.5",
    #                                                                     "legend"     : 6,
    #                                                                     "color"      : "ROOT.kBlue",
    #                                                                     "marker"      : "20",
    #                                                                     "drawOptions" : "HIST PC",
    #                                                                     "TObject"    : "",
    #                                                                     },
    #                              "acceptance_NWS_NLO_passSignalBeforeAllhadVeto_over_all": {"label"      : "X_{HH}",
    #                                                                                     "legend"     : 5,
    #                                                                                     "color"      : "ROOT.kGreen",
    #                                                                                     "drawOptions" : "HIST PC",
    #                                                                                     "marker"      : "20",
    #                                                                                     "TObject"    : "",
    #                                                                                     },
    #                              "acceptance_NWS_NLO_passHCdEta_over_all": {"label"      : "#Delta#eta_{HH}",
    #                                                                     "legend"     : 4,
    #                                                                     "color"      : "ROOT.kRed",
    #                                                                     "drawOptions" : "HIST PC",
    #                                                                     "marker"      : "20",
    #                                                                     "TObject"    : "",
    #                                                                     },
    #                              "acceptance_NWS_NLO_passHCPt_over_all": {"label"      : "H p_{T}",
    #                                                                   "legend"     : 3,
    #                                                                   "color"      : "ROOT.kOrange",
    #                                                                   "drawOptions" : "HIST PC",
    #                                                                   "marker"      : "20",
    #                                                                   "TObject"    : "",
    #                                                                   },
    #                              "acceptance_NWS_NLO_passHCJetPairing_over_all": {"label"      : "#DeltaR_{jj}",
    #                                                                           "legend"     : 2,
    #                                                                           "color"      : "ROOT.kAzure+2",
    #                                                                           "drawOptions" : "HIST PC",
    #                                                                           "marker"      : "20",
    #                                                                           "TObject"    : "",
    #                                                                           },
    #                              "acceptance_NWS_NLO_passHCJetSelection_over_all": {"label"      : "4 b-jets",
    #                                                                             "legend"     : 1,
    #                                                                             "color"      : "ROOT.kMagenta",
    #                                                                             "drawOptions" : "HIST PC",
    #                                                                             "marker"      : "20",
    #                                                                             "TObject"    : "",
    #                                                                             },
    #                              },
    #            }

    # parameters = {"title"      : "",
    #               "status"     : "Simulation "+status,
    #               "yTitle"     : "Acceptance #times Efficiency",
    #               "xTitle"     : "m,Scalar [GeV]",
    #               "xTitleOffset": 0.95,
    #               "legendTextSize":0.04,
    #               "canvasSize" : [600,500],
    #               "rMargin"    : 0.05,
    #               "lMargin"    : 0.12,
    #               "yTitleOffset": 1.1,
    #               "lumi"       : [o.year,lumi],
    #               "rebin"      : 1, 
    #               "yMin"       : 0,
    #               "yMax"       : 0.23,
    #               "xleg"       : [0.15,0.43],
    #               "yleg"       : [0.49,0.86],
    #               "labelSize"  : 16,
    #               "xatlas"     : 0.34,
    #               "yatlas"     : 0.875,
    #               "xlumi"      : 0.57,
    #               "ylumi"      : 0.82,
    #               "satlas"     : 0.05,
    #               "statusOffset": 0.15,
    #               "logY"       : False,
    #               #"ratio"      : False,
    #               "outputDir"  : outDir,
    #               "outputName" : "absoluteAcceptance_NWS_NLO",
    #               }
    
    # plot(samples,parameters)

    samples = {files["trigger"]:{# "acceptance_SMNR_MhhWeight_passSignal_HLT_over_all": {"label"      : "Trigger",
                                 #                                            "legend"     : 7,
                                 #                                            "color"      : "ROOT.kBlack",
                                 #                                            "drawOptions" : "HIST P",
                                 #                                            "marker"      : "20",
                                 #                                            "TObject"    : "",
                                 #                                            },
                                 "acceptance_SMNR_MhhWeight_passSignal_over_all": {"label"      : "X_{Wt}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST P",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_SMNR_MhhWeight_passSignalBeforeAllhadVeto_over_all": {"label"      : "X_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST P",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_SMNR_MhhWeight_passHCdEta_over_all": {"label"      : "#Delta#eta_{HH}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST P",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_SMNR_MhhWeight_passHCPt_over_all": {"label"      : "H p_{T}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST P",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_SMNR_MhhWeight_passHCJetPairing_over_all": {"label"      : "#DeltaR_{jj}",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST P",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 "acceptance_SMNR_MhhWeight_passHCJetSelection_over_all": {"label"      : "4 b-jets",
                                                                                "legend"     : 1,
                                                                                "color"      : "ROOT.kMagenta",
                                                                                "drawOptions" : "HIST P",
                                                                                "marker"      : "20",
                                                                                "TObject"    : "",
                                                                                },
                                 },
               }


    parameters = {"title"      : "",
                  #"status"     : "Simulation",
                  "yTitle"     : "",
                  "yTickLength": 0.1,
                  "xTitle"     : "",
                  "xTitleOffset": 1,
                  "legendTextSize":0.04,
                  "canvasSize" : [125,500],
                  "rMargin"    : 0.08,
                  "lMargin"    : 0.4,
                  "yTitleOffset": 2,
                  #"lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 0.06,
                  "xleg"       : [2,2],
                  "yleg"       : [1,1],
                  "labelSize"  : 18,
                  "xatlas"     : 0.455,
                  "yatlas"     : 0.92,
                  "atlasSize"  : 12,
                  "statusSize" : 12,
                  "satlas"     : 0.025,
                  "smallStatus": "Simulation "+status,
                  "statusOffset": 10,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "absoluteAcceptance_SMNR",
                  }
    
    plot(samples,parameters)

    samples = {files["trigger"]:{"acceptance_SMNR_MhhWeight_passSignal_HLT_over_passSignal": {"label"      : "Trigger / X_{Wt}",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST P",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_SMNR_MhhWeight_passSignal_over_passSignalBeforeAllhadVeto": {"label"      : "X_{Wt} / X_{HH}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST P",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_SMNR_MhhWeight_passSignalBeforeAllhadVeto_over_passHCdEta": {"label"      : "X_{HH} / #Delta#eta_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST P",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_SMNR_MhhWeight_passHCdEta_over_passHCPt": {"label"      : "#Delta#eta_{HH} / H p_{T}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST P",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_SMNR_MhhWeight_passHCPt_over_passHCJetPairing": {"label"      : "H p_{T} / #DeltaR_{jj}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST P",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_SMNR_MhhWeight_passHCJetPairing_over_passHCJetSelection": {"label"      : "#DeltaR_{jj} / 4 b-jets",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST P",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 },
               }

    parameters = {"title"      : "",
                  "atlas"      : "Thesis",                  
                  "status"     : "Simulation",
                  "yTitle"     : "",
                  "yTickLength": 0.1,
                  "xTitle"     : "",
                  "xTitleOffset": 1,
                  "legendTextSize":0.04,
                  "canvasSize" : [125,500],
                  "rMargin"    : 0.08,
                  "lMargin"    : 0.4,
                  "yTitleOffset": 2,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0.4,
                  "yMax"       : 1,
                  "xleg"       : [2,2],
                  "yleg"       : [1,1],
                  "labelSize"  : 18,
                  "xatlas"     : 2.4,
                  "yatlas"     : 0.8,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "relativeAcceptance_SMNR",
                  }
    
    plot(samples,parameters)

    # samples = {files["trigger"]:{"acceptance_ttbar_passSignal_HLT_over_all": {"label"      : "Trigger",
    #                                                                         "legend"     : 7,
    #                                                                         "color"      : "ROOT.kBlack",
    #                                                                         "drawOptions" : "HIST P0",
    #                                                                         "marker"      : "20",
    #                                                                         "TObject"    : "",
    #                                                                         },
    #                              "acceptance_ttbar_passSignal_over_all": {"label"      : "X_{Wt}",
    #                                                                     "legend"     : 6,
    #                                                                     "color"      : "ROOT.kBlue",
    #                                                                     "marker"      : "20",
    #                                                                     "drawOptions" : "HIST P0",
    #                                                                     "TObject"    : "",
    #                                                                     },
    #                              "acceptance_ttbar_passSignalBeforeAllhadVeto_over_all": {"label"      : "X_{HH}",
    #                                                                                     "legend"     : 5,
    #                                                                                     "color"      : "ROOT.kGreen",
    #                                                                                     "drawOptions" : "HIST P0",
    #                                                                                     "marker"      : "20",
    #                                                                                     "TObject"    : "",
    #                                                                                     },
    #                              "acceptance_ttbar_passHCdEta_over_all": {"label"      : "#Delta#eta_{HH}",
    #                                                                     "legend"     : 4,
    #                                                                     "color"      : "ROOT.kRed",
    #                                                                     "drawOptions" : "HIST P0",
    #                                                                     "marker"      : "20",
    #                                                                     "TObject"    : "",
    #                                                                     },
    #                              "acceptance_ttbar_passHCPt_over_all": {"label"      : "H p_{T}",
    #                                                                   "legend"     : 3,
    #                                                                   "color"      : "ROOT.kOrange",
    #                                                                   "drawOptions" : "HIST P0",
    #                                                                   "marker"      : "20",
    #                                                                   "TObject"    : "",
    #                                                                   },
    #                              "acceptance_ttbar_passHCJetPairing_over_all": {"label"      : "#DeltaR_{jj}",
    #                                                                           "legend"     : 2,
    #                                                                           "color"      : "ROOT.kAzure+2",
    #                                                                           "drawOptions" : "HIST P0",
    #                                                                           "marker"      : "20",
    #                                                                           "TObject"    : "",
    #                                                                           },
    #                              "acceptance_ttbar_passHCJetSelection_over_all": {"label"      : "4 b-jets",
    #                                                                             "legend"     : 1,
    #                                                                             "color"      : "ROOT.kMagenta",
    #                                                                             "drawOptions" : "HIST P0",
    #                                                                             "marker"      : "20",
    #                                                                             "TObject"    : "",
    #                                                                             },
    #                              },
    #            }


    # parameters = {"title"      : "",
    #               "status"     : "Simulation",
    #               "yTitle"     : "",
    #               "yTickLength": 0.1,
    #               "xTitle"     : "",
    #               "xTitleOffset": 1,
    #               "legendTextSize":0.04,
    #               "canvasSize" : [200,500],
    #               "rMargin"    : 0.08,
    #               "lMargin"    : 0.4,
    #               "yTitleOffset": 2,
    #               "lumi"       : [o.year,lumi],
    #               "rebin"      : 1, 
    #               "yMin"       : 0,
    #               "yMax"       : 0.0005,
    #               "xleg"       : [2,2],
    #               "yleg"       : [1,1],
    #               "labelSize"  : 18,
    #               "xatlas"     : 2.4,
    #               "yatlas"     : 0.8,
    #               "logY"       : False,
    #               "maxDigits"   : 3,
    #               #"ratio"      : False,
    #               "outputDir"  : outDir,
    #               "outputName" : "absoluteAcceptance_ttbar",
    #               }
    
    # plot(samples,parameters)
    samples = {files["trigger"]:{"acceptance_allhad_passSignal_HLT_over_all": {"label"      : "Trigger",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST P",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_allhad_passSignal_over_all": {"label"      : "X_{Wt}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST P",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_allhad_passSignalBeforeAllhadVeto_over_all": {"label"      : "X_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST P",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_allhad_passHCdEta_over_all": {"label"      : "#Delta#eta_{HH}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST P",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_allhad_passHCPt_over_all": {"label"      : "H p_{T}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST P",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_allhad_passHCJetPairing_over_all": {"label"      : "#DeltaR_{jj}",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST P",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 "acceptance_allhad_passHCJetSelection_over_all": {"label"      : "4 b-jets",
                                                                                "legend"     : 1,
                                                                                "color"      : "ROOT.kMagenta",
                                                                                "drawOptions" : "HIST P",
                                                                                "marker"      : "20",
                                                                                "TObject"    : "",
                                                                                },
                                 },
               }


    parameters = {"title"      : "",
                  "status"     : "Simulation",
                  "yTitle"     : "",
                  "yTickLength": 0.1,
                  "xTitle"     : "",
                  "xTitleOffset": 1,
                  "legendTextSize":0.04,
                  "canvasSize" : [125,500],
                  "rMargin"    : 0.14,
                  "lMargin"    : 0.34,
                  "yTitleOffset": 2,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 0.0005,
                  "xleg"       : [2,2],
                  "yleg"       : [1,1],
                  "labelSize"  : 15,
                  "xatlas"     : 2.4,
                  "yatlas"     : 0.8,
                  "logY"       : False,
                  "maxDigits"   : 3,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "absoluteAcceptance_allhad",
                  }
    
    plot(samples,parameters)

    samples = {files["trigger"]:{"acceptance_nonallhad_passSignal_HLT_over_all": {"label"      : "Trigger",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST P",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_nonallhad_passSignal_over_all": {"label"      : "X_{Wt}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST P",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_nonallhad_passSignalBeforeAllhadVeto_over_all": {"label"      : "X_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST P",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_nonallhad_passHCdEta_over_all": {"label"      : "#Delta#eta_{HH}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST P",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_nonallhad_passHCPt_over_all": {"label"      : "H p_{T}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST P",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_nonallhad_passHCJetPairing_over_all": {"label"      : "#DeltaR_{jj}",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST P",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 "acceptance_nonallhad_passHCJetSelection_over_all": {"label"      : "4 b-jets",
                                                                                "legend"     : 1,
                                                                                "color"      : "ROOT.kMagenta",
                                                                                "drawOptions" : "HIST P",
                                                                                "marker"      : "20",
                                                                                "TObject"    : "",
                                                                                },
                                 },
               }


    parameters = {"title"      : "",
                  "status"     : "Simulation",
                  "yTitle"     : "",
                  "yTickLength": 0.1,
                  "xTitle"     : "",
                  "xTitleOffset": 1,
                  "legendTextSize":0.04,
                  "canvasSize" : [125,500],
                  "rMargin"    : 0.14,
                  "lMargin"    : 0.34,
                  "yTitleOffset": 2,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 0.0005,
                  "xleg"       : [2,2],
                  "yleg"       : [1,1],
                  "labelSize"  : 15,
                  "xatlas"     : 2.4,
                  "yatlas"     : 0.8,
                  "logY"       : False,
                  "maxDigits"   : 3,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "absoluteAcceptance_nonallhad",
                  }
    
    plot(samples,parameters)

    samples = {files["trigger"]:{"acceptance_allhad_passSignal_HLT_over_passSignal": {"label"      : "Trigger / X_{Wt}",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST P",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_allhad_passSignal_over_passSignalBeforeAllhadVeto": {"label"      : "X_{Wt} / X_{HH}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST P",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_allhad_passSignalBeforeAllhadVeto_over_passHCdEta": {"label"      : "X_{HH} / #Delta#eta_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST P",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_allhad_passHCdEta_over_passHCPt": {"label"      : "#Delta#eta_{HH} / H p_{T}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST P",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_allhad_passHCPt_over_passHCJetPairing": {"label"      : "H p_{T} / #DeltaR_{jj}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST P",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_allhad_passHCJetPairing_over_passHCJetSelection": {"label"      : "#DeltaR_{jj} / 4 b-jets",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST P",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 },
               }

    parameters = {"title"      : "",
                  "status"     : "Simulation",
                  "yTitle"     : "",
                  "yTickLength": 0.1,
                  "xTitle"     : "",
                  "xTitleOffset": 1,
                  "legendTextSize":0.04,
                  "canvasSize" : [125,500],
                  "rMargin"    : 0.14,
                  "lMargin"    : 0.34,
                  "yTitleOffset": 2,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1,
                  "xleg"       : [2,2],
                  "yleg"       : [1,1],
                  "labelSize"  : 15,
                  "xatlas"     : 2.4,
                  "yatlas"     : 0.8,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "relativeAcceptance_allhad",
                  }
    
    plot(samples,parameters)

    samples = {files["trigger"]:{"acceptance_nonallhad_passSignal_HLT_over_passSignal": {"label"      : "Trigger / X_{Wt}",
                                                                            "legend"     : 7,
                                                                            "color"      : "ROOT.kBlack",
                                                                            "drawOptions" : "HIST P",
                                                                            "marker"      : "20",
                                                                            "TObject"    : "",
                                                                            },
                                 "acceptance_nonallhad_passSignal_over_passSignalBeforeAllhadVeto": {"label"      : "X_{Wt} / X_{HH}",
                                                                        "legend"     : 6,
                                                                        "color"      : "ROOT.kBlue",
                                                                        "marker"      : "20",
                                                                        "drawOptions" : "HIST P",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_nonallhad_passSignalBeforeAllhadVeto_over_passHCdEta": {"label"      : "X_{HH} / #Delta#eta_{HH}",
                                                                                        "legend"     : 5,
                                                                                        "color"      : "ROOT.kGreen",
                                                                                        "drawOptions" : "HIST P",
                                                                                        "marker"      : "20",
                                                                                        "TObject"    : "",
                                                                                        },
                                 "acceptance_nonallhad_passHCdEta_over_passHCPt": {"label"      : "#Delta#eta_{HH} / H p_{T}",
                                                                        "legend"     : 4,
                                                                        "color"      : "ROOT.kRed",
                                                                        "drawOptions" : "HIST P",
                                                                        "marker"      : "20",
                                                                        "TObject"    : "",
                                                                        },
                                 "acceptance_nonallhad_passHCPt_over_passHCJetPairing": {"label"      : "H p_{T} / #DeltaR_{jj}",
                                                                      "legend"     : 3,
                                                                      "color"      : "ROOT.kOrange",
                                                                      "drawOptions" : "HIST P",
                                                                      "marker"      : "20",
                                                                      "TObject"    : "",
                                                                      },
                                 "acceptance_nonallhad_passHCJetPairing_over_passHCJetSelection": {"label"      : "#DeltaR_{jj} / 4 b-jets",
                                                                              "legend"     : 2,
                                                                              "color"      : "ROOT.kAzure+2",
                                                                              "drawOptions" : "HIST P",
                                                                              "marker"      : "20",
                                                                              "TObject"    : "",
                                                                              },
                                 },
               }

    parameters = {"title"      : "",
                  "status"     : "Simulation",
                  "yTitle"     : "",
                  "yTickLength": 0.1,
                  "xTitle"     : "",
                  "xTitleOffset": 1,
                  "legendTextSize":0.04,
                  "canvasSize" : [125,500],
                  "rMargin"    : 0.14,
                  "lMargin"    : 0.34,
                  "yTitleOffset": 2,
                  "lumi"       : [o.year,lumi],
                  "rebin"      : 1, 
                  "yMin"       : 0,
                  "yMax"       : 1,
                  "xleg"       : [2,2],
                  "yleg"       : [1,1],
                  "labelSize"  : 15,
                  "xatlas"     : 2.4,
                  "yatlas"     : 0.8,
                  "logY"       : False,
                  #"ratio"      : False,
                  "outputDir"  : outDir,
                  "outputName" : "relativeAcceptance_nonallhad",
                  }
    
    plot(samples,parameters)

        # samples = {files[o.year]["trigger"]:{"SMNR_MhhWeight_"+cutflow+"_Acceptance_numer_Xhh_passHLT_over_all": {"label"      : "Trigger",
        #                                                                                                     "legend"     : 5,
        #                                                                                                     "color"      : "ROOT.kBlack",
        #                                                                                                     "drawOptions" : "HIST P",
        #                                                                                                     "marker"      : "24",
        #                                                                                                     "TObject"    : "",
        #                                                                                                     },
        #                                      "SMNR_MhhWeight_"+cutflow+"_Acceptance_numer_Xhh_over_all": {"label"      : "X_{HH}",
        #                                                                                             "legend"     : 4,
        #                                                                                             "color"      : "ROOT.kBlue",
        #                                                                                             "marker"      : "26",
        #                                                                                             "drawOptions" : "HIST P",
        #                                                                                             "TObject"    : "",
        #                                                                                             },
        #                                      "SMNR_MhhWeight_"+cutflow+"_Acceptance_numer_PassHCdR_over_all": {"label"      : "m_{4j} Dependent Cuts, #DeltaR_{hh}",
        #                                                                                                  "legend"     : 3,
        #                                                                                                  "color"      : "ROOT.kGreen",
        #                                                                                                  "drawOptions" : "HIST P",
        #                                                                                                  "marker"      : "25",
        #                                                                                                  "TObject"    : "",
        #                                                                                                  },
        #                                      "SMNR_MhhWeight_"+cutflow+"_Acceptance_numer_PassHCdRjj_over_all": {"label"      : "#DeltaR_{jj}",
        #                                                                                                  "legend"     : 2,
        #                                                                                                  "color"      : "ROOT.kRed",
        #                                                                                                  "drawOptions" : "HIST P",
        #                                                                                                  "marker"      : "25",
        #                                                                                                  "TObject"    : "",
        #                                                                                                  },
        #                                      "SMNR_MhhWeight_"+cutflow+"_Acceptance_numer_nBJets_over_all": {"label"      : "4 b-tagged jets",
        #                                                                                                "legend"     : 1,
        #                                                                                                "color"      : "ROOT.kOrange",
        #                                                                                                "drawOptions" : "HIST P",
        #                                                                                                "marker"      : "24",
        #                                                                                                "TObject"    : "",
        #                                                                                                },
        #                                      },
        #            }

        # parameters = {"title"      : "",
        #               "yTitle"     : "",
        #               "yTickLength": 0.1,
        #               "xTitle"     : "",
        #               "xTitleOffset": 1,
        #               "legendTextSize":0.03,
        #               "canvasSize" : [125,500],
        #               "rMargin"    : 0.08,
        #               "lMargin"    : 0.4,
        #               "yTitleOffset": 2,
        #               "lumi"       : [o.year,lumi],
        #               "rebin"      : 1, 
        #               "yMin"       : 0,
        #               "yMax"       : 0.08,
        #               "xleg"       : [2,2],
        #               "yleg"       : [1,1],
        #               "labelSize"  : 18,
        #               "xatlas"     : 2.4,
        #               "yatlas"     : 0.8,
        #               "logY"       : False,
        #               #"ratio"      : False,
        #               "outputDir"  : outDir+"/acceptance/"+cutflow+"/",
        #               "outputName" : "absoluteAcceptance_SMNR_MhhWeight_simple",
        #               }
    
        # plot(samples,parameters)

varLabels = {
             "m4j_cor_v"              : "m_{4j} (corrected) [GeV]",
             }
if o.doSyst:
    for dirName in ["PassAllhadVeto"]:
        for region in ["Signal"]:
            for var in varLabels:
                for sample in ["SMNR_MhhWeight"]:
                    for i in range(5):
                        samples = {files[sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sample,
                                                                                       "legend"   : 1,
                                                                                       "isData"   : True,
                                                                                       #"normalize": 1,
                                                                                       "ratio"    : "denom A",
                                                                                       "color"    : "ROOT.kBlack",
                                                                                       "TObject"  : "",
                                                                                       },
                                                  dirName+"_FourTag_"+region+"/"+var+"_bSF"+str(2*i+2): {"label"    : sample+" B"+str(i)+" Up",
                                                                                                         "legend"   : 2,
                                                                                                         "ratio"    : "numer A",
                                                                                                         #"normalize": 1,
                                                                                                         "color"    : "ROOT.kRed",
                                                                                                         "TObject"  : "",
                                                                                                         },
                                                  dirName+"_FourTag_"+region+"/"+var+"_bSF"+str(2*i+1): {"label"    : sample+" B"+str(i)+" Down",
                                                                                                         "legend"   : 3,
                                                                                                         "ratio"    : "numer A",
                                                                                                         #"normalize": 1,
                                                                                                         "color"    : "ROOT.kBlue",
                                                                                                         "TObject"  : "",
                                                                                                         },
                                                  },
                                   }
                
                        parameters = {"ratio"     : True,
                                      "status"     : "Simulation",
                                      "rTitle"    : "Syst./Nom.",
                                      "yTitle"    : "Events / Bin",
                                      "xTitle"    : varLabels[var],
                                      "title"     : "",
                                      "lumi"      : [o.year,lumi],
                                      "region"    : region if region != "FullMassPlane" else "",
                                      "outputDir" : outDir+dirName+"/"+sample+"/"+region+"/",
                                      "outputName": var+"_bSF_B"+str(i),
                                      "rebin"     : 1,
                                      #"chi2"      : True,
                                      }
                
                        plot(samples,parameters)
                        # parameters["logY"] = True
                        # parameters["outputName"] = parameters["outputName"]+"_logy"
                        # plot(samples,parameters)    

                    samples = {files[sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sample,
                                                                                   "legend"   : 1,
                                                                                   "isData"   : True,
                                                                                   #"normalize": 1,
                                                                                   "ratio"    : "denom A",
                                                                                   "color"    : "ROOT.kBlack",
                                                                                   "TObject"  : "",
                                                                                   },
                                                  dirName+"_FourTag_"+region+"/"+var+"_bSF48"  : {"label"    : sample+" FT EFF extrap. Up",
                                                                                                  "legend"   : 2,
                                                                                                  "ratio"    : "numer A",
                                                                                                  #"normalize": 1,
                                                                                                  "color"    : "ROOT.kRed",
                                                                                                  "TObject"  : "",
                                                                                                  },
                                                  dirName+"_FourTag_"+region+"/"+var+"_bSF47": {"label"    : sample+" FT EFF extrap. Down",
                                                                                                "legend"   : 3,
                                                                                                "ratio"    : "numer A",
                                                                                                #"normalize": 1,
                                                                                                "color"    : "ROOT.kBlue",
                                                                                                "TObject"  : "",
                                                                                                },
                                                  },
                                   }
                
                    parameters = {"ratio"     : True,
                                  "status"     : "Simulation",
                                  "rTitle"    : "Syst./Nom.",
                                  "yTitle"    : "Events / Bin",
                                  "xTitle"    : varLabels[var],
                                  "title"     : "",
                                  "lumi"      : [o.year,lumi],
                                  "region"    : region if region != "FullMassPlane" else "",
                                  "outputDir" : outDir+dirName+"/"+sample+"/"+region+"/",
                                  "outputName": var+"_B_FT_EFF_extrap",
                                  "rebin"     : 1,
                                  #"chi2"      : True,
                                  }
                
                    plot(samples,parameters)

                    samples = {files[sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sample,
                                                                                   "legend"   : 1,
                                                                                   "isData"   : True,
                                                                                   #"normalize": 1,
                                                                                   "ratio"    : "denom A",
                                                                                   "color"    : "ROOT.kBlack",
                                                                                   "TObject"  : "",
                                                                                   },
                                                  dirName+"_FourTag_"+region+"/"+var+"_tSF_up"  : {"label"    : sample+" trig SF Up",
                                                                                                   "legend"   : 2,
                                                                                                   "ratio"    : "numer A",
                                                                                                   #"normalize": 1,
                                                                                                   "color"    : "ROOT.kRed",
                                                                                                   "TObject"  : "",
                                                                                                   },
                                                  dirName+"_FourTag_"+region+"/"+var+"_tSF_down": {"label"    : sample+" trig SF Down",
                                                                                                   "legend"   : 3,
                                                                                                   "ratio"    : "numer A",
                                                                                                   #"normalize": 1,
                                                                                                   "color"    : "ROOT.kBlue",
                                                                                                   "TObject"  : "",
                                                                                                   },
                                                  },
                                   }
                
                    parameters = {"ratio"     : True,
                                  "status"     : "Simulation",
                                  "rTitle"    : "Syst / Nom",
                                  "yTitle"    : "Events / Bin",
                                  "xTitle"    : varLabels[var],
                                  "title"     : "",
                                  "lumi"      : [o.year,lumi],
                                  "region"    : region if region != "FullMassPlane" else "",
                                  "outputDir" : outDir+dirName+"/"+sample+"/"+region+"/",
                                  "outputName": var+"_tSF",
                                  "rebin"     : 1,
                                  #"chi2"      : True,
                                  }
                
                    plot(samples,parameters)

                    for NP in NPs:
                        if "1down" in NP: continue
                        samples = {files[sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sample,
                                                                                       "legend"   : 1,
                                                                                       "isData"   : True,
                                                                                       #"normalize": 1,
                                                                                       "ratio"    : "denom A",
                                                                                       "color"    : "ROOT.kBlack",
                                                                                       "TObject"  : "",
                                                                                       },
                                                  },
                                   filesNPs[NP][sample]:{dirName+"_FourTag_"+region+"/"+var: {"label"    : sample+" "+NPNames[NP],
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
                            samples[filesNPs[NPdown][sample]] = {dirName+"_FourTag_"+region+"/"+var: {"label"    : sample+" "+NPNames[NPdown],
                                                                                                      "legend"   : 3,
                                                                                                      "ratio"    : "numer A",
                                                                                                      #"normalize": 1,
                                                                                                      "color"    : "ROOT.kBlue",
                                                                                                      "TObject"  : "",
                                                                                                      },
                                                                 }
                
                        parameters = {"ratio"     : True,
                                      "rTitle"    : "Syst / Nom",
                                      "yTitle"    : "Events / Bin",
                                      "xTitle"    : varLabels[var],
                                      "title"     : "",
                                      "lumi"      : [o.year,lumi],
                                      "region"    : region if region != "FullMassPlane" else "",
                                      "outputDir" : outDir+dirName+"/"+sample+"/"+region+"/",
                                      "outputName": var+"_"+NP.replace("__1up",""),
                                      "rebin"     : 1,
                                      #"chi2"      : True,
                                      }

                        plot(samples,parameters)
