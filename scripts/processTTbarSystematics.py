

import ROOT


allhad_files = [
    "group.phys-exotics.mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410008.aMcAtNloHerwigppEvtGen_ttbar_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410163.PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410162.PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172p5_up_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410161.PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410024.Sherpa_CT10_ttbar_AllHadron_MEPS_NLO.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410042.PowhegPythiaEvtGen_P2012_ttbar_hdamp170_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410043.PowhegPythiaEvtGen_P2012_ttbar_hdamp171p5_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410044.PowhegPythiaEvtGen_P2012_ttbar_hdamp173p5_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410045.PowhegPythiaEvtGen_P2012_ttbar_hdamp175_allhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410046.PowhegPythiaEvtGen_P2012_ttbar_hdamp177p5_allhad.hh4b-01-02-03_MiniNTuple.root",
    ]

# non-all had
nonallhad_files = [
    "group.phys-exotics.mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410003.aMcAtNloHerwigppEvtGen_ttbar_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410004.PowhegHerwigppEvtGen_UEEE5_ttbar_hdamp172p5_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410002.PowhegPythiaEvtGen_P2012radLo_ttbar_hdamp172_up_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410001.PowhegPythiaEvtGen_P2012radHi_ttbar_hdamp345_down_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410022.Sherpa_CT10_ttbar_SingleLeptonP_MEPS_NLO.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410023.Sherpa_CT10_ttbar_SingleLeptonM_MEPS_NLO.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410037.PowhegPythiaEvtGen_P2012_ttbar_hdamp170_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410038.PowhegPythiaEvtGen_P2012_ttbar_hdamp171p5_nonallhad.hh4b-01-02-03_MiniNTuple.root",                 
    "group.phys-exotics.mc15_13TeV.410039.PowhegPythiaEvtGen_P2012_ttbar_hdamp173p5_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410040.PowhegPythiaEvtGen_P2012_ttbar_hdamp175_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    "group.phys-exotics.mc15_13TeV.410041.PowhegPythiaEvtGen_P2012_ttbar_hdamp177p5_nonallhad.hh4b-01-02-03_MiniNTuple.root",
    ]

combinedFiles = [
    "m177.5.root",
    "nominal.root",
    "aMcAtNloHerwig.root",
    "radLo.root",
    "m173.5.root",
    "m170.root",
    "m175.root",
    "radHi.root",
    "PowhegHerwig.root",
    "m171.5.root",
    ]

def getYeild(fileName,dirName):
    inFile = ROOT.TFile(fileName,"READ")

    #hist = inFile.Get("Loose/DhhMin/TwoTag/Signal/hCandDr")
    #hist2b = inFile.Get("Loose/DhhMin/TwoTag/Signal/hCandDr")
    hist = inFile.Get("PassHCdEta_"+dirName+"_Signal/hCandDr")
    #hist = inFile.Get("Loose/DhhMin/"+dirName+"/Signal/hCandDr")

    #integral = ROOT.Double()
    error    = ROOT.Double()
    integral = hist.IntegralAndError(0,hist.GetNbinsX(),error)
    inFile.Close()
    return integral,error



def relativeUncert(name, var1, var2, nominal):
    diff = abs(var1[0] - var2[0])
    diff_err = pow(var1[1]**2 + var2[1]**2,0.5)
    rat = diff/nominal[0]
    rat_err_1 = rat/diff       * nominal[1]
    rat_err_2 = rat/nominal[0] * diff_err
    rat_err   = pow(rat_err_1*rat_err_1 + rat_err_2*rat_err_2,0.5) 
    print name,rat,rat_err
    return rat

topDirName = "hist-ttbarSysteamticsNew_2016_75GeV"

for d in ["FourTag","TwoTag"]:
    print 
    print
    nominal  = getYeild(topDirName+"/nominal.root",       d)
    aMcAtNlo = getYeild(topDirName+"/aMcAtNloHerwig.root",d)
    powHer   = getYeild(topDirName+"/PowhegHerwig.root",  d)
    radLo    = getYeild(topDirName+"/radLo.root",         d)
    radHi    = getYeild(topDirName+"/radHi.root",         d)
    massHi   = getYeild(topDirName+"/m177.5.root",        d)
    massLo   = getYeild(topDirName+"/m170.root",          d)

    allUncert = []
    allUncert.append(relativeUncert("Hard Scatter",aMcAtNlo, powHer, nominal))
    allUncert.append(relativeUncert("Frag/Had.",   nominal,  powHer, nominal))
    allUncert.append(relativeUncert("Radiation",   radHi,    radLo,  nominal))
    allUncert.append(relativeUncert("TopMass",     massHi,   massLo, nominal))
    print "Scale",29.20/831.76
    allUncert.append(29.20/831.76)
    print "PDF", 35.06/831.
    allUncert.append(35.06/831.)
    
    print "-"*20
    print "Total:",
    sum2 = 0
    for a in allUncert:
        sum2 += a*a
    print pow(sum2,0.5)
    print

#for f in combinedFiles: #allhad_files + nonallhad_files:
#
#    print f
#    print "\t",
#    #dirName = f.replace(".root","").replace("group.phys-exotics.","")
#    #doFile(topDirName+"/"+dirName+"/hist-"+f+".root")
#
#    doFile(p
#

#doFile("hist-ttbarSysteamtics_2016/mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.hh4b-01-02-03_MiniNTuple/fetch/hist-group.phys-exotics.mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.hh4b-01-02-03_MiniNTuple.root-0.root")
#doFile("hist-ttbarSysteamtics_2016/mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.hh4b-01-02-03_MiniNTuple/fetch/hist-group.phys-exotics.mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.hh4b-01-02-03_MiniNTuple.root-0.root")
#
#
#doFile("hist-ttbarSysteamtics_2016/mc15_13TeV.410008.aMcAtNloHerwigppEvtGen_ttbar_allhad.hh4b-01-02-03_MiniNTuple/fetch/hist-group.phys-exotics.mc15_13TeV.410008.aMcAtNloHerwigppEvtGen_ttbar_allhad.hh4b-01-02-03_MiniNTuple.root-0.root")
#doFile("hist-ttbarSysteamtics_2016/mc15_13TeV.410003.aMcAtNloHerwigppEvtGen_ttbar_nonallhad.hh4b-01-02-03_MiniNTuple/fetch/hist-group.phys-exotics.mc15_13TeV.410003.aMcAtNloHerwigppEvtGen_ttbar_nonallhad.hh4b-01-02-03_MiniNTuple.root-0.root")
