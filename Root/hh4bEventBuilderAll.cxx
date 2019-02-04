#include <EventLoop/Job.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <AsgTools/MessageCheck.h>

#include <XhhResolved/hh4bEventBuilderAll.h>
#include <xAODAnaHelpers/HelperFunctions.h>

#include "TFile.h"
#include "TH1D.h"
#include "TKey.h"
#include "TLorentzVector.h"
#include "TSystem.h"

#include <utility>      
#include <iostream>
#include <fstream>

using namespace std;
using xAH::Jet;

// this is needed to distribute the algorithm to the workers
ClassImp(hh4bEventBuilderAll)

hh4bEventBuilderAll :: hh4bEventBuilderAll () :
  m_mc(false),
  m_doTrigEmulation(false),
  m_minJetPtCut(25.),
  m_triggerDetailStr(""), m_jetDetailStr(""), 
  m_leadMass_SR(0), m_sublMass_SR(0), 
  m_radius_SR(0),   m_radius_CR(0), m_radius_SB(0),
  m_CR_shift(1.0), m_SB_shift(1.0),
  m_lumi(0),
  m_mcEventWeight(1.0),
  m_sampleEvents(0),
  m_nevents(0),
  m_useWeighted(false),
  m_doPUReweight(false),
  m_doCleaning(false),
  m_applyGRL(true),
  m_GRLxml("$ROOTCOREBIN/data/XhhResolved/data15_13TeV.periodAllYear_DetStatus-v73-pro19-08_DQDefects-00-01-02_PHYS_StandardGRL_All_Good.xml"),
  m_randGen    (new TRandom3()),
  m_grl(nullptr),
  m_nJetsAbove3(0),
  m_nBJetsAll(0),
  m_nBJetsAbove3(0),
  m_nBJetsEqual4(0)

{
  Info("hh4bEventBuilderAll()", "Calling constructor");
}

EL::StatusCode hh4bEventBuilderAll :: setupJob (EL::Job& /*job*/)
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilderAll :: histInitialize ()
{
  Info("histInitialize()", "Calling histInitialize \n");

  //
  // data model
  m_eventData=hh4bEvent::global();
  m_eventData->m_minJetPtCut = m_minJetPtCut;

  m_eventData->setTriggerDetail(m_triggerDetailStr);
  if(!m_jetDetailStr.empty())    m_eventData->initializeJets   ("resolvedJets",m_jetDetailStr);

  //
  // Cutflow
  m_cutflow=new CutflowHists(m_name, "");
  ANA_CHECK(m_cutflow->initialize() );
  
  m_cutflow->addCut("passDerivation");
  m_cutflow->addCut("nJetsAbove3");
  m_cutflow->addCut("NBJetsAbove3");
  m_cutflow->addCut("NBJetsEqual4");
  m_cf_init    =m_cutflow->addCut("init");
  m_cf_grl     =m_cutflow->addCut("grl");
  if(!m_mc || !m_doTrigEmulation) m_cf_trigger = m_cutflow->addCut("trigger");
  m_cf_less4Jets         = m_cutflow->addCut("less4Jets");
  m_cf_less2BJets        = m_cutflow->addCut("less2BJets");
  m_cf_jetcleaning       = m_cutflow->addCut("jetCleaning");
  m_cf_comb_4b           = m_cutflow->addCut("comb_4b");
  m_cf_drjj_4b           = m_cutflow->addCut("drjj_4b");
  m_cf_dphi_4b           = m_cutflow->addCut("dphi_4b");
  m_cf_comb_QCD          = m_cutflow->addCut("comb_QCD");
  m_cf_drjj_QCD          = m_cutflow->addCut("drjj_QCD");
  m_cf_dphi_QCD          = m_cutflow->addCut("dphi_QCD");
  m_cutflow->record(wk());
  
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilderAll :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilderAll :: changeInput (bool firstFile)
{
  if(m_debug) std::cout << "hh4bEventBuilderAll::changeInput(" << firstFile << ")" << std::endl;

  //
  // Update cutflow hists
  TFile* inputFile = wk()->inputFile();

  // Here you do everything you need to do when we change input files,
  // e.g. resetting branch addresses on trees.  If you are using
  // D3PDReader or a similar service this method is not needed.
  if(firstFile){

    TIter next(inputFile->GetListOfKeys());
    TKey *key;
    while ((key = (TKey*)next())) {
      std::string keyName = key->GetName();
      if(m_debug) cout << "keyName " << keyName << endl;
      // std::size_t found = keyName.find("cutflow");
      // bool foundCutFlow = (found!=std::string::npos);

      // found = keyName.find("weighted");
      // bool foundWeighted = (found!=std::string::npos);

      std::size_t found = keyName.find("MetaData");
      bool foundMetaData = (found!=std::string::npos);

      if(foundMetaData){
        cout << "Getting NSample events from " << keyName << endl;
	m_sampleEvents = ((TH1F*)key->ReadObj())->GetBinContent(3);
	cout << "Setting Sample events to: " << m_sampleEvents << endl;
	cout << "Setting Lumi  to: " << m_lumi << endl;
      }

    }//over Keys
    
  }// first file

  //
  // Update the 
  //
  TH1D* MetaData_EventCount=dynamic_cast<TH1D*>(inputFile->Get("MetaData_EventCount_XhhMiniNtuple"));
  if(!MetaData_EventCount)
    {
      inputFile->ls();
      Error("hh4bEventBuilderAll::changeInput()","Missing input event count histogram!");
      return EL::StatusCode::FAILURE;
    }

  float totalEvents= MetaData_EventCount->GetBinContent(1);
  std::cout << "\ttotalEvents = " << totalEvents << std::endl;
  
  float totalWeight= MetaData_EventCount->GetBinContent(3);
  std::cout << "\ttotalWeight = " << totalWeight << std::endl;

  m_cutflow->executeInitial(totalEvents, totalWeight);

  float passDerivationEvents= MetaData_EventCount->GetBinContent(2);
  std::cout << "\tpassDerivationEvents = " << passDerivationEvents << std::endl;
  
  float passDerivationWeight= MetaData_EventCount->GetBinContent(4);
  std::cout << "\tpassDerivationWeight = " << passDerivationWeight << std::endl;

  m_cutflow->executeInitial(passDerivationEvents, passDerivationWeight, "passDerivation");


  TH1F* h_nJet (0);
  TH1F* h_nBJet(0);

  TIter next(inputFile->GetListOfKeys());
  TKey *key;
  while ((key = (TKey*)next())) {

    std::string keyName = key->GetName();
    if(m_debug) cout << "keyName " << keyName << endl;

    //
    //  find nJet
    //
    std::size_t foundNJet = keyName.find("nJet");
    bool didFindNJet = (foundNJet!=std::string::npos);

    if(didFindNJet){
      h_nJet = ((TH1F*)key->ReadObj());
    }

    //
    //  find nBJet
    //
    std::size_t foundNBJet = keyName.find("nBJet");
    bool didFindNBJet = (foundNBJet!=std::string::npos);
    if(didFindNBJet){
      h_nBJet = ((TH1F*)key->ReadObj());
    }
    
  }//over Keys


  //
  //  Get jet multiplicities 
  //                                                    
  if(h_nJet){
    m_nJetsAbove3  += h_nJet->Integral(5,10);
  }
  
  if(h_nBJet){
    m_nBJetsAll          += h_nBJet->Integral(-1,10);
    m_nBJetsAbove3       += h_nBJet->Integral(5,10);
    cout << "...Adding NBjet s >= 4 " << h_nBJet->Integral(5,5) << endl;
    m_nBJetsEqual4 += h_nBJet->Integral(5,5);
  }


  //
  // Prepare the branches
  TTree *tree = wk()->tree();
  m_eventData->setTree(tree);

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilderAll :: initialize ()
{
  // Here you do everything that you need to do after the first input
  // file has been connected and before the first event is processed,
  // e.g. create additional histograms based on which variables are
  // available in the input files.  You can also create all of your
  // histograms and trees in here, but be aware that this method
  // doesn't get called if no events are processed.  So any objects
  // you create here won't be available in the output if you have no
  // input events.

  if(m_applyGRL)
    {
      m_grl = new GoodRunsListSelectionTool("GoodRunsListSelectionTool");
      std::vector<std::string> vecStringGRL;
      m_GRLxml = gSystem->ExpandPathName( m_GRLxml.c_str() );
      vecStringGRL.push_back(m_GRLxml);
      ANA_CHECK(m_grl->setProperty( "GoodRunsListVec", vecStringGRL));
      ANA_CHECK(m_grl->setProperty("PassThrough", false));
      ANA_CHECK(m_grl->initialize());
    }

  Info("initialize()", "Succesfully initialized! \n");
  return EL::StatusCode::SUCCESS;
}


EL::StatusCode hh4bEventBuilderAll :: execute ()
{
  if(m_debug) Info("execute()", "Processing Event");

  // EDM
  wk()->tree()->GetEntry (wk()->treeEntry());
  m_eventData->updateEntry();

  //
  //  Count events
  //
  //  ++m_nevents;
//  if(m_nevents < 258400){
//    wk()->skipEvent();
//    return EL::StatusCode::SUCCESS; // go to next event
//  }
  //std::cout << "Event Numbers " << m_nevents << std::endl;
  //
  // Cuts
  float eventWeight    = m_eventData->getEventWeight();
  //m_totalWeight = eventWeight;

  m_cutflow->execute(m_cf_init, eventWeight, m_mcEventWeight);

  //
  // do GRL
  //
  if(!m_mc && m_applyGRL)
    {
      if ( !m_grl->passRunLB( m_eventData->m_eventInfo->m_runNumber, m_eventData->m_eventInfo->m_lumiBlock ) ) {
	if(m_debug) std::cout << " Fail GRL" << endl;
	wk()->skipEvent();
        return EL::StatusCode::SUCCESS; // go to next event
      }
    }
  m_cutflow->execute(m_cf_grl, eventWeight, m_mcEventWeight);

  //
  // do Trigger
  //
  if(!m_mc || !m_doTrigEmulation){
    
    //m_eventData->passTrig("")

    bool HLT_j70_bmedium_3j70_L13J25_0ETA23  = m_eventData->passTrig("HLT_j70_bmedium_3j70_L13J25.0ETA23");
    bool HLT_j175_bmedium_j60_bmedium        = m_eventData->passTrig("HLT_j175_bmedium_j60_bmedium");
    bool HLT_2j35_btight_2j35_L13J25_0ETA23  = m_eventData->passTrig("HLT_2j35_btight_2j35_L13J25.0ETA23"); 
    bool HLT_2j45_bmedium_2j45_L13J25_0ETA23 = m_eventData->passTrig("HLT_2j45_bmedium_2j45_L13J25.0ETA23");
    bool HLT_j100_2j55_bmedium               = m_eventData->passTrig("HLT_j100_2j55_bmedium"); 
    bool HLT_j225_bloose                     = m_eventData->passTrig("HLT_j225_bloose"); 
    bool HLT_ht850                           = m_eventData->passTrig("HLT_ht850") || m_eventData->passTrig("HLT_ht850_L1J75"); 
	

    bool passHLT  = (HLT_j70_bmedium_3j70_L13J25_0ETA23 || 
		     HLT_2j35_btight_2j35_L13J25_0ETA23 ||
		     HLT_2j45_bmedium_2j45_L13J25_0ETA23 ||
		     HLT_j100_2j55_bmedium ||
		     HLT_j225_bloose ||
		     HLT_ht850 ||
		     HLT_j175_bmedium_j60_bmedium
		     );
    if(!passHLT){
      if(m_debug) std::cout << " Fail Trigger" << endl;
      wk()->skipEvent();
      return EL::StatusCode::SUCCESS; // go to next event
    }
    m_cutflow->execute(m_cf_trigger, eventWeight);
  }

  //
  //  NJets
  //
  unsigned int nTaggedJets    = m_eventData->m_taggedJets->size();
  unsigned int nNonTaggedJets = m_eventData->m_nonTaggedJets->at("NonTagged").size();
  if ( (nTaggedJets + nNonTaggedJets) < 4 ) {
    if(m_debug) std::cout << " Fail nJets" << endl;
    wk()->skipEvent();
    return EL::StatusCode::SUCCESS; // go to next event
  }  
  m_cutflow->execute(m_cf_less4Jets, eventWeight);

  //
  //  NTagged Jets
  //
  if ( nTaggedJets < 2 ) {
    if(m_debug) std::cout << " Fail nBJets" << endl;
    wk()->skipEvent();
    return EL::StatusCode::SUCCESS; // go to next event
  }  
  m_cutflow->execute(m_cf_less2BJets, eventWeight);

  //
  //  Do Jet cleaning
  //
  //
  // doing cleaning
  //
  bool  passCleaning   = true;
  for(unsigned int i = 0;  i<m_eventData->m_jets->size(); ++i){
    
    const Jet& jet=m_eventData->m_jets->at(i);

    if(jet.p4.Pt() > 25.){
      
      if(!jet.clean_passLooseBad) passCleaning = false;

    }//else break;
  }


  //
  //  Jet Cleaning 
  //
  if(m_doCleaning && !passCleaning){
    if(m_debug) std::cout << " Fail cleaning" << std::endl;
    wk()->skipEvent();
    return EL::StatusCode::SUCCESS;
  }
  m_cutflow->execute(m_cf_jetcleaning, eventWeight);

  //
  // For the cut flow
  //
  bool pass_drjj_QCD = false;
  bool pass_dphi_QCD = false;
  bool pass_drjj_4b  = false;
  bool pass_dphi_4b  = false;


  //
  //  Make the differnet event combinations
  //
  EventCombVec* eventCombsQCD = m_eventData->m_eventComb->at("QCD");
  // Can probably add one for "tight-QCD" too
  EventCombVec* eventCombs4b  = m_eventData->m_eventComb->at("4b");



  //
  // Build the QCD Candidates
  //
  if(nTaggedJets < 3){

    m_cutflow->execute(m_cf_comb_QCD, eventWeight);  

    const Jet* bjet0 = m_eventData->m_taggedJets->at(0);
    const Jet* bjet1 = m_eventData->m_taggedJets->at(1);

    // 
    // Loop over all pairs of non-tagged jets
    //
    for(unsigned int iNonTag0 = 0; iNonTag0 < nNonTaggedJets; ++iNonTag0){
    
      for(unsigned int iNonTag1 = iNonTag0+1; iNonTag1 < nNonTaggedJets; ++iNonTag1){
      	
      	//if(iNonTag1 == iNonTag0) continue;
	
	//
	eventCombsQCD->push_back(new EventComb());

      	EventComb* thisComb = eventCombsQCD->back();
	
	thisComb->m_HCJets   ->push_back(bjet0);
	thisComb->m_HCJets   ->push_back(bjet1);
	thisComb->m_HCJets   ->push_back(m_eventData->m_nonTaggedJets->at("NonTagged").at(iNonTag0));
	thisComb->m_HCJets   ->push_back(m_eventData->m_nonTaggedJets->at("NonTagged").at(iNonTag1));

	//
	// Add other jets
	//
	for(unsigned int iNonTagOther = 0; iNonTagOther < nNonTaggedJets; ++iNonTagOther){
	  if(iNonTagOther == iNonTag0) continue;
	  if(iNonTagOther == iNonTag1) continue;

	  thisComb->m_nonHCJets->push_back(m_eventData->m_nonTaggedJets->at("NonTagged").at(iNonTagOther));
	}

	thisComb->buildAndSelectEventViews(m_leadMass_SR, m_sublMass_SR, m_radius_SR, m_radius_CR, m_radius_SB, m_CR_shift, m_SB_shift,
					   pass_drjj_QCD, pass_dphi_QCD, m_randGen);
      }
    }
    

  } else if(nTaggedJets < 4){

    // Do Nothing with 3-tag SR now
  }

  //
  // Build the Signal Candidates
  //
  else{

    m_cutflow->execute(m_cf_comb_4b, eventWeight);  

    eventCombs4b->push_back(new EventComb());
    EventComb* thisComb = eventCombs4b->back();

    // 
    // Take the first 4 tagged jets.
    //
    for(unsigned int iTag = 0; iTag < nTaggedJets; ++iTag){
      if(iTag < 4) thisComb->m_HCJets   ->push_back(m_eventData->m_taggedJets->at(iTag));
      else         thisComb->m_nonHCJets->push_back(m_eventData->m_taggedJets->at(iTag));
    }

    // 
    // nonTagged Jets get considered as nonBJets
    //
    for(unsigned int iNonTag = 0; iNonTag < nNonTaggedJets; ++iNonTag){
      thisComb->m_nonHCJets->push_back(m_eventData->m_nonTaggedJets->at("NonTagged").at(iNonTag));
    }
    
    thisComb->buildAndSelectEventViews(m_leadMass_SR, m_sublMass_SR, m_radius_SR, m_radius_CR, m_radius_SB, m_CR_shift, m_SB_shift,
				       pass_drjj_4b, pass_dphi_4b, m_randGen);
    
  }

  if(pass_drjj_QCD) m_cutflow->execute(m_cf_drjj_QCD, eventWeight);  
  if(pass_dphi_QCD) m_cutflow->execute(m_cf_dphi_QCD, eventWeight);  
  if(pass_drjj_4b)  m_cutflow->execute(m_cf_drjj_4b,  eventWeight);  
  if(pass_dphi_4b)  m_cutflow->execute(m_cf_dphi_4b,  eventWeight);  

  
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode hh4bEventBuilderAll :: postExecute ()
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilderAll :: finalize ()
{
  m_cutflow->executeInitial(m_nJetsAbove3,  m_nJetsAbove3  * getEventWeight(), "nJetsAbove3");
  m_cutflow->executeInitial(m_nBJetsAbove3, m_nBJetsAbove3 * getEventWeight(), "NBJetsAbove3");
  m_cutflow->executeInitial(m_nBJetsEqual4, m_nBJetsEqual4 * getEventWeight(), "NBJetsEqual4");
  return EL::StatusCode::SUCCESS;
}


float hh4bEventBuilderAll::getEventWeight(){

  float eventWeight = m_eventData->m_weight;
  m_mcEventWeight = 1.0;
  if(m_mc && m_useWeighted){

    eventWeight  = m_sampleEvents ? (m_eventData->m_weight * m_lumi /m_sampleEvents) : m_eventData->m_weight;

    if(m_debug) cout << "m_sampleEvents " << m_sampleEvents << " m_weight " << m_eventData->m_weight << " m_lumi " << m_lumi << " m_weight * m_lumi /m_sampleEvents = " << (m_eventData->m_weight * m_lumi /m_sampleEvents) << endl;

    // Some samples have 0 cross section in 00-07-00
    if(!m_eventData->m_weight_xs) eventWeight = 1.0;
    m_mcEventWeight = m_eventData->m_weight_xs ? (m_eventData->m_weight / m_eventData->m_weight_xs) : 1.0;
  }

  if(m_mc && m_doPUReweight) eventWeight *= m_eventData->m_eventInfo->m_weight_pileup;
  
  return eventWeight;
}



EL::StatusCode hh4bEventBuilderAll :: histFinalize ()
{
  ANA_CHECK(m_cutflow->finalize());
  delete m_cutflow;

  return EL::StatusCode::SUCCESS;
}


