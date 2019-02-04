#import ROOT
# def get(rootFile, path):
#     obj = rootFile.Get(path)
#     if str(obj) == "<ROOT.TObject object at 0x(nil)>": 
#         rootFile.ls()
#         print 
#         print "ERROR: Object not found -", rootFile, path
#         sys.exit()

#     else: return obj

def w(outFile,line):
    outFile.write(line+" \n")

def round(n,d):
    return "%."+str(d)+"f" % float(n)

def read_mu_qcd_file(inFileName):
    inFile = open(inFileName,"r")
    outputDict = {}

    for line in inFile:
        words =  line.split()
        
        if not len(words): continue

        if not len(words) == 2: 
            print "Cannot parse",line
            continue

        outputDict[words[0]] = float(words[1])
    inFile.close()
    return outputDict

weightSet = "redo"
cut       = "PassHCdEta"

def psTagRate():
    f=open("psRateTable.tex","w")
    w(f,"\\begin{table}")
    w(f,"\\begin{center}")
    w(f,"\\begin{tabular}{l *2{S[round-mode=figures,round-precision=2]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1]} }")
    w(f,"\\toprule")
    w(f,"Iteration        & \\multicolumn{2}{c}{2015}         & \\multicolumn{2}{c}{2016} \\\\")
    for i in range(8):
        psr2015 = read_mu_qcd_file("XhhResolved/data/singleTagProb_FourTag_"+weightSet+"_2015_Nominal_"+str(i)+".txt")
        psr2016 = read_mu_qcd_file("XhhResolved/data/singleTagProb_FourTag_"+weightSet+"_2016_Nominal_"+str(i)+".txt")
        psrName = "singleTagProb_qcd_"+cut
        pseName = psrName+"_err"
        str2015 = str(psr2015[psrName])+" & "+str(psr2015[pseName])
        str2016 = str(psr2016[psrName])+" & "+str(psr2016[pseName])
        if not i:
            str2015 = "\\multicolumn{2}{S[round-mode=places,round-precision=2,table-format=1.2]}{"+str(psr2015[psrName])+"}"
            str2016 = "\\multicolumn{2}{S[round-mode=places,round-precision=2,table-format=1.2]}{"+str(psr2016[psrName])+"}"
            
        w(f,"\\midrule")
        w(f,str(i)+("        " if i else " (guess)")+"        & "+str2015+" & "+str2016+" \\\\")
    w(f,"\\bottomrule")
    w(f,"\\end{tabular}")
    w(f,"\\caption{Best fit pseudo-tag rate at each iteration of the reweighting. The values are not expected to be consistent between years due to the change in online \\btagging. Uncertainties are purely statistical.}")
    w(f,"\\label{tab:psTagRate}")
    w(f,"\\end{center}")
    w(f,"\\end{table}")

    f.close()

def nonallhadScale(doCR=False):
    cut="PassHCdEta"
    f=open("nonallhadScaleTable"+("CR" if doCR else "")+".tex","w")
    k2015 = read_mu_qcd_file("XhhResolved/data/mu_qcd_FourTag_"+weightSet+("_CR" if doCR else "")+"_2015_Nominal_7.txt")
    k2016 = read_mu_qcd_file("XhhResolved/data/mu_qcd_FourTag_"+weightSet+("_CR" if doCR else "")+"_2016_Nominal_7.txt")
    str2b2015 = str(k2015["mu_nonallhad2b_"+cut])+" & "+str(k2015["mu_nonallhad2b_"+cut+"_err"])
    str4b2015 = str(k2015["mu_nonallhad4b_"+cut])+" & "+str(k2015["mu_nonallhad4b_"+cut+"_err"])
    str2b2016 = str(k2016["mu_nonallhad2b_"+cut])+" & "+str(k2016["mu_nonallhad2b_"+cut+"_err"])
    str4b2016 = str(k2016["mu_nonallhad4b_"+cut])+" & "+str(k2016["mu_nonallhad4b_"+cut+"_err"])
    w(f,"\\begin{table}")
    w(f,"\\begin{center}")
    w(f,"\\begin{tabular}{l *2{S[round-mode=figures,round-precision=2,table-format=1.2]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.2]} }")
    w(f,"\\toprule")
    w(f,"        & \\multicolumn{2}{c}{2015}  & \\multicolumn{2}{c}{2016} \\\\")
    w(f,"\\midrule")
    w(f,"Two Tag        & "+str2b2015+" & "+str2b2016+" \\\\")
    w(f,"\\midrule")
    w(f,"Four Tag       & "+str4b2015+" & "+str4b2016+" \\\\")
    w(f,"\\bottomrule")
    w(f,"\\end{tabular}")
    w(f,"\\caption{Scale factors for the two and four tag nonallhadronic \\ttbar MC samples used for 2015 and 2016 data as measured in the "+("Sideband" if not doCR else "Control Region")+". Uncertainties are purely statistical}")
    w(f,"\\label{tab:nonallhadScale}")
    w(f,"\\end{center}")
    w(f,"\\end{table}")

    f.close()


def allhadFit(doCR=False):
    cut="PassHCdEta"
    f=open("allhadFitTable"+("CR" if doCR else "")+".tex","w")
    k2015 = read_mu_qcd_file("XhhResolved/data/mu_qcd_FourTag_"+weightSet+("_CR" if doCR else "")+"_2015_Nominal_7.txt")
    k2016 = read_mu_qcd_file("XhhResolved/data/mu_qcd_FourTag_"+weightSet+("_CR" if doCR else "")+"_2016_Nominal_7.txt")

    noError="\\multicolumn{2}{S[round-mode=places,round-precision=3,table-format=1.5]}"
    strPreFit2015  = noError+"{"+str(k2015["mu_qcd_prefit_"+cut])+"} & "+noError+"{"+str(k2015["mu_allhad_prefit_"+cut])+"}"
    strPreFit2016  = noError+"{"+str(k2016["mu_qcd_prefit_"+cut])+"} & "+noError+"{"+str(k2016["mu_allhad_prefit_"+cut])+"}"
    strPostFit2015 = str(k2015["mu_qcd_"+cut])+" & "+str(k2015["mu_qcd_"+cut+"_err"])+" & "+str(k2015["mu_allhad_"+cut])+" & "+str(k2015["mu_allhad_"+cut+"_err"])
    strPostFit2016 = str(k2016["mu_qcd_"+cut])+" & "+str(k2016["mu_qcd_"+cut+"_err"])+" & "+str(k2016["mu_allhad_"+cut])+" & "+str(k2016["mu_allhad_"+cut+"_err"])

    w(f,"\\begin{table}")
    w(f,"\\begin{center}")
    w(f,"\\begin{tabular}{l *1{S[round-mode=figures,round-precision=2,table-format=1.3]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.3]} \n"
                          +"*1{S[round-mode=figures,round-precision=2,table-format=1.1]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.1]} \n"
                          +"*1{S[round-mode=figures,round-precision=3,table-format=1.3]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.3]} \n"
                          +"*1{S[round-mode=figures,round-precision=2,table-format=1.1]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.1]} \n"
                           +"}")
    w(f,"\\toprule")
    w(f,"&                   \\multicolumn{4}{c}{2015}                                &                  \\multicolumn{4}{c}{2016} \\\\")
    w(f,"        & \\multicolumn{2}{c}{\\muqcd} & \\multicolumn{2}{c}{\\alphaAllhad} & \\multicolumn{2}{c}{\\muqcd}  & \\multicolumn{2}{c}{\\alphaAllhad} \\\\")
    w(f,"\\midrule")
    w(f,"Prefit  & "+strPreFit2015+" & "+strPreFit2016+" \\\\")
    w(f,"\\midrule")
    w(f,"Postfit & "+strPostFit2015+" & "+strPostFit2016+" \\\\")
    w(f,"\\bottomrule")
    w(f,"\\end{tabular}")
    w(f,"\\caption{Scale factors before and after the combined fit to the multijet, allhadronic \\ttbar and non-allhadronic \\ttbar enriched regions in the "+("Sideband" if not doCR else "Control Region")+"}")
    w(f,"\\label{tab:allhadFit"+("CR" if doCR else "")+"}")
    w(f,"\\end{center}")
    w(f,"\\end{table}")


# def everything(doCR=False):
#     cut="PassHCdEta"
#     f=open("everythingTable"+("CR" if doCR else "")+".tex","w")
#     k2015 = read_mu_qcd_file("XhhResolved/data/mu_qcd_FourTag_"+weightSet+("_CR" if doCR else "")+"_2015_Nominal_7.txt")
#     k2016 = read_mu_qcd_file("XhhResolved/data/mu_qcd_FourTag_"+weightSet+("_CR" if doCR else "")+"_2016_Nominal_7.txt")

#     w(f,"\\begin{table}")
#     w(f,"\\begin{center}")
#     w(f,"\\begin{tabular}{l *1{S[round-mode=figures,round-precision=2,table-format=1.3]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.3]} \n"
#                           +"*1{S[round-mode=figures,round-precision=2,table-format=1.1]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.1]} \n"
#                           +"*1{S[round-mode=figures,round-precision=3,table-format=1.3]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.3]} \n"
#                           +"*1{S[round-mode=figures,round-precision=2,table-format=1.1]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=1,table-format=1.1]} \n"
#                            +"}")
#     w(f,"\\toprule")
#     w(f,"&                   \\multicolumn{4}{c}{2015}                                &                  \\multicolumn{4}{c}{2016} \\\\")
#     w(f,"        & \\multicolumn{2}{c}{\\muqcd} & \\multicolumn{2}{c}{\\alphaAllhad} & \\multicolumn{2}{c}{\\muqcd}  & \\multicolumn{2}{c}{\\alphaAllhad} \\\\")
#     w(f,"\\midrule")
#     w(f,"Prefit  & "+strPreFit2015+" & "+strPreFit2016+" \\\\")
#     w(f,"\\midrule")
#     w(f,"Postfit & "+strPostFit2015+" & "+strPostFit2016+" \\\\")
#     w(f,"\\bottomrule")
#     w(f,"\\end{tabular}")
#     w(f,"\\caption{Scale factors before and after the combined fit to the multijet, allhadronic \\ttbar and non-allhadronic \\ttbar enriched regions in the "+("Sideband" if not doCR else "Control Region")+"}")
#     w(f,"\\label{tab:allhadFit"+("CR" if doCR else "")+"}")
#     w(f,"\\end{center}")
#     w(f,"\\end{table}")

psTagRate()
nonallhadScale()
nonallhadScale(True)
allhadFit()
allhadFit(True)






import sys
sys.path.insert(0, 'XhhResolved/plotting/')
import rootFiles
import ROOT

iteration="7"
nTuple="02-03-04"
year="2015"
inDir="hists_"+year+"_"+weightSet
rootFiles2015 = rootFiles.getFiles(iteration,nTuple,inDir,year)
year="2016"
inDir="hists_"+year+"_"+weightSet
rootFiles2016 = rootFiles.getFiles(iteration,nTuple,inDir,year)


class sample:
    def __init__(self, path, tag, scale = 1, error=0):
        f = ROOT.TFile(path,"read")
        self.path = path
        self.n_pm_e = {}
        self.n = {}
        self.e = {}
        self.cuts = ["Inclusive","PassHCdEta","PassAllhadVeto"]
        self.regions = ["Sideband","Control","Signal"]
        for cut in self.cuts:
            self.n_pm_e[cut] = {}
            self.n[cut] = {}
            self.e[cut] = {}
            for region in self.regions:
                h = f.Get(cut+"_"+tag+"Tag_"+region+"/dhh")
                h.Scale(scale)

                #make single bin to make integral and error easy with GetBinContent(1) and GetBinError(1)
                nBins = h.GetNbinsX()
                h.Rebin(nBins)

                n = h.GetBinContent(1)
                e = h.GetBinError(1)
                if error and region != "Sideband":#scale has an error, add it in quadrature. Error was derived in sideband, so don't double count
                    e = (e**2 + (n*error)**2)**0.5
                self.n[cut][region] = n
                self.e[cut][region] = e
                self.n_pm_e[cut][region] = str(self.n[cut][region])+" & "+str(self.e[cut][region])
                
                if "data" in self.path: #this doesn't have an error, it has been observed as a single value!
                    self.n_pm_e[cut][region] = "\\multicolumn{2}{S[round-mode=places,round-precision=0,table-format=5.0]}{"+str(self.n[cut][region])+"}"

                del h

    def addSample(self,otherSample):
        for cut in self.cuts:
            for region in self.regions:
                self.n[cut][region] += otherSample.n[cut][region]
                self.e[cut][region]  = (self.e[cut][region]**2 + otherSample.e[cut][region]**2)**0.5
                self.n_pm_e[cut][region] = str(self.n[cut][region])+" & "+str(self.e[cut][region])
                
                if "data" in self.path: #this doesn't have an error, it has been observed as a single value!
                    self.n_pm_e[cut][region] = "\\multicolumn{2}{S[round-mode=places,round-precision=0,table-format=5.0]}{"+str(self.n[cut][region])+"}"
                
def getTotal(nList,eList):
    n = sum(nList)
    e = 0.0
    for error in eList: e += error**2
    #add root(n) in quadrature to total error, ie gaussian error from total expected yield
    e += n
    e = e**0.5
    return str(n)+" & "+str(e)

class model:
    def __init__(self,rootFiles,kDict,kCut,fCut,year=None):#kCut is the cut used to get scale factors while fCut is the final analysis selection
        self.n = sample(rootFiles["nonallhad"]  ,"Four",kDict["mu_nonallhad4b_"+kCut],kDict["mu_nonallhad4b_"+kCut+"_err"])
        self.a = sample(rootFiles["allhadShape"],"Two" ,kDict["mu_allhad_"+kCut],     kDict["mu_allhad_"+kCut+"_err"])
        self.m = sample(rootFiles["qcd"]        ,"Two" ,kDict["mu_qcd_"+kCut],        kDict["mu_qcd_"+kCut+"_err"])
        self.d = sample(rootFiles["data"]       ,"Four")
        self.s = sample(rootFiles["SMNR_MhhWeight"]       ,"Four")
        self.year=year
        self.kCut=kCut
        self.fCut=fCut
        self.storeStrings()
        self.getTotals()

    def storeStrings(self):
        self.nSB, self.nCR, self.nSR = self.n.n_pm_e[self.fCut]["Sideband"], self.n.n_pm_e[self.fCut]["Control"], self.n.n_pm_e[self.fCut]["Signal"]
        self.aSB, self.aCR, self.aSR = self.a.n_pm_e[self.fCut]["Sideband"], self.a.n_pm_e[self.fCut]["Control"], self.a.n_pm_e[self.fCut]["Signal"]
        self.mSB, self.mCR, self.mSR = self.m.n_pm_e[self.fCut]["Sideband"], self.m.n_pm_e[self.fCut]["Control"], self.m.n_pm_e[self.fCut]["Signal"]
        self.dSB, self.dCR, self.dSR = self.d.n_pm_e[self.fCut]["Sideband"], self.d.n_pm_e[self.fCut]["Control"], self.d.n_pm_e[self.fCut]["Signal"]
        self.sSB, self.sCR, self.sSR = self.s.n_pm_e[self.fCut]["Sideband"], self.s.n_pm_e[self.fCut]["Control"], self.s.n_pm_e[self.fCut]["Signal"]

    def getTotals(self):
        self.tSB = getTotal([self.n.n[self.fCut]["Sideband"],
                             self.a.n[self.fCut]["Sideband"],
                             self.m.n[self.fCut]["Sideband"]], 
                            [self.n.e[self.fCut]["Sideband"],
                             self.a.e[self.fCut]["Sideband"],
                             self.m.e[self.fCut]["Sideband"]])
        self.tCR = getTotal([self.n.n[self.fCut]["Control"],
                             self.a.n[self.fCut]["Control"],
                             self.m.n[self.fCut]["Control"]], 
                            [self.n.e[self.fCut]["Control"],
                             self.a.e[self.fCut]["Control"],
                             self.m.e[self.fCut]["Control"]])
        self.tSR = getTotal([self.n.n[self.fCut]["Signal"],
                             self.a.n[self.fCut]["Signal"],
                             self.m.n[self.fCut]["Signal"]], 
                            [self.n.e[self.fCut]["Signal"],
                             self.a.e[self.fCut]["Signal"],
                             self.m.e[self.fCut]["Signal"]])

    def regionYieldsTable(self):
        f=open("regionYields"+self.year+".tex","w")
        w(f,"\\begin{table}")
        w(f,"\\begin{center}")
        w(f,"\\begin{tabular}{r *3{S[round-mode=places,round-precision=1,table-format=5.1]@{\\,$\\pm$\\,}S[round-mode=figures,round-precision=2]} }")
        w(f,"\\toprule")
        w(f,"                   & \\multicolumn{2}{c}{Sideband} &  \\multicolumn{2}{c}{Control} &   \\multicolumn{2}{c}{Signal} \\\\")
        w(f,"\\midrule")
        w(f," nonallhad \\ttbar & "+self.nSB+" & "+self.nCR+" & "+self.nSR+" \\\\")
        w(f,"    allhad \\ttbar & "+self.aSB+" & "+self.aCR+" & "+self.aSR+" \\\\")
        w(f,"  multijet         & "+self.mSB+" & "+self.mCR+" & "+self.mSR+" \\\\")
        w(f,"\\midrule")
        w(f,"     total         & "+self.tSB+" & "+self.tCR+" & "+self.tSR+" \\\\")
        w(f,"\\midrule")
        w(f,"   SM Non-resonant & "+self.sSB+" & "+self.sCR+" & "+self.sSR+" \\\\")
        w(f,"\\midrule")
       #w(f,"      data         & "+self.dSB+" & "+self.dCR+" &  \\multicolumn{2}{c}{Blinded} \\\\")
        w(f,"      data         & "+self.dSB+" & "+self.dCR+" & "+self.dSR+" \\\\")
        w(f,"\\bottomrule")
        w(f,"\\end{tabular}")
        w(f,"\\caption{Predicted and observed event yields in the Sideband, Control and Signal regions for the "+self.year+" data set. Uncertainties are purely statistical and include statistical precision of multijet and \\ttbar scale factors. The uncertainty on the total background includes $\sqrt{N}$ in quadrature.}")
        w(f,"\\label{tab:regionYields"+self.year+"}")
        w(f,"\\end{center}")
        w(f,"\\end{table}")
        f.close()

    def addYear(self,newYear):
        self.year+="+"+newYear.year
        self.n.addSample(newYear.n)
        self.a.addSample(newYear.a)
        self.m.addSample(newYear.m)
        self.d.addSample(newYear.d)
        self.s.addSample(newYear.s)
        self.storeStrings()
        self.getTotals()



def regionYields():
    k2015 = read_mu_qcd_file("XhhResolved/data/mu_qcd_FourTag_"+weightSet+"_2015_Nominal_7.txt")
    k2016 = read_mu_qcd_file("XhhResolved/data/mu_qcd_FourTag_"+weightSet+"_2016_Nominal_7.txt")

    kCut = "PassHCdEta"
    fCut = "PassAllhadVeto"

    model5 = model(rootFiles2015,k2015,kCut,fCut,"2015")
    model5.regionYieldsTable()

    model6 = model(rootFiles2016,k2016,kCut,fCut,"2016")
    model6.regionYieldsTable()

    #add together years and made another table
    model5.addYear(model6)
    model5.regionYieldsTable()



regionYields()
