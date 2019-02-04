#ifndef XhhResolved_hCand_H
#define XhhResolved_hCand_H

#include <TTree.h>
#include <TLorentzVector.h>

#include <xAODAnaHelpers/Jet.h>
#include <vector>
#include <string>

class hCand
{
 public:

  hCand(const xAH::Jet* leadJet, const xAH::Jet* sublJet);

  ~hCand();
  
  const xAH::Jet* m_leadJet;
  const xAH::Jet* m_sublJet;
  float m_jetPtAsymmetry;
  TLorentzVector* p4;
  TLorentzVector* p4cor;
  TLorentzVector* p4corZ;
  TLorentzVector* p4corH;

  float m_sumPt;
  float m_dRjj;
  float m_MV2;

  float m_JVC;

};


#endif // XhhResolved_hCand_H
