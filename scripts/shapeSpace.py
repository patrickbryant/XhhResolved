import sys
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
rebins["m4j_cor_l"] = [100,250,270,350,430,
                       510,590,730,1200]
#rebins["m4j_cor_l"] = [100,250,270,290,330,360,450,580,800,1500]

#rebins["m4j_cor_l"] = [100,250,290,330,360,400,460,530,610,720,850,1500]

#get files
f_data  = ROOT.TFile(files["data"])
f_qcd   = ROOT.TFile(files["qcd"])
f_allhad = ROOT.TFile(files["allhadShape"])
f_nonallhad = ROOT.TFile(files["nonallhad"])



# gauss = ROOT.TF1("gauss","gaus",-10,10)
# gauss.SetParameters(1,0,1)
# def cdf(res):
#     prob = gauss.Integral(-abs(res/3),abs(res/3))
#     return prob
# gauss.SetParameter(0,1/cdf(10))

# def significanceAdjustHist(hist):
#     adjusted = ROOT.TH1F(hist)
#     adjusted.SetName(hist.GetName()+"_sigScale")
#     adjusted.SetLineColor(ROOT.kBlack)
#     for bin in range(1,hist.GetNbinsX()+1):
#         h     = hist.GetBinContent(bin)
#         h_err = hist.GetBinError(bin)
#         res = (h-1)/h_err if h_err else 0
#         cor = cdf(res)
#         h_cor = 1+(h-1)*cor

#         h_up = h+h_err
#         res_up = res+1
#         h_cor_up = 1+(h_up-1)*cdf(res_up)

#         h_down = h-h_err
#         res_down = res-1
#         h_cor_down = 1+(h_down-1)*cdf(res_down)

#         h_cor_err = (h_cor_up - h_cor_down)/2

#         adjusted.SetBinContent(bin,h_cor if h else 0)
#         adjusted.SetBinError(bin,h_cor_err if h else 0)
#     return adjusted



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
    if region == "Control":
        for t in range(nToys):
            v_qcd_toys .append(throwToyHist(v_qcd ["Control"],t))
            v_data_toys.append(throwToyHist(v_data["Control"],t))

    #divide data by qcd
    v_data[region].Divide(v_qcd[region])
    
    if region == "Control":
        for t in range(nToys):
            v_data_toys[t].Divide(v_qcd_toys[t])


#Project onto Legendre Polynomials. x = 2*(m - 175)/(1500-175) - 1 = (m-175)/662.5 - 1 = (m-175-662.5)/662.5 = (m-837.5)/662.5
lmin =  250
#lmax = lmin + (rebins["m4j_cor_l"][-1]-lmin)*2
lmax = lmin + (rebins["m4j_cor_l"][-1]-lmin)
x="((x-"+str((lmax-lmin)/2+lmin)+")/"+str((lmax-lmin)/2)+")"
pstring=["((2* 0+1.)/"+str(lmax-lmin)+")^(0.5)*"+"1",
         "((2* 1+1.)/"+str(lmax-lmin)+")^(0.5)*"+x,
         "((2* 2+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./  2)*(3*"+x+"^2-1)",
         "((2* 3+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./  2)*(5*"+x+"^3-3*"+x+")",
         "((2* 4+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./  8)*(35*"+x+"^4-30*"+x+"^2+3)",
         "((2* 5+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./  8)*(63*"+x+"^5-70*"+x+"^3+15*"+x+")",
         "((2* 6+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./ 16)*(231*"+x+"^6-315*"+x+"^4+105*"+x+"^2-5)",
         "((2* 7+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./ 16)*(429*"+x+"^7-693*"+x+"^5+315*"+x+"^3-35*"+x+")",
         "((2* 8+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./128)*(6435*"+x+"^8-12012*"+x+"^6+6930*"+x+"^4-1260*"+x+"^2+35)",
         "((2* 9+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./128)*(12155*"+x+"^9-25740*"+x+"^7+18018*"+x+"^5-4620*"+x+"^3+315*"+x+")",
         "((2*10+1.)/"+str(lmax-lmin)+")^(0.5)*"+"(1./256)*(46189*"+x+"^10-109395*"+x+"^8+90090*"+x+"^6-30030*"+x+"^4+3465*"+x+"^2-63)",
         ]

p=[]
I=[]
for i in range(len(pstring)):
    p.append(ROOT.TF1("p"+str(i),pstring[i],lmin,lmax))
    I.append(p[-1].Integral(lmin,lmax))
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

    i = func.Integral(hist.GetBinLowEdge(lastBin)+hist.GetBinWidth(lastBin),lmax)
    s += i

    return s

def mean(l):
    return float(sum(l))/len(l)

def std(l):
    l2 = [x**2 for x in l]
    return (mean(l2)-mean(l)**2)**0.5

def makePlh(c,n,name):
    plh = ""
    for i in range(n):
        plh += str(c[i])+"*"+pstring[i]+" + "
    plh += str(c[n])+"*"+pstring[n]

    f_plh = ROOT.TF1("plh"+name,plh,lmin,lmax)
    f_plh.SetLineColor(ROOT.kRed)
    f_plh.SetLineStyle(1)
    f_plh.SetLineWidth(1)
    return f_plh

def fit_LPs(hist,n,clh):
    fit_plh = makePlh(["["+str(i)+"]" for i in range(n+1)],n,"_fit"+str(n))
    for i in range(n+1):
        fit_plh.SetParameter(i,clh[i])
    hist.Fit("plh_fit"+str(n),"I")
    clh_fit = [fit_plh.GetParameter(i) for i in range(n+1)]
    return clh_fit

def iterative_fit(hist):#add one LP at a time, each time fixing paramters from previous fit
    fixed = []
    for i in range(len(p)):
        fit_plh = makePlh(["["+str(x)+"]" for x in range(i+1)],i,"_fit"+str(i))
        for j in range(len(fixed)):
            fit_plh.FixParameter(j,fixed[j])
        hist.Fit("plh_fit"+str(i),"QI0") #print less, use Integral of func over bin, don't attach func to hist
        fixed.append(fit_plh.GetParameter(i))
    return (fixed, fit_plh)

def makeLP(c,n,name):
    LP = str(c)+"*"+pstring[n]

    f_LP = ROOT.TF1("LP"+name,LP,lmin,lmax)
    f_LP.SetLineColor(ROOT.kRed)
    f_LP.SetLineStyle(1)
    f_LP.SetLineWidth(1)
    return f_LP

def project_all(hist):
    fixed = []        
    for i in range(len(p)):
        thisLP = makeLP("[0]",i,"_project"+str(i))
        thisLP.SetParameter(0,1)
        c = project(hist,thisLP)
        thisLP.FixParameter(0,c)
        fixed.append(c)
    
    projected_plh = makePlh([str(x) for x in fixed],len(p)-1,"_projected")

    return (fixed,projected_plh)

def independent_fit(hist):#add one LP at a time, each time fixing paramters from previous fit
    fixed = []
    for i in range(len(p)):
        fit_LP = makeLP(("[0]" if not i else "1+[0]"),i,"_fit"+str(i))
        hist.Fit("LP_fit"+str(i),"QI0") #print less, use Integral of func over bin, don't attach func to hist
        fixed.append(fit_LP.GetParameter(0))
    return (fixed, fit_LP)


# def getChi2NDF(hist,func):
#     ndf  = 0
#     chi2 = 0
#     for bin in range(1,hist.GetNbinsX()+1):
#         a = hist.GetBinLowEdge(bin)
#         c = hist.GetBinCenter(bin)
#         w = hist.GetBinWidth(bin)
#         b = a + w
#         h = hist.GetBinContent(bin)
#         i = func.Integral(a,b)/w
#         if h: 
#             ndf+=1
#             chi2+=(h-i)**2/h
#     return (chi2,ndf)
    


def plot_fit(hist,func):
    cp = ROOT.TCanvas()
    hist.SetTitle("")
    hist.SetStats(0)
    hist.SetMaximum(1.6)
    hist.SetMinimum(0.6)
    hist.SetYTitle("#frac{Data-t#bar{t}}{multijet}")
    hist.SetXTitle("m_{4j} (corrected) [GeV]")
    hist.Draw("PE")
    func.SetLineWidth(2)
    func.SetLineColor(ROOT.kBlack)
    #chi2 = func.GetChisquare()
    #(chi2,ndf) = getChi2NDF(hist,func)
    #print "chi2",chi2
    #ndf  = func.GetNDF()
    #chi2text = ROOT.TLatex(1500, 1.62, "#chi^{2}/NDF = "+str(int(chi2*100)/100.)+"/"+str(ndf)+" = "+(str(int(chi2/ndf*100)/100.)) if ndf else "NaN")
    #chi2text.SetTextSize(19)
    #chi2text.SetTextFont(43)
    #chi2text.SetTextAlign(31)
    #chi2text.Draw("SAME")
    func.Draw("SAME")
    l=ROOT.TLegend(0.70,0.75,0.9,0.9)
    l.AddEntry(hist,"ratio","lp")
    l.AddEntry(func,"iterative fit","l")
    l.Draw("SAME")
    cp.SaveAs(o.outDir+"/control_ratio.pdf")


def makeB_i(c,i,name):
    color = [51,53,56,62,66,75,91,95,99,50,40,30,15]

    #reflect function around y=1 if down
    if i == 0:
        B_i = (  "" if name == "up" else "2-")+str(c)+"*"+pstring[i]
    else:
        B_i = ("1+" if name == "up" else "1-")+str(c)+"*"+pstring[i]

    f_B_i = ROOT.TF1("B_"+str(i)+"_"+name,B_i,lmin,lmax)
    f_B_i.SetLineColor(color[i])
    f_B_i.SetLineStyle(1)
    f_B_i.SetLineWidth(1)
    return f_B_i

# def plotAdjustment(hist,adjusted):
#     cp = ROOT.TCanvas()
#     hist.SetTitle("")
#     hist.SetStats(0)
#     hist.SetMaximum(1.6)
#     hist.SetMinimum(0.6)
#     hist.SetYTitle("#frac{Data-t#bar{t}}{multijet}")
#     hist.SetXTitle("m_{4j} (corrected) [GeV]")
#     hist.Draw("PE")
#     adjusted.SetLineWidth(2)
#     adjusted.Draw("PE SAME")
#     l=ROOT.TLegend(0.70,0.75,0.9,0.9)
#     l.AddEntry(hist,"ratio")
#     l.AddEntry(adjusted,"adjusted")
#     l.Draw("SAME")
#     cp.SaveAs(o.outDir+"/control_adjusted_ratio.pdf")
    


def plotPlh(hist,n,c_up,c_down,sig):
    cp = ROOT.TCanvas()
    l=ROOT.TLegend(0.65,0.65,0.9,0.9)
    l.SetEntrySeparation(0.4)
    hist.SetTitle("")
    hist.SetStats(0)
    hist.SetMaximum(1.6)
    hist.SetMinimum(0.6)
    hist.SetYTitle("#frac{Data-t#bar{t}}{multijet}")
    hist.SetXTitle("m_{4j} (corrected) [GeV]")
    hist.Draw("PE")

    #v_ratio_adjusted["Control"].Draw("PE SAME")
    
    funcs = []
    for i in range(n,n+1):
        funcs.append(makeB_i(c_up  [i],i,"up"))
        funcs.append(makeB_i(c_down[i],i,"down"))
        funcs[-1].SetLineStyle(2)

    funcs.append(makePlh(clh,n,"_sum"+str(n)))
    #(chi2, ndf) = getChi2NDF(hist,funcs[-1])
    #print "my chi2",chi2
    funcs[-1].SetLineColor(ROOT.kBlack)
    funcs[-1].SetLineWidth(2)

    #chi2text = ROOT.TLatex(1500, 1.62, "#chi^{2}/NDF = "+str(int(chi2*100)/100.)+"/"+str(ndf)+" = "+(str(int(chi2/ndf*100)/100.)) if ndf else "NaN")
    #chi2text.SetTextSize(19)
    #chi2text.SetTextFont(43)
    #chi2text.SetTextAlign(31)
    #chi2text.Draw("SAME")
        
    l.AddEntry(hist,"ratio","lp")
    # l.AddEntry(funcs[0],("1+" if n else "  ")+"(c_{"+str(n)+"}+#sigma_{"+str(n)+"})LP_{"+str(n)+"}","l")
    # l.AddEntry(funcs[1],("1-" if n else "2-")+"(c_{"+str(n)+"}+#sigma_{"+str(n)+"})LP_{"+str(n)+"}","l")
    l.AddEntry(funcs[0],("1+" if n else "  ")+"c_{"+str(n)+"}"+"LP_{"+str(n)+"}","l")
    l.AddEntry(funcs[1],("1-" if n else "2-")+"c_{"+str(n)+"}"+"LP_{"+str(n)+"}","l")
    l.AddEntry(funcs[2],"#Sigma_{i=0}^{i="+str(n)+"}c_{i}LP_{i}","l")
    l.Draw("SAME")
    for func in funcs:
        func.Draw("SAME")
        #l.AddEntry(func)

    t = ROOT.TLatex(250,1.5,"Shape Significance = "+str(sig[n])[:4])
    t.SetTextAlign(11)
    t.SetTextSize(19)
    t.SetTextFont(43)
    t.Draw("SAME")

    cp.SaveAs(o.outDir+"/control_qcd_shape_"+str(n)+".pdf")


def plotToys(i,c_vec):
    cp = ROOT.TCanvas()
    x_low  = -3 if i else 27
    x_high =  3 if i else 33
    hist = ROOT.TH1F("toys"+str(i),"toys"+str(i),100,x_low,x_high)
    hist.SetTitle("")
    hist.SetStats(0)
    hist.SetYTitle("Toys (Normalized)")
    hist.SetXTitle("c_{"+str(i)+"}")

    for c in c_vec: hist.Fill(c)

    hist.Scale(1.0/hist.Integral())
    #hist.SetMaximum(1)
    hist.SetMinimum(0)
    hist.Draw("HIST")

    #line for mean value
    mean_c = mean(c_vec)
    y_max = hist.GetBinContent(hist.GetXaxis().FindBin(mean_c))
    m = ROOT.TLine(mean_c,0,mean_c,y_max)
    m.SetLineColor(ROOT.kRed)
    m.Draw("SAME")

    m_t = ROOT.TLatex(mean_c,y_max,"<c_{"+str(i)+"}>")
    m_t.Draw("SAME")

    # t = ROOT.TLatex(250,1.5,"Shape Significance = "+str(sig[n])[:4])
    # t.SetTextAlign(11)
    # t.SetTextSize(19)
    # t.SetTextFont(43)
    # t.Draw("SAME")

    cp.SaveAs(o.outDir+"/control_toys_"+str(i)+".pdf")


def makePositive(hist):
    for bin in range(1,hist.GetNbinsX()+1):
        x   = hist.GetXaxis().GetBinCenter(bin)
        y   = hist.GetBinContent(bin)
        err = hist.GetBinError(bin)
        hist.SetBinContent(bin, y if y > 0 else 0.0)
        hist.SetBinError(bin, err if y > 0 else 0.0)


def storeShapes(hist, c_up, c_down):
    makePositive(hist)
    limitFile.Append(hist)
    up   = []
    down = []
    h_up   = []
    h_down = []
    for i in range(len(pstring)):
        up  .append( makeB_i(c_up  [i],i,"up"  ) )
        down.append( makeB_i(c_down[i],i,"down") )
        h_up  .append( ROOT.TH1F(hist) )
        h_up  [-1].SetName(hist.GetName()+"_lp"+str(i)+"_up")
        h_down.append( ROOT.TH1F(hist) )
        h_down[-1].SetName(hist.GetName()+"_lp"+str(i)+"_down")

    for bin in range(1,hist.GetNbinsX()+1):
        c = hist.GetBinContent(bin)
        e = hist.GetBinError(bin)
        w = hist.GetBinWidth(bin)
        l = hist.GetBinLowEdge(bin)
        for i in range(len(pstring)):
            u = up  [i].Integral(l,l+w)/w
            d = down[i].Integral(l,l+w)/w
            h_up  [i].SetBinContent(bin, c*u)
            h_down[i].SetBinContent(bin, c*d)
            h_up  [i].SetBinError(bin, e*u)
            h_down[i].SetBinError(bin, e*d)

    for i in range(len(pstring)):
        limitFile.Append(h_up  [i])
        limitFile.Append(h_down[i])
            
#########
## Idea:
# Find space of shape variations consistent to 1 sigma in CR down to a cutoff scale. 
#   Bin by bin is too small a feature size and will only be sampling stat error.
#   Try Legendre polynomials as a basis. By shifting endpoints can allow features to be smaller at low m4j than at high m4j
#
# 1. Project CR ratio onto basis vectors to find 'origin'. 
# 2. Vary coordinates by SDoM of respective coordinate, giving an up/down shape variation (1 nuisance parameter) for each basis vector
# 3. Check what stat tools do with these NPs in CR.
#        Add higher Legendre polynomials until CR can be fit with ch2/ndf < 1
# 4. Test in VRs

####################
## (1 and 2) Project hist onto poly ortho-basis

# clh = []
# elh = []
# for i in range(len(p)):
#     c = project(v_ratio_adjusted["Control"],p[i],i)
#     clh.append(c)
#     print str(c).ljust(50)#,"+/-",str(int(abs(e/c)*100))+"%"
# print clh

#clh_fit = fit_LPs(v_data["Control"],8,clh)
#(clh,v_fit) = iterative_fit(v_data["Control"])
(clh,v_fit) = project_all(v_data["Control"])
#(clh,v_fit) = independent_fit(v_data["Control"])
plot_fit(v_data["Control"],v_fit)
#print clh_fit

#get distributions from toys
clh_toys = []
for i in range(len(p)): clh_toys.append([])

for t in range(nToys):
    if t%(nToys/10)==0:print "Fitting Toy:",t
    #(c, fit_toy) = iterative_fit(v_data_toys[t])
    (c, fit_toy) = project_all(v_data_toys[t])
    #(c, fit_toy) = independent_fit(v_data_toys[t])
    for i in range(len(p)):
        clh_toys[i].append(c[i])

for i in range(len(p)):
    plotToys(i,clh_toys[i])
  
print "Toys:"
mean_clh = []
std_clh  = []
sig_clh  = []
clh_up   = []
clh_down = []
print "i    <c_i>  <c_i>/nToys^0.5   w_i   |f_i-<c_i>|/w_i    |<c_i>-c_i|/w_i"
for i in range(len(p)):      
    std_clh .append(  std(clh_toys[i]) )
    mean_clh.append( mean(clh_toys[i]) )
    sig_clh .append( abs(mean_clh[i]-I[i])/std_clh[i] )
    print str(i).rjust(2),str(mean_clh[i])[:6].rjust(7),"(+/-"+str(std_clh[i]/(nToys**0.5))[:6]+")".ljust(7),
    print str(std_clh[i])[:6].ljust(7),str(sig_clh[i])[:6].rjust(7),
    print str(abs(clh[i]-mean_clh[i])/std_clh[i])
    # clh_up  .append( abs(clh[i])+std_clh[i] )
    # clh_down.append( abs(clh[i])+std_clh[i] )
    clh_up  .append( clh[i] )
    clh_down.append( clh[i] )

#make plots
for n in range(len(p)):
    plotPlh(v_data["Control"],n,clh_up,clh_down,sig_clh)


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
