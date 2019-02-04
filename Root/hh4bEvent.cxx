#include "XhhResolved/hh4bEvent.h"

#include <iostream>

hh4bEvent* hh4bEvent::m_event=0;
using xAH::Jet;

using std::cout;  using std::endl; 

//float hh4bEvent::MV2c20CutValue    = -0.0436;

hh4bEvent* hh4bEvent::global()
{
  if(hh4bEvent::m_event==0)
    hh4bEvent::m_event=new hh4bEvent();
  return m_event;
}

hh4bEvent::hh4bEvent()
  : 
  m_debug(false),
  m_mc(false),
  m_useWeighted(false),
  m_useMhhWeight(false),
  m_doMCNorm(true),
  m_doPUReweight(false),
  m_promoteMuons(false),
  m_minJetPtCut(25),
  m_promptMuonPtCut(25),
  m_promptMuonPtCone20RelIsoCut(0.1),
  m_tagger("MV2c10"),
  m_MV2CutValue(0.8244),
  //m_MV2CutValueTightQCD(0.1758),
  m_MV2CutValueTightQCD(-0.5),
  m_sampleEvents(0),
  m_lumi(0),
  m_eventInfo(nullptr),
  m_ht(0),
  m_mht(0),
  m_mZmumu(0),
  m_truth(0), 
  m_jets(0), 
  m_baselineJets(0),
  m_selectedJets(0),
  m_taggedJets(0), 
  m_nonTaggedJets(0), 
  //m_qcdTightJets(0), 
  m_looseTaggedJets(0),
  // m_TruthBJets(0),
  // m_TaggedTruthBJets(0),
  m_muons(0), 
  m_elecs(0), 
  m_promptMuons(0), 
  m_promotedMuons(0),
  m_met(nullptr),
  m_eventComb(0), 
  //m_pseudoTaggedJets(0),
  //m_pseudoNonTaggedJets(0),
  m_xwt(9999),
  m_xwt_ave(9999),
  m_xtt(9999),
  m_passXtt(true),
  m_triggerInfoSwitch(0)
{

  setTriggerDetail("");

  m_passedTriggers          = new std::vector<std::string>();
  m_passedEmulatedTriggers  = new std::vector<std::string>();
  
}

hh4bEvent::~hh4bEvent()
{
  delete m_eventInfo;

  delete m_triggerInfoSwitch;

  delete m_passedTriggers;
  delete m_passedEmulatedTriggers;

  if(m_jets)            delete m_jets;
  if(m_selectedJets)    delete m_selectedJets;
  if(m_taggedJets)      delete m_taggedJets;
  if(m_baselineJets)  delete m_baselineJets;
  if(m_nonTaggedJets)   delete m_nonTaggedJets;
  //if(m_qcdTightJets)    delete m_qcdTightJets;
  if(m_looseTaggedJets) delete m_looseTaggedJets;

  // if(m_mc){
  //   delete m_TruthBJets;
  //   delete m_TaggedTruthBJets;
  // }

  if(m_muons)         delete m_muons;
  if(m_promptMuons)   delete m_promptMuons;
  if(m_promotedMuons) delete m_promotedMuons;

  if(m_elecs)         delete m_elecs;

  delete m_met;

  if(m_eventComb){  

    for(auto comb_entry : *m_eventComb) {
      
      for( EventComb* eventComb : *(comb_entry.second)){
	delete eventComb;
      }
      
      comb_entry.second->clear();
    }

    delete m_eventComb;

  }

}

void hh4bEvent::setTree(TTree *tree)
{
  if(m_debug) cout << " in setTree " << endl;
  m_tree=tree;

  //
  // Connect branches
  tree->SetBranchStatus ("*", 0);

  // Event info
  m_eventInfo->setTree(tree);

  // tree->SetBranchStatus  ("eventNumber",    1);
  // tree->SetBranchAddress ("eventNumber",    &m_eventNumber);

  if(m_triggerInfoSwitch->m_passTriggers){
    tree->SetBranchStatus  ("passedTriggers",   1);
    tree->SetBranchAddress ("passedTriggers",   &m_passedTriggers);
  }

  if(m_triggerInfoSwitch->m_passTriggers){
    tree->SetBranchStatus  ("passedEmulatedTriggers",   1);
    tree->SetBranchAddress ("passedEmulatedTriggers",   &m_passedEmulatedTriggers);
  }


  // weights
  tree->SetBranchStatus  ("weight", 1);
  tree->SetBranchAddress ("weight", &m_weight);

  tree->SetBranchStatus  ("weight_xs", 1);
  tree->SetBranchAddress ("weight_xs", &m_weight_xs);

  // particles
  if(m_mc && m_truth)   m_truth   ->setTree(tree);
  if(m_jets)            m_jets    ->setTree(tree, m_tagger);

  if(m_muons)   m_muons   ->setTree(tree);

  // Met
  m_met->setTree(tree);

  //m_skim = tree->CloneTree(0);

  if(m_debug) cout << " leave setTree " << endl;
}

void hh4bEvent::updateEntry()
{
  if(m_debug) cout << " in updateEntry " << endl;
  if(m_mc && m_truth)   m_truth   ->updateEntry();
  if(m_jets)            m_jets    ->updateEntry();
  if(m_muons)           m_muons   ->updateEntry();
  if(m_elecs)           m_elecs   ->updateEntry();

  if(m_debug) cout << __FILE__ << ": " << __LINE__ << endl;

  for(auto comb_entry : *m_eventComb) {

    for( EventComb* eventComb : *(comb_entry.second)){
      delete eventComb;
    }
    comb_entry.second->clear();

  }

  //
  // Tag Jets
  //
  m_selectedJets ->clear();
  m_taggedJets   ->clear();
  m_baselineJets ->clear();
  m_ht = 0;
  m_mht = 0;
  m_xwt = 9999;
  m_mZmumu = 0;
  TLorentzVector sumJetPt;
  m_nonTaggedJets->at("NonTagged")     .clear();
  m_nonTaggedJets->at("NonTaggedTight").clear();
  //m_qcdTightJets   ->clear();
  m_looseTaggedJets->clear();

  // if(m_mc){
  //   m_TruthBJets      ->clear();
  //   m_TaggedTruthBJets->clear();
  // }

  for(unsigned int iJet = 0; iJet < m_jets->size(); ++iJet){
    Jet* thisJet = &(m_jets->at_nonConst(iJet));
    thisJet->muonInJetCorrection(m_muons);

    float thisJetPt = thisJet->p4.Pt();
    if(thisJetPt < m_minJetPtCut) continue;
    m_baselineJets   ->push_back(thisJet);
    m_ht += thisJetPt;
    sumJetPt = (sumJetPt + thisJet->p4);


    m_selectedJets->push_back(thisJet);

    if(thisJet->MV2    > m_MV2CutValue){
      m_taggedJets   ->push_back(thisJet);
    }else{
      m_nonTaggedJets->at("NonTagged").push_back(thisJet);

      if(thisJet->MV2    > m_MV2CutValueTightQCD){
	m_nonTaggedJets->at("NonTaggedTight").push_back(thisJet);
      }
    }
    
    if(thisJet->MV2    > m_MV2CutValueTightQCD){
      m_looseTaggedJets->push_back(thisJet);
    }

  //   if(m_mc){//Truth match b-jets
  //     if(thisJet->HadronConeExclTruthLabelID == 5){
  // 	m_TruthBJets->push_back(thisJet);
  // 	if(thisJet->MV2 > m_MV2CutValue) 
  // 	  m_TaggedTruthBJets->push_back(thisJet);
  //     }
  //   }
  }
  if(m_debug) cout << __FILE__ << ": " << __LINE__ << endl;

  //
  // Muons (initialize in case we are going to use Zbb->mumubb for Zbb->bbbb and we want to promote muons to jets)
  //
  m_promptMuons   ->clear();
  m_promotedMuons ->clear();
  for(unsigned int iMuon = 0; iMuon < m_muons->size(); ++iMuon){
    xAH::Muon* thisMuon = &(m_muons->at_nonConst(iMuon));
    float muonPt = thisMuon->p4.Pt();
    if(muonPt < m_promptMuonPtCut) continue;
    
    if( (thisMuon->ptcone40/muonPt) > m_promptMuonPtCone20RelIsoCut) continue;
    m_promptMuons   ->push_back(thisMuon);

    if(m_promoteMuons){
      if(muonPt < m_minJetPtCut) continue;
      m_promotedMuons->push_back(thisMuon);
      Jet* thisJet = new Jet();
      thisJet->p4.SetPtEtaPhiE(thisMuon->p4.Pt(),
			       thisMuon->p4.Eta(),
			       thisMuon->p4.Phi(),
			       thisMuon->p4.E());
      thisJet->MV2c10 = 1.0;
      m_ht += thisJet->p4.Pt();
      sumJetPt = (sumJetPt + thisJet->p4);
      m_baselineJets->push_back(thisJet);
      m_selectedJets->push_back(thisJet);      
      m_taggedJets  ->push_back(thisJet);
    }
  }

  m_mht = sumJetPt.Pt();
  std::sort(m_selectedJets->begin(), m_selectedJets->end(), MV2_greater_than());
  std::sort(m_looseTaggedJets->begin(), m_looseTaggedJets->end(), MV2_greater_than());

  std::sort(m_taggedJets->begin(), m_taggedJets->end(), MV2_greater_than());

  //std::cout << "| " << std::endl;
  //std::cout << "| " << std::endl;
  //for(const Jet* thisJet : *m_taggedJets)
  //  std::cout << " " << thisJet->MV2c20 << std::endl;
  //if(m_eventNumber == 53995) dump();

  //
  // mhh weight
  //
  //
  // 
  //
  if(m_mc && m_useMhhWeight){
   
    //
    // Get the two higgs indices
    //
    const xAH::TruthPart* h1 = nullptr;
    const xAH::TruthPart* h2 = nullptr;
    unsigned int nHiggs  = 0;

    for(unsigned int iTruth = 0; iTruth < m_truth->size(); ++iTruth){
      const xAH::TruthPart& thisTruth = m_truth->at(iTruth);
      int thisPDGID = thisTruth.pdgId;
      
      if(thisPDGID == 25){
	if(nHiggs == 0)  h1 = &thisTruth;
	if(nHiggs == 1)  h2 = &thisTruth;
	++nHiggs;
      }
      
    }

    if(h1 && h2 && nHiggs == 2){
      float mhh_truth_MEV = (h1->p4+h2->p4).M()*1000;
      m_weight_mhh = m_hhWeightTool->getWeight(mhh_truth_MEV);
    }else if(nHiggs > 2){
      std::cout << "ERROR Too many Higgs ! " << std::endl;
    }

  }//mc




  if(m_debug) cout << " leave updateEntry " << endl;  
}

void hh4bEvent::setTriggerDetail(const std::string &detailStr)
{
  if(m_debug) cout << " In setTriggerDetail " << endl;
  if(m_triggerInfoSwitch) delete m_triggerInfoSwitch;
  m_triggerInfoSwitch=new HelperClasses::TriggerInfoSwitch(detailStr);
}

void hh4bEvent::initializeJets(const std::string& name, const std::string& detailStr)
{
  if(m_debug) cout << " In initializeJets " << endl;
  m_jets   =new xAH::JetContainer   (name, detailStr, 1e3, m_mc);
  m_jets   ->m_debug=m_debug;

  m_selectedJets    = new std::vector<const Jet*>();
  m_taggedJets      = new std::vector<const Jet*>();
  m_baselineJets  = new std::vector<const Jet*>();
  m_nonTaggedJets = new std::map<std::string, std::vector<const Jet*> >();
  (*m_nonTaggedJets)["NonTagged"];
  (*m_nonTaggedJets)["NonTaggedTight"];
  //m_qcdTightJets    = new std::vector<const Jet*>();
  m_looseTaggedJets = new std::vector<const Jet*>();
  // if(m_mc){
  //   m_TruthBJets       = new std::vector<const Jet*>();
  //   m_TaggedTruthBJets = new std::vector<const Jet*>();
  // }

  m_eventComb     = new std::map<std::string, EventCombVec*>();
  //m_eventComb->insert(std::make_pair("QCD",          new std::vector<EventComb*>()));
  //m_eventComb->insert(std::make_pair("QCDExclusive", new std::vector<EventComb*>()));

  if(m_debug) cout << " Left initializeJets " << endl;
}

void hh4bEvent::initializeEvent(const std::string& detailStr)
{
  if(m_debug) cout << " In initializeEvent " << endl;
  m_eventInfo = new xAH::EventInfo(detailStr, 1e3, m_mc);
}

void hh4bEvent::initializeMet(const std::string& detailStr)
{
  if(m_debug) cout << " In initializeMet " << endl;
  m_met = new xAH::MetContainer(detailStr, 1e3);
}


void hh4bEvent::initializeMuons(const std::string& name, const std::string& detailStr)
{
  if(m_debug) cout << " In initializeTruth " << endl;
  m_muons   =new xAH::MuonContainer (name, detailStr);
  m_muons   ->m_mc=m_mc;

  m_promptMuons    = new std::vector<const xAH::Muon*>();
  m_promotedMuons  = new std::vector<const xAH::Muon*>();

}

void hh4bEvent::initializeHHWeightTool(std::string hhReweightFile){
  m_hhWeightTool = new xAOD::hhWeightTool("hhWeights");
  m_hhWeightTool->setProperty("ReweightFile",hhReweightFile);
  m_hhWeightTool->initialize();
}

void hh4bEvent::initializeTruth(const std::string& name, const std::string& detailStr)
{
  if(m_debug) cout << " In initializeTruth " << endl;
  m_truth   =new xAH::TruthContainer   (name, detailStr);
  m_truth   ->m_debug=m_debug;
}



void hh4bEvent::initializeElectrons(const std::string& name, const std::string& detailStr)
{
  m_elecs   =new xAH::ElectronContainer (name, detailStr);
  m_elecs   ->m_mc=m_mc;
}


bool hh4bEvent::passTrig(const std::string& trigName) const{
  return (find(m_passedTriggers->begin(), m_passedTriggers->end(), trigName ) != m_passedTriggers->end());
}

bool hh4bEvent::passEmulatedTrig(const std::string& trigName) const{
  return (find(m_passedEmulatedTriggers->begin(), m_passedEmulatedTriggers->end(), trigName ) != m_passedEmulatedTriggers->end());
}



void hh4bEvent::printTriggers() const{
  std::cout << "=============== Triggers " << std::endl;
  for(std::string& trig : *m_passedTriggers) std::cout << trig << std::endl;
}


void hh4bEvent::printEmulatedTriggers() const{
  std::cout << "=============== Emulated Triggers " << std::endl;
  for(std::string& trig : *m_passedEmulatedTriggers) std::cout << trig << std::endl;
}



float hh4bEvent::getEventWeight() const{

  float eventWeight = m_weight;
  if(m_mc && m_useWeighted){

    if(m_doMCNorm)
      eventWeight = m_sampleEvents ? (m_weight * m_lumi /m_sampleEvents) : m_weight;
    else
      eventWeight = m_weight;

    if(!m_weight_xs) eventWeight = 1.0;
  }

  if(m_mc && m_doPUReweight){
    if(m_debug) cout << "m_eventInfo->m_weight_pileup = "<<m_eventInfo->m_weight_pileup<<endl;
    eventWeight *= m_eventInfo->m_weight_pileup;
  }

  if(m_useMhhWeight) eventWeight *= m_weight_mhh;

  return eventWeight;
}


float hh4bEvent::mcEventWeight() const{
  float mcEventWeight = 1.0;

  if(m_mc && m_useWeighted){
    mcEventWeight = m_weight_xs ? (m_weight / m_weight_xs) : 1.0;
  }

  return mcEventWeight;
}


void hh4bEvent::dump() const{
  cout << "Dump hh4bEvent: " << m_eventNumber << endl;
  cout << "Selected Jets:" << endl;
  cout << std::setw(10) << "pt" << std::setw(10) << "mv2c10" << endl;
  for(unsigned int i = 0; i < m_selectedJets->size(); i++){
    cout << std::setw(10) << m_selectedJets->at(i)->p4.Pt() << std::setw(10) << m_selectedJets->at(i)->MV2 << endl;
  }
  
}
