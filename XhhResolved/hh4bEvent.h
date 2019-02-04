#ifndef XhhResolved_hh4bEvent_H
#define XhhResolved_hh4bEvent_H

#include "hhTruthWeightTools/hhWeightTool.h"

#include <TTree.h>
#include <TLorentzVector.h>

#include <vector>
#include <string>

#include <xAODAnaHelpers/EventInfo.h>
#include <xAODAnaHelpers/JetContainer.h>
#include <xAODAnaHelpers/TruthContainer.h>
#include <xAODAnaHelpers/MuonContainer.h>
#include <xAODAnaHelpers/ElectronContainer.h>
#include <xAODAnaHelpers/MetContainer.h>
#include <XhhResolved/EventComb.h>




typedef std::vector<EventComb*>      EventCombVec;
typedef std::vector<const xAH::Jet*> JetVec;

struct MV2_greater_than
{
  inline bool operator() (const xAH::Jet* struct1, const xAH::Jet* struct2)
  {
    return (struct1->MV2 > struct2->MV2);
  }
};


class hh4bEvent
{
public:
  static hh4bEvent *global();

  virtual ~hh4bEvent();

  void setTree(TTree *t);
  void updateEntry();

  void setTriggerDetail(const std::string& detailStr);

  void initializeEvent  (const std::string& detailStr);

  void initializeTruth  (const std::string& name, const std::string& detailStr);

  void initializeJets   (const std::string& name, const std::string& detailStr);

  void initializeMuons  (const std::string& name, const std::string& detailStr);

  void initializeElectrons  (const std::string& name, const std::string& detailStr);

  void initializeMet    (const std::string& detailStr);

  void initializeHHWeightTool(std::string hhReweightFile);

  void printTriggers  () const;

  void printEmulatedTriggers  () const;

  bool passTrig        (const std::string& trigName) const;
  bool passEmulatedTrig(const std::string& trigName) const;

  float getEventWeight() const;
  float mcEventWeight() const;

  void dump() const;

public:
  // Settings
  bool  m_debug;
  bool  m_mc;
  bool  m_useWeighted;
  bool  m_useMhhWeight;
  bool  m_doMCNorm;
  bool  m_doPUReweight;
  bool  m_promoteMuons;
  float m_minJetPtCut;
  float m_promptMuonPtCut;
  float m_promptMuonPtCone20RelIsoCut;
  std::string m_tagger;
  float m_MV2CutValue;
  float m_MV2CutValueTightQCD;
  float m_sampleEvents;      
  float m_lumi;      


  // Event variables
  xAH::EventInfo*    m_eventInfo; 
  float m_ht;
  float m_mht;
  long long m_eventNumber;
  float m_mZmumu;

  // Truth info
  /* std::vector<int>    *m_truth_part_pdgid; */
  /* std::vector<double> *m_truth_part_pt; */
  /* std::vector<double> *m_truth_part_eta; */
  /* std::vector<double> *m_truth_part_phi; */
  /* std::vector<double> *m_truth_part_m; */
  /* std::vector<int>    *m_truth_part_status; */

  // trigger
  std::vector<std::string> *m_passedTriggers;
  std::vector<std::string> *m_passedEmulatedTriggers;

  // weights
  float m_weight;
  float m_weight_xs;
  float m_weight_mhh;
  float m_totalWeight;

  // truth
  xAH::TruthContainer    *m_truth;

  // particles
  xAH::JetContainer    *m_jets;
  std::vector<const xAH::Jet*>* m_baselineJets;
  std::vector<const xAH::Jet*>* m_selectedJets;
  std::vector<const xAH::Jet*>* m_taggedJets;
  std::map<std::string, std::vector<const xAH::Jet*> >* m_nonTaggedJets;
  //std::vector<const xAH::Jet*>* m_qcdTightJets;
  std::vector<const xAH::Jet*>* m_looseTaggedJets;
  /* std::vector<const xAH::Jet*>* m_TruthBJets; */
  /* std::vector<const xAH::Jet*>* m_TaggedTruthBJets; */
  
  xAH::MuonContainer     *m_muons;
  xAH::ElectronContainer *m_elecs;
  std::vector<const xAH::Muon*>* m_promptMuons;
  std::vector<const xAH::Muon*>* m_promotedMuons;

  // met 
  xAH::MetContainer*  m_met; 

  //std::vector<EventComb*>*  m_eventComb;
  std::map<std::string, EventCombVec*>* m_eventComb;

  // In the QCD candidates
  //std::map<std::string, JetVec*>* m_pseudoTaggedJets;
  //std::map<std::string, JetVec*>* m_pseudoNonTaggedJets;

  float m_xwt;
  float m_xwt_ave;
  float m_xtt;
  bool m_passXtt = false;
  bool m_passAllhadVeto = false;
  bool m_store = false;
  //TTree *m_skim;

protected:
  hh4bEvent();

  TTree *m_tree;

private:
  static hh4bEvent *m_event;

  HelperClasses::TriggerInfoSwitch *m_triggerInfoSwitch;

  xAOD::hhWeightTool*          m_hhWeightTool = nullptr; //!

};

#endif // XhhResolved_hh4bEvent_H
