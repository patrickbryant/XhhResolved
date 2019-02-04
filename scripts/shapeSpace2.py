import sys
import time
sys.path.insert(0, 'XhhResolved/plotting/')
from plotTools import plot, read_mu_qcd_file, do_variable_rebinning
import ROOT
ROOT.Math.IntegratorOneDimOptions.SetDefaultIntegrator("Gauss")
from setupConfig import setGRL, setLumi, setRegions, setTagger
import rootFiles
import os
import optparse
import random
import math
parser = optparse.OptionParser()

parser.add_option('--outDir',         dest="outDir",                default="Plots-01-01-01/", help="")
parser.add_option('--inDir',          dest="inDir",                 default="hists", help="")
parser.add_option('-c', '--cut',    dest="cut",     default="PassHCdEta", help="")
parser.add_option('--variation',     dest="variation",     default="Nominal", help="")
parser.add_option('-i', '--iter',    dest="iteration",     default="0", help="")
parser.add_option('-v', '--nTuple',    dest="nTuple",     default="01-01-01", help="")
parser.add_option('-y', '--year',    dest="year",     default="2015", help="")
parser.add_option('--weights',   dest="weights",   default="")
parser.add_option('--threeTag',  dest="threeTag",  action="store_true", default=False)
parser.add_option('--limitFile', dest="limitFile", default="")

o, a = parser.parse_args()

###########
## Setup ##
###########
(leadMass_SR, sublMass_SR, radius_SR, radius_CR, radius_SB, inner_SB, CR_shift, SB_shift, doTightQCDTag, doLooseQCDTag, leadHCmassCut, sublHCmassCut, DhhCut) = setRegions(o.variation)

outDir = o.outDir
blind = True
if o.year == "2016": lumi = "24.3 fb^{-1}"

iteration = o.iteration

if o.threeTag: 
    tag = "Three"
else:
    tag = "Four"

if os.path.exists(o.limitFile):
    limitFile = ROOT.TFile.Open(o.limitFile, "UPDATE")
else:
    limitFile = ROOT.TFile.Open(o.limitFile, "RECREATE")

files = rootFiles.getFiles(iteration,o.nTuple, o.inDir, o.year)
muFile = "XhhResolved/data/mu_qcd_"+tag+"Tag_"+o.weights+"_"+o.year+"_"+o.variation+"_"+iteration+".txt"
mu_qcd_dict = read_mu_qcd_file(muFile)

rebins={}
#rebins["m4j_cor_l"] = [100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,
#                       500,520,540,560,580,600,640,680,720,820,900,1000,1500]
#rebins["m4j_cor_l"] = [100,250,270,290,330,360,400,450,510,580,680,800,1000,1500]
rebins["m4j_cor_l"] = [100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,
                   500,520,540,560,580,600,640,680,720,820,900,1000,1200]

# rebins["m4j_cor_l"] = [100,250,270,350,430,
#                       510,590,730,1200]

#rebins["m4j_cor_l"] = [100,250,270,290,330,360,450,580,800,1500]

#rebins["m4j_cor_l"] = [100,250,290,330,360,400,460,530,610,720,850,1500]

#get files
f_data  = ROOT.TFile(files["data"])
f_qcd   = ROOT.TFile(files["qcd"])
f_allhad = ROOT.TFile(files["allhadShape"])
f_nonallhad = ROOT.TFile(files["nonallhad"])


#get hists
regions = ["Sideband","Control","Signal","LMVR","HMVR"]
names   = {"Sideband"  :"SB",
           "Control"   :"CR",
           "Signal"    :"hh",
           "Signal_in" :"hhi",
           "Signal_out":"hho",
           "LMVR"      :"LM",
           "HMVR"      :"HM",}
h_data  = {}
v_data  = {}
h_qcd   = {}
v_qcd   = {}
h_qcd_up   = {}
h_qcd_down = {}
h_allhad = {}
h_allhad_up = {}
h_allhad_down = {}
v_allhad = {}
h_nonallhad = {}
v_nonallhad = {}

nToys = 1000
v_qcd_toys   = []
v_data_toys  = []
def throwToyHist(hist,t):
    toyHist = ROOT.TH1F(hist)
    toyHist.SetName(hist.GetName()+"_toy"+str(t))
    for bin in range(1,hist.GetNbinsX()+1):
        c = hist.GetBinContent(bin)
        e = hist.GetBinError(bin)
        n = random.gauss(c,e)
        toyHist.SetBinContent(bin,n)
        toyHist.SetBinError(bin,e)
    return toyHist

for region in regions:
    h_data [region] = f_data .Get(o.cut+"_FourTag_"+region+"/m4j_cor_l")
    h_data [region].SetName("data_"+names[region])

    h_qcd     [region] = f_qcd  .Get(o.cut+"_TwoTag_"+region+"/m4j_cor_l")
    h_qcd     [region].SetName("qcd_"+names[region])
    h_qcd_up  [region] = ROOT.TH1F(h_qcd[region])
    h_qcd_up  [region].SetName(h_qcd[region].GetName()+"_up")
    h_qcd_down[region] = ROOT.TH1F(h_qcd[region])
    h_qcd_down[region].SetName(h_qcd[region].GetName()+"_down")

    h_allhad     [region] = f_allhad.Get(o.cut+"_TwoTag_"+region+"/m4j_cor_l")
    h_allhad     [region].SetName("allhad_"+names[region])
    h_allhad_up  [region] = ROOT.TH1F(h_allhad[region])
    h_allhad_up  [region].SetName(h_allhad[region].GetName()+"_up")
    h_allhad_down[region] = ROOT.TH1F(h_allhad[region])
    h_allhad_down[region].SetName(h_allhad[region].GetName()+"_down")

    h_nonallhad[region] = f_nonallhad.Get(o.cut+"_FourTag_"+region+"/m4j_cor_l")
    h_nonallhad[region].SetName("nonallhad_"+names[region])

    #scale background
    h_qcd        [region].Scale(mu_qcd_dict["mu_qcd_PassHCdEta"])
    h_qcd_up     [region].Scale(mu_qcd_dict["mu_qcd_PassHCdEta"]+mu_qcd_dict["mu_qcd_PassHCdEta_err"])
    h_qcd_down   [region].Scale(mu_qcd_dict["mu_qcd_PassHCdEta"]-mu_qcd_dict["mu_qcd_PassHCdEta_err"])
    h_allhad     [region].Scale(mu_qcd_dict["mu_allhad_PassHCdEta"])
    h_allhad_up  [region].Scale(mu_qcd_dict["mu_allhad_PassHCdEta"]+mu_qcd_dict["mu_allhad_PassHCdEta_err"])
    h_allhad_down[region].Scale(mu_qcd_dict["mu_allhad_PassHCdEta"]-mu_qcd_dict["mu_allhad_PassHCdEta_err"])

    #rebin
    (v_data [region], binWidth) = do_variable_rebinning(h_data [region],rebins["m4j_cor_l"])
    (v_qcd  [region], binWidth) = do_variable_rebinning(h_qcd  [region],rebins["m4j_cor_l"])
    (v_allhad[region], binWidth) = do_variable_rebinning(h_allhad[region],rebins["m4j_cor_l"])
    (v_nonallhad[region], binWidth) = do_variable_rebinning(h_nonallhad[region],rebins["m4j_cor_l"])
    v_data[region].Sumw2()
    v_qcd[region].Sumw2()
    v_allhad[region].Sumw2()
    v_nonallhad[region].Sumw2()
    #subtract ttbar from data so that we can get qcd ratio
    v_data[region].Add(v_allhad[region],-1)
    v_data[region].Add(v_nonallhad[region],-1)
    
    #throw toys for Control hists
    # if region == "Control":
    #     for t in range(nToys):
    #         v_qcd_toys .append(throwToyHist(v_qcd ["Control"],t))
    #         v_data_toys.append(throwToyHist(v_data["Control"],t))

    #divide data by qcd
    v_data[region].Divide(v_qcd[region])
    
    # if region == "Control":
    #     for t in range(nToys):
    #         v_data_toys[t].Divide(v_qcd_toys[t])


#Project onto Legendre Polynomials. x = 2*(m - 175)/(1500-175) - 1 = (m-175)/662.5 - 1 = (m-175-662.5)/662.5 = (m-837.5)/662.5
lmin =  250
lmax = lmin + (rebins["m4j_cor_l"][-1]-lmin)*2
#lmax = lmin + (rebins["m4j_cor_l"][-1]-lmin)
x="((x-"+str((lmax-lmin)/2+lmin)+")/"+str((lmax-lmin)/2)+")"
# pstring=["((2* 0+1.)/"+str(lmax-lmin)+")^(0.5)*"+"1",
#          "((2* 1+1.)/"+str(lmax-lmin)+")^(0.5)*"+x,
#          "((2* 2+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./  2)*(3*"+x+"^2-1)",
#          "((2* 3+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./  2)*(5*"+x+"^3-3*"+x+")",
#          "((2* 4+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./  8)*(35*"+x+"^4-30*"+x+"^2+3)",
#          "((2* 5+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./  8)*(63*"+x+"^5-70*"+x+"^3+15*"+x+")",
#          "((2* 6+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./ 16)*(231*"+x+"^6-315*"+x+"^4+105*"+x+"^2-5)",
#          "((2* 7+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./ 16)*(429*"+x+"^7-693*"+x+"^5+315*"+x+"^3-35*"+x+")",
#          "((2* 8+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./128)*(6435*"+x+"^8-12012*"+x+"^6+6930*"+x+"^4-1260*"+x+"^2+35)",
#          "((2* 9+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./128)*(12155*"+x+"^9-25740*"+x+"^7+18018*"+x+"^5-4620*"+x+"^3+315*"+x+")",
#          "((2*10+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./256)*(46189*"+x+"^10-109395*"+x+"^8+90090*"+x+"^6-30030*"+x+"^4+3465*"+x+"^2-63)",
#          ]

pstring=["1",
         x,
         "(1./  2)*(3*"+x+"^2-1)",
         "(1./  2)*(5*"+x+"^3-3*"+x+")",
         "(1./  8)*(35*"+x+"^4-30*"+x+"^2+3)",
         "(1./  8)*(63*"+x+"^5-70*"+x+"^3+15*"+x+")",
         "(1./ 16)*(231*"+x+"^6-315*"+x+"^4+105*"+x+"^2-5)",
         "(1./ 16)*(429*"+x+"^7-693*"+x+"^5+315*"+x+"^3-35*"+x+")",
         "(1./128)*(6435*"+x+"^8-12012*"+x+"^6+6930*"+x+"^4-1260*"+x+"^2+35)",
         "(1./128)*(12155*"+x+"^9-25740*"+x+"^7+18018*"+x+"^5-4620*"+x+"^3+315*"+x+")",
         "(1./256)*(46189*"+x+"^10-109395*"+x+"^8+90090*"+x+"^6-30030*"+x+"^4+3465*"+x+"^2-63)",
         ]
fitOptions="QI0"
p=[]
I=[]
for i in range(len(pstring)):
    p.append(ROOT.TF1("p"+str(i),pstring[i],lmin,lmax))
    I.append(p[-1].Integral(lmin,lmax)/float(lmax-lmin))
    print "Integral LP["+str(i)+"] =",I[i]

    
def updateS(s,hist,bin,func,a,b):
    h = hist.GetBinContent(bin)
    i = func.Integral(a,b)
    s += h*i
    return s

def project(hist,func):
    s = 0

    firstBin = -1
    for bin in range(1,hist.GetNbinsX()+1):
        a = hist.GetBinLowEdge(bin)
        c = hist.GetBinCenter(bin)
        b = a + hist.GetBinWidth(bin)

        if c< 250:continue
        if firstBin == -1: firstBin = bin
        if b>lmax:continue
        lastBin = bin

        s = updateS(s,hist,bin,func,a,b)

    i = func.Integral(hist.GetBinLowEdge(lastBin)+hist.GetBinWidth(lastBin),lmax) * hist.GetBinContent(lastBin)
    s += i

    return s

def mean(l):
    return float(sum(l))/len(l)

def std(l):
    l2 = [x**2 for x in l]
    return (mean(l2)-mean(l)**2)**0.5

def makePlh(c,n,name):
    plh = ""
    d=len(c)
    #for i in range(n):
    for i in range(d-1):
        plh += str(c[i])+"*"+pstring[i]+" + "
    plh += str(c[d-1])+"*"+pstring[d-1]

    f_plh = ROOT.TF1("plh"+name,plh,lmin,lmax)
    f_plh.SetLineColor(ROOT.kRed)
    f_plh.SetLineStyle(1)
    f_plh.SetLineWidth(1)
    return f_plh

def makeLP(c,n,name):
    LP = str(c)+"*"+pstring[n]

    f_LP = ROOT.TF1("LP"+name,LP,lmin,lmax)
    f_LP.SetLineColor(ROOT.kRed)
    f_LP.SetLineStyle(1)
    f_LP.SetLineWidth(1)
    return f_LP

def getGoal(p,c,n):
    return p

def project_all(hist):
    d = len(p)
    n = None
    clh = []        
    partial = []
    goal = 0.95
    maxVar = 0
    for i in range(d):
        thisLP = makeLP("[0]",i,"_project"+str(i))
        thisLP.SetParameter(0,I[i])
        #c = project(hist,thisLP)
        clh.append(I[i])

        partial.append( makePlh(["["+str(i)+"]" for i in range(i+1)],i,"_partial"+str(i)) )
        #for j in range(i+1): partial[-1].FixParameter(j,I[j])
        for j in range(i+1): partial[-1].SetParameter(j,I[j])
        print "partial[-1].Eval(300)",partial[-1].Eval(300)

        hist.Fit(partial[-1].GetName(),fitOptions)
        for j in range(i+1): print partial[-1].GetParameter(j)
        prob = partial[-1].GetProb()
        chi2 = partial[-1].GetChisquare()
        ndf  = partial[-1].GetNDF()
        var  = getGoal(prob,chi2,ndf)
        #var = chi2/ndf
        print "prob("+str(i)+")",prob,"chi2",chi2,"ndf",ndf,"chi2/ndf",(chi2/ndf if ndf else "NaN")

        #if var > goal:
        if i == 1:
            n = i
            for j in range(n+1): clh[j] = partial[n].GetParameter(j)
            print "Need LPs up to",n,clh
            return (clh,partial[n])

    #return (clh,projected_plh)


def getChi2NDF(hist,func):
    ndf  = 0
    chi2 = 0
    for bin in range(1,hist.GetNbinsX()+1):
        a = hist.GetBinLowEdge(bin)
        w = hist.GetBinWidth(bin)
        b = a + w
        h = hist.GetBinContent(bin)
        i = func.Integral(a,b)/w
        if h: 
            ndf+=1
            chi2+=(h-i)**2/h
    return (chi2,ndf)
    
def vary_projection(hist,func,c):
    d = len(c)
    c_up   = []
    c_down = []
    for i in range(d):
        print "Varying LP",i
        
        #fix nominal parameters
        for p in range(d): func.FixParameter(p,c[p])
        # allow normalization to float for variations beyond LP0
        if i: func.ReleaseParameter(0)
        hist.Fit(func.GetName(),fitOptions)
        

        goal = 0.5

        chi2 = func.GetChisquare()
        ndf  = func.GetNDF()
        prob = func.GetProb()
        var  = getGoal(prob,chi2,ndf)
        scale= 2
        step = 1.0
        loop = 0
        while abs(var-goal)>0.01:
            if i: func.SetParameter(0,c[0])
            func.FixParameter(i,c[i]*scale)
            hist.Fit(func.GetName(),fitOptions)

            prev = var

            chi2 = func.GetChisquare()
            ndf  = func.GetNDF()
            prob = func.GetProb()
            var  = getGoal(prob,chi2,ndf)

            #check if overshoot. 
            crossed = ((prev - goal)>0) != ((var - goal)>0)
            #if overshoot, reduce stepsize and go the other way
            if crossed: step = -step/2
            scale = scale+step
            #print "prev",prev,"var",var,"crossed",crossed,"step",step,"scale",scale
            #raw_input()

            loop += 1
            if loop%1000==0: print "loop",loop,"prob",prob,"scale",scale

        print "  up:",i,scale,func.GetProb(),"loops:",loop
        c_up.append([])
        for j in range(d): c_up[-1].append(func.GetParameter(j))

        #fix nominal parameters
        for p in range(d): func.FixParameter(p,c[p])
        # allow normalization to float for variations beyond LP0
        if i: func.ReleaseParameter(0)
        hist.Fit(func.GetName(),fitOptions)

        chi2 = func.GetChisquare()
        ndf  = func.GetNDF()
        prob = func.GetProb()
        var  = getGoal(prob,chi2,ndf)
        scale= 0
        step = -1.0
        loop = 0
        while abs(var-goal) > .01:
            if i: func.SetParameter(0,c[0])
            func.FixParameter(i,c[i]*scale)
            hist.Fit(func.GetName(),fitOptions)

            prev = var

            chi2 = func.GetChisquare()
            ndf  = func.GetNDF()
            prob = func.GetProb()
            var  = getGoal(prob,chi2,ndf)

            #check if overshoot. 
            crossed = ((prev - goal)>0) != ((var - goal)>0)
            #if overshoot, reduce stepsize and go the other way
            if crossed: step = -step/2
            scale = scale+step
            #print "prev",prev,"var",var,"crossed",crossed,"step",step,"scale",scale
            #raw_input()

            loop += 1
            if loop%1000==0: print "loop",loop,"prob",prob,"scale",scale

        print "down:",i,scale,func.GetProb(),"loops:",loop
        c_down.append([])
        for j in range(d): c_down[-1].append(func.GetParameter(j))

        # ensure that up means up
        if c_up[-1][i] < c[i]: #swap up and down variations
            up   = c_up  [-1]
            down = c_down[-1]
            c_up  [-1] = down
            c_down[-1] = up 

    
    return (c_up,c_down)
            
def symmetrize(c,c_up,c_down):
    d = len(c_up)
    for i in range(d):
        # c_up  [i][0] = 1+(c_up  [i][0]-c[0])
        # c_down[i][0] = 1+(c_down[i][0]-c[0])
        # for j in range(1,d):
        #     c_up  [i][j] = c_up  [i][j]-c[j]
        #     c_down[i][j] = c_down[i][j]-c[j]

        #symmetrize variations to ensure all variation enclose origin of shape space (flat line at ratio=1)
        if (c_up[i][i] - I[i]) > (I[i]-c_down[i][i]): #up variation is larger
            c_down[i] = [2*I[j]-c_up  [i][j]  for j in range(d)]
        else: # down variation is larger
            c_up  [i] = [2*I[j]-c_down[i][j] for j in range(d)]

    return (c_up,c_down)        


def plot_projection(hist,func,name,clh=None,clh_up=None,clh_down=None):
    cp = ROOT.TCanvas()
    cp.SetName(str(time.time()))
    hist.SetTitle("")
    hist.SetStats(0)
    hist.SetMaximum(1.6)
    hist.SetMinimum(0.6)
    hist.SetYTitle("#frac{Data-t#bar{t}}{multijet}")
    hist.SetXTitle("m_{4j} (corrected) [GeV]")
    hist.Draw("PE")

    d=len(clh)
    upFuncs   = []
    downFuncs = []
    if clh_up:
        for i in range(d): 
            upFuncs.append(ROOT.TF1(func))
            upFuncs[-1].SetName(func.GetName()+"_up"+str(i))
            for j in range(d): upFuncs[-1].FixParameter(j,(clh_up[i][j]))
            upFuncs[-1].SetLineWidth(1)
            upFuncs[-1].SetLineColorAlpha(ROOT.kBlack,0.3)
            upFuncs[-1].Draw("SAME")

            downFuncs.append(ROOT.TF1(func))
            downFuncs[-1].SetName(func.GetName()+"_down"+str(i))
            for j in range(d): downFuncs[-1].FixParameter(j,(clh_down[i][j]))
            downFuncs[-1].SetLineWidth(1)
            downFuncs[-1].SetLineColorAlpha(ROOT.kBlack,0.3)
            downFuncs[-1].Draw("SAME")
        
    for i in range(d): func.FixParameter(i,clh[i])
    func.SetLineWidth(2)
    func.SetLineColor(ROOT.kBlack)
    func.Draw("SAME")

    l=ROOT.TLegend(0.70,0.75,0.9,0.9)
    l.AddEntry(hist,"ratio","lp")
    l.AddEntry(func,"projection","l")
    l.Draw("SAME")
    cp.SaveAs(o.outDir+"/"+name)


def makePositive(hist):
    for bin in range(1,hist.GetNbinsX()+1):
        x   = hist.GetXaxis().GetBinCenter(bin)
        y   = hist.GetBinContent(bin)
        err = hist.GetBinError(bin)
        hist.SetBinContent(bin, y if y > 0 else 0.0)
        hist.SetBinError(bin, err if y > 0 else 0.0)

def makeB_i(c,i,name):
    color = [51,53,56,62,66,75,91,95,99,50,40,30,15]

    if i == 0:
        B_i = str(c[0])+"*"+pstring[i]
    else:# 
        B_i = str(c[0])+"+"+str(c[i])+"*"+pstring[i]

    f_B_i = ROOT.TF1("B_"+str(i)+"_"+name,B_i,lmin,lmax)
    f_B_i.SetLineColor(color[i])
    f_B_i.SetLineStyle(1)
    f_B_i.SetLineWidth(1)
    return f_B_i

def storeShapes(hist, c_up, c_down):
    D = len(c_up)
    makePositive(hist)
    total = hist.Integral()
    limitFile.Append(hist)
    up   = []
    down = []
    h_up   = []
    h_down = []
    for i in range(D):
        # up  .append( makeB_i(c_up  [i],i,"up"  ) )
        # down.append( makeB_i(c_down[i],i,"down") )
        up  .append( makePlh(c_up  [i],i,"up"  ) )
        down.append( makePlh(c_down[i],i,"down") )
        h_up  .append( ROOT.TH1F(hist) )
        h_up  [-1].SetName(hist.GetName()+"_lp"+str(i)+"_up")
        h_down.append( ROOT.TH1F(hist) )
        h_down[-1].SetName(hist.GetName()+"_lp"+str(i)+"_down")

    for bin in range(1,hist.GetNbinsX()+1):
        c = hist.GetBinContent(bin)
        e = hist.GetBinError(bin)
        w = hist.GetBinWidth(bin)
        l = hist.GetBinLowEdge(bin)
        for i in range(D):
            u = up  [i].Integral(l,l+w)/w
            d = down[i].Integral(l,l+w)/w
            h_up  [i].SetBinContent(bin, c*u)
            h_down[i].SetBinContent(bin, c*d)
            h_up  [i].SetBinError(bin, e*u)
            h_down[i].SetBinError(bin, e*d)

    for i in range(D):
        #if i:#normalize shape variations
        #    h_up  [i].Scale(total/(h_up  [i].Integral()))
        #    h_down[i].Scale(total/(h_down[i].Integral()))
        limitFile.Append(h_up  [i])
        limitFile.Append(h_down[i])
            
#########
## Idea:
# Find space of shape variations consistent to 1 sigma in CR down to a cutoff scale. 
#   Bin by bin is too small a feature size and will only be sampling stat error.
#   Try Legendre polynomials as a basis. By shifting endpoints can allow features to be smaller at low m4j than at high m4j
#
# 1. Project CR ratio onto basis vectors to find 'origin'. 
# 2. Vary coordinates keeping chi^2 below some threshold to find region of shape space that is consistent with ratio
# 3. Check what stat tools do with these NPs in CR.
#        Add higher Legendre polynomials until CR can be fit with ch2/ndf < 1
# 4. Test in VRs

####################
## (1 and 2) Project hist onto poly ortho-basis


(clh,v_projection) = project_all(v_data["Control"])
#plot_projection(v_data["Control"],v_projection)

(clh_up,clh_down) = vary_projection(v_data["Control"],v_projection,clh)
plot_projection(v_data["Control"] ,v_projection, "control_ratio_variations.pdf",clh,clh_up,clh_down)
plot_projection(v_data["Sideband"],v_projection,"sideband_ratio_variations.pdf",clh,clh_up,clh_down)

(clh_up,clh_down) = symmetrize(clh,clh_up,clh_down)
plot_projection(v_data["Control"] ,v_projection, "control_ratio_variations_symmetrized.pdf",clh,clh_up,clh_down)
plot_projection(v_data["Sideband"],v_projection,"sideband_ratio_variations_symmetrized.pdf",clh,clh_up,clh_down)

#store shape vars
for region in regions:
    storeShapes(h_qcd[region],clh_up,clh_down)
    makePositive(h_qcd_up     [region])
    makePositive(h_qcd_down   [region])
    makePositive(h_allhad     [region])
    makePositive(h_allhad_up  [region])
    makePositive(h_allhad_down[region])
    makePositive(h_nonallhad  [region])

    limitFile.Append( h_data       [region] )
    limitFile.Append( h_qcd_up     [region] )
    limitFile.Append( h_qcd_down   [region] )
    limitFile.Append( h_allhad     [region] )
    limitFile.Append( h_allhad_up  [region] )
    limitFile.Append( h_allhad_down[region] )
    limitFile.Append( h_nonallhad  [region] )

limitFile.Write()
