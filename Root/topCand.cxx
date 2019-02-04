#include "XhhResolved/topCand.h"
#include "XhhResolved/hh4bEvent.h"

#include <iostream>
#include <assert.h>     /* assert */


using std::cout;  using std::endl;  using std::vector;

topCand::topCand(vector<const xAH::Jet*>& jets_tag, vector<const xAH::Jet*>& jets_non)
  :    m_xwt(999)

{
  assert( ( (jets_tag.size() + jets_non.size()) == 3) && "topCand::Number of top-candidate jets not 3" );

  unsigned int nJets_tag = jets_tag.size();

  //
  //  Require at least one tagged jet for the b
  //
  if(nJets_tag == 0){
    return;
  }

  //
  //  Require at least one non-tagged jet in the W
  //
  // if(nJets_tag == 3){
  //  return;
  // }

  bool m_orderOnMV2 = true;
  if(m_orderOnMV2){
    MV2Order(jets_tag, jets_non);
  }else{
    noMV2Order(jets_tag, jets_non);
  }


}


void topCand::noMV2Order(const vector<const xAH::Jet*>& jets_tag, const vector<const xAH::Jet*>& jets_non)
{

  unsigned int nJets_tag = jets_tag.size();
  
  for(unsigned int jet_b = 0; jet_b < nJets_tag; ++jet_b){
    
    vector<const xAH::Jet*> wJets;
    for(unsigned int jet_wb = 0; jet_wb < nJets_tag; ++jet_wb){
      if(jet_wb == jet_b) continue;
      wJets.push_back(jets_tag.at(jet_wb));      
    }
    
    for(const xAH::Jet* jet_non : jets_non){
      wJets.push_back(jet_non);
    }

    assert( ( wJets.size() == 2) && "topCand::Number of w-candidate jets not 2" );
    mW = (wJets.at(0)->p4 + wJets.at(1)->p4).M();
    mT = (jets_tag.at(jet_b)->p4 + wJets.at(0)->p4 + wJets.at(1)->p4).M();

    w_sig    = (mW   -  80.4)/(0.1*mW);
    t_sig    = (mT - 172.5)  /(0.1*mT);
    float this_Xwt = sqrt(w_sig*w_sig + t_sig*t_sig);
    
    if(this_Xwt < m_xwt){
      m_xwt = this_Xwt;
      m_bjet = jets_tag.at(jet_b);
      m_wjets = wJets;
    }
  }
  
  return;
}


void topCand::MV2Order(vector<const xAH::Jet*>& jets_tag, vector<const xAH::Jet*>& jets_non)
{
  std::sort(jets_tag.begin(), jets_tag.end(), MV2_greater_than());
  
  m_bjet = jets_tag.at(0);
  
  for(unsigned int jet_wb = 0; jet_wb < jets_tag.size(); ++jet_wb){
    
    // Dont use highest mv2 for the leading w
    if(jet_wb == 0) continue;
    m_wjets.push_back(jets_tag.at(jet_wb));      
  }
    
  for(const xAH::Jet* jet_non : jets_non){
    m_wjets.push_back(jet_non);
  }

  assert( ( m_wjets.size() == 2) && "topCand::Number of w-candidate jets not 2" );
  mW = (m_wjets.at(0)->p4 + m_wjets.at(1)->p4).M();
  mT = (m_bjet->p4 + m_wjets.at(0)->p4 + m_wjets.at(1)->p4).M();

  w_sig  = (mW   -  80.4)/(0.1*mW);
  t_sig  = (mT - 172.5)  /(0.1*mT);
  m_xwt  = sqrt(w_sig*w_sig + t_sig*t_sig);

  return;
}


topCand::~topCand()
{
  //delete p4;
  //delete p4cor;
}

