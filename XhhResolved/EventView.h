#ifndef XhhResolved_EventView_H
#define XhhResolved_EventView_H

#include <TTree.h>
#include <TLorentzVector.h>

#include <xAODAnaHelpers/Jet.h>
#include <vector>
#include <string>
#include <map>
#include <XhhResolved/hCand.h>
#include "TRandom3.h"
//typedef unsigned long ulong;
typedef std::pair<const xAH::Jet*, const xAH::Jet*> jetPair;

class EventView
{
 public:

  EventView();
  ~EventView();

  float m_qcd_weight = 1;
  float m_nJetWeight = 1;

  std::vector<jetPair>*   m_HC_jets;

  void calcVars(float leadMass_SR, float sublMass_SR, float radius_SR, float radius_CR, float radius_SB, float CR_shift, float SB_shift);

  float GetBTagSF(unsigned int btagSFItr = 0) const;
  
  //
  // The two higgs candidates
  //
  hCand* m_HC_a;
  hCand* m_HC_b;
  TLorentzVector* hhp4;
  TLorentzVector* hhp4cor;
  TLorentzVector* hhp4corZ;
  TLorentzVector* hhp4corH;
  TLorentzVector* ggp4;

  //
  //  Pointers to the lead and subl
  //
  hCand* m_leadHC; //HC for higgs candidate. Sort by scalar sum Pt
  hCand* m_sublHC;
  hCand* m_leadPtHC; //HC for higgs candidate. Sort by vector sum Pt
  hCand* m_sublPtHC;
  hCand* m_leadGC; //GC for gluon candidate. Lead is jet pairing with smallest dRjj
  hCand* m_sublGC;

  //
  //  Event View vars
  //
  float m_Ht4j;
  float m_R_pt_4j;
  float m_theta_SR;
  float m_theta_hh;
  float m_rhh;
  float m_rRR;
  float m_dhh;
  float m_lhh;
  float m_hhJetEtaSum2;
  float m_HCJetAbsEta;
  float m_HCJetAR;
  float m_HCJetPtE1;
  float m_HCJetPtE2;
  float m_xhh;
  float m_xHM;
  float m_xLM;
  float m_dEta;
  float m_dPhi;
  float m_dR;

  float m_dEta_gg;
  float m_dPhi_gg;
  float m_dR_gg;

  float m_R_dRdR;
  float m_R_dRdR_gg;

  float m_GCdR_diff;
  float m_GCdR_sum;

  float m_HCdR_diff;
  float m_HCdR_sum;

  //
  // Cuts
  //
  bool m_passJVC;
  bool m_passHCPt_subl;
  bool m_passHCPt_lead;
  bool m_passHCPt     ;
  bool m_passHCdEta   ;
  bool m_passHCdPhi   ;
  bool m_passHCdR     ;
  bool m_pass_ggVeto  ;

  //b-tagging
  float m_mv2Cut;
  bool  m_twoTag;
  bool  m_fourTag;
  bool  m_leadTag;
  bool  m_sublTag;
  bool  m_twoTagSplit;

  bool m_passSideband;
  bool m_passControl;
  bool m_passControlD;
  bool m_passSignal;
  bool m_passSignal_in;
  bool m_passSignal_out;
  bool m_passLMVR;
  bool m_passHMVR;
  bool m_passLeadHC;
  bool m_passSublHC;
  bool m_passVbbVeto;
  TRandom3* m_randGen;
  float m_randViewWeight;
  std::vector<const xAH::Jet*>*  m_HCJets;
  bool m_debug;
};


#endif // XhhResolved_EventView_H
