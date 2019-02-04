#ifndef XHHRESOLVED_LEPTOPHISTS_H
#define XHHRESOLVED_LEPTOPHISTS_H

#include <XhhResolved/lepTopData.h>
#include <vector>
using namespace std;


//
// lepTop Hists
//
class lepTopHists{
  
 public:
  TH1F* h_pt;
  TH1F* h_pt_m;
  TH1F* h_pt_l;

  TH1F* h_pt_mub;
  TH1F* h_pt_mub_m;
  TH1F* h_pt_mub_l;

  TH1F* h_eta;
  TH1F* h_phi;
  TH1F* h_m;
  TH1F* h_dRmj;
  TH1F* h_mT;
  TH1F* h_meT;
  TH1F* h_meT_l;
  TH1F* h_mTop;

  TH2F*     h_mWmT;

  jetHists*  h_jet;
  muonHists* h_muon;

  lepTopHists(std::string name, EL::Worker* wk){
    h_pt        = book(wk, name, "Pt",       "p_{T} [GeV]",         100,  0,  500);
    h_pt_m      = book(wk, name, "Pt_m",     "p_{T} [GeV]",         100,  0, 1000);
    h_pt_l      = book(wk, name, "Pt_l",     "p_{T} [GeV]",         100,  0, 2000);
    h_pt_mub    = book(wk, name, "Pt_mub",   "p_{T} (mu-b) [GeV]",  100,  0,  500);
    h_pt_mub_m  = book(wk, name, "Pt_mub_m", "p_{T} (mu-b) [GeV]",  100,  0, 1000);
    h_pt_mub_l  = book(wk, name, "Pt_mub_l", "p_{T} (mu-b) [GeV]",  100,  0, 2000);
    h_eta       = book(wk, name, "Eta",      "Eta",                 100, -3,    3);
    h_phi       = book(wk, name, "Phi",      "Phi",                 100, -3.2,  3.2);
    h_m         = book(wk, name, "Mass",     "Mass [GeV]",          100,  0,  500);
    h_dRmj      = book(wk, name, "dRmj",     "dR(mj)",              100, -0.1,  5);
    h_mT        = book(wk, name, "mT",       "mT [GeV]",            100,  0,  200);
    h_meT       = book(wk, name, "meT",      "meT [GeV]",           100,  0,  200);
    h_meT_l     = book(wk, name, "meT_l",    "meT [GeV]",           100,  0,  500);
        
    h_jet    = new jetHists(name+"_jet",    wk,  "muonInJet");
    h_muon   = new muonHists(name+"_muon",    wk);

  }

  TH1F* book(EL::Worker* wk, std::string name, std::string hname, std::string title, int nBins, float xmin, float xmax){
    TH1F* h_tmp = new TH1F((name+"_"+hname).c_str(),(hname+";"+title+";Entries").c_str(), nBins, xmin,   xmax);
    wk->addOutput(h_tmp);
    return h_tmp;
  }

  
  void Fill(const lepTopData& lepTop, const float& weight){
    h_pt       -> Fill(lepTop.pt,       weight);
    h_pt_l     -> Fill(lepTop.pt,       weight);
    h_pt_m     -> Fill(lepTop.pt,       weight);

    TLorentzVector vec_mub = lepTop.vec_mub();
    h_pt_mub       -> Fill(vec_mub.Pt(),       weight);
    h_pt_mub_l     -> Fill(vec_mub.Pt(),       weight);
    h_pt_mub_m     -> Fill(vec_mub.Pt(),       weight);

    h_eta      -> Fill(lepTop.eta,      weight);
    h_phi      -> Fill(lepTop.phi,      weight);
    h_m        -> Fill(lepTop.m,        weight);
    h_dRmj     -> Fill(lepTop.drmj,     weight);

    h_mT       -> Fill(lepTop.Mt,       weight);
    h_meT      -> Fill(lepTop.met,       weight);
    h_meT_l    -> Fill(lepTop.met,       weight);

    h_jet   -> Fill(*lepTop.jet,  weight);
    h_muon  -> Fill(*lepTop.muon,  weight);

  }

};
#endif
