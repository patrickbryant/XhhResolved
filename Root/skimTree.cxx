#include "XhhResolved/skimTree.h"

using std::cout;  using std::endl; 

skimTree :: skimTree (const std::string& name, const std::string& detailStr, bool debug)
  : m_name(name), m_detailStr(detailStr), m_debug(debug), skimmedTree(0)
{ }

skimTree :: ~skimTree () 
{ }

StatusCode skimTree::initialize()
{
  skimmedTree = new TTree();
  skimmedTree->SetName((m_name+"Tree").c_str());
  //skimmedTree->Branch("NPV", m_NPV);
  skimmedTree->Branch("eventWeight",m_eventWeight);
  skimmedTree->Branch("leadHC_M", m_leadHC_M);
  skimmedTree->Branch("sublHC_M", m_sublHC_M);
  skimmedTree->Branch("leadHC_dRjj", m_leadHC_dRjj);
  skimmedTree->Branch("sublHC_dRjj", m_sublHC_dRjj);
  skimmedTree->Branch("Xhh",m_Xhh);
  skimmedTree->Branch("m4j", m_m4j);
							  
  return StatusCode::SUCCESS;
}

void skimTree::record(EL::Worker* wk)
{
  wk->addOutput(skimmedTree);
}


StatusCode skimTree::execute(const EventComb* eventComb, const hh4bEvent* /*event*/, float eventWeight)
{  
  if(m_debug) cout << "In skimTree::execute" << endl;
  const EventView* eventView = eventComb->m_selectedView;

  //*m_NPV = event->m_NPV;
  *m_eventWeight = eventWeight;
  *m_leadHC_M = eventView->m_leadHC->p4->M();
  *m_sublHC_M = eventView->m_sublHC->p4->M();
  *m_leadHC_dRjj = eventView->m_leadHC->m_dRjj;
  *m_sublHC_dRjj = eventView->m_sublHC->m_dRjj;
  *m_Xhh = eventView->m_xhh;
  *m_m4j = eventView->hhp4->M();

  if(m_debug) cout << "Fill skimmedTree" << endl;
  skimmedTree->Fill();
  if(m_debug) cout << "Filled skimmedTree" << endl;

  return StatusCode::SUCCESS;
}


StatusCode skimTree::finalize()
{
  if(m_debug) std::cout << "skimTree::finalize()" << std::endl;
  
  //delete skimmedTree;

  return StatusCode::SUCCESS;
}
