#include <EventLoop/Job.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <AsgTools/MessageCheck.h>

#include <XhhResolved/hh4bEventBuilder.h>
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

// this is needed to distribute the algorithm to the workers
ClassImp(hh4bEventBuilder)




hh4bEventBuilder :: hh4bEventBuilder () :
  m_mc(false),
  m_doMCNorm(true),
  m_tagger("MV2c10"),
  m_MV2CutValue(0.8244),
  //m_MV2CutValueTightQCD(0.1758),
  m_MV2CutValueTightQCD(-0.5),
  m_minJetPtCut(25.),
  m_eventDetailStr(""), 
  m_triggerDetailStr(""), 
  m_truthDetailStr(""), 
  m_jetDetailStr(""), 
  m_muonDetailStr(""), 
  m_elecDetailStr(""), 
  m_metDetailStr(""), 
  m_lumi(0),
  m_mcEventWeight(1.0),
  m_nevents(0),
  m_useWeighted(false),
  m_useMhhWeight(false),
  m_hhReweightFile("SMhh_mhh_kfactor.root"),
  m_doPUReweight(false),
  m_doCleaning(false),
  m_applyGRL(true),
  m_GRLxml("$ROOTCOREBIN/data/XhhResolved/data15_13TeV.periodAllYear_DetStatus-v73-pro19-08_DQDefects-00-01-02_PHYS_StandardGRL_All_Good.xml"),
  m_promoteMuons(false),
  m_grl(nullptr),
  m_nJetsAbove3(0),
  m_nBJetsAll(0),
  m_nBJetsAbove3(0),
  m_nBJetsEqual4(0), 
  h_metaDataOutput(nullptr)
{
  Info("hh4bEventBuilder()", "Calling constructor");
}

EL::StatusCode hh4bEventBuilder :: setupJob (EL::Job& /*job*/)
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilder :: histInitialize ()
{
  Info("histInitialize()", "Calling histInitialize \n");

  //
  // data model
  if(m_debug) Info("histInitialize()", "Getting eventData \n");
  m_eventData=hh4bEvent::global();
  m_eventData->m_minJetPtCut         = m_minJetPtCut;
  m_eventData->m_tagger              = m_tagger;
  m_eventData->m_MV2CutValue         = m_MV2CutValue;
  m_eventData->m_MV2CutValueTightQCD = m_MV2CutValueTightQCD;
  m_eventData->m_useWeighted         = m_useWeighted;
  m_eventData->m_useMhhWeight        = m_useMhhWeight;
  m_eventData->m_doPUReweight        = m_doPUReweight;
  m_eventData->m_lumi                = m_lumi;
  m_eventData->m_mc                  = m_mc;
  m_eventData->m_doMCNorm            = m_doMCNorm;
  m_eventData->m_debug               = m_debug;
  m_eventData->m_promoteMuons        = m_promoteMuons;
  if(m_debug) Info("histInitialize()", "Init eventData \n");

  m_eventData->initializeEvent(m_eventDetailStr);
  m_eventData->setTriggerDetail(m_triggerDetailStr);
  if(m_mc && !m_truthDetailStr.empty())    m_eventData->initializeTruth    ("truth",       m_truthDetailStr );
  if(!m_jetDetailStr.empty())              m_eventData->initializeJets     ("resolvedJets",m_jetDetailStr );
  if(!m_muonDetailStr.empty())             m_eventData->initializeMuons    ("muon",        m_muonDetailStr);
  if(!m_elecDetailStr.empty())             m_eventData->initializeElectrons("el",          m_elecDetailStr);
  m_eventData->initializeMet(m_metDetailStr);

  if(m_useMhhWeight){
    m_eventData->initializeHHWeightTool(m_hhReweightFile);
  }
  

  //
  // Cutflow
  if(m_debug) Info("histInitialize()", "Making Cut flow \n");
  m_cutflow=new CutflowHists(m_name, "");
  ANA_CHECK(m_cutflow->initialize() );
  
  m_cutflow->addCut("passDerivation");
  m_cutflow->addCut("nJetsAbove3");
  m_cutflow->addCut("NBJetsAbove3");
  m_cutflow->addCut("NBJetsEqual4");
  m_cf_init    =m_cutflow->addCut("init");
  m_cf_grl     =m_cutflow->addCut("grl");
  m_cf_less4Jets         = m_cutflow->addCut("less4Jets");
  m_cf_less2BJets        = m_cutflow->addCut("less2BJets");
  m_cf_jetcleaning       = m_cutflow->addCut("jetCleaning");
  m_cutflow->record(wk());

  if(m_debug) Info("histInitialize()", "Leaving histInitialize \n");
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilder :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilder :: changeInput (bool firstFile)
{
  if(m_debug) std::cout << "hh4bEventBuilder::changeInput(" << firstFile << ")" << std::endl;

  //
  // Update cutflow hists
  TFile* inputFile = wk()->inputFile();

  // Here you do everything you need to do when we change input files,
  // e.g. resetting branch addresses on trees.  If you are using
  // D3PDReader or a similar service this method is not needed.
  if(firstFile){

    TIter next(inputFile->GetListOfKeys());
    TKey *key;
    TH1F* h_metaData;
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
	h_metaData = ((TH1F*)key->ReadObj());	
	
	h_metaDataOutput = new TH1F(*h_metaData);
	h_metaDataOutput->SetName("MetaData_EventCount_XhhMiniNtuple");

        m_eventData->m_sampleEvents = h_metaData->GetBinContent(3);
        cout << "Setting Sample events to: " << m_eventData->m_sampleEvents << endl;
        cout << "Setting Lumi  to: " << m_eventData->m_lumi << endl;
	wk()->addOutput(h_metaDataOutput);
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
      Error("hh4bEventBuilder::changeInput()","Missing input event count histogram!");
      return EL::StatusCode::FAILURE;
    }

  if(!firstFile){
    for(int iBin = 0; iBin < (MetaData_EventCount->GetNbinsX()+1); ++iBin){
      float oldContent = h_metaDataOutput->GetBinContent(iBin);
      float thisValue  = MetaData_EventCount->GetBinContent(iBin);
      h_metaDataOutput->SetBinContent(iBin, oldContent + thisValue);
    }
  
  }
  

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
  //
  TTree *tree = wk()->tree();
  m_eventData->setTree(tree);

  //
  // Fill cutflow with information about complete sample and derivation
  //
  float totalEvents= MetaData_EventCount->GetBinContent(1);
  std::cout << "\ttotalEvents = " << totalEvents << std::endl;
  float passDerivationEvents= MetaData_EventCount->GetBinContent(2);
  std::cout << "\tpassDerivationEvents = " << passDerivationEvents << std::endl;
  
  float totalWeight= MetaData_EventCount->GetBinContent(3);
  float passDerivationWeight= MetaData_EventCount->GetBinContent(4);
  // if !m_doMCNorm, then we are just using the xs*mcEventWeight for hists and scaling later. 
  //    in this case, to get correct totalweight after scaling, want this hist to be multiplied by weight_xs
  if(m_mc){
    tree->GetEntry(0);
    float xs = m_eventData->m_weight_xs;
    std::cout << "\txs = " << xs << std::endl;
    totalWeight = totalWeight*xs;
    passDerivationWeight = passDerivationWeight*xs;
  }
  if(m_mc && m_doMCNorm){//need to further scale these bins by lumi/sampleEvents
    std::cout << "\tm_lumi/m_sampleEvents = " << m_lumi/m_eventData->m_sampleEvents << std::endl;
    totalWeight = totalWeight*m_lumi/m_eventData->m_sampleEvents;
    passDerivationWeight = passDerivationWeight*m_lumi/m_eventData->m_sampleEvents;
  }
  std::cout << "\ttotalWeight = " << totalWeight << std::endl;
  std::cout << "\tpassDerivationWeight = " << passDerivationWeight << std::endl;

  m_cutflow->executeInitial(totalEvents, totalWeight);
  m_cutflow->executeInitial(passDerivationEvents, passDerivationWeight, "passDerivation");


  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilder :: initialize ()
{
  if(m_applyGRL)
    {
      m_grl = new GoodRunsListSelectionTool("GoodRunsListSelectionTool");
      std::vector<std::string> vecStringGRL;
      m_GRLxml = gSystem->ExpandPathName( m_GRLxml.c_str() );
      vecStringGRL.push_back(m_GRLxml);
      ANA_CHECK( m_grl->setProperty( "GoodRunsListVec", vecStringGRL) );
      ANA_CHECK( m_grl->setProperty("PassThrough", false));
      ANA_CHECK( m_grl->initialize() );
    }


  Info("initialize()", "Succesfully initialized! \n");
  return EL::StatusCode::SUCCESS;
}


EL::StatusCode hh4bEventBuilder :: execute ()
{
  if(m_debug) Info("execute()", "Processing Event");

  // EDM
  if(m_debug) Info("execute()", "GetEntry");
  wk()->tree()->GetEntry (wk()->treeEntry());
  if(m_debug) Info("execute()", "updateEntry");
  m_eventData->updateEntry();
  if(m_debug) Info("execute()", "Entry updated");

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
  //m_eventData->m_totalWeight = eventWeight;

  m_cutflow->execute(m_cf_init, eventWeight, 1.0);

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
  m_cutflow->execute(m_cf_grl, eventWeight, 1.0);

  //
  //  NJets
  //
  unsigned int nTaggedJets    = m_eventData->m_taggedJets->size();
  unsigned int nNonTaggedJets = m_eventData->m_nonTaggedJets->at("NonTagged").size();
  if ( (nTaggedJets + nNonTaggedJets) < 4) {
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
    
    const xAH::Jet& jet=m_eventData->m_jets->at(i);

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
  // Zbb selection
  //
  if(m_promoteMuons){
    if(m_eventData->m_promotedMuons->size() != 2){
      wk()->skipEvent();
      return EL::StatusCode::SUCCESS;
    }
    else{
      m_eventData->m_mZmumu = (m_eventData->m_promotedMuons->at(0)->p4 + m_eventData->m_promotedMuons->at(1)->p4).M();
      if(fabs(m_eventData->m_mZmumu-91)>10){
	wk()->skipEvent();
	return EL::StatusCode::SUCCESS;
      }
    }
  }
  

  if(m_debug) Info("execute()", "Processed Event");
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode hh4bEventBuilder :: postExecute ()
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode hh4bEventBuilder :: finalize ()
{
  m_cutflow->executeInitial(m_nJetsAbove3,  m_nJetsAbove3  * m_eventData->getEventWeight(), "nJetsAbove3");
  m_cutflow->executeInitial(m_nBJetsAbove3, m_nBJetsAbove3 * m_eventData->getEventWeight(), "NBJetsAbove3");
  m_cutflow->executeInitial(m_nBJetsEqual4, m_nBJetsEqual4 * m_eventData->getEventWeight(), "NBJetsEqual4");
  return EL::StatusCode::SUCCESS;
}




EL::StatusCode hh4bEventBuilder :: histFinalize ()
{
  ANA_CHECK(m_cutflow->finalize());
  delete m_cutflow;

  return EL::StatusCode::SUCCESS;
}





