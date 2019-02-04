from iPlot import loadPath
loadPath()

from utils import parseOpts, getPM, setBatch, plot

setBatch()
(o,a) = parseOpts()
pm = getPM(o)
import OfficialAtlasStyle

#
#
#
import ROOT
from ROOT import gStyle                                                                                                                             

#plot("eta","PtCut",norm=0,logy=0)
#plot("eta","PtCut",norm=0,logy=1)

plot("eta",["Nominal75","Extended75"],norm=0,logy=1,doratio=1,rMin=0.8,rMax=1.,rebin=1,min=1e-1,labels=["Nominal","Extended Eta"])
plot("eta",["Nominal75","Extended75"],norm=0,logy=0,doratio=1,rMin=0.8,rMax=1.,rebin=1,min=1e-1,labels=["Nominal","Extended Eta"])
plot("mhh",["Nominal75","Extended75"],norm=0,logy=0,doratio=1,rMin=0.8,rMax=1.,rebin=2,labels=["Nominal","Extended Eta"])

plot("eta",["Nominal",  "Extended"],norm=0,logy=1,doratio=1,rMin=0.8,rMax=1.,rebin=1,min=1e1,labels=["Nominal","Extended Eta"])
plot("eta",["Nominal",  "Extended"],norm=0,logy=0,doratio=1,rMin=0.8,rMax=1.,rebin=1,min=1e1,labels=["Nominal","Extended Eta"])
plot("mhh",["Nominal",  "Extended"],  norm=0,logy=0,doratio=1,rMin=0.8,rMax=1.,rebin=2,labels=["Nominal","Extended Eta"])

