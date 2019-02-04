import ROOT
import sys
import os
import optparse

parser = optparse.OptionParser()


parser.add_option('-i', '--in',
                  dest="inFile",
                  default=""
                  )

o, a = parser.parse_args()

def get(rootFile, path):
    obj = rootFile.Get(path)
    if str(obj) == "<ROOT.TObject object at 0x(nil)>": 
        rootFile.ls()
        print 
        print "ERROR: Object not found -", rootFile, path
        sys.exit()

    else: return obj

f=ROOT.TFile(o.inFile,"read")

btagSFnames=["",
             "FT_EFF_Eigen_B_0__1down",
             "FT_EFF_Eigen_B_0__1up",
             "FT_EFF_Eigen_B_1__1down",
             "FT_EFF_Eigen_B_1__1up",
             "FT_EFF_Eigen_B_2__1down",
             "FT_EFF_Eigen_B_2__1up",
             "FT_EFF_Eigen_B_3__1down",
             "FT_EFF_Eigen_B_3__1up",
             "FT_EFF_Eigen_B_4__1down",
             "FT_EFF_Eigen_B_4__1up",
             "FT_EFF_Eigen_C_0__1down",
             "FT_EFF_Eigen_C_0__1up",
             "FT_EFF_Eigen_C_1__1down",
             "FT_EFF_Eigen_C_1__1up",
             "FT_EFF_Eigen_C_2__1down",
             "FT_EFF_Eigen_C_2__1up",
             "FT_EFF_Eigen_C_3__1down",
             "FT_EFF_Eigen_C_3__1up",
             "FT_EFF_Eigen_Light_0__1down",
             "FT_EFF_Eigen_Light_0__1up",
             "FT_EFF_Eigen_Light_1__1down",
             "FT_EFF_Eigen_Light_10__1down",
             "FT_EFF_Eigen_Light_10__1up",
             "FT_EFF_Eigen_Light_11__1down",
             "FT_EFF_Eigen_Light_11__1up",
             "FT_EFF_Eigen_Light_12__1down",
             "FT_EFF_Eigen_Light_12__1up",
             "FT_EFF_Eigen_Light_13__1down",
             "FT_EFF_Eigen_Light_13__1up",
             "FT_EFF_Eigen_Light_2__1down",
             "FT_EFF_Eigen_Light_2__1up",
             "FT_EFF_Eigen_Light_3__1down",
             "FT_EFF_Eigen_Light_3__1up",
             "FT_EFF_Eigen_Light_4__1down",
             "FT_EFF_Eigen_Light_4__1up",
             "FT_EFF_Eigen_Light_5__1down",
             "FT_EFF_Eigen_Light_5__1up",
             "FT_EFF_Eigen_Light_6__1down",
             "FT_EFF_Eigen_Light_6__1up",
             "FT_EFF_Eigen_Light_7__1down",
             "FT_EFF_Eigen_Light_7__1up",
             "FT_EFF_Eigen_Light_8__1down",
             "FT_EFF_Eigen_Light_8__1up",
             "FT_EFF_Eigen_Light_9__1down",
             "FT_EFF_Eigen_Light_9__1up",
             "FT_EFF_extrapolation__1down",
             "FT_EFF_extrapolation__1up",
             "FT_EFF_extrapolation_from_charm__1down",
             "FT_EFF_extrapolation_from_charm__1up",
             ]


h = get(f,"Loose/DhhMin/FourTag/Signal/m4j_l")
n = h.Integral()
print "Nominal Yield:",n

e = 0

for s in range(1,50):
    var = "m4j_l_SF"+str(s)

    h = get(f,"Loose/DhhMin/FourTag/Signal/"+var)
    v = h.Integral()
    print btagSFnames[s].ljust(45),v,abs(n-v)/n

    e+= (n-v)**2

e = e**0.5
print "b-tagging"
print "Error:",e
print "Fractional Error:",e/n

f.Close()

syst=["XhhMiniNtupleResolved_JET_GroupedNP_1__1up",
      "XhhMiniNtupleResolved_JET_GroupedNP_1__1down", 
      "XhhMiniNtupleResolved_JET_GroupedNP_2__1up",
      "XhhMiniNtupleResolved_JET_GroupedNP_2__1down",
      "XhhMiniNtupleResolved_JET_GroupedNP_3__1up",
      "XhhMiniNtupleResolved_JET_GroupedNP_3__1down",
      "XhhMiniNtupleResolved_JET_JER_SINGLE_NP__1up",
      "XhhMiniNtupleResolved_JET_EtaIntercalibration_NonClosure__1up",
      "XhhMiniNtupleResolved_JET_EtaIntercalibration_NonClosure__1down"]

e_JET=0
e_JES=0
e_JER=0
for s in syst:
    f = ROOT.TFile(o.inFile.replace("_20","_"+s+"_20"),"read")
    
    h = get(f, "Loose/DhhMin/FourTag/Signal/m4j_l")
    v = h.Integral()
    print s.ljust(45),v,abs(n-v)/n

    if "JER" in s: e_JER+=(n-v)**2
    else:          e_JES+=(n-v)**2

    e_JET+=(n-v)**2
    f.Close()

e_JET=e_JET**0.5
e_JER=e_JER**0.5
e_JES=e_JES**0.5

print "JES/JER"
print "JES",e_JES,e_JES/n
print "JER",e_JER,e_JER/n
print "Error:",e_JET
print "Fractional Error:",e_JET/n
print "---------------------------"
print "Total Error:",(e**2+e_JET**2)**0.5
print "Total Fractional Error:",(e**2+e_JET**2)**0.5/n
    
