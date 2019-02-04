import optparse
parser = optparse.OptionParser()

parser.add_option('--inFile',          dest="inFile",                 default="", help="")
o, a = parser.parse_args()

import ROOT

thisFile = ROOT.TFile(o.inFile,"READ")
h_cutFlow     = thisFile.Get("FourTag/cutflow_weighted")#only sees events in nTuple
h_cutFlowRaw  = thisFile.Get("FourTag/cutflow")#only sees events in nTuple
h_allFlow     = thisFile.Get("hhEventBuilder/cutflow_weighted")#this is where the 'all' information lives
h_allFlowRaw  = thisFile.Get("hhEventBuilder/cutflow")#this is where the 'all' information lives

cuts=[
    'all',
    'execute', 
    'passHCJetSelection', 
    'passHCJetPairing', 
    'passHCPt', 
    'passHCdEta', 
    'passSignalBeforeAllhadVeto', 
    'passAllhadVeto', 
    'passSignal',
    ]


HLTs=[
     'HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25', 
     'HLT_j100_2j55_bmv2c2060_split', 
     'HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25',
     'HLT_j225_bmv2c2060_split', 
     'HLT', 
     ]

def getYeild(cutName):
    if cutName == "all":
        yeild    = h_allFlow   .GetBinContent(h_allFlow   .GetXaxis().FindBin(cut))
        yeildRAW = h_allFlowRaw.GetBinContent(h_allFlowRaw.GetXaxis().FindBin(cut))
    else:
        yeild    = h_cutFlow   .GetBinContent(h_cutFlow   .GetXaxis().FindBin(cut))
        yeildRAW = h_cutFlowRaw.GetBinContent(h_cutFlowRaw.GetXaxis().FindBin(cut))
    return yeild, yeildRAW

for cut in cuts:
        
    yeild, yeildRAW = getYeild(cut)

    print cut,"\t...",yeild,"(",yeildRAW,")"


    #for trig in HLTs:
    #    #o.Append( makeTrigEff(samples,labels,c,cut,trig) )
    #    print "\t",trig,"\t",h_cutFlow.GetBinContent(h_cutFlow.GetXaxis().FindBin(cut+"_"+trig))
