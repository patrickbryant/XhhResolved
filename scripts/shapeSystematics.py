from sys import path
#import sys
#import time
path.insert(0, 'XhhResolved/plotting/')
from plotTools import plot, read_mu_qcd_file, do_variable_rebinning
#import ROOT
from ROOT import TFile, TH1F, Math
Math.IntegratorOneDimOptions.SetDefaultIntegrator("Gauss")
from setupConfig import setGRL, setLumi, setRegions, setTagger
import rootFiles
#import os
from os import path
#import optparse
from optparse import OptionParser
#import random
#import math
parser = OptionParser()

parser.add_option('--variation',    dest="variation", default="Nominal", help="")
parser.add_option('-i', '--iter',   dest="iteration", default="0", help="")
parser.add_option('-v', '--nTuple', dest="nTuple",    default="01-01-01", help="")
parser.add_option('-y', '--year',   dest="year",      default="2015", help="")
parser.add_option('-c', '--cut',    dest="cut",       default="PassHCdEta", help="cut to get shapes from")
parser.add_option(      '--var',    dest='var',       default='m4j_cor_l')
parser.add_option(  '--weights',    dest="weights",   default="")
parser.add_option('--limitFile',    dest="limitFile", default="")
parser.add_option('--noSyst',       dest="doSyst", action="store_false", default=True)
parser.add_option('--nameSuffix',
                  dest="histNameSuffix",
                  default=""
                  )

o, a = parser.parse_args()

###########
## Setup ##
###########
if o.year == "2016": lumi = "24.3 fb^{-1}"

if path.exists(o.limitFile):
    limitFile = TFile.Open(o.limitFile, "UPDATE")
else:
    limitFile = TFile.Open(o.limitFile, "RECREATE")

inDir = "hists_"+o.year+"_"+o.weights
files    = rootFiles.getFiles(o.iteration,o.nTuple, inDir      , o.year)
shapeVariation="_CR"
#shapeVariation="_CR"
if o.doSyst: 
    filesCRw = rootFiles.getFiles(o.iteration,o.nTuple, inDir+shapeVariation, o.year)

muFile = "XhhResolved/data/mu_qcd_FourTag_"+o.weights+"_"+o.year+"_"+o.variation+"_"+o.iteration+".txt"
mu_qcd_dict = read_mu_qcd_file(muFile)
if o.doSyst:
    muFileCRw = "XhhResolved/data/mu_qcd_FourTag_"+o.weights+shapeVariation+"_"+o.year+"_"+o.variation+"_"+o.iteration+".txt"
    mu_qcd_dictCRw = read_mu_qcd_file(muFileCRw)

useAllhad2bShape = True

#get files
f_data      = TFile(files   ["data"])
f_qcd       = TFile(files   ["qcd"])
f_allhad    = TFile(files   ["allhadShape" if useAllhad2bShape else "allhad"])
f_nonallhad = TFile(files   ["nonallhad"])
if o.doSyst:
    f_qcdCRw       = TFile(filesCRw["qcd"])
    f_allhadCRw    = TFile(filesCRw["allhadShape" if useAllhad2bShape else "allhad"])
    f_nonallhadCRw = TFile(filesCRw["nonallhad"])

###HACK TO TRY USING SR MODEL AS CENTRAL VALUE AND SB AS SYSTEMATIC
#filesCRw = rootFiles.getFiles(o.iteration,o.nTuple, inDir      , o.year)
#files    = rootFiles.getFiles(o.iteration,o.nTuple, inDir+"_CR", o.year)

#muFileCRw      = "XhhResolved/data/mu_qcd_FourTag_"+o.weights+"_"+o.year+"_"+o.variation+"_"+o.iteration+".txt"
#mu_qcd_dictCRw = read_mu_qcd_file(muFileCRw)
#muFile      = "XhhResolved/data/mu_qcd_FourTag_"+o.weights+"_CR_"+o.year+"_"+o.variation+"_"+o.iteration+".txt"
#mu_qcd_dict = read_mu_qcd_file(muFile)

#useAllhad2bShape = True

#get files
# f_data      = TFile(files   ["data"])
# f_qcd       = TFile(files   ["qcd"])
# f_allhad    = TFile(files   ["allhadShape" if useAllhad2bShape else "allhad"])
# f_nonallhad = TFile(files   ["nonallhad"])

# f_qcdCRw       = TFile(filesCRw["qcd"])
# f_allhadCRw    = TFile(filesCRw["allhadShape" if useAllhad2bShape else "allhad"])
# f_nonallhadCRw = TFile(filesCRw["nonallhad"])


#get hists
regions = ["Sideband","Control","Signal","LMVR","HMVR"]
names   = {"Sideband"  :"SB",
           "Control"   :"CR",
           "Signal"    :"hh",
           "LMVR"      :"LM",
           "HMVR"      :"HM",}

h_data        = {}
h_qcd         = {}
h_qcdCRw      = {}
h_qcdCRi      = {}
h_qcdLowHt = {}
h_qcdHighHt = {}
h_qcdLowHtCRw      = {}
h_qcdLowHtCRi      = {}
h_qcdHighHtCRw      = {}
h_qcdHighHtCRi      = {}
h_qcd_up      = {}
h_qcd_down    = {}
h_qcd_NP0_up  = {}
h_qcd_NP1_up  = {}
h_qcd_NP2_up  = {}
h_qcd_NP0_down  = {}
h_qcd_NP1_down  = {}
h_qcd_NP2_down  = {}
h_allhad      = {}
h_allhadCRw   = {}
h_allhadCRi   = {}
h_allhadLowHt = {}
h_allhadHighHt = {}
h_allhadLowHtCRw      = {}
h_allhadLowHtCRi      = {}
h_allhadHighHtCRw      = {}
h_allhadHighHtCRi      = {}
h_allhad_up   = {}
h_allhad_down = {}
h_allhad_NP0_up  = {}
h_allhad_NP1_up  = {}
h_allhad_NP2_up  = {}
h_allhad_NP0_down  = {}
h_allhad_NP1_down  = {}
h_allhad_NP2_down  = {}
h_nonallhad   = {}
h_nonallhad_up     = {}
h_nonallhad_down   = {}
h_nonallhad_NP0_up  = {}
h_nonallhad_NP1_up  = {}
h_nonallhad_NP2_up  = {}
h_nonallhad_NP0_down  = {}
h_nonallhad_NP1_down  = {}
h_nonallhad_NP2_down  = {}
h_nonallhadLowHt = {}
h_nonallhadHighHt = {}
h_nonallhadCRw     = {}
h_nonallhadCRi     = {}
h_nonallhadLowHtCRw      = {}
h_nonallhadLowHtCRi      = {}
h_nonallhadHighHtCRw      = {}
h_nonallhadHighHtCRi      = {}

h_total         = {}
h_totalCRw      = {}
h_totalCRi      = {}
h_totalLowHt = {}
h_totalHighHt = {}
h_totalLowHtCRw      = {}
h_totalLowHtCRi      = {}
h_totalHighHtCRw      = {}
h_totalHighHtCRi      = {}
h_total_NP0_up  = {}
h_total_NP1_up  = {}
h_total_NP2_up  = {}
h_total_NP0_down  = {}
h_total_NP1_down  = {}
h_total_NP2_down  = {}

zero=0.00000001
def getAndName(hist,name):
    name = name.replace(o.histNameSuffix,"")
    hist.SetName(name+(o.histNameSuffix if name[-1*len(o.histNameSuffix):] != o.histNameSuffix else ""))
    #HACK: SET BINS WITH EXCESS TO 0
    # hist.SetBinContent(4,zero)
    # hist.SetBinError(4,zero)
    # hist.SetBinContent(5,zero)
    # hist.SetBinError(5,zero)
    return hist

def makePositive(hist):
    for bin in range(1,hist.GetNbinsX()+1):
        x   = hist.GetXaxis().GetBinCenter(bin)
        if x<250: continue
        y   = hist.GetBinContent(bin)
        err = hist.GetBinError(bin)

        ###
        ### HACK: check CMS result by setting bin error to sqrt(N)
        ### 
        #err = y**0.5 if y>0 else 0

        hist.SetBinContent(bin, y if y > 0 else zero)
        hist.SetBinError(bin, err if y > 0 else zero)
        #if y<0: print hist.GetName(),"has negative bin at x =",x

        

def invert(hist,histCRw):
    histCRi = getAndName(TH1F(hist), histCRw.GetName().replace("CRw","CRi"))

    for bin in range(1,hist.GetNbinsX()+1):
        y    = hist   .GetBinContent(bin)
        yCRw = histCRw.GetBinContent(bin)
        yCRi = y*(y/yCRw) if yCRw>0 else 0.0
        err = max(hist.GetBinError(bin),histCRw.GetBinError(bin))

        histCRi.SetBinContent(bin,yCRi)
        histCRi.SetBinError(bin,err)

    return histCRi
    

for region in regions:
    h_data    [region] = getAndName(f_data   .Get(o.cut+"_FourTag_"+region+"/"+o.var), "data_"+names[region])
    print region ,h_data[region], h_data[region].Integral()

    h_qcd      [region] = getAndName(f_qcd    .Get(o.cut +"_TwoTag_"+region+"/"       +o.var), "qcd_" +names[region])
    h_qcd_up   [region] = getAndName(TH1F(h_qcd[region]), h_qcd[region].GetName()+"_up")
    h_qcd_down [region] = getAndName(TH1F(h_qcd[region]), h_qcd[region].GetName()+"_down")

    h_qcd_NP0_up  [region] = getAndName(TH1F(h_qcd[region]), h_qcd[region].GetName()+"_NP0_up")
    h_qcd_NP0_down[region] = getAndName(TH1F(h_qcd[region]), h_qcd[region].GetName()+"_NP0_down")
    h_qcd_NP1_up  [region] = getAndName(TH1F(h_qcd[region]), h_qcd[region].GetName()+"_NP1_up")
    h_qcd_NP1_down[region] = getAndName(TH1F(h_qcd[region]), h_qcd[region].GetName()+"_NP1_down")
    h_qcd_NP2_up  [region] = getAndName(TH1F(h_qcd[region]), h_qcd[region].GetName()+"_NP2_up")
    h_qcd_NP2_down[region] = getAndName(TH1F(h_qcd[region]), h_qcd[region].GetName()+"_NP2_down")

    h_allhad      [region] = getAndName(f_allhad.Get(o.cut+("_TwoTag_" if useAllhad2bShape else "_FourTag_")+region+"/"+o.var), "allhad_"+names[region])
    h_allhad_up   [region] = getAndName(TH1F(h_allhad[region]), h_allhad[region].GetName()+"_up")
    h_allhad_down [region] = getAndName(TH1F(h_allhad[region]), h_allhad[region].GetName()+"_down")

    h_allhad_NP0_up  [region] = getAndName(TH1F(h_allhad[region]), h_allhad[region].GetName()+"_NP0_up")
    h_allhad_NP0_down[region] = getAndName(TH1F(h_allhad[region]), h_allhad[region].GetName()+"_NP0_down")
    h_allhad_NP1_up  [region] = getAndName(TH1F(h_allhad[region]), h_allhad[region].GetName()+"_NP1_up")
    h_allhad_NP1_down[region] = getAndName(TH1F(h_allhad[region]), h_allhad[region].GetName()+"_NP1_down")
    h_allhad_NP2_up  [region] = getAndName(TH1F(h_allhad[region]), h_allhad[region].GetName()+"_NP2_up")
    h_allhad_NP2_down[region] = getAndName(TH1F(h_allhad[region]), h_allhad[region].GetName()+"_NP2_down")

    h_nonallhad      [region] = getAndName(f_nonallhad.Get(o.cut+"_FourTag_"+region+"/"+o.var),        "nonallhad_"+names[region])
    h_nonallhad_up  [region] = getAndName(TH1F(h_nonallhad[region]), h_nonallhad[region].GetName()+"_up")
    h_nonallhad_down[region] = getAndName(TH1F(h_nonallhad[region]), h_nonallhad[region].GetName()+"_down")

    h_nonallhad_NP0_up  [region] = getAndName(TH1F(h_nonallhad[region]), h_nonallhad[region].GetName()+"_NP0_up")
    h_nonallhad_NP0_down[region] = getAndName(TH1F(h_nonallhad[region]), h_nonallhad[region].GetName()+"_NP0_down")
    h_nonallhad_NP1_up  [region] = getAndName(TH1F(h_nonallhad[region]), h_nonallhad[region].GetName()+"_NP1_up")
    h_nonallhad_NP1_down[region] = getAndName(TH1F(h_nonallhad[region]), h_nonallhad[region].GetName()+"_NP1_down")
    h_nonallhad_NP2_up  [region] = getAndName(TH1F(h_nonallhad[region]), h_nonallhad[region].GetName()+"_NP2_up")
    h_nonallhad_NP2_down[region] = getAndName(TH1F(h_nonallhad[region]), h_nonallhad[region].GetName()+"_NP2_down")


    if o.doSyst:
        h_qcdLowHt [region] = getAndName(f_qcd    .Get(o.cut +"_TwoTag_"+region+"/lowHt_" +o.var), "qcd_" +names[region]+"_LowHt")
        h_qcdHighHt[region] = getAndName(f_qcd    .Get(o.cut +"_TwoTag_"+region+"/highHt_"+o.var), "qcd_" +names[region]+"_HighHt")
        h_allhadLowHt [region] = getAndName(f_allhad.Get(o.cut +"_TwoTag_"+region+"/lowHt_" +o.var), "allhad_" +names[region]+"_LowHt")
        h_allhadHighHt[region] = getAndName(f_allhad.Get(o.cut +"_TwoTag_"+region+"/highHt_"+o.var), "allhad_" +names[region]+"_HighHt")
        h_nonallhadLowHt [region] = getAndName(f_nonallhad.Get(o.cut+"_FourTag_"+region+"/lowHt_" +o.var), "nonallhad_"+names[region]+"_LowHt")
        h_nonallhadHighHt[region] = getAndName(f_nonallhad.Get(o.cut+"_FourTag_"+region+"/highHt_"+o.var), "nonallhad_"+names[region]+"_HighHt")

        print filesCRw["qcd"]
        print o.cut+"_TwoTag_" +region+"/"       +o.var
        h_qcdCRw      [region] = getAndName(f_qcdCRw.Get(o.cut+"_TwoTag_" +region+"/"       +o.var), "qcd_"+names[region]+"_CRw")
        h_qcdLowHtCRw [region] = getAndName(f_qcdCRw.Get(o.cut+"_TwoTag_" +region+"/lowHt_" +o.var), "qcd_"+names[region]+"_LowHtCRw")
        h_qcdHighHtCRw[region] = getAndName(f_qcdCRw.Get(o.cut+"_TwoTag_" +region+"/highHt_"+o.var), "qcd_"+names[region]+"_HighHtCRw")
        h_allhadCRw      [region] = getAndName(f_allhadCRw.Get(o.cut+("_TwoTag_" if useAllhad2bShape else "_FourTag_")+region+"/"+o.var), "allhad_"   +names[region]+"_CRw")
        h_allhadLowHtCRw [region] = getAndName(f_allhadCRw.Get(o.cut+"_TwoTag_" +region+"/lowHt_" +o.var), "allhad_"  +names[region]+"_LowHtCRw")
        h_allhadHighHtCRw[region] = getAndName(f_allhadCRw.Get(o.cut+"_TwoTag_" +region+"/highHt_"+o.var), "allhad_"  +names[region]+"_HighHtCRw")
        h_nonallhadCRw      [region] = getAndName(f_nonallhadCRw.Get(o.cut+"_FourTag_"+region+"/"       +o.var), "nonallhad_"+names[region]+"_CRw")
        h_nonallhadLowHtCRw [region] = getAndName(f_nonallhadCRw.Get(o.cut+"_FourTag_" +region+"/lowHt_" +o.var), "nonallhad_"+names[region]+"_LowHtCRw")
        h_nonallhadHighHtCRw[region] = getAndName(f_nonallhadCRw.Get(o.cut+"_FourTag_" +region+"/highHt_"+o.var), "nonallhad_"+names[region]+"_HighHtCRw")

    #scale background
    h_qcd        [region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"])
    h_qcd_up     [region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"]+mu_qcd_dict["mu_qcd_PassHCdEta_err"])
    h_qcd_down   [region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"]-mu_qcd_dict["mu_qcd_PassHCdEta_err"])

    h_qcd_NP0_up  [region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"]+mu_qcd_dict["mu_err_NP0_comp0"])
    h_qcd_NP0_down[region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"]-mu_qcd_dict["mu_err_NP0_comp0"])
    h_qcd_NP1_up  [region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"]+mu_qcd_dict["mu_err_NP1_comp0"])
    h_qcd_NP1_down[region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"]-mu_qcd_dict["mu_err_NP1_comp0"])
    h_qcd_NP2_up  [region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"]+mu_qcd_dict["mu_err_NP2_comp0"])
    h_qcd_NP2_down[region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"]-mu_qcd_dict["mu_err_NP2_comp0"])

    h_allhad      [region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"])
    h_allhad_up   [region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"]+mu_qcd_dict["mu_allhad_PassHCdEta_err"])
    h_allhad_down [region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"]-mu_qcd_dict["mu_allhad_PassHCdEta_err"])

    h_allhad_NP0_up  [region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"]+mu_qcd_dict["mu_err_NP0_comp1"])
    h_allhad_NP0_down[region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"]-mu_qcd_dict["mu_err_NP0_comp1"])
    h_allhad_NP1_up  [region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"]+mu_qcd_dict["mu_err_NP1_comp1"])
    h_allhad_NP1_down[region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"]-mu_qcd_dict["mu_err_NP1_comp1"])
    h_allhad_NP2_up  [region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"]+mu_qcd_dict["mu_err_NP2_comp1"])
    h_allhad_NP2_down[region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"]-mu_qcd_dict["mu_err_NP2_comp1"])

    h_nonallhad      [region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"])
    h_nonallhad_up   [region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"]+mu_qcd_dict["mu_nonallhad4b_PassHCdEta_err"])
    h_nonallhad_down [region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"]-mu_qcd_dict["mu_nonallhad4b_PassHCdEta_err"])

    h_nonallhad_NP0_up  [region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"]+mu_qcd_dict["mu_err_NP0_comp2"])
    h_nonallhad_NP0_down[region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"]-mu_qcd_dict["mu_err_NP0_comp2"])
    h_nonallhad_NP1_up  [region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"]+mu_qcd_dict["mu_err_NP1_comp2"])
    h_nonallhad_NP1_down[region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"]-mu_qcd_dict["mu_err_NP1_comp2"])
    h_nonallhad_NP2_up  [region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"]+mu_qcd_dict["mu_err_NP2_comp2"])
    h_nonallhad_NP2_down[region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"]-mu_qcd_dict["mu_err_NP2_comp2"])

    if o.doSyst:
        h_qcdLowHt   [region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"])
        h_qcdHighHt  [region].Scale(mu_qcd_dict   ["mu_qcd_PassHCdEta"])
        h_allhadLowHt [region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"])
        h_allhadHighHt[region].Scale(mu_qcd_dict   ["mu_allhad_PassHCdEta"])
        h_nonallhadLowHt [region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"])
        h_nonallhadHighHt[region].Scale(mu_qcd_dict   ["mu_nonallhad4b_PassHCdEta"])

        h_qcdCRw      [region].Scale(mu_qcd_dictCRw["mu_qcd_PassHCdEta"])
        h_qcdLowHtCRw [region].Scale(mu_qcd_dictCRw["mu_qcd_PassHCdEta"])
        h_qcdHighHtCRw[region].Scale(mu_qcd_dictCRw["mu_qcd_PassHCdEta"])
        h_allhadCRw      [region].Scale(mu_qcd_dictCRw["mu_allhad_PassHCdEta"])
        h_allhadLowHtCRw [region].Scale(mu_qcd_dictCRw["mu_allhad_PassHCdEta"])
        h_allhadHighHtCRw[region].Scale(mu_qcd_dictCRw["mu_allhad_PassHCdEta"])
        h_nonallhadCRw      [region].Scale(mu_qcd_dictCRw["mu_nonallhad4b_PassHCdEta"])
        h_nonallhadLowHtCRw [region].Scale(mu_qcd_dictCRw["mu_nonallhad4b_PassHCdEta"])
        h_nonallhadHighHtCRw[region].Scale(mu_qcd_dictCRw["mu_nonallhad4b_PassHCdEta"])

        #combine Ht regions to make total where each Ht region is varied separately
        h_qcdLowHtCRw [region].Add(h_qcdHighHt[region])
        h_qcdHighHtCRw[region].Add(h_qcdLowHt [region])
        h_allhadLowHtCRw [region].Add(h_allhadHighHt[region])
        h_allhadHighHtCRw[region].Add(h_allhadLowHt [region])
        h_nonallhadLowHtCRw [region].Add(h_nonallhadHighHt[region])
        h_nonallhadHighHtCRw[region].Add(h_nonallhadLowHt [region])

    makePositive(h_qcd        [region])
    makePositive(h_qcd_up     [region])
    makePositive(h_qcd_down   [region])
    makePositive(h_qcd_NP0_up     [region])
    makePositive(h_qcd_NP0_down   [region])
    makePositive(h_qcd_NP1_up     [region])
    makePositive(h_qcd_NP1_down   [region])
    makePositive(h_qcd_NP2_up     [region])
    makePositive(h_qcd_NP2_down   [region])
    makePositive(h_allhad      [region])
    makePositive(h_allhad_up   [region])
    makePositive(h_allhad_down [region])
    makePositive(h_allhad_NP0_up     [region])
    makePositive(h_allhad_NP0_down   [region])
    makePositive(h_allhad_NP1_up     [region])
    makePositive(h_allhad_NP1_down   [region])
    makePositive(h_allhad_NP2_up     [region])
    makePositive(h_allhad_NP2_down   [region])
    makePositive(h_nonallhad      [region])
    makePositive(h_nonallhad_up   [region])
    makePositive(h_nonallhad_down [region])
    makePositive(h_nonallhad_NP0_up     [region])
    makePositive(h_nonallhad_NP0_down   [region])
    makePositive(h_nonallhad_NP1_up     [region])
    makePositive(h_nonallhad_NP1_down   [region])
    makePositive(h_nonallhad_NP2_up     [region])
    makePositive(h_nonallhad_NP2_down   [region])
    if o.doSyst:
        makePositive(h_qcdLowHt   [region])
        makePositive(h_qcdHighHt  [region])
        makePositive(h_allhadLowHt [region])
        makePositive(h_allhadHighHt[region])
        makePositive(h_nonallhadLowHt [region])
        makePositive(h_nonallhadHighHt[region])
        makePositive(h_qcdCRw      [region])
        makePositive(h_qcdLowHtCRw [region])
        makePositive(h_qcdHighHtCRw[region])
        makePositive(h_allhadCRw      [region])
        makePositive(h_allhadLowHtCRw [region])
        makePositive(h_allhadHighHtCRw[region])
        makePositive(h_nonallhadCRw      [region])
        makePositive(h_nonallhadLowHtCRw [region])
        makePositive(h_nonallhadHighHtCRw[region])

    #invert CRw version wrt nominal
    if o.doSyst:
        h_qcdCRi      [region] = invert(h_qcd[region],h_qcdCRw      [region])
        h_qcdLowHtCRi [region] = invert(h_qcd[region],h_qcdLowHtCRw [region])
        h_qcdHighHtCRi[region] = invert(h_qcd[region],h_qcdHighHtCRw[region])
        h_allhadCRi      [region] = invert(h_allhad[region],h_allhadCRw      [region])
        h_allhadLowHtCRi [region] = invert(h_allhad[region],h_allhadLowHtCRw [region])
        h_allhadHighHtCRi[region] = invert(h_allhad[region],h_allhadHighHtCRw[region])
        h_nonallhadCRi      [region] = invert(h_nonallhad[region],h_nonallhadCRw      [region])
        h_nonallhadLowHtCRi [region] = invert(h_nonallhad[region],h_nonallhadLowHtCRw [region])
        h_nonallhadHighHtCRi[region] = invert(h_nonallhad[region],h_nonallhadHighHtCRw[region])
        

    #make total background hists
    h_total      [region] = getAndName(TH1F(h_qcd      [region]), "total_" +names[region])

    h_total[region].Add(h_allhad   [region])
    h_total[region].Add(h_nonallhad[region])

    if o.doSyst:
        h_totalLowHt [region] = getAndName(TH1F(h_qcdLowHt [region]), "total_" +names[region]+"_LowHt")
        h_totalHighHt[region] = getAndName(TH1F(h_qcdHighHt[region]), "total_" +names[region]+"_HighHt")
        h_totalLowHt[region].Add(h_allhadLowHt   [region])
        h_totalLowHt[region].Add(h_nonallhadLowHt[region])
        h_totalHighHt[region].Add(h_allhadHighHt   [region])
        h_totalHighHt[region].Add(h_nonallhadHighHt[region])

        h_totalCRw[region] = getAndName(TH1F(h_qcdCRw[region]), h_qcdCRw[region].GetName().replace("qcd","total"))
        h_totalCRi[region] = getAndName(TH1F(h_qcdCRi[region]), h_qcdCRi[region].GetName().replace("qcd","total"))
        h_totalLowHtCRw[region] = getAndName(TH1F(h_qcdLowHtCRw[region]), h_qcdLowHtCRw[region].GetName().replace("qcd","total"))
        h_totalLowHtCRi[region] = getAndName(TH1F(h_qcdLowHtCRi[region]), h_qcdLowHtCRi[region].GetName().replace("qcd","total"))
        h_totalHighHtCRw[region] = getAndName(TH1F(h_qcdHighHtCRw[region]), h_qcdHighHtCRw[region].GetName().replace("qcd","total"))
        h_totalHighHtCRi[region] = getAndName(TH1F(h_qcdHighHtCRi[region]), h_qcdHighHtCRi[region].GetName().replace("qcd","total"))

        h_totalCRw[region].Add(h_allhadCRw   [region])
        h_totalCRw[region].Add(h_nonallhadCRw[region])
        h_totalCRi[region].Add(h_allhadCRi   [region])
        h_totalCRi[region].Add(h_nonallhadCRi[region])

        h_totalLowHtCRw[region].Add(h_allhadLowHtCRw   [region])
        h_totalLowHtCRw[region].Add(h_nonallhadLowHtCRw[region])
        h_totalLowHtCRi[region].Add(h_allhadLowHtCRi   [region])
        h_totalLowHtCRi[region].Add(h_nonallhadLowHtCRi[region])

        h_totalHighHtCRw[region].Add(h_allhadHighHtCRw   [region])
        h_totalHighHtCRw[region].Add(h_nonallhadHighHtCRw[region])
        h_totalHighHtCRi[region].Add(h_allhadHighHtCRi   [region])
        h_totalHighHtCRi[region].Add(h_nonallhadHighHtCRi[region])

    h_total_NP0_up  [region] = getAndName(TH1F(h_qcd_NP0_up  [region]), h_qcd_NP0_up  [region].GetName().replace("qcd","total"))
    h_total_NP0_down[region] = getAndName(TH1F(h_qcd_NP0_down[region]), h_qcd_NP0_down[region].GetName().replace("qcd","total"))
    h_total_NP1_up  [region] = getAndName(TH1F(h_qcd_NP1_up  [region]), h_qcd_NP1_up  [region].GetName().replace("qcd","total"))
    h_total_NP1_down[region] = getAndName(TH1F(h_qcd_NP1_down[region]), h_qcd_NP1_down[region].GetName().replace("qcd","total"))
    h_total_NP2_up  [region] = getAndName(TH1F(h_qcd_NP2_up  [region]), h_qcd_NP2_up  [region].GetName().replace("qcd","total"))
    h_total_NP2_down[region] = getAndName(TH1F(h_qcd_NP2_down[region]), h_qcd_NP2_down[region].GetName().replace("qcd","total"))

    h_total_NP0_up  [region].Add(   h_allhad_NP0_up  [region])
    h_total_NP0_up  [region].Add(h_nonallhad_NP0_up  [region])
    h_total_NP0_down[region].Add(   h_allhad_NP0_down[region])
    h_total_NP0_down[region].Add(h_nonallhad_NP0_down[region])
    h_total_NP1_up  [region].Add(   h_allhad_NP1_up  [region])
    h_total_NP1_up  [region].Add(h_nonallhad_NP1_up  [region])
    h_total_NP1_down[region].Add(   h_allhad_NP1_down[region])
    h_total_NP1_down[region].Add(h_nonallhad_NP1_down[region])
    h_total_NP2_up  [region].Add(   h_allhad_NP2_up  [region])
    h_total_NP2_up  [region].Add(h_nonallhad_NP2_up  [region])
    h_total_NP2_down[region].Add(   h_allhad_NP2_down[region])
    h_total_NP2_down[region].Add(h_nonallhad_NP2_down[region])



#store shape vars
for region in regions:

    #HACK. SEE WHAT HAPPENS IF BIN WITH DEFICIT IS REMOVED
    # h_data[region].SetBinContent(25,h_total[region].GetBinContent(25))
    # h_data[region].SetBinError(  25,h_total[region].GetBinContent(25)**0.5)
    # h_data[region].SetBinContent(22,h_total[region].GetBinContent(22))
    # h_data[region].SetBinError(  22,h_total[region].GetBinContent(22)**0.5)

    limitFile.Append( h_data            [region] )
    limitFile.Append( h_qcd             [region] )
    limitFile.Append( h_qcd_up          [region] )
    limitFile.Append( h_qcd_down        [region] )
    limitFile.Append( h_qcd_NP0_up      [region] )
    limitFile.Append( h_qcd_NP0_down    [region] )
    limitFile.Append( h_qcd_NP1_up      [region] )
    limitFile.Append( h_qcd_NP1_down    [region] )
    limitFile.Append( h_qcd_NP2_up      [region] )
    limitFile.Append( h_qcd_NP2_down    [region] )
    limitFile.Append( h_allhad          [region] )
    limitFile.Append( h_allhad_up       [region] )
    limitFile.Append( h_allhad_down     [region] )
    limitFile.Append( h_allhad_NP0_up      [region] )
    limitFile.Append( h_allhad_NP0_down    [region] )
    limitFile.Append( h_allhad_NP1_up      [region] )
    limitFile.Append( h_allhad_NP1_down    [region] )
    limitFile.Append( h_allhad_NP2_up      [region] )
    limitFile.Append( h_allhad_NP2_down    [region] )
    limitFile.Append( h_nonallhad       [region] )
    limitFile.Append( h_nonallhad_up    [region] )
    limitFile.Append( h_nonallhad_down  [region] )
    limitFile.Append( h_nonallhad_NP0_up      [region] )
    limitFile.Append( h_nonallhad_NP0_down    [region] )
    limitFile.Append( h_nonallhad_NP1_up      [region] )
    limitFile.Append( h_nonallhad_NP1_down    [region] )
    limitFile.Append( h_nonallhad_NP2_up      [region] )
    limitFile.Append( h_nonallhad_NP2_down    [region] )
    limitFile.Append( h_total                 [region] )
    limitFile.Append( h_total_NP0_up          [region] )
    limitFile.Append( h_total_NP0_down        [region] )
    limitFile.Append( h_total_NP1_up          [region] )
    limitFile.Append( h_total_NP1_down        [region] )
    limitFile.Append( h_total_NP2_up          [region] )
    limitFile.Append( h_total_NP2_down        [region] )
    if o.doSyst:
        limitFile.Append( h_qcdCRw      [region] )
        limitFile.Append( h_qcdCRi      [region] )
        limitFile.Append( h_allhadCRw   [region] )
        limitFile.Append( h_allhadCRi   [region] )
        limitFile.Append( h_nonallhadCRw[region] )
        limitFile.Append( h_nonallhadCRi[region] )
        limitFile.Append( h_totalCRw    [region] )
        limitFile.Append( h_totalCRi    [region] )

        limitFile.Append( h_qcdLowHtCRw      [region] )
        limitFile.Append( h_qcdLowHtCRi      [region] )
        limitFile.Append( h_allhadLowHtCRw   [region] )
        limitFile.Append( h_allhadLowHtCRi   [region] )
        limitFile.Append( h_nonallhadLowHtCRw[region] )
        limitFile.Append( h_nonallhadLowHtCRi[region] )
        limitFile.Append( h_totalLowHtCRw    [region] )
        limitFile.Append( h_totalLowHtCRi    [region] )

        limitFile.Append( h_qcdHighHtCRw      [region] )
        limitFile.Append( h_qcdHighHtCRi      [region] )
        limitFile.Append( h_allhadHighHtCRw   [region] )
        limitFile.Append( h_allhadHighHtCRi   [region] )
        limitFile.Append( h_nonallhadHighHtCRw[region] )
        limitFile.Append( h_nonallhadHighHtCRi[region] )
        limitFile.Append( h_totalHighHtCRw    [region] )
        limitFile.Append( h_totalHighHtCRi    [region] )

limitFile.Write()
