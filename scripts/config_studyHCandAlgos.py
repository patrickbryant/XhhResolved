import ROOT
from xAH_config import xAH_config

import shlex
import argparse

parser = argparse.ArgumentParser(description='Test for extra options')
parser.add_argument('--tagger',    dest="tagger",    default="MV2c20")
parser.add_argument('--emu',       dest='emulate',   action="store_true", default=False)
parser.add_argument('--ZZ',        dest='doZZ',      action="store_true", default=False)
parser.add_argument('--tt',        dest='ttbar',     action="store_true", default=False)
parser.add_argument('--unBlind',   dest='unBlind',   action="store_true", default=False)
parser.add_argument('--noMCNorm',  dest='noMCNorm',  action="store_true", default=False)
parser.add_argument('--year',      dest="year",      default="2015")
parser.add_argument('--iteration', dest="iteration", default="0")
parser.add_argument('--variation', dest="variation", default="")
parser.add_argument('--debug', dest="debug", action="store_true", default=False)

o = parser.parse_args(shlex.split(args.extra_options))

c = xAH_config()

import sys, os
XhhDir = os.path.dirname(os.path.realpath("__file__"))
sys.path.insert(0,XhhDir+"/XhhResolved/scripts")

from setupConfig import setGRL, setLumi, setRegions, setTagger
(MV2CutValue, MV2CutValueQCD) = setTagger(o.tagger)
GRL      = setGRL(o.year)
lumi     = setLumi(o.year)
doMCNorm = not o.noMCNorm

if o.ttbar: lumi = lumi*1.195 #kfactor: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryTTbar

doTrigEmulation = o.emulate

variation = o.variation
(leadMass_SR, sublMass_SR, radius_SR, radius_CR, radius_SB, inner_SB, CR_shift, SB_shift, doTightQCDTag, doLooseQCDTag, leadHCmassCut, sublHCmassCut, DhhCut) = setRegions(variation)

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
else: m_weightsFile = "$ROOTCOREBIN/data/XhhResolved/weights2bto4b_"+o.year+"_"+variation+str(iteration)+".root"

#
# Process Ntuple
#
c.setalg("studyHCandAlgos", { "m_name"                   : "studyHCandAlgos",
                              "m_debug"                  : o.debug,
                              "m_doBlind"                : (not args.is_MC and not o.unBlind),
                              "m_doTrigEmulation"        : doTrigEmulation,
                              "m_radius_SR"              : radius_SR,
                              "m_radius_CR"              : radius_CR,
                              "m_radius_SB"              : radius_SB,
                              "m_inner_SB"               : inner_SB,
                              "m_leadMass_SR"            : leadMass_SR,
                              "m_sublMass_SR"            : sublMass_SR,
                              "m_CR_shift"               : CR_shift,
                              "m_SB_shift"               : SB_shift,
                              "m_doTightQCDTag"          : doTightQCDTag,
                              "m_doLooseQCDTag"          : doLooseQCDTag,
                              "m_leadHCmassCut"          : leadHCmassCut,
                              "m_sublHCmassCut"          : sublHCmassCut,
                              "m_DhhCut"                 : DhhCut,
                              "m_tagger"                 : o.tagger,
                              "m_MV2CutValue"            : MV2CutValue,
                              "m_MV2CutValueQCD"         : MV2CutValueQCD,
                              "m_year"                   : o.year,
                              "m_doMCNorm"               : doMCNorm,
#                              "m_doTrigger"              : True,
#                              "m_doTruthOnly"            : False,
                              "m_useWeighted"            : args.is_MC,
                              "m_weightsFile"            : m_weightsFile,
                              "m_doKinematicWeights"     : True if iteration else False,
                              "m_lumi"                   : lumi, #in pb^-1
                              "m_applyGRL"               : applyGRL,
                              "m_doData"                 : (not args.is_MC),
                              "m_GRLxml"                 : GRL,
                              } )

