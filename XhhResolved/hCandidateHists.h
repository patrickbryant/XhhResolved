#ifndef XhhResolved_hCandidateHists_H
#define XhhResolved_hCandidateHists_H

#include <xAODAnaHelpers/HistogramManager.h>
#include <xAODAnaHelpers/HelperClasses.h>
#include <xAODAnaHelpers/JetHists.h>

#include <XhhResolved/hCand.h>


class hCandidateHists : public HistogramManager
{
public:
  hCandidateHists(const std::string& name, const std::string& hCandName, const std::string& detailStr="");
  virtual ~hCandidateHists();

  virtual void record(EL::Worker *wk);

  virtual StatusCode initialize();
  virtual StatusCode execute(const hCand& hcand, float eventWeight) ;
  virtual StatusCode finalize();
  using HistogramManager::book; // make other overloaded version of book() to show up in subclass
  using HistogramManager::execute; // overload

private:

  std::string m_hCandName;

  TH1F* h_pt;
  TH1F* h_pt_m;
  TH1F* h_pt_l;

  TH1F* h_pt_cor;
  TH1F* h_pt_cor_m;
  TH1F* h_pt_cor_l;

  TH1F* h_pt_diff;

  TH1F* h_ht;
  TH1F* h_ht_m;
  TH1F* h_ht_l;

  TH1F* h_eta;
  TH1F* h_phi;
  TH1F* h_m;
  TH1F* h_dRjj;
  TH1F* h_mW;
  TH1F* h_WdRjj;
  TH1F* h_mTop;
  TH1F* h_TdRwb;
  TH1F* h_Xtt;
  TH1F* h_nTags;

  TH2F*     h_mWmT;

  TH1F* h_jetPtAsymmetry;
  
  //TH1F* h_JVC;

  JetHists *h_leadJet;
  JetHists *h_sublJet;

//  jetHists* h_leadJet_tagged;
//  jetHists* h_leadJet_untagged;
//  jetHists* h_sublJet_tagged;
//  jetHists* h_sublJet_untagged;

};

#endif
