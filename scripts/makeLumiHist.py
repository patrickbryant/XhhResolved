import ROOT

f_d=ROOT.TFile("hists_2016_redo/data_iter7/hists.root","READ")
f_l=ROOT.TFile("XhhResolved/data/ilumiHist2016.root")

c=ROOT.TCanvas("eventsPerLumi","",1200,600)
ROOT.gPad.SetBottomMargin(0.12)
ROOT.gPad.SetLeftMargin(0.06)
ROOT.gPad.SetRightMargin(0.02)
ROOT.gPad.SetTopMargin(0.05)
legend=ROOT.TLegend(0.7,0.65,0.97,0.92)

h_l=f_l.Get("lumi_histo")
x_l=h_l.GetXaxis()

def makeRateHist(cut,name,color):
    h_d=f_d.Get(cut+"/eventsPerRun")
    h_d.LabelsDeflate("X")

    x_d=h_d.GetXaxis()

    for b in range(1,h_d.GetNbinsX()):
        if x_d.GetBinLabel(b) != x_l.GetBinLabel(b): print b,x_d.GetBinLabel(b),"!=",x_l.GetBinLabel(b)
        events=h_d.GetBinContent(b)
        lumi=h_l.GetBinContent(b)
        if lumi <= 0: 
            #print "Lumi is zero in run:",x_d.GetBinLabel(b)
            if events:
                print "ERROR: events in run with no lumi"
            continue
        rate=events/lumi
        #print x_d.GetBinLabel(b),str(events).rjust(10),str(lumi).rjust(20),str(rate).rjust(20)


    h_r=ROOT.TH1F(h_d)
    h_r.SetName(cut+name)
    h_r.SetTitle("")
    h_r.GetYaxis().SetTitle("Events/pb^{-1}")
    h_r.GetXaxis().SetTitle("Run Number")
    h_r.GetXaxis().SetLabelSize(0.02)
    h_r.GetXaxis().SetLabelFont(82)
    h_r.GetXaxis().SetTitleOffset(1.5)
    h_r.GetYaxis().SetTitleOffset(0.8)
    h_r.Divide(h_l)
    h_r.SetStats(0)
    h_r.SetMinimum(0.01)
    h_r.SetMaximum(1000)
    h_r.SetLineColor(eval(color))
    h_r.SetMarkerColor(eval(color))
    legend.AddEntry(h_r,name,"LPE")
    h_r.Draw("SAME PE")
    return h_r

rates=[]
rates.append(makeRateHist("Inclusive_FourTag_FullMassPlane","4 b-tags, MDRs, Trigger","ROOT.kRed"))
rates.append(makeRateHist("Inclusive_FourTag_Signal",       "X_{hh}<1.6",    "ROOT.kOrange"))
rates.append(makeRateHist("PassHCdEta_FourTag_Signal",       "MDCs",    "ROOT.kGreen"))
rates.append(makeRateHist("PassAllhadVeto_FourTag_Signal","X_{wt}<1.5","ROOT.kBlue"))
rates.append(makeRateHist("Excess_FourTag_Signal","262 < m4j_cor < 288","ROOT.kBlack"))
legend.Draw()
c.SetLogy()
c.SaveAs("eventsPerLumi_2016.pdf")
