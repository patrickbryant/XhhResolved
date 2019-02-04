#include <EventLoop/Job.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <XhhResolved/hCandBuilderBase.h>
#include <xAODAnaHelpers/HelperFunctions.h>

#include "TFile.h"
#include "TH1D.h"
#include "TKey.h"
#include "TLorentzVector.h"
#include "TSystem.h"

#include <iostream>
#include <fstream>


using namespace std;

// this is needed to distribute the algorithm to the workers
ClassImp(hCandBuilderBase)

hCandBuilderBase :: hCandBuilderBase () :
  m_debug(false),
  m_mc(false),
  m_doTrigEmulation(false),
  m_useTrigSF(false),
  m_promoteMuons(false),
  m_year  ("2016"),
  m_tagger("MV2c10"),
  m_combName("4b"),
  m_nonTaggedName("NonTagged"),
  m_minTagJets(0),
  m_maxTagJets(1000),
  m_minTotalJets(4),
  m_leadMass_SR(0), m_sublMass_SR(0), 
  m_radius_SR(0),   m_radius_CR(0), m_radius_SB(0),
  m_CR_shift(1.0),  m_SB_shift(1.0),
  m_do2015(false),
  m_trigEmulation(nullptr),
  m_combList(0),
  m_eventData(0)
{
  Info("hCandBuilderBase()", ("Calling constructor: "+m_combName).c_str());
}

EL::StatusCode hCandBuilderBase :: setupJob (EL::Job& /*job*/)
{
  Info("hCandBuilderBase()", "setupJob");
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hCandBuilderBase :: histInitialize ()
{
  Info("histInitialize()", "Calling histInitialize \n");

  //
  // data model
  m_eventData=hh4bEvent::global();

  m_eventData->m_eventComb->insert(std::make_pair(m_combName,           new EventCombVec()));
  m_combList = m_eventData->m_eventComb->at(m_combName);

  //
  // Cutflow
  m_cutflow=new CutflowHists(m_name, "");
  ANA_CHECK( m_cutflow->initialize() );
  
  m_cf_comb             = m_cutflow->addCut("comb");
  m_cf_drjj             = m_cutflow->addCut("drjj");
  m_cf_dphi             = m_cutflow->addCut("dphi");
  m_cf_passMinNTagJets  = m_cutflow->addCut("passMinNTagJets");
  m_cf_passMaxNTagJets  = m_cutflow->addCut("passMaxNTagJets");
  m_cf_passMinNTotalJet = m_cutflow->addCut("passMinNTotalJets");
  m_cutflow->record(wk());

  if(m_year == "2015") m_do2015 = true;
  else                 m_do2015 = false;

  // Trigger Emulation
  if(m_doTrigEmulation){
    if(m_year == "2015") m_trigEmulation = new TriggerEmulation(true );
    else                 m_trigEmulation = new TriggerEmulation(false);
  }

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hCandBuilderBase :: fileExecute ()
{
  Info("hCandBuilderBase()", "fileExecute");
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed
  return EL::StatusCode::SUCCESS;
}





EL::StatusCode hCandBuilderBase :: initialize ()
{
  Info("initialize()", "Succesfully initialized! \n");
  return EL::StatusCode::SUCCESS;
}


EL::StatusCode hCandBuilderBase :: execute ()
{
  if(m_debug) Info("execute()", "Processing Event (hCandBuilderBase)");

  float eventWeight    = m_eventData->getEventWeight();


  unsigned int nTaggedJets      = m_eventData->m_taggedJets     ->size();
  //unsigned int nTotalJets       = m_eventData->m_selectedJets   ->size();
  unsigned int nLooseTaggedJets = m_eventData->m_looseTaggedJets->size();

  //
  //  NTagged Jets
  //
  if ( nTaggedJets < m_minTagJets ) {
    if(m_debug) std::cout << " Fail min nTag Jets" << endl;
    return EL::StatusCode::SUCCESS; // go to next event
  }  
  m_cutflow->execute(m_cf_passMinNTagJets, eventWeight);

  if ( nTaggedJets > m_maxTagJets ) {
    if(m_debug) std::cout << " Fail max nTag Jets" << endl;
    return EL::StatusCode::SUCCESS; // go to next event
  }  
  m_cutflow->execute(m_cf_passMaxNTagJets, eventWeight);

  //if ( nTotalJets < m_minTotalJets ) {
  if( nLooseTaggedJets < m_minTotalJets ) {
    if(m_debug) std::cout << " Fail min nTotal(loose tag) Jets" << endl;
    return EL::StatusCode::SUCCESS; // go to next event
  }  
  m_cutflow->execute(m_cf_passMinNTotalJet, eventWeight);

  //
  // Out sourced...
  //
  buildHCands();

  //
  //  Count cut flow
  //
  if(m_pass_drjj) m_cutflow->execute(m_cf_drjj, eventWeight);  
  if(m_pass_dphi) m_cutflow->execute(m_cf_dphi, eventWeight);  
  
  if(m_debug) Info("execute()", "Processed Event (hCandBuilderBase)");
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode hCandBuilderBase :: postExecute ()
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hCandBuilderBase :: finalize ()
{
  Info("hCandBuilderBase()", "finalize");
  return EL::StatusCode::SUCCESS;
}




EL::StatusCode hCandBuilderBase :: histFinalize ()
{
  ANA_CHECK(m_cutflow->finalize());
  delete m_cutflow;

  return EL::StatusCode::SUCCESS;
}



void hCandBuilderBase :: addEvent (const vector<const xAH::Jet*>& HCJets, const vector<const xAH::Jet*>& nonHCJets, TRandom3* rand)
{
  m_combList->push_back(new EventComb());
  EventComb* thisComb = m_combList->back();
  thisComb->m_debug = m_debug;

  // 
  // Take the first 4 tagged jets.
  //
  for(const xAH::Jet* hcJet : HCJets){
    thisComb->m_HCJets        ->push_back(hcJet);
    thisComb->m_HCJets_mv2Sort->push_back(hcJet);
  }

  // 
  // nonTagged Jets get considered as nonBJets
  //
  for(const xAH::Jet* nonHCJet : nonHCJets){
    thisComb->m_nonHCJets   ->push_back(nonHCJet);
  }
    
  thisComb->buildAndSelectEventViews(m_leadMass_SR, m_sublMass_SR, m_radius_SR, m_radius_CR, m_radius_SB, m_CR_shift, m_SB_shift,
				     m_pass_drjj, m_pass_dphi, rand);

  //
  // Set Trigger Decisions
  //

  //
  // do Trigger (If data or if not emulating Trigger) 
  //
  bool L1_4J15_ETA25 = false;
  bool L1_J75_3J20   = false;
  bool L1_J100       = false;

  bool HLT_2j35_btight_2j35_L14J15 = false;
  bool HLT_j100_2j55_bmedium       = false;
  bool HLT_j225_bloose             = false;

  bool HLT_2j35_bmv2c2060_split_2j35_L14J15 = false;
  bool HLT_j100_2j55_bmv2c2060_split        = false;
  bool HLT_j225_bmv2c2060_split             = false;

  bool HLT_mu26_ivarmedium_2j35_boffperf = false;
 
  //
  //  Use the trigger bits in data and MC if not doing emulation
  //
  if(m_debug) m_eventData->printTriggers();
  L1_4J15_ETA25 = m_eventData->passTrig("L1_4J15.0ETA25");
  L1_J75_3J20   = m_eventData->passTrig("L1_J75_3J20");
  L1_J100       = m_eventData->passTrig("L1_J100");

  if(L1_4J15_ETA25) thisComb->m_passedL1Triggers->push_back("L1_4J15.0ETA25");
  if(L1_J75_3J20)   thisComb->m_passedL1Triggers->push_back("L1_J75_3J20");
  if(L1_J100)       thisComb->m_passedL1Triggers->push_back("L1_J100");

  if(L1_4J15_ETA25 | L1_J75_3J20 | L1_J100) thisComb->m_passedL1Triggers->push_back("L1");

  if(!m_mc || !m_doTrigEmulation){

    if(m_do2015){
      HLT_2j35_btight_2j35_L14J15  = m_eventData->passTrig("HLT_2j35_btight_2j35_L14J15.0ETA25");
      HLT_j100_2j55_bmedium        = m_eventData->passTrig("HLT_j100_2j55_bmedium"); 
      HLT_j225_bloose              = m_eventData->passTrig("HLT_j225_bloose");       

    } else {
      if(m_debug){
	for(auto trig : *(m_eventData->m_passedTriggers)) std::cout << "hCandBuilderBase::addEvent trig "<<trig<<std::endl;
      }
      HLT_2j35_bmv2c2060_split_2j35_L14J15 = m_eventData->passTrig("HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25");
      HLT_j100_2j55_bmv2c2060_split        = m_eventData->passTrig("HLT_j100_2j55_bmv2c2060_split");
      HLT_j225_bmv2c2060_split             = m_eventData->passTrig("HLT_j225_bmv2c2060_split");
    }//year

  }// no trig emulation

  //
  // Emulate the trigger. If using prompt muons as b-jets, emulate trigger.
  //
  if((m_mc && m_doTrigEmulation) || m_promoteMuons){
    
    if(m_do2015){

      m_trigEmulation->emulateTrigger2015(m_eventData);

      HLT_2j35_btight_2j35_L14J15  = m_trigEmulation->m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25;
      HLT_j100_2j55_bmedium        = m_trigEmulation->m_pass_HLT_j100_2j55_bmedium;
      HLT_j225_bloose              = m_trigEmulation->m_pass_HLT_j225_bloose;

    } else { // 2016

      m_trigEmulation->emulateTrigger2016(m_eventData);
      
      //
      // Get the PV efficiency
      //
      m_trigEmulation->apply2016PVEff(m_eventData, thisComb->m_trigSF, thisComb->m_trigSFErr);

      HLT_2j35_bmv2c2060_split_2j35_L14J15 = m_trigEmulation->m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25;
      HLT_j100_2j55_bmv2c2060_split        = m_trigEmulation->m_pass_HLT_j100_2j55_bmv2c2060_split;
      HLT_j225_bmv2c2060_split             = m_trigEmulation->m_pass_HLT_j225_bmv2c2060_split;

      thisComb->m_passHLTTrig = (HLT_2j35_bmv2c2060_split_2j35_L14J15 || HLT_j100_2j55_bmv2c2060_split || HLT_j225_bmv2c2060_split);
    }

  }// do trig emulation
  
  //
  // set the bits
  //
  if(m_do2015){
    thisComb->m_trigBits = (((int)HLT_2j35_btight_2j35_L14J15)<<0)
                         + (((int)HLT_j100_2j55_bmedium)      <<1)
	                 + (((int)HLT_j225_bloose)            <<3);

    if (HLT_2j35_btight_2j35_L14J15) thisComb->m_passedTriggers->push_back("HLT_2j35_btight_2j35_L14J15.0ETA25");
    if (HLT_j100_2j55_bmedium)       thisComb->m_passedTriggers->push_back("HLT_j100_2j55_bmedium");
    if (HLT_j225_bloose)             thisComb->m_passedTriggers->push_back("HLT_j225_bloose");

    thisComb->m_passHLTTrig = (HLT_2j35_btight_2j35_L14J15 || HLT_j100_2j55_bmedium || HLT_j225_bloose);
    
  } else {  //2016
  
    thisComb->m_trigBits = (((int)HLT_2j35_bmv2c2060_split_2j35_L14J15)<<0) // 2b60
	                   + (((int)HLT_j100_2j55_bmv2c2060_split)       <<1) // 2b60
	                   + (((int)HLT_j225_bmv2c2060_split)            <<3);// 1b60

    if (HLT_2j35_bmv2c2060_split_2j35_L14J15) thisComb->m_passedTriggers->push_back("HLT_2j35_bmv2c2060_split_2j35_L14J15.0ETA25");
    if (HLT_j100_2j55_bmv2c2060_split)        thisComb->m_passedTriggers->push_back("HLT_j100_2j55_bmv2c2060_split");
    if (HLT_j225_bmv2c2060_split)             thisComb->m_passedTriggers->push_back("HLT_j225_bmv2c2060_split");
    
    thisComb->m_passHLTTrig = (HLT_j225_bmv2c2060_split || HLT_j100_2j55_bmv2c2060_split || HLT_2j35_bmv2c2060_split_2j35_L14J15);
  }

  //
  // In the SR use the SF
  //
  if(m_mc && m_doTrigEmulation && m_useTrigSF && thisComb->m_selectedView && thisComb->m_selectedView->m_passSignal){

    thisComb->m_passHLTTrig = true;
    
    if(m_do2015)  m_trigEmulation->emulateTriggerSF2015(m_eventData, thisComb->m_trigSF, thisComb->m_trigSFErr);
    else          m_trigEmulation->emulateTriggerSF2016(m_eventData, thisComb->m_trigSF, thisComb->m_trigSFErr);
    
  }

  //
  //  Set BTagging SF
  //
  if(m_mc){
    if(thisComb->m_selectedView){
      thisComb->m_btagSF = thisComb->m_selectedView->GetBTagSF(0);      
    }
  }

  //
  // For z+jets selection
  //
  // if(m_promoteMuons){
  //   HLT_mu26_ivarmedium_2j35_boffperf  = m_eventData->passTrig("HLT_mu26_ivarmedium_2j35_boffperf");
  //   thisComb->m_passHLTTrig = HLT_mu26_ivarmedium_2j35_boffperf;
  // }
  
  return;
}

const std::vector<const xAH::Jet*> hCandBuilderBase::overlapRemove(const std::vector<const xAH::Jet*>& HCJets, 
								   const std::vector<const xAH::Jet*>& allJets)
{
  std::vector<const xAH::Jet*> overlapRemovedJets;

  for(const xAH::Jet* aJet : allJets){
    if( find(HCJets.begin(), HCJets.end(), aJet) == HCJets.end())
      overlapRemovedJets.push_back(aJet);
  }
  
  return overlapRemovedJets;
}

