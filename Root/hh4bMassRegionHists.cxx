#include "XhhResolved/hh4bMassRegionHists.h"

using std::cout;  using std::endl; 

hh4bMassRegionHists :: hh4bMassRegionHists (const std::string& name, const std::string& detailStr, const std::string& signalExtras, bool doTagCategories, bool doJetCategories)
  : HistogramManager(name, detailStr), m_debug(false), m_fast(false), m_doTagCategories(doTagCategories), m_doJetCategories(doJetCategories), 
    h_Inclusive(0), h_NoSR(0), h_Sideband(0), h_Control(0), h_Signal(0), h_LMVR(0), h_HMVR(0),
    h_FullMassPlane(0),
    h_FullMassPlane_nJet4(0), h_FullMassPlane_nJet5(0),
    h_NoSR_nJet4(0), h_NoSR_nJet5(0),
    h_Sideband_nJet4(0), h_Sideband_nJet5(0),// h_Sideband_nJet6(0),
    h_Control_nJet4(0), h_Control_nJet5(0),// h_Control_nJet6(0),
    h_Signal_nJet4(0), h_Signal_nJet5(0),// h_Signal_nJet6(0),
    m_signalHistExtraFlags(signalExtras)
{ }

hh4bMassRegionHists :: ~hh4bMassRegionHists () 
{ }

StatusCode hh4bMassRegionHists::initialize()
{
  h_Sideband         = new hh4bHists(m_name+"Sideband",  m_detailStr);
  h_Sideband->initialize();				  
							  
  h_Control          = new hh4bHists(m_name+"Control",   m_detailStr);
  h_Control->initialize();				  
							  
  h_Signal           = new hh4bHists(m_name+"Signal",    m_detailStr+" "+m_signalHistExtraFlags);
  h_Signal->initialize();

  if(m_fast) return::StatusCode::SUCCESS;

  h_Inclusive        = new hh4bHists(m_name+"Inclusive", m_detailStr);
  h_Inclusive->initialize();

  h_NoSR             = new hh4bHists(m_name+"NoSR", m_detailStr);
  h_NoSR->initialize();

  h_LMVR         = new hh4bHists(m_name+"LMVR",  m_detailStr);
  h_LMVR->initialize();

  h_HMVR         = new hh4bHists(m_name+"HMVR",  m_detailStr);
  h_HMVR->initialize();

  h_FullMassPlane = new hh4bHists(m_name+"FullMassPlane",m_detailStr);
  h_FullMassPlane->initialize();


  if(m_doJetCategories){
    h_Sideband_nJet4         = new hh4bHists(m_name+"Sideband_nJet4",  m_detailStr);
    h_Sideband_nJet5         = new hh4bHists(m_name+"Sideband_nJet5",  m_detailStr);
    h_Sideband_nJet4->initialize();				  
    h_Sideband_nJet5->initialize();				  

    h_Control_nJet4         = new hh4bHists(m_name+"Control_nJet4",  m_detailStr);
    h_Control_nJet5         = new hh4bHists(m_name+"Control_nJet5",  m_detailStr);
    h_Control_nJet4->initialize();				  
    h_Control_nJet5->initialize();				  

    h_Signal_nJet4         = new hh4bHists(m_name+"Signal_nJet4",  m_detailStr);
    h_Signal_nJet5         = new hh4bHists(m_name+"Signal_nJet5",  m_detailStr);
    h_Signal_nJet4->initialize();				  
    h_Signal_nJet5->initialize();				  

    h_FullMassPlane_nJet4         = new hh4bHists(m_name+"FullMassPlane_nJet4",  m_detailStr);
    h_FullMassPlane_nJet5         = new hh4bHists(m_name+"FullMassPlane_nJet5",  m_detailStr);
    h_FullMassPlane_nJet4->initialize();				  
    h_FullMassPlane_nJet5->initialize();				  

    h_NoSR_nJet4         = new hh4bHists(m_name+"NoSR_nJet4",  m_detailStr);
    h_NoSR_nJet5         = new hh4bHists(m_name+"NoSR_nJet5",  m_detailStr);
    h_NoSR_nJet4->initialize();				  
    h_NoSR_nJet5->initialize();				  

  }
  return StatusCode::SUCCESS;
}

void hh4bMassRegionHists::record(EL::Worker* wk)
{
  HistogramManager::record(wk);
  h_Sideband      ->record(wk);
  h_Control       ->record(wk);
  h_Signal        ->record(wk);

  if(m_fast) return;

  h_Inclusive     ->record(wk);
  h_NoSR          ->record(wk);
  h_LMVR      ->record(wk);
  h_HMVR      ->record(wk);
  h_FullMassPlane->record(wk);

  if(m_doJetCategories){
    h_Sideband_nJet4->record(wk);
    h_Sideband_nJet5->record(wk);

    h_Control_nJet4->record(wk);
    h_Control_nJet5->record(wk);

    h_Signal_nJet4->record(wk);
    h_Signal_nJet5->record(wk);

    h_FullMassPlane_nJet4->record(wk);
    h_FullMassPlane_nJet5->record(wk);

    h_NoSR_nJet4->record(wk);
    h_NoSR_nJet5->record(wk);
  }

}


StatusCode hh4bMassRegionHists::execute(const EventComb* eventComb, const hh4bEvent* event, float eventWeight)
{
  ANA_CHECK(HistogramManager::execute());
  if(m_debug) std::cout << "hh4bMassRegionHists::execute()" << std::endl;
  
  const EventView* eventView = eventComb->m_selectedView;

  //if(eventView->m_dhh>20) return StatusCode::SUCCESS;

  if(m_debug) std::cout << "hh4bMassRegionHists::execute() start filling mass regions" << std::endl;
  if(eventView->m_passSideband) h_Sideband->execute(eventComb, event, eventWeight);
  if(eventView->m_passControl ) h_Control ->execute(eventComb, event, eventWeight);
  if(eventView->m_passSignal  ) h_Signal  ->execute(eventComb, event, eventWeight);
  if(m_fast) return StatusCode::SUCCESS;
 
  h_FullMassPlane->execute(eventComb, event, eventWeight);
  
  if(eventView->m_passSideband || eventView->m_passControl || eventView->m_passSignal)
    h_Inclusive-> execute(eventComb, event, eventWeight);
  if((eventView->m_passSideband || eventView->m_passControl) && !eventView->m_passSignal)
    h_NoSR->execute(eventComb, event, eventWeight);
  if(eventView->m_passLMVR) h_LMVR->execute(eventComb, event, eventWeight);
  if(eventView->m_passHMVR) h_HMVR->execute(eventComb, event, eventWeight);

  if(m_doJetCategories){
    if(eventView->m_passSideband && eventComb->m_nonHCJets->size() == 0) h_Sideband_nJet4->execute(eventComb, event, eventWeight);
    if(eventView->m_passSideband && eventComb->m_nonHCJets->size() >= 1) h_Sideband_nJet5->execute(eventComb, event, eventWeight);

    if(eventView->m_passControl && eventComb->m_nonHCJets->size() == 0) h_Control_nJet4->execute(eventComb, event, eventWeight);
    if(eventView->m_passControl && eventComb->m_nonHCJets->size() >= 1) h_Control_nJet5->execute(eventComb, event, eventWeight);

    if(eventView->m_passSignal && eventComb->m_nonHCJets->size() == 0) h_Signal_nJet4->execute(eventComb, event, eventWeight);
    if(eventView->m_passSignal && eventComb->m_nonHCJets->size() >= 1) h_Signal_nJet5->execute(eventComb, event, eventWeight);

    if(eventComb->m_nonHCJets->size() == 0) h_FullMassPlane_nJet4->execute(eventComb, event, eventWeight);
    if(eventComb->m_nonHCJets->size() >= 1) h_FullMassPlane_nJet5->execute(eventComb, event, eventWeight);

    if((eventView->m_passSideband || eventView->m_passControl) && !eventView->m_passSignal && eventComb->m_nonHCJets->size() == 0) 
      h_NoSR_nJet4->execute(eventComb, event, eventWeight);
    if((eventView->m_passSideband || eventView->m_passControl) && !eventView->m_passSignal && eventComb->m_nonHCJets->size() >= 1) 
      h_NoSR_nJet5->execute(eventComb, event, eventWeight);
  }
  return StatusCode::SUCCESS;
}


StatusCode hh4bMassRegionHists::finalize()
{
  if(m_debug) std::cout << "hh4bMassRegionHists::finalize()" << std::endl;
  HistogramManager::finalize();

  h_Sideband     ->finalize();
  delete h_Sideband;

  h_Control     ->finalize();
  delete h_Control;

  h_Signal     ->finalize();
  delete h_Signal;

  if(m_fast) return::StatusCode::SUCCESS;

  h_Inclusive     ->finalize();
  delete h_Inclusive;

  h_NoSR          ->finalize();
  delete h_NoSR;

  h_LMVR     ->finalize();
  delete h_LMVR;

  h_HMVR     ->finalize();
  delete h_HMVR;

  h_FullMassPlane->finalize();
  delete h_FullMassPlane;

  if(m_doJetCategories){
    h_Sideband_nJet4->finalize();
    h_Sideband_nJet5->finalize();
    delete h_Sideband_nJet4;
    delete h_Sideband_nJet5;

    h_Control_nJet4->finalize();
    h_Control_nJet5->finalize();
    delete h_Control_nJet4;
    delete h_Control_nJet5;

    h_Signal_nJet4->finalize();
    h_Signal_nJet5->finalize();
    delete h_Signal_nJet4;
    delete h_Signal_nJet5;

    h_FullMassPlane_nJet4->finalize();
    h_FullMassPlane_nJet5->finalize();
    delete h_FullMassPlane_nJet4;
    delete h_FullMassPlane_nJet5;

    h_NoSR_nJet4->finalize();
    h_NoSR_nJet5->finalize();
    delete h_NoSR_nJet4;
    delete h_NoSR_nJet5;
  }

  return StatusCode::SUCCESS;
}
