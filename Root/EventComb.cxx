#include "XhhResolved/EventComb.h"

#include <iostream>
#include <assert.h>     /* assert */
#include <vector>


using std::cout;  using std::endl; 

struct dhh_less_than
{
  inline bool operator() (const EventView* struct1, const EventView* struct2)
  {
    return (struct1->m_dhh < struct2->m_dhh);
  }
};

struct leadHC_jetPtAsymmetry_less_than
{
  inline bool operator() (const EventView* struct1, const EventView* struct2)
  {
    return (struct1->m_leadHC->m_jetPtAsymmetry < struct2->m_leadHC->m_jetPtAsymmetry);
  }
};

struct rhh_less_than
{
  inline bool operator() (const EventView* struct1, const EventView* struct2)
  {
    return (struct1->m_rhh < struct2->m_rhh);
  }
};

struct random_less_than
{
  inline bool operator() (const EventView* struct1, const EventView* struct2)
  {
    return (struct1->m_randViewWeight < struct2->m_randViewWeight);
  }
};

struct pt_greater_than
{
  inline bool operator() (const xAH::Jet* struct1, const xAH::Jet* struct2)
  {
    return (struct1->p4.Pt() > struct2->p4.Pt());
  }
};

struct mv2_greater_than
{
  inline bool operator() (const xAH::Jet* struct1, const xAH::Jet* struct2)
  {
    return (struct1->MV2 > struct2->MV2);
  }
};

EventComb::EventComb()
  : 
    m_HCJets(0),
    m_HCJets_mv2Sort(0),
    m_nonHCJets(0),
    m_views(0),
    m_DhhMinView(0),
    m_RhhMinView(0),
    m_selectedView(0),
    m_debug(false),
    m_passedTriggers(0),
    m_passedL1Triggers(0),
    m_passHLTTrig(false),
    m_trigBits(0),
    m_trigSF(1.0),
    m_trigSFErr(0.0),
    m_btagSF(1.0),
    m_xtt(9999),
    m_xtt_ave(9999),
    m_minSum_xtt_1(9999),
    m_minSum_xtt_2(9999),
    m_nTopCands(0),
    m_nTopCands3(0),
    m_nTopCandsAll(0)
{
  m_HCJets          = new std::vector<const xAH::Jet*>;
  m_HCJets_mv2Sort  = new std::vector<const xAH::Jet*>;
  m_nonHCJets       = new std::vector<const xAH::Jet*>;
  m_views           = new std::vector<EventView*>;
  m_passedTriggers  = new std::vector<std::string>();
  m_passedL1Triggers  = new std::vector<std::string>();
}



EventComb::~EventComb()
{
  if(m_debug) cout << __FILE__ << ": " << __LINE__ << endl;
  delete m_HCJets;
  delete m_HCJets_mv2Sort;
  delete m_nonHCJets;
  for(EventView* thisView : *m_views) delete thisView;
  delete m_views;
  delete m_passedTriggers;
  delete m_passedL1Triggers;
}



void EventComb::buildAndSelectEventViews(float leadMass_SR, float sublMass_SR, float radius_SR, float radius_CR, float radius_SB, float CR_shift, float SB_shift, 
					 bool& event_PassDrjj, bool& event_PassDphi, TRandom3* rand, bool /*debug*/)
{
  //
  // In each EventComb there will be 4 "b-jets"
  //
  assert(m_HCJets->size() == 4 && "EventComb::Number of higgs-candidate jets not 4" );
  std::sort(m_HCJets->begin(), m_HCJets->end(), pt_greater_than());
  std::sort(m_HCJets_mv2Sort->begin(), m_HCJets_mv2Sort->end(), mv2_greater_than());

  const xAH::Jet* higgsA_jet0 = m_HCJets->at(0);
  
  //
  // Consider all possible pairings of the b-jets
  //
  for(unsigned int hcandA_j1 = 1; hcandA_j1 < 4; ++hcandA_j1){

    const xAH::Jet* higgsA_jet1 = m_HCJets->at(hcandA_j1);

    //
    // Find the other 2 jets
    //
    //std::vector<const xAH::Jet*> higgsB_jets;
    unsigned int hcandB_j0 = 5;
    unsigned int hcandB_j1 = 5;
    for(unsigned int hcandB_j = 1; hcandB_j < 4; ++hcandB_j){
      if(hcandB_j == hcandA_j1) continue;
      if(hcandB_j0 == 5){
	hcandB_j0 = hcandB_j;
	continue;
      }
      hcandB_j1 = hcandB_j;
      //higgsB_jets.push_back(m_HCJets->at(hcandB_j));
    }

    //assert(higgsB_jets.size() == 2 && "EventComb::Number of other bjets not 2" );
    //const xAH::Jet* higgsB_jet0 = higgsB_jets.at(0);
    //const xAH::Jet* higgsB_jet1 = higgsB_jets.at(1);
    const xAH::Jet* higgsB_jet0 = m_HCJets->at(hcandB_j0);
    const xAH::Jet* higgsB_jet1 = m_HCJets->at(hcandB_j1);

    //
    //  Apply cuts to the considered views
    //
    float m4j       = (higgsA_jet0->p4 + higgsA_jet1->p4 + higgsB_jet0->p4 + higgsB_jet1->p4).M();
    float drjjA     = higgsA_jet0->p4.DeltaR(higgsA_jet1->p4);
    float drjjB     = higgsB_jet0->p4.DeltaR(higgsB_jet1->p4);

    float lead_drjj = drjjA;
    float subl_drjj = drjjB;
    if(  (higgsA_jet0->p4.Pt() + higgsA_jet1->p4.Pt()) < (higgsB_jet0->p4.Pt() + higgsB_jet1->p4.Pt()) ){
      lead_drjj = drjjB;
      subl_drjj = drjjA;
    }
    
    
    bool passLeadDrjj = ( (  (lead_drjj > 360.000/m4j-0.5000000) && (lead_drjj < 652.863/m4j+0.474449) && (m4j <  1250) ) ||
    			  (  (lead_drjj < 0.9967394)             && (m4j >= 1250) ) ); 
    bool passSublDrjj = ( (  (subl_drjj > 235.242/m4j+0.0162996) && (subl_drjj < 874.890/m4j+0.347137) && (m4j <  1250) ) ||
    			  (  (subl_drjj < 1.047049)              && (m4j >= 1250) ) );
    // bool passLeadDrjj = ( lead_drjj < 652.863/m4j+0.474449 && m4j <  1250 ) || 
    //                     ( lead_drjj < 0.9967394            && m4j >= 1250 ); 
    // bool passSublDrjj = ( subl_drjj < 874.890/m4j+0.347137 && m4j <  1250 ) ||
    //                     ( subl_drjj < 1.047049             && m4j >= 1250 );
    bool passDrjj     = (passLeadDrjj && passSublDrjj);


    if(m_debug) cout << "\t\tpassDrjj: " << passDrjj << " (" << passLeadDrjj << " " << passSublDrjj << ")" << " " << m4j << endl;
  

    if(!passDrjj)  continue;
    event_PassDrjj = true;

    //float dphi4j      = (higgsA_jet0->p4 + higgsA_jet1->p4).DeltaPhi( (higgsB_jet0->p4 + higgsB_jet1->p4) );
    //bool  passdPhi    = (fabs(dphi4j) > (1.5 - 0.00333*m4j));
    //if(!passdPhi)  continue;
    event_PassDphi = true;

    //
    // If pass cuts make an event view
    //
    m_views->push_back(new EventView());
    EventView* thisView = m_views->back();
    thisView->m_debug = m_debug;

    if(thisView->m_HC_jets->size() != 0) cout << " ERROR: m_HC_jets is not empty" << endl;
    
    if(higgsA_jet0->p4.Pt() > higgsA_jet1->p4.Pt()) thisView->m_HC_jets->push_back(std::make_pair(higgsA_jet0, higgsA_jet1));
    else                                            thisView->m_HC_jets->push_back(std::make_pair(higgsA_jet1, higgsA_jet0));

    if(higgsB_jet0->p4.Pt() > higgsB_jet1->p4.Pt()) thisView->m_HC_jets->push_back(std::make_pair(higgsB_jet0, higgsB_jet1));
    else                                            thisView->m_HC_jets->push_back(std::make_pair(higgsB_jet1, higgsB_jet0));

    thisView->m_HCJets = m_HCJets;
    thisView->m_randViewWeight = rand->Uniform();
    thisView->calcVars(leadMass_SR, sublMass_SR, radius_SR, radius_CR, radius_SB, CR_shift, SB_shift);

  }

  m_nViews = m_views->size();

  //rhh min
  std::sort(m_views->begin(), m_views->end(), rhh_less_than());

  if(m_nViews){
    m_RhhMinView = m_views->at(0);
    m_passRhhMin = m_RhhMinView->m_rhh > 100.0;// && m_RhhMinView->m_leadHC->p4->M() > 50 && m_RhhMinView->m_sublHC->p4->M() > 50;
    //m_passRhhMin = m_RhhMinView->m_leadHC->p4->M() > 85 && m_RhhMinView->m_sublHC->p4->M() > 80;
  }
  else
    m_RhhMinView = 0;

  //dhh min
  std::sort(m_views->begin(), m_views->end(), dhh_less_than());
  if(m_nViews){
    // for(int i = 0; i < m_nViews; i++){
    //   if(m_debug) cout << "loop over views to find view passing JVC "<< i << endl;
    //   if(m_views->at(i)->m_passJVC){
    // 	m_DhhMinView = m_views->at(i);
    // 	break;
    //   }
    // }
    m_DhhMinView = m_views->at(0);
    m_passLhh = m_DhhMinView->m_lhh > 110;
  }
  else
    m_DhhMinView = 0;
  
  if(m_debug) cout << "m_nViews: " << m_nViews << " m_DhhMinView: " << m_DhhMinView << endl;
  
  m_selectedView = m_DhhMinView;


  return;
}

bool EventComb::passTrig(std::string trigName) const{
  if( trigName == "") return m_passHLTTrig;
  return (find(m_passedTriggers->begin(), m_passedTriggers->end(), trigName ) != m_passedTriggers->end());
}

// for boosted and susy people to play with
float EventComb::ResolvedXhhFrom4Jets(std::vector<const xAH::Jet*>* top4MV2Jets){
  //
  // Consider all possible pairings of the 4 jets
  //
  float dhh_min = 1e6;
  float xhh = 1e6;

  const xAH::Jet* higgsA_jet0 = top4MV2Jets->at(0);
  for(unsigned int hcandA_j1 = 1; hcandA_j1 < 4; ++hcandA_j1){

    const xAH::Jet* higgsA_jet1 = top4MV2Jets->at(hcandA_j1);

    //
    // Find the other 2 jets
    //
    unsigned int hcandB_j0 = 5;
    unsigned int hcandB_j1 = 5;
    for(unsigned int hcandB_j = 1; hcandB_j < 4; ++hcandB_j){
      if(hcandB_j == hcandA_j1) continue;
      if(hcandB_j0 == 5){
	hcandB_j0 = hcandB_j;
	continue;
      }
      hcandB_j1 = hcandB_j;
    }

    const xAH::Jet* higgsB_jet0 = top4MV2Jets->at(hcandB_j0);
    const xAH::Jet* higgsB_jet1 = top4MV2Jets->at(hcandB_j1);

    //
    //  Apply cuts to the considered pairing
    //
    float m4j       = (higgsA_jet0->p4 + higgsA_jet1->p4 + higgsB_jet0->p4 + higgsB_jet1->p4).M();
    float drjjA     = higgsA_jet0->p4.DeltaR(higgsA_jet1->p4);
    float drjjB     = higgsB_jet0->p4.DeltaR(higgsB_jet1->p4);

    float mjjA = (higgsA_jet0->p4 + higgsA_jet1->p4).M();
    float mjjB = (higgsB_jet0->p4 + higgsB_jet1->p4).M();

    float lead_drjj = drjjA;
    float subl_drjj = drjjB;

    float lead_mjj = mjjA;
    float subl_mjj = mjjB;

    // sort on scalar sum of HC jet pts
    if(  (higgsA_jet0->p4.Pt() + higgsA_jet1->p4.Pt()) < (higgsB_jet0->p4.Pt() + higgsB_jet1->p4.Pt()) ){
      lead_drjj = drjjB;
      subl_drjj = drjjA;
      lead_mjj = mjjB;
      subl_mjj = mjjA;
    }
    
    // m4j dependent dRjj requirements on jet pairings
    bool passLeadDrjj = ( (  (lead_drjj > 360.000/m4j-0.5000000) && (lead_drjj < 652.863/m4j+0.474449) && (m4j <  1250) ) ||
    			  (  (lead_drjj < 0.9967394)             && (m4j >= 1250) ) ); 

    bool passSublDrjj = ( (  (subl_drjj > 235.242/m4j+0.0162996) && (subl_drjj < 874.890/m4j+0.347137) && (m4j <  1250) ) ||
    			  (  (subl_drjj < 1.047049)              && (m4j >= 1250) ) );

    bool passDrjj     = (passLeadDrjj && passSublDrjj);

    if(!passDrjj)  continue;

    //
    // If pass cuts, apply dhh min
    //

    //angle of line through origin and center of SR
    float theta_SR = atan(110./120.); 

    //angle of this point above the theta_SR line  
    float theta_hh = atan(subl_mjj/lead_mjj) - theta_SR; 

    //Distance from origin in GeV 
    float rhh  = sqrt( pow(lead_mjj,2) + pow(subl_mjj,2) ); 

    // distance of point from line: theta = theta_SR                                           
    float dhh  = rhh * fabs(sin( theta_hh )); 
    
    // if this has smaller dhh, update xhh
    if(dhh < dhh_min){
      dhh_min = dhh;
      xhh = sqrt( (pow ( ( (lead_mjj - 120.)/(0.1*lead_mjj) ), 2 ) +
		  (pow ( ( (subl_mjj - 110.)/(0.1*subl_mjj) ), 2 ) )));
    }
    
  }
  return xhh;
}
