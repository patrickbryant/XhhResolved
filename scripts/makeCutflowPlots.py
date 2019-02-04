import sys
sys.path.insert(0, 'XhhResolved/plotting/')
import ROOT
import rootFiles
import optparse
import random
import math
import array
parser = optparse.OptionParser()

parser.add_option('--inDir',          dest="inDir",                 default="hists", help="")
parser.add_option('--out',         dest="out",                default="", help="")
parser.add_option('-i', '--iter',    dest="iteration",     default="0", help="")
parser.add_option('-v', '--nTuple',    dest="nTuple",     default="01-01-01", help="")
parser.add_option('-y', '--year',    dest="year",     default="2015", help="")

o, a = parser.parse_args()

iteration=o.iteration
nTuple=o.nTuple
inDir=o.inDir
year=o.year
out=o.out

files = rootFiles.getFiles(iteration,nTuple,inDir,year)

L1s=[
     'L1_4J15.0ETA25', 
     'L1_J75_3J20',
     'L1_J100', 
     'L1',
     ]

HLTs=[
     'HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25', 
     'HLT_j100_2j55_bmv2c2060_split', 
     'HLT_j225_bmv2c2060_split', 
     'HLT', 
     'HLT_SF_up',
     'HLT_SF_down',
     ]

if o.year == "2015":
    HLTs=[
         'HLT_2j35_btight_2j35_L14J15.0ETA25',
         'HLT_j100_2j55_bmedium',
         'HLT_j225_bloose',
         'HLT',
         'HLT_SF_up',
         'HLT_SF_down',
        ]


cuts=[
     'execute', 
     'passHCJetSelection', 
     'passHCJetPairing', 
     'passHCPt', 
     'passHCdEta', 
     'passSignalBeforeAllhadVeto', 
     'passAllhadVeto', 
     'passSignal',
     ]


# Scalar 2016 MC
#      OR    2j35  2j55  j225
#  260 0.68  0.67  0.06  0.00
#  300 0.77  0.76  0.11  0.00
#  400 0.91  0.88  0.37  0.01
#  500 0.97  0.94  0.84  0.04
#  600 0.99  0.95  0.96  0.19
#  800 0.995 0.96  0.98  0.73
# 1000 0.99  0.84  0.95  0.91
# 1100 0.985 0.72  0.92  0.93
# 1200 0.98  0.61  0.83  0.94
ScalarAllMCt=["HLT","HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25","HLT_j100_2j55_bmv2c2060_split","HLT_j225_bmv2c2060_split"]
ScalarAllMCm=[260,300,400,500,600,800,1000,1100,1200]
ScalarAllMCe=[[0.68,0.77,0.91,0.97,0.99,0.995,0.99,0.985,0.98],
              [0.67,0.76,0.88,0.94,0.95,0.96,0.84,0.72,0.61],
              [0.06,0.11,0.37,0.84,0.96,0.98,0.95,0.92,0.83],
              [0.00,0.00,0.01,0.04,0.19,0.73,0.91,0.93,0.94],
              ]

# Scalar 2015 MC
#      OR    2j35  2j55  j225
#  260 0.35  0.33  0.04  0.00
#  300 0.41  0.37  0.09  0.00
#  400 0.61  0.48  0.30  0.01
#  500 0.81  0.51  0.71  0.04
#  600 0.87  0.50  0.82  0.18
#  800 0.93  0.44  0.79  0.69
# 1000 0.935 0.32  0.745 0.86
# 1100 0.94  0.25  0.69  0.88
# 1200 0.93  0.15  0.60  0.895
if o.year == "2015":
    ScalarAllMCt=["HLT","HLT_2j35_btight_2j35_L14J15.0ETA25","HLT_j100_2j55_bmedium","HLT_j225_bloose"]
    ScalarAllMCe=[[0.35,0.41,0.61,0.81,0.87,0.93,0.935,0.94,0.93],
                  [0.33,0.37,0.48,0.51,0.50,0.44,0.32,0.25,0.15],
                  [0.04,0.09,0.30,0.71,0.82,0.79,0.745,0.69,0.60],
                  [0.00,0.00,0.01,0.04,0.18,0.69,0.86,0.88,0.895],
                  ]


def makeTrigEffMC(trigs,masses,efficiencies,sampleType="NWS",cut="passSignal",trig="HLT"):
    name = "trigEffMC_"+sampleType+"_"+cut+"_"+trig
    print "Making",name
    
    if sampleType=="NWS" or sampleType[0]=="R":
        bins = array.array('d',[250,270,330,470,530,670,930,1070,1130,1270])
        h=ROOT.TH1F(name,name,9,bins)
    else:
        h=ROOT.TH1F()
        h.SetName(name)
        
    for mass in masses:
        i_m = masses.index(mass)
        i_t = trigs .index(trig)
        eff = efficiencies[i_t][i_m]
        h.Fill(mass,eff)
        h.SetBinError(h.GetXaxis().FindBin(mass),0)
        
    #h.LabelsDeflate("X")
    return h


def getLabel(sample):
    mass = ""
    for i in range(len(sample)):
        if sample[i] in "0123456789":
            mass = mass+sample[i]
    if mass: return int(mass)
    if "SMNR" in sample: return "SMNR"
    if sample == "allhad": return "Hadronic t#bar{t}"
    if sample == "nonallhad": return "Semileptonic t#bar{t}"
    return sample


def getSampleType(sample):
    if sample[0] == "M": return "RSG_c10"
    if sample[0] == "R": return "RSG_c20"
    if sample[0] == "H": return "NWS"
    if sample[0] == "N": return "NWS_NLO"
    #if "had" in sample: return "ttbar"
    return sample


def getCutflows(samples):
    sampleType = getSampleType(samples[0])
    labels = sorted([getLabel(sample) for sample in samples])
    if "0" in samples[0][-1]:
        labels = sorted([int(label) for label in labels])
        labels = [int(label) for label in labels]
    f={}
    c={}
    a={}
    for sample in samples:
        if getSampleType(sample) != sampleType: print "ERROR: Mixed Sample Types",sampleType,getSampleType(sample)

        label = getLabel(sample)
        f[label] = ROOT.TFile(files[sample],"READ")
        c[label] = f[label].Get("FourTag/cutflow_weighted")#only sees events in nTuple
        c[label].SetName(sampleType+"_nTuple_weighted")
        c[label].SetDirectory(0)
        a[label] = f[label].Get("hhEventBuilder/cutflow_weighted")#this is where the 'all' information lives
        a[label].SetName(sampleType+"_sample_weighted")
        a[label].SetDirectory(0)
    
    return (labels,c,a)


def getTrigEff(hist,cut,trig):
    n = hist.GetBinContent(hist.GetXaxis().FindBin(cut+"_"+trig))
    d = hist.GetBinContent(hist.GetXaxis().FindBin(cut))
    ne = hist.GetBinError(hist.GetXaxis().FindBin(cut+"_"+trig))
    de = hist.GetBinError(hist.GetXaxis().FindBin(cut))
    if n and d:
        return (n/d, ne/d)
    if n and not d:
        return (float(1), float(0))
    return (float(0), float(0))


def makeTrigEff(samples,lables,c,cut,trig,debug=False):
    sampleType = getSampleType(samples[0])
    name = "trigEff_"+sampleType+"_"+cut+"_"+trig
    print "Making",name

    if type(labels[0]) == type(1):
        # if sampleType=="NWS":
        #     bins = array.array('d',[255,265,275,285,295,305,495,505,695,705,895,905,1095,1105,1295])
        # else:
        #     bins = array.array('d',    [270,330,470,530,670,730,870,930,1070,1130,1270])
        #bins = array.array('d',[255,265,275,285,295,305,495,505,695,705,895,905,1095,1105,1295])
        bins = array.array('d',[250,270,330,470,530,670,730,870,930,1070,1130,1270])
        h=ROOT.TH1F(name,name,len(labels),bins)
    else:
        h=ROOT.TH1F()
        h.SetName(name)

    for label in labels:
        (eff,err) = getTrigEff(c[label],cut,trig)
        if label == "SMNR": label = "SM HH"
        if label == "allhad": label = "Hadronic t#bar{t}"
        if label == "nonallhad": label = "Semileptonic t#bar{t}"
        if debug: print label,cut,trig,eff
        h.Fill(label,eff)
        h.SetBinError(h.GetXaxis().FindBin(label),err)

    #h.LabelsDeflate("X")
    return h


def makeAcceptance(samples,labels,c,a,numer,denom):
    sampleType = getSampleType(samples[0])
    name = "acceptance_"+sampleType+"_"+numer+"_over_"+denom
    print "Making",name

    if type(labels[0]) == type(1):
        # if sampleType=="NWS":
        #     bins = array.array('d',[250,270,330,470,530,670,730,870,930,1070,1130,1270])
        # else:
        #     bins = array.array('d',    [270,330,470,530,670,730,870,930,1070,1130,1270])
        #bins = array.array('d',[255,265,275,285,295,305,495,505,695,705,895,905,1095,1105,1295])
        # if sampleType=="NWS_NLO":
        #     bins = array.array('d',[350,450,550,650,750,850,950,1050])
        # else:
        bins = array.array('d',[250,270,330,470,530,670,730,870,930,1070,1130,1270])
        h=ROOT.TH1F(name,name,len(labels),bins)
    else:
        h=ROOT.TH1F()
        h.SetName(name)

    for label in labels:
        d = 0
        if "all" in denom: d = a[label].GetBinContent(a[label].GetXaxis().FindBin(denom))
        else             : d = c[label].GetBinContent(c[label].GetXaxis().FindBin(denom))
        n  = c[label].GetBinContent(c[label].GetXaxis().FindBin(numer))
        ne = c[label].GetBinError  (c[label].GetXaxis().FindBin(numer))

        acceptance = 0
        error = 0
        if n and not d: acceptance = 1
        if n and     d: 
            acceptance = n/d
            error      = ne/d

        if label == "SMNR": label = "SM HH"
        h.Fill(label,acceptance)
        h.SetBinError(h.GetXaxis().FindBin(label),ne)

    #h.LabelsDeflate("X")
    return h



o=ROOT.TFile(out,"RECREATE")
o.cd()

sampleDict = {
              "RSG_c10":["M260","M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200"],
              "RSG_c20":["R260","R300","R400","R500","R600","R700","R800","R900","R1000","R1100","R1200"],
              "NWS":["H260","H300","H400","H500","H600","H700","H800","H900","H1000","H1100","H1200"],
              #"NWS_NLO":["N400","N500","N600","N700","N900","N1000"],
              "SMNR":["SMNR_MhhWeight"],
              "allhad":["allhad"],
              "nonallhad":["nonallhad"],
              #"ttbar":["allhad","nonallhad"],
              }


for key in sampleDict:
    samples = sampleDict[key]
    (labels,c,a) = getCutflows(samples)

    #make acceptance plots
    for i in range(len(cuts)):
        o.Append( makeAcceptance(samples,labels,c,a,cuts[i]       ,"all") )
        o.Append( makeAcceptance(samples,labels,c,a,cuts[i]+"_HLT","all") )
        for j in range(i+1,len(cuts)):
            o.Append( makeAcceptance(samples,labels,c,a,cuts[j]       ,cuts[i]) )
            o.Append( makeAcceptance(samples,labels,c,a,cuts[j]+"_HLT",cuts[i]) )
        # for trig in HLTs:
        #     numer = cut+"_"+trig
        #     o.Append( makeAcceptance(samples,labels,c,a,numer,"all") )
    o.Append( makeAcceptance(samples,labels,c,a,cuts[-1]+"_HLT",cuts[-1]) )

    #make trigger plots
    if key == "RSG_c20" or "had" in key: continue
    for cut in cuts:
        for trig in HLTs:
            o.Append( makeTrigEff(samples,labels,c,cut,trig) )
            if "passSignal" in cut and "SF" not in trig: o.Append( makeTrigEffMC(ScalarAllMCt, ScalarAllMCm, ScalarAllMCe, "NWS", cut, trig) )
        for trig in L1s:
            o.Append( makeTrigEff(samples,labels,c,cut,trig, True) )

    

o.Write()
o.Close()
