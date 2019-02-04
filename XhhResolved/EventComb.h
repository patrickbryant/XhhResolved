#ifndef XhhResolved_EventComb_H
#define XhhResolved_EventComb_H

#include <TTree.h>
#include <TLorentzVector.h>

#include <xAODAnaHelpers/Jet.h>
#include <vector>
#include <string>
#include <XhhResolved/EventView.h>

#include "TRandom3.h"

class EventComb
{
 public:

  EventComb();

  ~EventComb();

  std::vector<const xAH::Jet*>*  m_HCJets;
  std::vector<const xAH::Jet*>*  m_HCJets_mv2Sort;
  std::vector<const xAH::Jet*>*  m_nonHCJets;
  std::vector<EventView*>*  m_views;
  EventView*                m_DhhMinView;
  EventView*                m_RhhMinView;
  EventView*                m_selectedView;

  bool m_debug;
  bool m_passRhhMin = false;
  bool m_passLhh    = false;
  std::vector<std::string> *m_passedTriggers;
  std::vector<std::string> *m_passedL1Triggers;
  std::vector<const xAH::Jet*>            m_pseudoTaggedJets;
  std::vector<const xAH::Jet*>            m_pseudoNonTaggedJets;
  
  int m_nViews;
  
  bool m_passHLTTrig;
  int  m_trigBits;
  float m_trigSF;
  float m_trigSFErr;
  float m_btagSF;

  float     m_xtt;
  float     m_xtt_ave;
  float     m_minSum_xtt_1;
  float     m_minSum_xtt_2;
  unsigned int m_nTopCands;
  unsigned int m_nTopCands3;
  unsigned int m_nTopCandsAll;

  void buildAndSelectEventViews(float leadMass_SR, float sublMass_SR, float radius_SR, float radius_CR, float radius_SB, float CR_shift, float SB_shift,
				bool& passDrjj, bool& passDphi, TRandom3* rand, bool debug=false);

  bool passTrig(std::string trigName) const;

  float ResolvedXhhFrom4Jets(std::vector<const xAH::Jet*>* top4MV2Jets);
};


#endif // XhhResolved_EventComb_H
