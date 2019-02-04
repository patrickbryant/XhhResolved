import ROOT
from ROOT import TH1F, TCanvas, TPad
import sys
import os
import optparse
from plotTools import read_mu_qcd_file
import rootFiles

parser = optparse.OptionParser()
parser.add_option('-o', '--outFile',
                  dest="outFile",
                  default="hists-01-01-01/trigger",
                  )
parser.add_option('-v', '--nTuple',    dest="nTuple",     default="01-01-01", help="")
parser.add_option('-y', '--year',      dest="year",       default="2015", help="")

o, a = parser.parse_args()

#mu_qcd_dict = read_mu_qcd_file(o.mu)
#cutflow = "Loose"
#algo    = "DhhMin"
if not os.path.exists(o.outFile):
    os.makedirs(o.outFile)

outFile = ROOT.TFile(o.outFile+"/efficiencies_acceptances.root","RECREATE")

def get(rootFile, path):
    obj = rootFile.Get(path)
    if str(obj) == "<ROOT.TObject object at 0x(nil)>": 
        rootFile.ls()
        print 
        print "ERROR: Object not found -", rootFile, path
        sys.exit()

    else: return obj

def histCleanup(h):
    h.SetStats(0)
    h.GetXaxis().SetLabelFont(43)
    h.GetXaxis().SetLabelSize(16)
    h.GetYaxis().SetLabelFont(43)
    h.GetYaxis().SetLabelSize(16)
    h.GetXaxis().SetTitleFont(43)
    h.GetXaxis().SetTitleSize(20)
    h.GetYaxis().SetTitleFont(43)
    h.GetYaxis().SetTitleSize(20)
    h.GetXaxis().SetTitleOffset(2.8)
    h.GetYaxis().SetTitleOffset(1.6)



files = rootFiles.getFiles("0",o.nTuple,"hists",o.year)

masses=["M300","M400","M500","M600","M700","M800","M900","M1000","M1100","M1200","SMNR"]
#masses=["M300"]




f={}
c={}

if o.year == "2015":
    L1  = ["passL1",
           "L1_J100",
           "L1_4J20",
           "L1_3J25.0ETA23",
           "L1_4J15.0ETA25",
           "L1_J75_3J20"]
    HLT = ["passHLT",
           "HLT_j70_bmedium_3j70_L13J25.0ETA23",
           "HLT_2j35_btight_2j35_L13J25.0ETA23",
           "HLT_2j45_bmedium_2j45_L13J25.0ETA23",
           "HLT_j70_bmedium_3j70_L14J15.0ETA25",
           "HLT_2j35_btight_2j35_L14J15.0ETA25",
           "HLT_2j45_bmedium_2j45_L14J15.0ETA25",
           "HLT_j175_bmedium_j60_bmedium",
           "HLT_j100_2j55_bmedium",
           "HLT_j225_bloose",
           "HLT_ht850",
           "HLT_j70_bmedium_3j70_L13J25.0ETA23only",
           "HLT_2j35_btight_2j35_L13J25.0ETA23only",
           "HLT_2j45_bmedium_2j45_L13J25.0ETA23only",
           "HLT_j70_bmedium_3j70_L14J15.0ETA25only",
           "HLT_2j35_btight_2j35_L14J15.0ETA25only",
           "HLT_2j45_bmedium_2j45_L14J15.0ETA25only",
           "HLT_j175_bmedium_j60_bmediumonly",
           "HLT_j100_2j55_bmediumonly",
           "HLT_j225_blooseonly",
           "HLT_ht850only"]

if o.year == "2016":
    L1  = ["passL1",
           "L1_J100",
           "L1_4J20",
           "L1_3J25.0ETA23",
           "L1_4J15.0ETA25",
           "L1_J75_3J20"]
    HLT = ["passHLT",
           "HLT_j175_bmv2c2040_split",
           "HLT_j225_bmv2c2060_split",
           "HLT_j275_bmv2c2070_split",
           "HLT_j300_bmv2c2077_split",
           "HLT_j360_bmv2c2085_split",
           "HLT_j55_bmv2c2060_split_ht500_L14J15",
           "HLT_j65_bmv2c2070_split_3j65_L14J15",
           "HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25",
           "HLT_j75_bmv2c2077_split_3j75_L14J15",
           "HLT_j150_bmv2c2060_split_j50_bmv2c2060_split",
           "HLT_j100_2j55_bmv2c2060_split",
           "HLT_2j70_bmv2c2050_split_j70",
           "HLT_2j75_bmv2c2060_split_j75",
           "HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25",
           "HLT_2j55_bmv2c2060_split_ht300_L14J15",
           "HLT_2j45_bmv2c2077_split_3j45_L14J15.0ETA25",
           "HLT_ht850",
           "HLT_j175_bmv2c2040_splitonly",
           "HLT_j225_bmv2c2060_splitonly",
           "HLT_j275_bmv2c2070_splitonly",
           "HLT_j300_bmv2c2077_splitonly",
           "HLT_j360_bmv2c2085_splitonly",
           "HLT_j55_bmv2c2060_split_ht500_L14J15only",
           "HLT_j65_bmv2c2070_split_3j65_L14J15only",
           "HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25only",
           "HLT_j75_bmv2c2077_split_3j75_L14J15only",
           "HLT_j150_bmv2c2060_split_j50_bmv2c2060_splitonly",
           "HLT_j100_2j55_bmv2c2060_splitonly",
           "HLT_2j70_bmv2c2050_split_j70only",
           "HLT_2j75_bmv2c2060_split_j75only",
           "HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25only",
           "HLT_2j55_bmv2c2060_split_ht300_L14J15only",
           "HLT_2j45_bmv2c2077_split_3j45_L14J15.0ETA25only",
           "HLT_ht850only",
           ]
           

cuts = ["nSample",
        "nTuple",
        "ViewSelection",
        "JetCleaning",
        "nBJets",
        "PassM4j",
        "PassHCJetPt",
        "PassHCdRjj",
        "PassHCPt",
        "PassHCdEta",
        "PassHCdR",
        "Xhh"]

cutflows = ["Loose"]
truth=["","Right"]
for mass in masses:
    f[mass] = ROOT.TFile.Open(files[mass],"READ")

for cutflow in cutflows:
    for req in truth:
        for mass in masses:
            c[cutflow+req+mass] = get(f[mass],cutflow+"/DhhMin"+req+"/FourTag/CutFlow")


def makeHist(numer,denom, name):
    for cutflow in cutflows:
        for req in truth:
            # print cutflow
            # print truth
            # print name
            # print numer,"/",denom
            h_eff = ROOT.TH1F()
            h_eff.SetName(cutflow+req+"_"+name)
            h_eff.SetDirectory(0)
            h_RSG = ROOT.TH1F("RSG_"+cutflow+req+"_"+name,"RSG_"+cutflow+"_"+name,len(masses)-1,250,1250)
            h_RSG.SetDirectory(0)
            h_SMNR = ROOT.TH1F()
            h_SMNR.SetName("SMNR_"+cutflow+req+"_"+name)
            h_SMNR.SetDirectory(0)

            for mass in masses:
                nCut      = c[cutflow+req+mass].GetBinContent(c[cutflow+req+mass].GetXaxis().FindBin(denom))
                nCut_trig = c[cutflow+req+mass].GetBinContent(c[cutflow+req+mass].GetXaxis().FindBin(numer))
                eff_trig  = nCut_trig/nCut if nCut else 0.0
                h_eff.Fill(mass,eff_trig)
                bin = h_eff.GetXaxis().FindBin(mass)
                h_eff.SetBinError(bin,eff_trig/nCut_trig**0.5 if nCut_trig > 0 else 0.0)

                if "0" in mass:
                    h_RSG.Fill(float(mass.replace("M","")),eff_trig)
                    h_RSG.SetBinError(bin,eff_trig/nCut_trig**0.5 if nCut_trig > 0 else 0.0)
                else:
                    h_SMNR.Fill(mass,eff_trig)
                    h_SMNR.SetBinError(bin,eff_trig/nCut_trig**0.5 if nCut_trig > 0 else 0.0)

                #print mass.rjust(5),str(eff_trig)[:5].rjust(7)

            h_eff.LabelsDeflate("X")
            h_SMNR.LabelsDeflate("X")
            outFile.cd()
            h_eff.Write()
            h_RSG.Write()
            h_SMNR.Write()
            del h_eff
            del h_RSG
            del h_SMNR


for cut in cuts:
    for trig in L1:
        numer = cut+"_"+trig
        denom = cut
        makeHist(numer,denom,"TrigEff_numer_"+numer+"_denom_"+denom)
    for trig in HLT:
        numer = cut+"_"+trig
        denom = cut
        makeHist(numer,denom,"TrigEff_numer_"+numer+"_denom_"+denom)
        denom = cut+"_passL1"
        makeHist(numer,denom,"TrigEff_numer_"+numer+"_denom_"+denom)

for i in range(len(cuts)):
    numer = cuts[i]
    denom = cuts[0]
    makeHist(numer,denom,"Acceptance_numer_"+numer+"_denom_"+denom)
    numer = cuts[i]+"_"+L1[0]
    makeHist(numer,denom,"Acceptance_numer_"+numer+"_denom_"+denom)
    numer = cuts[i]+"_"+HLT[0]
    makeHist(numer,denom,"Acceptance_numer_"+numer+"_denom_"+denom)

outFile.Close()
