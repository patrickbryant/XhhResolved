def w(line):
    outFile.write(line+" \n")

# #-------------------------------------------------------------------------------------        
# cuts = ["All",
#         "PassGRL",
#         "Pass2DiJets",
#         "PassBJetSkim",
#         #"PassJetPt",
#         "PassDiJetPt",
#         "PassTrig",
#         "PassM4j",
#         "PassTTVeto"]

# massRegions = ["", "Sideband", "Control", "Signal"]

# cutLabels = {"All"         :"nTuple                 ",
#              "PassGRL"     :"GRL                    ",
#              "Pass2DiJets" :"$\geq$ 2 dijets        ",
#              "PassBJetSkim":"$\geq$ 4 bJets         ",
#              "PassJetPt"   :"Associated jet $p_{t}$ ",
#              "PassDiJetPt" :"dijet $p_{t}$          ",
#              "PassTrig"    :"Trigger                ",
#              "PassM4j"     :"MDCs                   ",
#              "PassTTVeto"  :"\\ttbar Veto           "}

# lumi = "3.50"
# nTuple = "hh4b-00-05-00"

# #-------------------------------------------------------------------------------------        
# def parseRootFile(rootFile, mu_qcd, mu_qcd_error, doWeighted = False, sample = ""):
#     import ROOT

#     f = ROOT.TFile(rootFile)

#     c = f.Get("CutFlow2bRaw")
#     qcdCutFlow = c.GetPrimitive("CutFlow2bRaw__data")
#     qcdCutFlow.Scale(mu_qcd)
#     c = f.Get("CutFlow4bRaw")
#     dataCutFlow = c.GetPrimitive("CutFlow4bRaw__data")

#     qcdCount = {}
#     qcdError = {}
#     dataCount = {}
#     dataError = {}
#     for massRegion in massRegions:
#         for cut in cuts:
#             bin = qcdCutFlow.GetXaxis().FindBin(cut+massRegion)
#             qcdCount[cut+massRegion] = qcdCutFlow.GetBinContent(bin)
#             # for now calculate error on QCD prediction using mu_qcd_error/mu_qcd calculated by makeWeights.py
#             qcdError[cut+massRegion] = qcdCount[cut+massRegion] * mu_qcd_error/mu_qcd

#             bin = dataCutFlow.GetXaxis().FindBin(cut+massRegion)
#             dataCount[cut+massRegion] = dataCutFlow.GetBinContent(bin) if cut != "Pass2DiJets" else qcdCount[cut+massRegion]*(1/mu_qcd)
#             dataError[cut+massRegion] = dataCutFlow.GetBinError(bin)   if cut != "Pass2DiJets" else qcdCutFlow.GetBinError(bin)*(1/mu_qcd)

#     return (dataCount,dataError,qcdCount,qcdError)

# #-------------------------------------------------------------------------------------        
# def compareDataMC(dataCount, ttbarCount = {}):
#     #cut flow table, data compared to signal and ttbar samples
#     tableList = []
#     tableList.append("\\begin{table}")
#     tableList.append("\\begin{center}")
#     tableList.append("\\begin{tabular}{ l | c | c | c | c }")
#     tableList.append("Cut & Data & $M_{G} = 500$ & $M_{G} = 1000$ & \\ttbar  \\\\")
#     tableList.append("\\hline\\hline")
#     #tableList.append("& & & \\\\")
#     if not ttbarCount:
#         for cut in cuts:
#             tableList.append(cutLabels[cut]+"& "+str(int(dataCount[cut]))+" & -- & -- & -- \\\\")
#     else:
#         for cut in cuts:
#             tableList.append(cutLabels[cut]+"& "+str(int(dataCount[cut]))+" & -- & -- & "+str(int(ttbarCount[cut]))+" \\\\")

#     #tableList.append("& & & \\\\")
#     tableList.append("\\hline\\hline")
#     tableList.append("\\end{tabular}")
#     tableList.append("\\caption{Made with "+lumi+"$fb^{-1}$ and nTuple "+nTuple+".")
#     tableList.append("          Signal region blinded after requiring at least")
#     tableList.append("          two dijets.}")
#     tableList.append("\\label{tab:cutFlowMCcomp}")
#     tableList.append("\\end{center}")
#     tableList.append("\\end{table}")

#     return tableList

# #-------------------------------------------------------------------------------------        
# def cutFlow4bMassRegions(dataCount):
#     #cut flow table, data in sideband, control and signal
#     tableList = []
#     tableList.append("\\begin{table}")
#     tableList.append("\\begin{center}")
#     tableList.append("\\begin{tabular}{ l | c | c | c }")
#     tableList.append("Cut & Sideband & Control & Signal  \\\\")
#     tableList.append("\\hline\\hline")
#     #tableList.append("& & & \\\\")
#     for cut in cuts:
#         if dataCount[cut+"Sideband"] == 0: sideband = str(int(dataCount[cut]))
#         else: sideband = str(int(dataCount[cut+"Sideband"]))
#         if dataCount[cut+"Control" ] == 0: control  = str(int(dataCount[cut]))
#         else: control  = str(int(dataCount[cut+"Control"]))
#         if dataCount[cut+"Signal"  ] == 0: signal   = str(int(dataCount[cut]))
#         else: 
#             print "WARNING: UNBLINDED for cut",cut
#             signal = str(int(dataCount[cut+"Signal"]))

#         if sideband == control:
#             tableList.append(cutLabels[cut]+"& \\multicolumn{3}{c}{--- "+sideband+" ---} \\\\")
#         else:
#             tableList.append(cutLabels[cut]+"& "+sideband+" & "+control+" & Blinded \\\\")

#     #tableList.append("& & & \\\\")
#     tableList.append("\\hline\\hline")
#     tableList.append("\\end{tabular}")
#     tableList.append("\\caption{Made with "+lumi+"$fb^{-1}$ and nTuple "+nTuple+".")
#     tableList.append("          Signal region blinded after requiring at least")
#     tableList.append("          two dijets.}")
#     tableList.append("\\label{tab:cutFlow}")
#     tableList.append("\\end{center}")
#     tableList.append("\\end{table}")

#     return tableList

# #-------------------------------------------------------------------------------------        
# def cutFlowQCDMassRegions(qcdCount, mu_qcd, mu_qcd_error):
#     #cut flow table, qcd in sideband, control, signal
#     tableList = []
#     tableList.append("\\begin{table}")
#     tableList.append("\\begin{center}")
#     tableList.append("\\begin{tabular}{ l | c | c | c }")
#     tableList.append("Cut & Sideband & Control & Signal  \\\\")
#     tableList.append("\\hline\\hline")
#     #tableList.append("& & & \\\\")
#     for cut in cuts:
#         if qcdCount[cut+"Sideband"] == 0: sideband = str(int(qcdCount[cut]))
#         else: sideband = str(int(qcdCount[cut+"Sideband"]))
#         if qcdCount[cut+"Control" ] == 0: control  = str(int(qcdCount[cut]))
#         else: control  = str(int(qcdCount[cut+"Control"]))
#         if qcdCount[cut+"Signal"  ] == 0: signal   = str(int(qcdCount[cut]))
#         else: signal   = str(int(qcdCount[cut+"Signal"]))

#         if sideband == control:
#             tableList.append(cutLabels[cut]+"& \\multicolumn{3}{c}{--- "+sideband+" ---} \\\\")
#         else:
#             tableList.append(cutLabels[cut]+"& "+sideband+" & "+control+" & "+signal+" \\\\")


#     #tableList.append("& & & \\\\")
#     tableList.append("\\hline\\hline")
#     tableList.append("\\end{tabular}")
#     tableList.append("\\caption{Made with "+lumi+"$fb^{-1}$ and nTuple "+nTuple+".")
#     tableList.append("          Shows QCD prediction through cut flow. Divide by $\\mu_{QCD}$ to get the 2-tag region event count.")
#     tableList.append("          $\\mu_{QCD} = " + str(float(int(mu_qcd*100000))/100000) + " \pm " + str(float(int(mu_qcd_error/mu_qcd*1000))/10) + "\% $}" )
#     tableList.append("\\label{tab:cutFlowQCD}")
#     tableList.append("\\end{center}")
#     tableList.append("\\end{table}")

#     return tableList


#-------------------------------------------------------------------------------------        
import ROOT

def round(n,d):
    return str(int(n*10**d)/float(10**d))


def get(rootFile, path):
    obj = rootFile.Get(path)
    if str(obj) == "<ROOT.TObject object at 0x(nil)>": 
        rootFile.ls()
        print 
        print "ERROR: Object not found -", rootFile, path
        sys.exit()

    else: return obj

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
    return outputDict

#def bkgComposition(qcdCount,qcdError,dataCount,dataError, ttbarCount = {}, ttbarError = {}):
def bkgComposition(data,ttbar,mu_qcd_file,unblinded):
    # get 2b data count, 4b ttbar count, 4b data count for each region
    mu_qcd = read_mu_qcd_file(mu_qcd_file)

    regions=["Sideband","Control","Signal"]
    f_data  = ROOT.TFile.Open(data,"READ")
    f_ttbar = ROOT.TFile.Open(ttbar,"READ")

    
    h_4bdata = {}
    h_2bdata = {}
    h_4bttbar= {}
    h_2bttbar= {}
    
    n_4bdata = {}
    n_2bdata = {}
    n_4bttbar= {}
    n_2bttbar= {}

    for region in regions:
        print region
        h_4bdata[region] = f_data.Get("Loose/DhhMin/FourTag/"+region+"/hCandDeta")
        h_4bdata[region].SetName("4bdata"+region)
        n_4bdata[region] = h_4bdata[region].Integral() 
        print "4bdata",h_4bdata[region],n_4bdata[region]

        h_2bdata[region] = f_data.Get("Loose/DhhMin/TwoTag/"+region+"/hCandDeta")
        h_2bdata[region].SetName("2bdata"+region)
        n_2bdata[region] = h_2bdata[region].Integral() 
        print "2bdata",h_2bdata[region],n_2bdata[region]

        h_4bttbar[region] = f_ttbar.Get("Loose/DhhMin/FourTag/"+region+"/hCandDeta")
        h_4bttbar[region].SetName("4bttbar"+region)
        n_4bttbar[region] = h_4bttbar[region].Integral() 
        print "4bttbar",h_4bttbar[region],n_4bttbar[region]

        h_2bttbar[region] = f_ttbar.Get("Loose/DhhMin/TwoTag/"+region+"/hCandDeta")
        h_2bttbar[region].SetName("2bttbar"+region)
        n_2bttbar[region] = h_2bttbar[region].Integral() 
        print "2bttbar",h_2bttbar[region],n_2bttbar[region]

    # calculate QCD from 2b data, mu_qcd and 2b ttbar
    n_qcd = {}
    for region in regions:
        n_qcd[region] = (n_2bdata[region] - n_2bttbar[region]) * mu_qcd["mu_qcd_LooseDhhMin"]

    # calculate statistical error on n_qcd and n_ttbar. Comes from fractional error on mu_qcd and mu_ttbar
    qcd_err   = {}
    ttbar_err = {}
    data_err  = {}
    for region in regions:
        if region == "Sideband":
            qcd_err[region]   = n_qcd[region] * mu_qcd["mu_qcd_LooseDhhMin_err"]/mu_qcd["mu_qcd_LooseDhhMin"]
            ttbar_err[region] = n_4bttbar[region] * mu_qcd["mu_ttbar_LooseDhhMin_err"]/mu_qcd["mu_ttbar_LooseDhhMin"]
        else:
            qcd_err[region]   = ((n_qcd[region] * mu_qcd["mu_qcd_LooseDhhMin_err"]/mu_qcd["mu_qcd_LooseDhhMin"])**2 + n_qcd[region])**0.5
            ttbar_err[region] = ((n_4bttbar[region] * mu_qcd["mu_ttbar_LooseDhhMin_err"]/mu_qcd["mu_ttbar_LooseDhhMin"])**2 + n_4bttbar[region])**0.5
        data_err[region]  = n_4bdata[region] ** 0.5

    # Background prediction table
    tableList = []
    tableList.append("\\begin{tabular}{ l | c | c | c  }")
    tableList.append("Sample & Sideband Region & Control Region & Signal Region  \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("& & & \\\\")
    
    qcd = " & ".join([str(int(n_qcd["Sideband"]))+" $\\pm$ "+str(int(qcd_err["Sideband"])),
                      str(int(n_qcd["Control" ]))+" $\\pm$ "+str(int(qcd_err["Control" ])),                      
                      str(int(n_qcd["Signal"  ]))+" $\\pm$ "+str(int(qcd_err["Signal"  ])) ])

    tableList.append("QCD          & "+qcd+"\\\\")
    ttbar = " & ".join([str(int(n_4bttbar["Sideband"]))+" $\\pm$ "+str(float(int(ttbar_err["Sideband"]*10))/10),
                        str(int(n_4bttbar["Control" ]))+" $\\pm$ "+str(float(int(ttbar_err["Control" ]*10))/10),                      
                        str(int(n_4bttbar["Signal"  ]))+" $\\pm$ "+str(float(int(ttbar_err["Signal"  ]*10))/10) ])

    tableList.append("\\ttbar      & "+ttbar+"\\\\")

    #tableList.append("Z+jets       & -- & -- & -- \\\\")
    tableList.append("& & & \\\\")

    total_SR     = n_4bttbar["Signal"]+n_qcd["Signal"]
    total_err_SR = (ttbar_err["Signal"]**2 + qcd_err["Signal"]**2)**0.5
    total_CR     = n_4bttbar["Control"]+n_qcd["Control"]
    total_err_CR = (ttbar_err["Control"]**2 + qcd_err["Control"]**2)**0.5
    total_SB     = n_4bttbar["Sideband"]+n_qcd["Sideband"]
    total_err_SB = (ttbar_err["Sideband"]**2 + qcd_err["Sideband"]**2)**0.5

    tableList.append("Total        & "+round(total_SB,1)+" $\\pm$ "+round(total_err_SB,1)+" & "+round(total_CR,1)+" $\\pm$ "+round(total_err_CR,1)+" & "+round(total_SR,1)+" $\\pm$ "+round(total_err_SR,1)+" \\\\")

    tableList.append("& & & \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("& & & \\\\")

    data = " & ".join([str(int(n_4bdata["Sideband"]))+" $\\pm$ "+str(float(int(data_err["Sideband"]*10))/10),
                       str(int(n_4bdata["Control" ]))+" $\\pm$ "+str(float(int(data_err["Control" ]*10))/10),
                       str(int(n_4bdata["Signal"  ]))+" $\\pm$ "+str(float(int(data_err["Signal"  ]*10))/10) if unblinded else "Blinded"])

    tableList.append("Data         & "+data+"\\\\")
    tableList.append("& & & \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")

    return tableList

#-------------------------------------------------------------------------------------        
def bkgSR(data,ttbar,mu_qcd_file,SR,unblinded):
    # get 2b data count, 4b ttbar count, 4b data count for each region
    mu_qcd = read_mu_qcd_file(mu_qcd_file)

    regions = ["Signal"+SR]
    Blind=not unblinded
    if SR: Blind = False
    f_data  = ROOT.TFile.Open(data,"READ")
    f_ttbar = ROOT.TFile.Open(ttbar,"READ")

    h_4bdata = {}
    h_2bdata = {}
    h_4bttbar= {}
    h_2bttbar= {}
    
    n_4bdata = {}
    n_2bdata = {}
    n_4bttbar= {}
    n_2bttbar= {}

    for region in regions:
        print region
        h_4bdata[region] = f_data.Get("Loose/DhhMin/FourTag/"+region+"/hCandDeta")
        h_4bdata[region].SetName("4bdata"+region)
        n_4bdata[region] = h_4bdata[region].Integral() 
        print "4bdata",h_4bdata[region],n_4bdata[region]

        h_2bdata[region] = f_data.Get("Loose/DhhMin/TwoTag/"+region+"/hCandDeta")
        h_2bdata[region].SetName("2bdata"+region)
        n_2bdata[region] = h_2bdata[region].Integral() 
        print "2bdata",h_2bdata[region],n_2bdata[region]

        h_4bttbar[region] = f_ttbar.Get("Loose/DhhMin/FourTag/"+region+"/hCandDeta")
        h_4bttbar[region].SetName("4bttbar"+region)
        n_4bttbar[region] = h_4bttbar[region].Integral() 
        print "4bttbar",h_4bttbar[region],n_4bttbar[region]

        h_2bttbar[region] = f_ttbar.Get("Loose/DhhMin/TwoTag/"+region+"/hCandDeta")
        h_2bttbar[region].SetName("2bttbar"+region)
        n_2bttbar[region] = h_2bttbar[region].Integral() 
        print "2bttbar",h_2bttbar[region],n_2bttbar[region]

    # calculate QCD from 2b data, mu_qcd and 2b ttbar
    n_qcd = {}
    for region in regions:
        n_qcd[region] = (n_2bdata[region] - n_2bttbar[region]) * mu_qcd["mu_qcd_LooseDhhMin"]

    # calculate statistical error on n_qcd and n_ttbar. Comes from fractional error on mu_qcd and mu_ttbar
    qcd_err   = {}
    ttbar_err = {}
    data_err  = {}
    for region in regions:
        qcd_err[region]   = ((n_qcd[region] * mu_qcd["mu_qcd_LooseDhhMin_err"]/mu_qcd["mu_qcd_LooseDhhMin"])**2 + n_qcd[region])**0.5
        ttbar_err[region] = ((n_4bttbar[region] * mu_qcd["mu_ttbar_LooseDhhMin_err"]/mu_qcd["mu_ttbar_LooseDhhMin"])**2 + n_4bttbar[region])**0.5
        data_err[region]  = n_4bdata[region] ** 0.5

    # Background prediction table
    tableList = []
    tableList.append("\\begin{tabular}{ l | c }")
    tableList.append("Sample & Signal Region  \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("& \\\\")
    
    qcd = " & ".join([str(int(n_qcd[regions[0]]))+" $\\pm$ "+str(int(qcd_err[regions[0]])) ])

    tableList.append("QCD          & "+qcd+"\\\\")
    ttbar = " & ".join([str(int(n_4bttbar[regions[0]]))+" $\\pm$ "+str(float(int(ttbar_err[regions[0]]*10))/10) ])

    tableList.append("\\ttbar      & "+ttbar+"\\\\")
    tableList.append("& \\\\")
    total     = n_4bttbar[regions[0]]+n_qcd[regions[0]]
    total_err = (ttbar_err[regions[0]]**2 + qcd_err[regions[0]]**2)**0.5
    tableList.append("Total        & "+str(int(total))+" $\\pm$ "+str(float(int(total_err)*10)/10)+" \\\\")
    tableList.append("& \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("& \\\\")

    data = " & ".join(["Blinded"])
    if unblinded: data= " & ".join([str(n_4bdata[regions[0]])+" $\\pm$ "+str(float(int(data_err[regions[0]])*10)/10)])

    tableList.append("Data         & "+data+"\\\\")
    tableList.append("& \\\\")
    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")

    return tableList

#-------------------------------------------------------------------------------------        



def compareDataMC(data,SMNR,m300,m700,m1100,ttbar,unblinded):
    f_data  = ROOT.TFile.Open(data, "READ")
    f_SMNR  = ROOT.TFile.Open(SMNR, "READ")
    f_m300  = ROOT.TFile.Open(m300, "READ")
    f_m700  = ROOT.TFile.Open(m700, "READ")
    f_m1100 = ROOT.TFile.Open(m1100,"READ")
    f_ttbar = ROOT.TFile.Open(ttbar,"READ")

    c_data  = get(f_data, "Loose/DhhMin/FourTag/CutFlow")
    c_SMNR  = get(f_SMNR, "Loose/DhhMin/FourTag/CutFlow")
    c_m300  = get(f_m300, "Loose/DhhMin/FourTag/CutFlow")
    c_m700  = get(f_m700, "Loose/DhhMin/FourTag/CutFlow")
    c_m1100 = get(f_m1100,"Loose/DhhMin/FourTag/CutFlow")
    c_ttbar = get(f_ttbar,"Loose/DhhMin/FourTag/CutFlow")

    cuts = ["nSample",
            "nTuple",
            "ViewSelection_passHLT",
            "JetCleaning_passHLT",
            "nBJets_passHLT",
#            "PassHCJetPt_passHLT",
            "PassHCdRjj_passHLT",
            "PassHCPt_passHLT",
            "PassHCdEta_passHLT",
            "PassHCdR_passHLT",
            "Xhh_passHLT"]

    n_data  = []
    n_SMNR  = []
    n_m300  = []
    n_m700  = []
    n_m1100 = []
    n_ttbar = []

    for i in range(len(cuts)):
        n_data .append(c_data .GetBinContent(c_data .GetXaxis().FindBin(cuts[i])))
        if "Xhh" in cuts[i] and not unblinded:
            n_data[i] = "BLINDED"
        if "nSample" in cuts[i]:
            n_data[i] = " -- "
        n_SMNR .append(c_SMNR .GetBinContent(c_SMNR .GetXaxis().FindBin(cuts[i]))*(0.577**2))
        n_m300 .append(c_m300 .GetBinContent(c_m300 .GetXaxis().FindBin(cuts[i]))*(0.577**2))
        n_m700 .append(c_m700 .GetBinContent(c_m700 .GetXaxis().FindBin(cuts[i]))*(0.577**2))
        n_m1100.append(c_m1100.GetBinContent(c_m1100.GetXaxis().FindBin(cuts[i]))*(0.577**2))
        n_ttbar.append(c_ttbar.GetBinContent(c_ttbar.GetXaxis().FindBin(cuts[i])))

    cutNames = ["Derivation",
                "nTuple",
                "Trigger",
                "JetCleaning",
                "$\\geq$ 4 $b$-jets",
#                "HC jet p$_{T}$",
                "HC $\\Delta$R$(j,j)$",
                "HC p$_{T}$",
                "$\\Delta\\eta($HC,HC$)$",
                "$\\Delta$R$($HC,HC$)$",
                "X$_{hh}$"]

    #cut flow table, data compared to signal and ttbar samples
    tableList = []
    tableList.append("\\begin{tabular}{ l | c | c | c | c | c | c }")
    tableList.append("Cut & Data & SM di$-$higgs & $M_{G} = 300$ GeV & $M_{G} = 700$ GeV & $M_{G} = 1100$ GeV & \\ttbar  \\\\")
    tableList.append("\\hline\\hline")

    for i in range(len(cuts)):
        ndata = str(int(n_data[i])) if type(1.) == type(n_data[i]) else n_data[i]
        nSMNR = round(n_SMNR[i],1) if type(1.) == type(n_SMNR[i]) else n_SMNR[i]
        n300  = round(n_m300[i],1) if type(1.) == type(n_m300[i]) else n_m300[i]
        n700  = round(n_m700[i],1) if type(1.) == type(n_m700[i]) else n_m700[i]
        n1100  = round(n_m1100[i],1) if type(1.) == type(n_m1100[i]) else n_m1100[i]
        nttbar  = round(n_ttbar[i],1) if type(1.) == type(n_ttbar[i]) else n_ttbar[i]
        tableList.append(cutNames[i]+" & "+ndata+" & "+nSMNR+" & "+n300+" & "+n700+" & "+n1100+" & "+nttbar+" \\\\")

    tableList.append("\\hline\\hline")
    tableList.append("\\end{tabular}")

    return tableList
