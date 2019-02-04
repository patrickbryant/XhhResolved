#include <EventLoop/Job.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <XhhResolved/TriggerEmulationStudy.h>
#include <xAODAnaHelpers/HelperFunctions.h>

#include "TFile.h"
#include "TKey.h"
#include "TLorentzVector.h"
#include "TSystem.h"

#include <utility>      
#include <iostream>
#include <fstream>

using namespace std;

// this is needed to distribute the algorithm to the workers
ClassImp(TriggerEmulationStudy)

TriggerEmulationStudy :: TriggerEmulationStudy () :
  m_debug        (false),
  m_printTriggers(false),
  m_printEmulatedTriggers(false),
  m_doAll(false),
  m_combName("")
{
  Info("TriggerEmulationStudy()", "Calling constructor");
}

EL::StatusCode TriggerEmulationStudy :: histInitialize ()
{
  Info("histInitialize()", "Calling histInitialize \n");

  //
  // data model
  m_event = hh4bEvent::global();

  //
  //  Setup the trigger emulation tool
  //
  m_trigEmulation          = new TriggerEmulation(false, false, false, false);
  m_trigEmulationData      = new TriggerEmulation(false, false, true,  false);
  m_trigEmulation_2015     = new TriggerEmulation(true , false, false, false);
  m_trigEmulation_2015Data = new TriggerEmulation(true , false, true,  false);
  
  //
  // Cutflow
  m_cutflow=new CutflowHists(m_name, "");
  ANA_CHECK( m_cutflow->initialize() );
  
  m_cf_all    = m_cutflow->addCut("all");
  m_cf_view   = m_cutflow->addCut("hasView");
  m_cf_HCPt   = m_cutflow->addCut("passHCPt");
  m_cf_HCdEta = m_cutflow->addCut("passHCdEta");
  m_cf_signal = m_cutflow->addCut("passSignal");

  m_cutflow->record(wk());

  //
  // Trigger Counts
  //

  m_passTrig=new CutflowHists(m_name+"/passTrig_", "");
  ANA_CHECK( m_passTrig->initialize() );

  m_passTrigEmu=new CutflowHists(m_name+"/passTrigEmu_", "");
  ANA_CHECK( m_passTrigEmu->initialize() );

  m_passBJetEmu=new CutflowHists(m_name+"/passBJetEmu_", "");
  ANA_CHECK( m_passBJetEmu->initialize() );


  // MC Triggers

  if(m_doAll){
    // b
    addTrig("HLT_j175_bmv2c2085_split");
    addTrig("HLT_j175_bmv2c2077_split");
  
    // b + 3j
    //addTrig("HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25");
    addTrig("HLT_j65_bperf_split_3j65_L14J15.0ETA25");
    addTrig("HLT_j65_bmv2c2070_split_3j65_L13J25.0ETA23");

    addTrig("HLT_j70_bmv2c2070_split_3j70_L13J25.0ETA23");
    addTrig("HLT_j70_bmv2c2077_split_3j70_L14J15.0ETA25");
    addTrig("HLT_j75_bmv2c2077_split_3j75_L13J25.0ETA23");

    addTrig("HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25");
    // addTrig("HLT_j75_boffperf_split_3j75_L14J15.0ETA25");


    // 2b + j 
    addTrig("HLT_2j65_bmv2c2070_split_j65");
    addTrig("HLT_2j70_bmv2c2077_split_j70");
    addTrig("HLT_2j70_bmv2c2070_split_j70");
    addTrig("HLT_2j75_bmv2c2077_split_j75");

    // 2b + 2j
    addTrig("HLT_2j35_bmv2c2070_split_2j35_L14J15.0ETA25");
    addTrig("HLT_2j45_bmv2c2070_split_2j45_L13J25.0ETA23");
    addTrig("HLT_2j45_bmv2c2077_split_2j45_L14J15.0ETA25");
    addTrig("HLT_2j55_bmv2c2077_split_2j55_L13J25.0ETA23");

    //
    //  2015
    //
    addTrig("HLT_2j45_bmedium_split_2j45_L14J15.0ETA25");
    addTrig("HLT_j175_bmedium_split_j60_bmedium_split");
    addTrig("HLT_2j55_bmedium_split_2j55_L13J25.0ETA23");
    addTrig("HLT_2j35_btight_split_2j35_L14J15.0ETA25");
    addTrig("HLT_2j45_btight_split_2j45_L13J25.0ETA23");
    addTrig("HLT_j225_bloose_split");
    addTrig("HLT_j300_bloose_split");
    
  }

  //
  //  hh4b triggers
  //
  addTrig("HLT_j225_bmv2c2060_split");
  addTrig("HLT_j100_2j55_bmv2c2060_split");
  addTrig("HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25");
  addTrig("HLT_hh4b_OR");  
  addTrig("HLT_hh4b_OR_SF");  
  addTrig("HLT_hh4b_OR_SFUp");  
  addTrig("HLT_hh4b_OR_SFDown");  
  addTrig("HLT_hh4b_OR_SFData");  
  addTrig("HLT_hh4b_OR_SFDataUp");  
  addTrig("HLT_hh4b_OR_SFDataDown");  

  addTrig("HLT_j70_bmedium_3j70_L14J15.0ETA25");
  addTrig("HLT_2j35_btight_2j35_L14J15.0ETA25");
  addTrig("HLT_j100_2j55_bmedium");
  addTrig("HLT_j225_bloose");
  addTrig("HLT_hh4b2015_OR");
  addTrig("HLT_hh4b2015_OR_SF");
  addTrig("HLT_hh4b2015_OR_SFUp");
  addTrig("HLT_hh4b2015_OR_SFDown");
  addTrig("HLT_hh4b2015_OR_SFData");  
  addTrig("HLT_hh4b2015_OR_SFDataUp");  
  addTrig("HLT_hh4b2015_OR_SFDataDown");  


  addTrig("HLT_j100_2j55_bperf");
  addTrig("HLT_j225_bperf");
  addTrig("HLT_2j35_bperf_2j35_L14J15.0ETA25");
  addTrig("HLT_j100_2j55_bperf_split");
  addTrig("HLT_j100_2j55_boffperf_split");
  addTrig("HLT_j225_bperf_split");
  addTrig("HLT_2j35_bperf_split_2j35_L14J15.0ETA25");

  m_passTrig   ->record(wk());
  m_passTrigEmu->record(wk());
  m_passBJetEmu->record(wk());


  return EL::StatusCode::SUCCESS;
}

EL::StatusCode TriggerEmulationStudy :: initialize ()
{
  if(m_debug) Info("initialize()", "Calling initialize");
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode TriggerEmulationStudy :: execute ()
{
  if(m_debug) Info("execute()", "Processing Event");
  float eventWeight    =m_event->getEventWeight();

  if(m_printTriggers){
    m_event->printTriggers();
  }

  if(m_printEmulatedTriggers){
    m_event->printEmulatedTriggers();
  }

  m_cutflow->execute(m_cf_all, eventWeight, 1.0);

  if(m_event->m_eventComb->at(m_combName)->size()==0){
    if(m_debug) cout << " Fail nJets/nbJets" << endl;
    return EL::StatusCode::SUCCESS;
  }

  EventComb* thisComb = m_event->m_eventComb->at(m_combName)->at(0);

  EventView* thisView = thisComb->m_selectedView;
  if(!thisView)   return EL::StatusCode::SUCCESS;

  //
  // Only fill combinations with a valid event view
  //
  float viewWeight = eventWeight * thisView->m_qcd_weight;
  m_cutflow->execute(m_cf_view, viewWeight, 1.0);

  //
  //  dR/dPhi cuts for studies (nominal is no cut)
  //
  if(!thisView->m_passHCPt) return EL::StatusCode::SUCCESS;
  m_cutflow->execute(m_cf_HCPt, eventWeight, 1.0); 

  if(!thisView->m_passHCdEta) return EL::StatusCode::SUCCESS;
  m_cutflow->execute(m_cf_HCdEta, eventWeight, 1.0); 
    
  if(!thisView->m_passSignal) return EL::StatusCode::SUCCESS;
  m_cutflow->execute(m_cf_signal, eventWeight, 1.0); 

  m_passTrig   ->execute("all", eventWeight, 1.0);
  m_passBJetEmu->execute("all", eventWeight, 1.0);
  m_passTrigEmu->execute("all", eventWeight, 1.0);

  //
  //  Checkt the bits
  //
  for(auto trigEntry : m_trigMap) {
    checkTrigBits(trigEntry.first, eventWeight);
  }

  //
  // Fill OR
  //
  if(m_event->passEmulatedTrig("HLT_j225_bmv2c2060_split")      || 
     m_event->passEmulatedTrig("HLT_j100_2j55_bmv2c2060_split") ||
     m_event->passEmulatedTrig("HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25") ){
    ANA_CHECK( m_passBJetEmu   ->execute(m_emulated_BJetMap["HLT_hh4b_OR"],          eventWeight, 1.0)  ); 
  }
  
  if(m_event->passEmulatedTrig("HLT_2j35_btight_2j35_L14J15.0ETA25")      || 
     m_event->passEmulatedTrig("HLT_j100_2j55_bmedium") ||
     m_event->passEmulatedTrig("HLT_j225_bloose") ){
    ANA_CHECK( m_passBJetEmu->execute(m_emulated_BJetMap["HLT_hh4b2015_OR"], eventWeight, 1.0) ); 
  }


  m_trigEmulation    ->emulateTrigger2016(m_event);
  float trigSF2016    = 1;
  float trigSFErr2016 = 0;
  m_trigEmulation->apply2016PVEff      (m_event, trigSF2016, trigSFErr2016);
  m_trigEmulation->emulateTriggerSF2016(m_event, trigSF2016, trigSFErr2016);


  m_trigEmulationData->emulateTrigger2016(m_event);
  float trigSF2016Data    = 1;
  float trigSFErr2016Data = 0;
  m_trigEmulationData->apply2016PVEff      (m_event, trigSF2016Data, trigSFErr2016Data);  
  m_trigEmulationData->emulateTriggerSF2016(m_event, trigSF2016Data, trigSFErr2016Data);

  if(m_doAll){
    checkTrigEmulation("HLT_j175_bmv2c2085_split", m_trigEmulation->m_pass_HLT_j175_bmv2c2085_split, eventWeight );
    checkTrigEmulation("HLT_j175_bmv2c2077_split", m_trigEmulation->m_pass_HLT_j175_bmv2c2077_split, eventWeight );
  
    // b + 3j
    checkTrigEmulation("HLT_j65_bperf_split_3j65_L14J15.0ETA25"    , m_trigEmulation->m_pass_HLT_j65_bperf_split_3j65_L14J15_0ETA25      , eventWeight);
    checkTrigEmulation("HLT_j65_bmv2c2070_split_3j65_L13J25.0ETA23", m_trigEmulation->m_pass_HLT_j65_bmv2c2070_split_3j65_L13J25_0ETA23  , eventWeight);

    checkTrigEmulation("HLT_j70_bmv2c2070_split_3j70_L13J25.0ETA23", m_trigEmulation->m_pass_HLT_j70_bmv2c2070_split_3j70_L13J25_0ETA23 , eventWeight);
    checkTrigEmulation("HLT_j70_bmv2c2077_split_3j70_L14J15.0ETA25", m_trigEmulation->m_pass_HLT_j70_bmv2c2077_split_3j70_L14J15_0ETA25 , eventWeight);
    checkTrigEmulation("HLT_j75_bmv2c2077_split_3j75_L13J25.0ETA23", m_trigEmulation->m_pass_HLT_j75_bmv2c2077_split_3j75_L13J25_0ETA23 , eventWeight);
    checkTrigEmulation("HLT_j75_bmv2c2070_split_3j75_L14J15.0ETA25",   m_trigEmulation->m_pass_HLT_j75_bmv2c2070_split_3j75_L14J15_0ETA25 , eventWeight);
    checkTrigEmulation("HLT_j75_boffperf_split_3j75_L14J15.0ETA25",    m_trigEmulation->m_pass_HLT_j75_bmv2c2070_split_3j75_L14J15_0ETA25 , eventWeight);


    // 2b + j 
    checkTrigEmulation("HLT_2j65_bmv2c2070_split_j65",  m_trigEmulation->m_pass_HLT_2j65_bmv2c2070_split_j65,  eventWeight);
    checkTrigEmulation("HLT_2j70_bmv2c2077_split_j70",  m_trigEmulation->m_pass_HLT_2j70_bmv2c2077_split_j70,  eventWeight);
    checkTrigEmulation("HLT_2j70_bmv2c2070_split_j70",  m_trigEmulation->m_pass_HLT_2j70_bmv2c2070_split_j70,  eventWeight);
    checkTrigEmulation("HLT_2j75_bmv2c2077_split_j75",  m_trigEmulation->m_pass_HLT_2j75_bmv2c2077_split_j75,  eventWeight);

    // 2b + 2j
    checkTrigEmulation("HLT_2j35_bmv2c2070_split_2j35_L14J15.0ETA25",  m_trigEmulation->m_pass_HLT_2j35_bmv2c2070_split_2j35_L14J15_0ETA25   , eventWeight);
    checkTrigEmulation("HLT_2j45_bmv2c2070_split_2j45_L13J25.0ETA23",  m_trigEmulation->m_pass_HLT_2j45_bmv2c2070_split_2j45_L13J25_0ETA23   , eventWeight);
    checkTrigEmulation("HLT_2j45_bmv2c2077_split_2j45_L14J15.0ETA25",  m_trigEmulation->m_pass_HLT_2j45_bmv2c2077_split_2j45_L14J15_0ETA25   , eventWeight);
    checkTrigEmulation("HLT_2j55_bmv2c2077_split_2j55_L13J25.0ETA23",  m_trigEmulation->m_pass_HLT_2j55_bmv2c2077_split_2j55_L13J25_0ETA23   , eventWeight);
  }
  
  //
  //  hh4b triggers
  //
  checkTrigEmulation("HLT_j225_bmv2c2060_split",                     m_trigEmulation->m_pass_HLT_j225_bmv2c2060_split , eventWeight   );
  checkTrigEmulation("HLT_j100_2j55_bmv2c2060_split",                m_trigEmulation->m_pass_HLT_j100_2j55_bmv2c2060_split, eventWeight   );
  checkTrigEmulation("HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25",  m_trigEmulation->m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25 , eventWeight   );
  checkTrigEmulation("HLT_hh4b_OR",                                  m_trigEmulation->m_pass_HLT_hh4b_OR , eventWeight   );
  checkTrigEmulation("HLT_hh4b_OR_SF",                               true , eventWeight*trigSF2016   );
  checkTrigEmulation("HLT_hh4b_OR_SFUp",                             true , eventWeight*(trigSF2016-trigSFErr2016)   );
  checkTrigEmulation("HLT_hh4b_OR_SFDown",                           true , eventWeight*(trigSF2016+trigSFErr2016)   );
  checkTrigEmulation("HLT_hh4b_OR_SFData",                           true , eventWeight*trigSF2016Data   );
  checkTrigEmulation("HLT_hh4b_OR_SFDataUp",                         true , eventWeight*(trigSF2016Data-trigSFErr2016Data)   );
  checkTrigEmulation("HLT_hh4b_OR_SFDataDown",                       true , eventWeight*(trigSF2016Data+trigSFErr2016Data)   );
  
  
  m_trigEmulation_2015->emulateTrigger2015(m_event);
  float trigSF2015    = 1;
  float trigSFErr2015 = 0;
  m_trigEmulation_2015->emulateTriggerSF2015(m_event, trigSF2015, trigSFErr2015);

  m_trigEmulation_2015Data->emulateTrigger2015(m_event);
  float trigSF2015Data    = 1;
  float trigSFErr2015Data = 0;
  m_trigEmulation_2015Data->emulateTriggerSF2015(m_event, trigSF2015Data, trigSFErr2015Data);

  

  if(m_doAll){
    checkTrigEmulation("HLT_2j45_bmedium_split_2j45_L14J15.0ETA25" , m_trigEmulation_2015->m_pass_HLT_2j45_bmedium_split_2j45_L14J15_0ETA25  , eventWeight   );
    checkTrigEmulation("HLT_j175_bmedium_split_j60_bmedium_split"  , m_trigEmulation_2015->m_pass_HLT_j175_bmedium_split_j60_bmedium_split   , eventWeight   );
    checkTrigEmulation("HLT_2j55_bmedium_split_2j55_L13J25.0ETA23" , m_trigEmulation_2015->m_pass_HLT_2j55_bmedium_split_2j55_L13J25_0ETA23  , eventWeight   );
    checkTrigEmulation("HLT_2j35_btight_split_2j35_L14J15.0ETA25"  , m_trigEmulation_2015->m_pass_HLT_2j35_btight_split_2j35_L14J15_0ETA25   , eventWeight   );
    checkTrigEmulation("HLT_2j45_btight_split_2j45_L13J25.0ETA23"  , m_trigEmulation_2015->m_pass_HLT_2j45_btight_split_2j45_L13J25_0ETA23   , eventWeight   );
    checkTrigEmulation("HLT_j225_bloose_split"                     , m_trigEmulation_2015->m_pass_HLT_j225_bloose_split                      , eventWeight   );
    checkTrigEmulation("HLT_j300_bloose_split"                     , m_trigEmulation_2015->m_pass_HLT_j300_bloose_split                      , eventWeight   );
  }
  
  //
  //  hh4b triggers
  //
  //checkTrigEmulation("HLT_j70_bmedium_3j70_L14J15.0ETA25",           m_trigEmulation_2015->m_pass_HLT_j70_bmedium_3j70_L14J15_0ETA25 , eventWeight   );
  checkTrigEmulation("HLT_2j35_btight_2j35_L14J15.0ETA25" ,          m_trigEmulation_2015->m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25 , eventWeight   );
  checkTrigEmulation("HLT_j100_2j55_bmedium",                        m_trigEmulation_2015->m_pass_HLT_j100_2j55_bmedium , eventWeight   );              
  checkTrigEmulation("HLT_j225_bloose",                              m_trigEmulation_2015->m_pass_HLT_j225_bloose , eventWeight   );
  checkTrigEmulation("HLT_hh4b2015_OR",                              m_trigEmulation_2015->m_pass_HLT_hh4b2015_OR , eventWeight   );
  checkTrigEmulation("HLT_hh4b2015_OR_SF",                           true , eventWeight*trigSF2015   );
  checkTrigEmulation("HLT_hh4b2015_OR_SFUp",                         true , eventWeight*(trigSF2015-trigSFErr2015)   );
  checkTrigEmulation("HLT_hh4b2015_OR_SFDown",                       true , eventWeight*(trigSF2015+trigSFErr2015)   );
  checkTrigEmulation("HLT_hh4b2015_OR_SFData",                       true , eventWeight*trigSF2015Data   );
  checkTrigEmulation("HLT_hh4b2015_OR_SFDataUp",                     true , eventWeight*(trigSF2015Data-trigSFErr2015Data)   );
  checkTrigEmulation("HLT_hh4b2015_OR_SFDataDown",                   true , eventWeight*(trigSF2015Data+trigSFErr2015Data)   );


  //checkTrigEmulation("HLT_j70_bperf_3j70_L14J15.0ETA25",           m_trigEmulation_2015->m_pass_HLT_j70_bperf_3j70_L14J15_0ETA25 , eventWeight   );
  checkTrigEmulation("HLT_2j35_bperf_2j35_L14J15.0ETA25" ,         m_trigEmulation_2015->m_pass_HLT_2j35_bperf_2j35_L14J15_0ETA25 , eventWeight   );
  checkTrigEmulation("HLT_j100_2j55_bperf",                        m_trigEmulation_2015->m_pass_HLT_j100_2j55_bperf , eventWeight   );              
  checkTrigEmulation("HLT_j225_bperf",                             m_trigEmulation_2015->m_pass_HLT_j225_bperf , eventWeight   );
  checkTrigEmulation("HLT_j100_2j55_bperf_split",                  m_trigEmulation     ->m_pass_HLT_j100_2j55_bperf , eventWeight   );              


  //
  //  Debugging
  //
  if(m_event->passEmulatedTrig("HLT_j100_2j55_bmedium"))         thisComb->m_passedTriggers->push_back("HLT_j100_2j55_bmed_BJetTrigEMu");
  if(m_event->passEmulatedTrig("HLT_j100_2j55_bmv2c2060_split")) thisComb->m_passedTriggers->push_back("HLT_j100_2j55_b60_BJetTrigEMu");
  if(m_trigEmulation_2015->m_pass_HLT_j100_2j55_bmedium)         thisComb->m_passedTriggers->push_back("HLT_j100_2j55_bmed_EMu");               
  if(m_trigEmulation     ->m_pass_HLT_j100_2j55_bmv2c2060_split) thisComb->m_passedTriggers->push_back("HLT_j100_2j55_b60_EMu");               

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode TriggerEmulationStudy :: histFinalize ()
{
  ANA_CHECK(m_cutflow->finalize());
  delete m_cutflow;

  ANA_CHECK(m_passTrig->finalize());
  delete m_passTrig;

  ANA_CHECK(m_passTrigEmu->finalize());
  delete m_passTrigEmu;

  ANA_CHECK(m_passBJetEmu->finalize());
  delete m_passBJetEmu;

  return EL::StatusCode::SUCCESS;
}


void TriggerEmulationStudy::addTrig(std::string trigName)
{
  int cf_thiscut   = m_passTrig->addCut(trigName);
  m_trigMap.insert(make_pair(trigName, cf_thiscut));

  cf_thiscut   = m_passTrigEmu->addCut(trigName);
  m_emulated_trigMap.insert(make_pair(trigName, cf_thiscut));

  cf_thiscut   = m_passBJetEmu->addCut(trigName);
  m_emulated_BJetMap.insert(make_pair(trigName, cf_thiscut));

  return;
}

void TriggerEmulationStudy::checkTrigBits(const std::string& trigName, float eventWeight)
{
  if(m_event->passTrig(trigName))          m_passTrig   ->execute(m_trigMap[trigName],          eventWeight, 1.0) ; 
  if(m_event->passEmulatedTrig(trigName))  m_passBJetEmu->execute(m_emulated_BJetMap[trigName], eventWeight, 1.0) ; 
  return;
}

void TriggerEmulationStudy::checkTrigEmulation(const std::string& trigName, bool passTrig, float eventWeight)
{
  if(passTrig) m_passTrigEmu->execute(m_emulated_trigMap[trigName], eventWeight, 1.0); 
  return;
}
