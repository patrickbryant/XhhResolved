#include <XhhResolved/hCandidateHists.h>

using std::cout; using std::endl;

hCandidateHists :: hCandidateHists (const std::string& name, const std::string& hCandName, const std::string& detailStr ) 
  : HistogramManager(name, detailStr),
    m_hCandName(hCandName), h_leadJet(0), h_sublJet(0)
 
{ }

hCandidateHists :: ~hCandidateHists () 
{}

void hCandidateHists::record(EL::Worker* wk)
{
  HistogramManager::record(wk);

  h_leadJet    ->record(wk);
  h_sublJet    ->record(wk);
}


StatusCode hCandidateHists::initialize()
{
  h_pt        = book(m_name, "Pt",   "p_{T} [GeV]",   100,  0,  500);
  h_pt_m      = book(m_name, "Pt_m", "p_{T} [GeV]",   100,  0, 1000);
  h_pt_l      = book(m_name, "Pt_l", "p_{T} [GeV]",   100,  0, 2000);
  h_pt_cor    = book(m_name, "Pt_cor",   "p_{T} (corrected) [GeV]",   100,  0,  500);
  h_pt_cor_m  = book(m_name, "Pt_cor_m", "p_{T} (corrected) [GeV]",   100,  0, 1000);
  h_pt_cor_l  = book(m_name, "Pt_cor_l", "p_{T} (corrected) [GeV]",   100,  0, 2000);
  h_pt_diff   = book(m_name, "Pt_diff",  "p_{T} (corrected diff) [GeV]",   100,  -500,  500);

  h_ht        = book(m_name, "Ht",   "H_{T} [GeV]",   100,  0,  500);
  h_ht_m      = book(m_name, "Ht_m", "H_{T} [GeV]",   100,  0, 1000);
  h_ht_l      = book(m_name, "Ht_l", "H_{T} [GeV]",   100,  0, 2000);
  h_eta       = book(m_name, "Eta",  "Eta",           200, -5,    5);
  h_phi       = book(m_name, "Phi",  "Phi",            50, -3.2,  3.2);
  h_m         = book(m_name, "Mass", "Mass [GeV]",    100,  0,  500);
  h_dRjj      = book(m_name, "dRjj", "dR(jj)",        305, -0.1,  6);
  h_mW        = book(m_name, "mW",   "mW [GeV]",      100, 40,  200);
  h_WdRjj     = book(m_name, "WdRjj","W dR(jj)",      305, -0.1,  6);
  h_mTop      = book(m_name, "mTop", "mTop [GeV]",    100, 80,  300);
  h_TdRwb     = book(m_name, "TdRwb","T dR(bW)",      205, -0.1,  4);
  h_Xtt       = book(m_name, "Xtt",  "Xtt",           100, -0.1, 15);
  h_nTags     = book(m_name, "nTags","nTags",           3, -0.5,  2.5);
  h_mWmT      = book(m_name,  "mWmT", "mWmT",   50, 40,   120, "m_{W} [GeV];m_{T} [GeV]",  50, 130, 210);

  //h_JVC       = book(m_name, "JVC", "JVC", 100, -5, 5);

  h_jetPtAsymmetry = book(m_name, "jetPtAsymmetry", "jetPtAsymmetry", 100, 0, 500);

  h_leadJet = new JetHists(m_name+"leadJet_" , "flavorTag", "", m_hCandName+" leadJet " );
  h_leadJet->initialize();

  h_sublJet = new JetHists(m_name+"sublJet_" , "flavorTag", "", m_hCandName+" sublJet ");
  h_sublJet->initialize();

  return StatusCode::SUCCESS;
}

StatusCode hCandidateHists::execute(const hCand& hcand, float eventWeight) 
{
  TLorentzVector* hp4 = hcand.p4;
  float pt = hp4->Pt();
  h_pt       -> Fill(pt,       eventWeight);
  h_pt_l     -> Fill(pt,       eventWeight);
  h_pt_m     -> Fill(pt,       eventWeight);

  float pt_cor = hcand.p4cor->Pt();
  h_pt_cor       -> Fill(pt_cor,       eventWeight);
  h_pt_cor_l     -> Fill(pt_cor,       eventWeight);
  h_pt_cor_m     -> Fill(pt_cor,       eventWeight);

  h_pt_diff     -> Fill(pt_cor-pt,       eventWeight);


  h_ht       -> Fill(hcand.m_sumPt,       eventWeight);
  h_ht_l     -> Fill(hcand.m_sumPt,       eventWeight);
  h_ht_m     -> Fill(hcand.m_sumPt,       eventWeight);

  h_eta      -> Fill(hp4->Eta(),      eventWeight);
  h_phi      -> Fill(hp4->Phi(),      eventWeight);
  h_m        -> Fill(hp4->M(),        eventWeight);
  h_dRjj     -> Fill(hcand.m_dRjj,    eventWeight);

  h_jetPtAsymmetry->Fill(hcand.m_jetPtAsymmetry, eventWeight);

  //h_JVC->Fill(hcand.m_JVC, eventWeight);

  h_leadJet   ->execute(hcand.m_leadJet   , eventWeight);
  h_sublJet   ->execute(hcand.m_sublJet   , eventWeight);


  return StatusCode::SUCCESS;
}

StatusCode hCandidateHists::finalize()
{
  
  HistogramManager::finalize();

  h_leadJet   ->finalize();
  h_sublJet   ->finalize();

  delete h_leadJet;
  delete h_sublJet;

  return StatusCode::SUCCESS;
}
