#ifndef XhhResolved_hh4bHists_H
#define XhhResolved_hh4bHists_H

#include <TH1F.h>
#include <XhhResolved/hh4bEvent.h>
#include <XhhResolved/hCandidateHists.h>
#include <xAODAnaHelpers/JetHists.h>
#include <xAODAnaHelpers/MuonHists.h>
#include <xAODAnaHelpers/ElectronHists.h>

#include <xAODAnaHelpers/HistogramManager.h>

class hh4bHists : public HistogramManager
{
 public:

  hh4bHists(const std::string& name, const std::string& detailStr);
  ~hh4bHists();

  virtual void record(EL::Worker *wk);

  bool m_debug;
  bool m_doReweight;
  bool m_doBTagSF;
  unsigned int m_nBTagSFVar;
  virtual StatusCode initialize();
  StatusCode execute(const EventComb* eventComb, const hh4bEvent* event, float eventWeight);
  virtual StatusCode finalize();

  using HistogramManager::book;    // make other overloaded version of book() to show up in subclass
  using HistogramManager::execute; // make other overloaded version of execute() to show up in subclass

 private:
  TH1F*     h_NPV;
  TH1F*     h_mu_ave;
  TH1F*     h_nJetOther;
  TH1F*     h_nJetOther_u;
  TH1F*     h_nJetOther_l;
  TH1F*     h_nMuons;
  TH1F*     h_nPromptMuons;
  TH1F*     h_nPromptElecs;
  TH1F*     h_nLooseOther;

  TH1F*     h_m4j;
  TH1F*     h_m4j10;
  TH1F*     h_m4j25;
  TH1F*     h_m4j50;
  TH1F*     h_m4j_l;
  TH1F*     h_m_4j;
  
  TH1F*     h_trigBits;

  TH1F*     h_m4j_cor;
  TH1F*     h_m4j_cor_l;
  TH1F*     h_m4j_cor_1;
  TH1F*     h_m4j_cor_v;
  TH1F*     h_m4j_cor_f;
  //TH1F*     h_m4j_cor_v_s;
  //TH1F*     h_m4j_cor_f_s;
  TH1F*     h_Ht4j_l;
  TH1F*     h_R_pt_4j_l;
  TH1F*     h_lowHt_m4j_cor_l;
  TH1F*     h_lowHt_m4j_cor_v;
  TH1F*     h_lowHt_m4j_cor_f;
  //TH1F*     h_lowHt_m4j_cor_v_s;
  //TH1F*     h_lowHt_m4j_cor_f_s;
  TH2F*     h_lowHt_m12m34;
  TH1F*     h_highHt_m4j_cor_l;
  TH1F*     h_highHt_m4j_cor_v;
  TH1F*     h_highHt_m4j_cor_f;
  //TH1F*     h_highHt_m4j_cor_v_s;
  //TH1F*     h_highHt_m4j_cor_f_s;
  TH2F*     h_highHt_m12m34;
  std::vector<TH1F*>* h_m4j_cor_l_bSF;
  std::vector<TH1F*>* h_m4j_cor_1_bSF;
  std::vector<TH1F*>* h_m4j_cor_v_bSF;
  std::vector<TH1F*>* h_m4j_cor_f_bSF;
  //std::vector<TH1F*>* h_m4j_cor_v_s_bSF;
  //std::vector<TH1F*>* h_m4j_cor_f_s_bSF;

  TH1F* h_m4j_cor_l_tSF_up;
  TH1F* h_m4j_cor_1_tSF_up;
  TH1F* h_m4j_cor_v_tSF_up;
  TH1F* h_m4j_cor_f_tSF_up;
  //TH1F* h_m4j_cor_v_s_tSF_up;
  //TH1F* h_m4j_cor_f_s_tSF_up;
  TH1F* h_m4j_cor_l_tSF_down;
  TH1F* h_m4j_cor_1_tSF_down;
  TH1F* h_m4j_cor_v_tSF_down;
  TH1F* h_m4j_cor_f_tSF_down;
  //TH1F* h_m4j_cor_v_s_tSF_down;
  //TH1F* h_m4j_cor_f_s_tSF_down;

  TH1F*     h_m_4j_cor;
  TH1F*     h_m4j25_cor;
  TH1F*     h_m4j50_cor;

  TH1F*     h_m4j_cor_Z;
  TH1F*     h_m4j_cor_Z_l;
  TH1F*     h_m4j_cor_Z_v;
  TH1F*     h_m4j_cor_Z_f;

  TH1F*     h_m4j_cor_H;
  TH1F*     h_m4j_cor_H_l;
  TH1F*     h_m4j_cor_H_v;
  TH1F*     h_m4j_cor_H_f;

  TH1F*     h_m4j_diff;

  TH1F*     h_dEta_hh;
  TH1F*     h_abs_dEta_hh;
  TH1F*     h_dPhi_hh;
  TH1F*     h_dR_hh;
  TH1F*     h_Pt_hh;

  TH1F*     h_dEta_gg;
  TH1F*     h_abs_dEta_gg;
  TH1F*     h_dPhi_gg;
  TH1F*     h_dR_gg;
  TH1F*     h_Pt_gg;

  TH1F*     h_R_dRdR;
  TH1F*     h_R_dRdR_gg;

  TH1F*     h_GCdR_diff;
  TH1F*     h_GCdR_sum;

  TH1F*     h_HCdR_diff;
  TH1F*     h_HCdR_sum;

  TH1F*     h_njets;
  TH1F*     h_nbjets;
  TH1F*     h_nbjetsInHCs;

  TH1F*     h_ht;
  TH1F*     h_ht_l;
  TH1F*     h_mht;
  TH1F*     h_mht_l;

  TH1F*     h_xhh;
  TH1F*     h_dhh;
  TH1F*     h_lhh;
  TH1F*     h_rhh;
  TH1F*     h_rhhMin;

  TH1F*     h_hhJetEtaSum2;
  TH1F*     h_HCJetAbsEta;
  TH1F*     h_HCJetAR;
  
  TH1F*     h_HCJetPtE1;
  TH1F*     h_HCJetPtE2;

  TH1F*     h_xwt;
  TH1F*     h_xwt_ave;
  TH1F*     h_xtt;
  TH1F*     h_minSum_xtt_1;
  TH1F*     h_minSum_xtt_2;
  TH1F*     h_nTopCands;
  TH1F*     h_nTopCands3;
  TH1F*     h_nTopCandsAll;
  TH1F*     h_xtt_2j;
  TH1F*     h_xtt_2j_ave;
  TH1F*     h_nTopCands_2j;
  TH1F*     h_nTopCands3_2j;
  TH1F*     h_nTopCandsAll_2j;

  TH2F*     h_m12m34;
  TH2F*     h_GC_m12m34;
  TH2F*     h_dR12dR34;
  TH2F*     h_GC_dR12dR34;

  //MDC plots
  TH2F*     h_m4jnJetOther;
  TH2F*     h_m4jLeadHCandPt;
  TH2F*     h_m4jSublHCandPt;
  TH2F*     h_m4jHCdEta;
  TH2F*     h_m4jHCdPhi;
  TH2F*     h_m4jLeadHCdRjj;
  TH2F*     h_m4jSublHCdRjj;
  TH2F*     h_m4jLeadGCdRjj;
  TH2F*     h_m4jSublGCdRjj;
  TH2F*     h_m4jLeadPtHCandPt;
  TH2F*     h_m4jSublPtHCandPt;
  TH2F*     h_m4jLeadPtHCdRjj;
  TH2F*     h_m4jSublPtHCdRjj;
  TH1F*     h_m4j_l_truth;

  TH2F*     h_m4j_nViews;

  TH2F*     h_pt2pt4;

  TH1F*     h_metClusEt;
  TH1F*     h_metClusEt_l;
  TH1F*     h_metClusPhi;
 
  TH1F*     h_metTrkEt;
  TH1F*     h_metTrkEt_l;
  TH1F*     h_metTrkPhi;

  TH1F*     h_m4j_l_lhh00;
  TH1F*     h_m4j_l_lhh02;
  TH1F*     h_m4j_l_lhh10;

  TH1F*     h_m4j_cor_l_lhh00;
  TH1F*     h_m4j_cor_l_lhh02;
  TH1F*     h_m4j_cor_l_lhh10;

  TH1F*     h_m4j_cor_v_lhh00;
  TH1F*     h_m4j_cor_v_lhh02;
  TH1F*     h_m4j_cor_v_lhh10;

  TH1F*     h_m4j_cor_f_lhh00;
  TH1F*     h_m4j_cor_f_lhh02;
  TH1F*     h_m4j_cor_f_lhh10;

  TH1F* h_nTruthElec  ;
  TH1F* h_nTruthMuon  ;
  TH1F* h_nTruthTau   ;
  TH1F* h_nTruthElMu  ;
  TH1F* h_nTruthLep   ;
  TH1F* h_nTruthCharm ;
  TH1F* h_nTruthLF    ;

  TFile* m_lhh_reweightFile;

  hCandidateHists* h_leadHC;
  hCandidateHists* h_sublHC;

  hCandidateHists* h_leadGC;
  hCandidateHists* h_sublGC;

  JetHists *h_HCJet1;
  JetHists *h_HCJet2;
  JetHists *h_HCJet3;
  JetHists *h_HCJet4;

  JetHists *h_jetsHC;
  JetHists *h_jetsOther;

  TH1F* h_eventWeight_s;
  TH1F* h_eventWeight_m;
  TH1F* h_eventWeight_l;

  
  MuonHists*     h_muons;
  MuonHists*     h_promptMuons;
  ElectronHists* h_elecs;

  JetHists *h_preSelJets;

  TH1F* h_mZmumu;
  /* TH1F* h_TaggedBJets_pt; */
  /* TH1F* h_TruthBJets_pt; */
  /* TH1F* h_TaggedTruthBJets_pt; */
  TH1F* h_eventsPerRun;

};


#endif // XhhResolved_EventComb_H
