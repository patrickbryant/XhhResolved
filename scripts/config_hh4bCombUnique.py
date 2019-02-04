import ROOT
from xAH_config import xAH_config
import sys
sys.path.insert(0, 'XhhResolved/plotting/')
from plotTools import read_mu_qcd_file

import shlex
import argparse

parser = argparse.ArgumentParser(description='Test for extra options')
parser.add_argument('--tagger',    dest="tagger",    default="MV2c20")
parser.add_argument('--emu',       dest='emulate',   action="store_true", default=False)
parser.add_argument('--year',      dest="year",      default="2015")
parser.add_argument('--iteration', dest="iteration", default="0")
parser.add_argument('--variation', dest="variation", default="")
parser.add_argument('--ttbarVariation', dest="ttbarVariation", default="")
parser.add_argument('--ttbarVariationCombName', dest="ttbarVariationCombName", default="")
parser.add_argument('--weights',   dest="weights",   default="")
parser.add_argument('--lumiSF',    dest="lumiSF",    default=1.0)
parser.add_argument('--scale2b',   dest="scale2b",   default=1.0)
parser.add_argument('--scale4b',   dest="scale4b",   default=1.0)
#parser.add_argument('--ttbar',     dest="ttbar",     action="store_true", default=False)
parser.add_argument('--allhad',     dest="allhad",     action="store_true", default=False)
parser.add_argument('--nonallhad',     dest="nonallhad",     action="store_true", default=False)
parser.add_argument('--noMCNorm',  dest="doMCNorm",  action="store_false", default=True)
parser.add_argument('--useMhhWeight',  dest="useMhhWeight",  action="store_true", default=False)
parser.add_argument('--hhReweightFile',  dest="hhReweightFile",  default="$ROOTCOREBIN/data/hhTruthWeightTools/SMhh_mhh_ReWeight.root")
parser.add_argument('--uselhhWeight',  dest="uselhhWeight",  action="store_true", default=False)
parser.add_argument('--signal',     dest="signal",     action="store_true", default=False)
parser.add_argument('--doTrigSF',   dest="doTrigSF",     action="store_true", default=False)
parser.add_argument('--doBTagSF',   dest="doBTagSF",     action="store_true", default=False)
parser.add_argument('--threeTag',  dest="threeTag",  action="store_true", default=False)
parser.add_argument('--debug',     dest="debug",     action="store_true", default=False)
parser.add_argument('--fast',     dest="fast",     action="store_true", default=False)# only run critical hists for reweighting to speed up derivation of weights
parser.add_argument('--promoteMuons',   dest="promoteMuons",     action="store_true", default=False)

o = parser.parse_args(shlex.split(args.extra_options))
c = xAH_config()

blind = False
doJetCategories=False
doTrigEmulation=True
import sys, os
XhhDir = os.path.dirname(os.path.realpath("__file__"))
sys.path.insert(0,XhhDir+"/XhhResolved/scripts")

from setupConfig import setGRL, setLumi, setRegions, setTagger
(MV2CutValue, MV2CutValueQCD) = setTagger(o.tagger)
GRL  = setGRL(o.year)
lumi = setLumi(o.year)

print("LumiSF is",float(o.lumiSF))
print("Lumi is",lumi)
lumi = lumi*float(o.lumiSF)

scale2b = float(o.scale2b)
scale4b = float(o.scale4b)

(leadMass_SR, sublMass_SR, radius_SR, radius_CR, radius_SB, inner_SB, CR_shift, SB_shift, doTightQCDTag, doLooseQCDTag, leadHCmassCut, sublHCmassCut, DhhCut) = setRegions(o.variation)

#
#  Data Config
#
if not args.is_MC:
    applyGRL           = True

#
#  MC Config
#
else:
    applyGRL           = False

iteration = int(o.iteration)
if   iteration == 0: m_weightsFile = ""
else: m_weightsFile = "$ROOTCOREBIN/data/XhhResolved/weights2bto"+("3" if o.threeTag else "4")+"b_"+o.weights+"_"+o.year+"_"+o.variation+"_"+str(iteration)+".root"

m_singleTagProb = 1
if not o.signal and not o.promoteMuons:
    singleTagProbDict = read_mu_qcd_file("XhhResolved/data/singleTagProb_FourTag_"+o.weights+"_"+o.year+"_"+o.variation+"_"+o.iteration+".txt")
    m_singleTagProb = singleTagProbDict["singleTagProb_qcd_PassHCdEta"]

if o.year == "2016":
    #if o.allhad: m_singleTagProb = 0.03313746619 #ntuple 02-03-02
    if o.allhad: m_singleTagProb = 0.03972047306 #ntuple 02-03-04

if o.year == "2015":
    #if o.allhad: m_singleTagProb = 0.03011344277 #ntuple 02-03-02
    if o.allhad: m_singleTagProb = 0.0422378966 #ntuple 02-03-04


#
# Build the Event Data
#
c.setalg("hh4bEventBuilder", { "m_name"                   : "hhEventBuilder",
                               "m_debug"                  : o.debug,
                               "m_tagger"                 : o.tagger,
                               "m_MV2CutValue"            : MV2CutValue,
                               "m_MV2CutValueTightQCD"    : MV2CutValueQCD,
                               "m_minJetPtCut"            : 40,
                               "m_useWeighted"            : args.is_MC,
                               "m_useMhhWeight"           : o.useMhhWeight,
                               "m_doPUReweight"           : False,
                               "m_hhReweightFile"         : o.hhReweightFile,
                               #"m_doKinematicWeights"     : True if iteration else False,
                               "m_lumi"                   : lumi, #in pb^-1
                               "m_eventDetailStr"         : "pileup",
                               "m_triggerDetailStr"       : "passTriggers",
                               "m_jetDetailStr"           : "kinematic clean flavorTag sfFTagFix70 JVC",# + (" truth truth_details" if args.is_MC else ""),
                               #"m_jetDetailStr"           : "kinematic clean flavorTag sfFTagFix70 JVC",# + (" truth truth_details" if args.is_MC else ""),
                               "m_muonDetailStr"          : "kinematic quality energyLoss isolation",
                               "m_elecDetailStr"          : "kinematic quality PID isolation",
                               "m_metDetailStr"           : "",
                               "m_truthDetailStr"         : "kinematic",
                               #"m_truthDetailStr"         : "kinematic",
                               "m_applyGRL"               : applyGRL,
                               "m_mc"                     : args.is_MC,
                               "m_GRLxml"                 : GRL,
                               "m_doMCNorm"               : o.doMCNorm,
                               "m_promoteMuons"           : o.promoteMuons,
                               } )

#
# Build 2tag higgs cands
#
if not o.promoteMuons:
    c.setalg("hCandBuilderQCDUnique", { "m_name"                   : "hCandBuilderQCD",
                                        "m_combName"               : "QCD",
                                        "m_minTagJets"             : 2,
                                        "m_maxTagJets"             : 2,
                                        "m_minTotalJets"           : 4,
                                        "m_singleTagProb"          : m_singleTagProb,
                                        "m_debug"                  : o.debug,
                                        "m_year"                   : o.year,
                                        "m_radius_SR"              : radius_SR,
                                        "m_radius_CR"              : radius_CR,
                                        "m_radius_SB"              : radius_SB,
                                        "m_CR_shift"               : CR_shift,
                                        "m_SB_shift"               : SB_shift,
                                        "m_leadMass_SR"            : leadMass_SR,
                                        "m_sublMass_SR"            : sublMass_SR,
                                        "m_mc"                     : args.is_MC,
                                        "m_doTrigEmulation"        : doTrigEmulation,
                                        } )


if not o.threeTag:
    #
    # Build 4b higgs cands
    #
    c.setalg("hCandBuilderMVSort", { "m_name"                   : "hCandBuilder4b",
                                     "m_combName"               : "4b",
                                     "m_minTagJets"             : 4,
                                     "m_debug"                  : o.debug,
                                     "m_year"                   : o.year,
                                     "m_radius_SR"              : radius_SR,
                                     "m_radius_CR"              : radius_CR,
                                     "m_radius_SB"              : radius_SB,
                                     "m_CR_shift"               : CR_shift,
                                     "m_SB_shift"               : SB_shift,
                                     "m_leadMass_SR"            : leadMass_SR,
                                     "m_sublMass_SR"            : sublMass_SR,
                                     "m_mc"                     : args.is_MC,
                                     "m_doTrigEmulation"        : doTrigEmulation,
                                     "m_useTrigSF"              : o.doTrigSF,
                                     "m_promoteMuons"           : o.promoteMuons,
                                     } )

else:
    #
    # Build 3b higgs cands
    #
    c.setalg("hCandBuilderMVSort", { "m_name"                   : "hCandBuilder3b",
                                     "m_combName"               : "3b",
                                     "m_minTagJets"             : 3,
                                     "m_maxTagJets"             : 3,
                                     "m_debug"                  : o.debug,
                                     "m_year"                   : o.year,
                                     "m_radius_SR"              : radius_SR,
                                     "m_radius_CR"              : radius_CR,
                                     "m_radius_SB"              : radius_SB,
                                     "m_CR_shift"               : CR_shift,
                                     "m_SB_shift"               : SB_shift,
                                     "m_leadMass_SR"            : leadMass_SR,
                                     "m_sublMass_SR"            : sublMass_SR,
                                     "m_mc"                     : args.is_MC,
                                     "m_doTrigEmulation"        : doTrigEmulation,
                                     "m_useTrigSF"              : False,
                                     } )


c.setalg("topCandBuilder", { "m_name"                   : "topCandBuilder",
                             "m_combName"               : "4b",
                             "m_debug"                  : o.debug,
                             } )

if not o.promoteMuons:
    c.setalg("topCandBuilder", { "m_name"                   : "topCandBuilderQCD",
                                 "m_combName"               : "QCD",
                                 "m_debug"                  : o.debug,
                                 } )

#artificial ttbar reweight to account for possible ttbar mismodeling 
if o.ttbarVariation and o.ttbarVariation:
    c.setalg("ttbarVariation", { "m_name"                  : "Reweight_ttbar",
                                 "m_combName"              : o.ttbarVariationCombName,
                                 "m_weightsFile"           : "$ROOTCOREBIN/data/XhhResolved/ttbar_variations.root",
                                 "m_variation"             : o.ttbarVariation,
                                 "m_doKinematicWeights"    : True,
                                 "m_debug"                 : o.debug,
                                 } )

# c.setalg("topCandBuilderKLFitter", { "m_name"                   : "topCandBuilderKLFitter",
#                                      "m_combName"               : "4b",
#                                      "m_debug"                  : o.debug,
#                                      } )

#c.setalg("topCandBuilderKLFitter", { "m_name"                   : "topCandBuilderKLFitterQCD",
#                                     "m_combName"               : "QCD",
#                                     "m_debug"                  : o.debug,
#                                     } )




# c.setalg("topCandBuilder", { "m_name"                   : "topCandBuilderQCDTight",
#                              "m_combName"               : "QCDTight",
#                              "m_debug"                  : False,
#                              } )



#
# Reweight
#
if iteration:
    #weightBaseName = "$ROOTCOREBIN/data/XhhResolved/weights2bto4bStudyHCandAlgos"+o.year+"_"+o.variation+"_TWOTAGNAME_iter"+str(iteration)+".root"
    
    c.setalg("hh4bReweightAlgo", { "m_name"                  : "Reweight_TwoTag",
                                   "m_combName"              : "QCD",
                                   #"m_postFix"               : "_TwoTag",    
                                   "m_weightsFile"           : m_weightsFile,
                                   "m_doKinematicWeights"    : True,
                                   "m_debug"                 : o.debug,
                                   "m_MV2CutValue"           : MV2CutValue,
                                   } )

    # c.setalg("hh4bReweightAlgo", { "m_name"                  : "Reweight_TwoTagTight",
    #                                "m_combName"              : "QCDTight",
    #                                "m_postFix"               : "_TwoTagTight",    
    #                                "m_weightsFile"           : weightBaseName.replace("TWOTAGNAME","TwoTagTight"),
    #                                "m_doKinematicWeights"    : True,
    #                                #"m_debug"                 : True,
    #                                } )


if not o.threeTag:
    #
    # Plot 4b Events
    #
    c.setalg("hh4bHistsAlgo", { "m_name"                   : "FourTag",
                                "m_scale"                  : scale4b,
                                "m_combName"               : "4b",
                                "m_debug"                  : o.debug,
                                "m_doBlind"                : blind,
                                "m_mc"                     : args.is_MC,
                                "m_doJetCategories"        : doJetCategories,
                                "m_fast"                   : o.fast,
                                "m_signalHistExtraFlags"   : ("doBTagSF" if o.doBTagSF else "")+(" doReweight" if o.uselhhWeight else ""),
                                } )

else:
    c.setalg("hh4bHistsAlgo", { "m_name"                   : "ThreeTag",
                                "m_combName"               : "3b",
                                "m_debug"                  : o.debug,
                                "m_doBlind"                : blind,
                                "m_mc"                     : args.is_MC,
                                "m_doJetCategories"        : doJetCategories,
                                "m_fast"                   : o.fast,
                                } )


#
# Plot QCD Events
#
if not o.promoteMuons:
    c.setalg("hh4bHistsAlgo", { "m_name"                   : "TwoTag",
                                "m_scale"                  : scale2b,
                                "m_combName"               : "QCD",
                                "m_debug"                  : o.debug,
                                "m_doBlind"                : False,
                                "m_doTagCategories"        : False,
                                "m_doJetCategories"        : doJetCategories,
                                "m_mc"                     : args.is_MC,
                                "m_fast"                   : o.fast,
                                } )


def addRegion(c, postfix, m_trigRequirement, m_minDr, m_mc, m_minMeT=-1000):

    regions = [("FourTag","4b"),("TwoTag","QCD"),("TwoTagTight","QCDTight")]
    
    for r in regions:
        regName  = r[0]
        candName = r[1]
        
        if regName == "FourTag": m_doBlind = True
        else:                    m_doBlind = False

        c.setalg("hh4bHistsAlgo", { "m_name"                   : regName+postfix,
                                    "m_combName"               : candName,
                                    "m_minDr"                  : m_minDr,
                                    "m_doBlind"                : m_doBlind,
                                    "m_trigRequirement"        : m_trigRequirement,
                                    "m_signalHistExtraFlags"   : "",
                                    "m_minMeT"                 : m_minMeT,
                                    #"m_signalHistExtraFlags"   : "doReweight doBTagSF",
                                    "m_mc"                     : m_mc,
                                    } )


#addRegion(c, "",         "", m_minDr=1.5,  m_mc=args.is_MC)
#addRegion(c, "_HighMet", "", m_minDr=1.5,  m_mc=args.is_MC, m_minMeT = 125)



# c.setalg("TriggerEmulationStudy", { "m_name"                   : "TrigStudy",
#                                     "m_combName"               : "4b",
#                                     "m_debug"                  : False,
#                                     } )


#
# Trigger Studies
#
doTrigStudies = False
if doTrigStudies:

    
    if o.year == "2015":
        #trig_2b2j = "HLT_2j35_btight_2j35_L13J25.0ETA23"
        trig_2b2j = "HLT_2j35_btight_2j35_L14J15.0ETA25"
        trig_j2b  = "HLT_j100_2j55_bmedium"
        trig_b    = "HLT_j225_bloose"
        trig_b3j  = "HLT_j70_bmedium_3j70_L14J15.0ETA25"
    else:
        trig_2b2j = "HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25"
        trig_j2b  = "HLT_j100_2j55_bmv2c2060_split"
        trig_b    = "HLT_j225_bmv2c2060_split"
        trig_b3j  = "HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25"
    
    addRegion(c, "_2b2j", trig_2b2j, m_minDr=1.5,  m_mc = args.is_MC)
    addRegion(c, "_j2b",  trig_j2b,  m_minDr=1.5,  m_mc = args.is_MC)
    addRegion(c, "_b",    trig_b,    m_minDr=1.5,  m_mc = args.is_MC)
    addRegion(c, "_b3j",  trig_b3j,  m_minDr=1.5,  m_mc = args.is_MC)
    
    c.setalg("hh4bHistsAlgo", { "m_name"                   : "FourTag_2b2j",
                                "m_trigRequirement"        : trig_2b2j,
                                "m_combName"               : "4b",
                                "m_doBlind"                : blind,
                                "m_mc"                     : args.is_MC,
                                } )
    
    c.setalg("hh4bHistsAlgo", { "m_name"                   : "FourTag_j2b",
                                "m_trigRequirement"        : trig_j2b,
                                "m_combName"               : "4b",
                                "m_doBlind"                : blind,
                                "m_mc"                     : args.is_MC,
                                } )
    
    c.setalg("hh4bHistsAlgo", { "m_name"                   : "FourTag_b",
                                "m_trigRequirement"        : trig_b,
                                "m_combName"               : "4b",
                                "m_doBlind"                : blind,
                                "m_mc"                     : args.is_MC,
                                } )
    
    c.setalg("hh4bHistsAlgo", { "m_name"                   : "FourTag_b3j",
                                "m_trigRequirement"        : trig_b3j,
                                "m_combName"               : "4b",
                                "m_doBlind"                : blind,
                                "m_mc"                     : args.is_MC,
                                } )
    
