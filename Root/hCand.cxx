#include "XhhResolved/hCand.h"

#include <iostream>

using std::cout;  using std::endl; 


hCand::hCand(const xAH::Jet* leadJet, const xAH::Jet* sublJet)
  : m_leadJet(leadJet),
    m_sublJet(sublJet),
    m_jetPtAsymmetry(0),
    p4(0),
    p4cor(0),
    p4corZ(0),
    p4corH(0),
    m_sumPt(0),
    m_dRjj(0),
    m_MV2(0),
    m_JVC(0)
{
  m_sumPt = leadJet->p4.Pt() + sublJet->p4.Pt();
  m_dRjj  = leadJet->p4.DeltaR(sublJet->p4);

  p4      = new TLorentzVector((leadJet->p4 + sublJet->p4));

  float alpha = p4->M() ? 125.0/p4->M() : 1.0;
  p4cor   = new TLorentzVector(alpha * (*p4));


  float alphaZ = p4->M() ? 91.0/p4->M() : 1.0;
  p4corZ  = new TLorentzVector(alphaZ * (*p4));

  float alphaH = p4->M() ? 155.0/p4->M() : 1.0;
  p4corH  = new TLorentzVector(alphaH * (*p4));
  

  m_jetPtAsymmetry = leadJet->p4.Pt() - sublJet->p4.Pt();

  //m_MV2 = pow( pow(m_leadJet->MV2+1,2) + pow(m_sublJet->MV2+1,2), 0.5) - 1;
  m_MV2 = m_leadJet->MV2 + m_sublJet->MV2;

  m_JVC = m_leadJet->JVC + m_sublJet->JVC;

}



hCand::~hCand()
{
  delete p4;
  delete p4cor;
}

