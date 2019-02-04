#include "XhhResolved/EventView.h"

#include <iostream>

using std::cout;  using std::endl; 

struct pt_greater_than
{
  inline bool operator() (const xAH::Jet* struct1, const xAH::Jet* struct2)
  {
    return (struct1->p4.Pt() > struct2->p4.Pt());
  }
};

struct MV2_greater_than
{
  inline bool operator() (const xAH::Jet* struct1, const xAH::Jet* struct2)
  {
    return (struct1->MV2 > struct2->MV2);
  }
};

EventView::EventView()
  : m_qcd_weight(1.0),
    m_HC_jets(0),
    m_HC_a(0),
    m_HC_b(0),
    hhp4(0),
    hhp4cor(0),
    hhp4corZ(0),
    hhp4corH(0),
    ggp4(0),
    m_leadHC(0),
    m_sublHC(0),
    m_leadPtHC(0),
    m_sublPtHC(0),
    m_leadGC(0),
    m_sublGC(0),
    m_theta_SR(0),
    m_theta_hh(0),
    m_rhh(0),
    m_rRR(0),
    m_dhh(0), 
    m_lhh(0),
    m_hhJetEtaSum2(0),
    m_xhh(0), 
    m_xHM(0), 
    m_xLM(0), 
    //m_xvbb(0),
    m_dEta(0),
    m_dPhi(0),
    m_dR(0), 
    m_dEta_gg(0),
    m_dPhi_gg(0),
    m_dR_gg(0), 
    m_R_dRdR(0),
    m_R_dRdR_gg(0),
    m_passHCPt_subl(false),
    m_passHCPt_lead(false),
    m_passHCPt     (false),
    m_passHCdEta   (false),
    m_passHCdPhi   (false),
    m_mv2Cut       (0.8244),
    m_twoTag       (false),
    m_fourTag      (false),
    m_leadTag      (false),
    m_sublTag      (false),
    m_twoTagSplit  (false),
    m_passSideband (false),
    m_passControl  (false),
    m_passSignal   (false),
    m_passSignal_in (false),
    m_passSignal_out(false),
    m_passLMVR (false),
    m_passLeadHC   (false),
    m_passSublHC   (false),
    m_passVbbVeto(false),
    m_randGen    (new TRandom3()),
    m_randViewWeight(0),
    m_HCJets(0),
    m_debug(false)
{
  m_HC_jets = new std::vector<jetPair>;
  m_HCJets  = new std::vector<const xAH::Jet*>;//the not stupid way...
}



EventView::~EventView()
{
  if(m_debug) cout << __FILE__ << ": " << __LINE__ << endl;
  delete m_HC_jets;
  delete m_HC_a;
  delete m_HC_b;
  delete hhp4;
  delete ggp4;
  delete m_randGen;
}

void EventView::calcVars(float leadMass_SR, float sublMass_SR, float radius_SR, float radius_CR, float radius_SB, float CR_shift, float SB_shift)
{

  float dR_min = 1e3;
  int a = -1, b = -1, c = -1, d = -1;
  for(int i = 0; i < 4; i++){
    //m_aveJVC += m_HCJets->at(i)->JVC;
    for(int j = i+1; j < 4; j++){
      float dR = m_HCJets->at(i)->p4.DeltaR(m_HCJets->at(j)->p4);
      if(dR<dR_min){
	dR_min = dR;
	a = i;//i is always smaller than j
	b = j;

	//find other two jet indices
	c = -1;
	for(int z = 0; z < 4; z++){
	  if(a ==  z) continue;
	  if(b ==  z) continue;
	  if(c == -1){ c = z; continue; }
	  d = z;
	}

      }

    }
  }

  m_leadGC = new hCand(m_HCJets->at(a), m_HCJets->at(b));
  m_sublGC = new hCand(m_HCJets->at(c), m_HCJets->at(d));
  ggp4     = new TLorentzVector( *m_leadGC->p4 + *m_sublGC->p4 );
  //m_xvbb   = pow( (m_sublGC->p4->M()-80.4)/(m_sublGC->p4->M()*0.1),2 ) + pow( (m_leadGC->p4->M()-40)/(m_leadGC->p4->M()*0.25),2 );
  m_passVbbVeto = m_sublGC->p4->M()>100 || m_sublGC->p4->M()<70 || m_leadGC->p4->M()>55;

  m_HC_a  = new hCand(m_HC_jets->at(0).first,  m_HC_jets->at(0).second);
  m_HC_b  = new hCand(m_HC_jets->at(1).first,  m_HC_jets->at(1).second);  

  // Want JVC of jets matched to HCs to be as consistent as possible with b\bar{b}
  //                        _______________________
  //                 ______|_______________________|___________  
  //                |      |                       |           |
  // JVC<0 ---------a1-----b2--------0-------------b1----------a2------- JVC>0  (passing)
  //
  //                 ______                         ___________  
  //                |      |                       |           |
  // JVC<0 ---------b1-----b2--------0-------------a1----------a2------- JVC>0  (not passing)
  //
  //                 ______________________________
  //                |       _______________________|___________
  //                |      |                       |           |
  // JVC<0 ---------b1-----a2--------0-------------b2----------a1------- JVC>0  (passing)
  //
  // Detect passing by checking if invervals overlap.
  // In cases with multiple views massing dRjj cuts, consider only views which passJVC for Dhh minimization
  // m_passJVC = ((m_HC_a->m_leadJet->JVC - m_HC_b->m_leadJet->JVC)*(m_HC_a->m_sublJet->JVC - m_HC_b->m_leadJet->JVC) <= 0) ||
  //             ((m_HC_a->m_leadJet->JVC - m_HC_b->m_sublJet->JVC)*(m_HC_a->m_sublJet->JVC - m_HC_b->m_sublJet->JVC) <= 0);
  m_passJVC = true;
  if(m_debug){
    cout << "m_HC_a->m_leadJet->JVC " << m_HC_a->m_leadJet->JVC << endl;
    cout << "m_HC_a->m_sublJet->JVC " << m_HC_a->m_sublJet->JVC << endl;
    cout << "m_HC_b->m_leadJet->JVC " << m_HC_b->m_leadJet->JVC << endl;
    cout << "m_HC_b->m_sublJet->JVC " << m_HC_b->m_sublJet->JVC << endl;
  }

  hhp4      = new TLorentzVector((*m_HC_a->p4)     + (*m_HC_b->p4)   );
  hhp4cor   = new TLorentzVector((*m_HC_a->p4cor)  + (*m_HC_b->p4cor));
  hhp4corZ  = new TLorentzVector((*m_HC_a->p4corZ) + (*m_HC_b->p4corZ));
  hhp4corH  = new TLorentzVector((*m_HC_a->p4corH) + (*m_HC_b->p4corH));
  float m4j = hhp4->M();

  if(fabs(ggp4->Pt() - hhp4->Pt()) > 1){
    cout << "ERROR: ggp4->Pt() = " << ggp4->Pt() << " != " << hhp4->Pt() << " hhp4->Pt()" << endl;
  }

  //if(m_HC_a->p4->Pt() > m_HC_b->p4->Pt()){
  //if(m_randViewWeight > 0.5){
  if((m_HC_a->m_leadJet->p4.Pt() + m_HC_a->m_sublJet->p4.Pt()) > (m_HC_b->m_leadJet->p4.Pt() + m_HC_b->m_sublJet->p4.Pt())){
    m_leadHC = m_HC_a;
    m_sublHC = m_HC_b;
  }else{
    m_leadHC = m_HC_b;
    m_sublHC = m_HC_a;
  }

  if((m_HC_a->m_leadJet->p4 + m_HC_a->m_sublJet->p4).Pt() > (m_HC_b->m_leadJet->p4 + m_HC_b->m_sublJet->p4).Pt() ){
    m_leadPtHC = m_HC_a;
    m_sublPtHC = m_HC_b;
  }else{
    m_leadPtHC = m_HC_b;
    m_sublPtHC = m_HC_a;
  }


  m_R_dRdR    = sqrt(m_leadHC->m_dRjj*m_leadHC->m_dRjj + m_sublHC->m_dRjj*m_sublHC->m_dRjj);
  m_R_dRdR_gg = sqrt(m_leadGC->m_dRjj*m_leadGC->m_dRjj + m_sublGC->m_dRjj*m_sublGC->m_dRjj);

  m_GCdR_diff = m_sublGC->m_dRjj - m_leadGC->m_dRjj;
  m_GCdR_sum  = m_sublGC->m_dRjj + m_leadGC->m_dRjj;

  m_HCdR_diff = m_sublHC->m_dRjj - m_leadHC->m_dRjj;
  m_HCdR_sum  = m_sublHC->m_dRjj + m_leadHC->m_dRjj;

  //Ht of selected jets
  m_Ht4j    = m_HC_a->m_leadJet->p4.Pt() + m_HC_a->m_sublJet->p4.Pt() + m_HC_b->m_leadJet->p4.Pt() + m_HC_b->m_sublJet->p4.Pt();
  m_R_pt_4j = sqrt(pow(m_HC_a->m_leadJet->p4.Pt()-40,2) + pow(m_HC_a->m_sublJet->p4.Pt()-40,2) + pow(m_HC_b->m_leadJet->p4.Pt()-40,2) + pow(m_HC_b->m_sublJet->p4.Pt()-40,2));

  //get b-tag category
  int lead_tags = (int)(m_leadHC->m_leadJet->MV2 > m_mv2Cut) + (int)(m_leadHC->m_sublJet->MV2 > m_mv2Cut);
  int subl_tags = (int)(m_sublHC->m_leadJet->MV2 > m_mv2Cut) + (int)(m_sublHC->m_sublJet->MV2 > m_mv2Cut);

  m_fourTag     = (lead_tags == 2 && subl_tags == 2);
  m_twoTag      = (lead_tags      +  subl_tags == 2);
  m_leadTag     = (lead_tags == 2 && subl_tags == 0);
  m_sublTag     = (lead_tags == 0 && subl_tags == 2);
  m_twoTagSplit = (lead_tags == 1 && subl_tags == 1);

  //angle of line through origin and center of SR
  float m_theta_SR = atan(sublMass_SR/leadMass_SR); 

  float sublHCandMass = m_sublHC->p4->M();
  float leadHCandMass = m_leadHC->p4->M();

  //angle of this point above the theta_SR line  
  m_theta_hh = atan(sublHCandMass/leadHCandMass) - m_theta_SR; 

  //Distance from origin in GeV 
  m_rhh  = sqrt( pow(leadHCandMass,2) + pow(sublHCandMass,2) ); 

  // distance of point from line: theta = theta_SR                                           
  m_dhh  = m_rhh * fabs(sin( m_theta_hh )); 
  m_lhh  = m_rhh * fabs(cos( m_theta_hh )); 

  m_hhJetEtaSum2 = pow(m_leadHC->m_leadJet->p4.Eta(),2) + pow(m_leadHC->m_sublJet->p4.Eta(),2) 
                 + pow(m_sublHC->m_leadJet->p4.Eta(),2) + pow(m_sublHC->m_sublJet->p4.Eta(),2);

  m_HCJetAbsEta  = ( fabs(m_leadHC->m_leadJet->p4.Eta()) + fabs(m_leadHC->m_sublJet->p4.Eta()) 
		   + fabs(m_sublHC->m_leadJet->p4.Eta()) + fabs(m_sublHC->m_sublJet->p4.Eta()) )/4;

  m_HCJetAR = sqrt( pow(1-m_leadHC->m_leadJet->p4.Pt()/m_leadHC->m_leadJet->p4.E(),2)
		  + pow(1-m_leadHC->m_sublJet->p4.Pt()/m_leadHC->m_sublJet->p4.E(),2)
		  + pow(1-m_sublHC->m_leadJet->p4.Pt()/m_sublHC->m_leadJet->p4.E(),2)
		  + pow(1-m_sublHC->m_sublJet->p4.Pt()/m_sublHC->m_sublJet->p4.E(),2) )/2; // Jet Activity Radius: ~0 for events with jet central jet energy
                                                                                         //                      ~1 for forward jet energy
  m_HCJetPtE1 = (  m_leadHC->m_leadJet->p4.Pt()/m_leadHC->m_leadJet->p4.E()
		 + m_leadHC->m_sublJet->p4.Pt()/m_leadHC->m_sublJet->p4.E()
		 + m_sublHC->m_leadJet->p4.Pt()/m_sublHC->m_leadJet->p4.E()
		 + m_sublHC->m_sublJet->p4.Pt()/m_sublHC->m_sublJet->p4.E() )/4;

  m_HCJetPtE2 = ( pow(m_leadHC->m_leadJet->p4.Pt()/m_leadHC->m_leadJet->p4.E(),2)
		+ pow(m_leadHC->m_sublJet->p4.Pt()/m_leadHC->m_sublJet->p4.E(),2)
	        + pow(m_sublHC->m_leadJet->p4.Pt()/m_sublHC->m_leadJet->p4.E(),2)
		+ pow(m_sublHC->m_sublJet->p4.Pt()/m_sublHC->m_sublJet->p4.E(),2) )/(4*m_HCJetPtE1);

    
  m_dPhi = m_leadHC->p4->DeltaPhi(*m_sublHC->p4);
  m_dEta = m_leadHC->p4->Eta()- m_sublHC->p4->Eta();
  m_dR   = m_leadHC->p4->DeltaR(*m_sublHC->p4);

  m_dPhi_gg = m_leadGC->p4->DeltaPhi(*m_sublGC->p4);
  m_dEta_gg = m_leadGC->p4->Eta()- m_sublGC->p4->Eta();
  m_dR_gg   = m_leadGC->p4->DeltaR(*m_sublGC->p4);


  m_xhh = sqrt( (pow ( ( (leadHCandMass - leadMass_SR)/(0.1*leadHCandMass) ), 2 ) +
		(pow ( ( (sublHCandMass - sublMass_SR)/(0.1*sublHCandMass) ), 2 ) )));

  m_xLM = sqrt( (pow ( ( (leadHCandMass - 89.7)/(0.1*leadHCandMass) ), 2 ) +
		(pow ( ( (sublHCandMass - 82.2)/(0.1*sublHCandMass) ), 2 ) )));

  m_xHM = sqrt( (pow ( ( (leadHCandMass - 160.0)/(0.1*leadHCandMass) ), 2 ) +
		(pow ( ( (sublHCandMass - 146.7)/(0.1*sublHCandMass) ), 2 ) )));

  //
  //  Set Cuts
  //

  float sublHCandPt   = m_sublPtHC->p4->Pt();
  float leadHCandPt   = m_leadPtHC->p4->Pt();
  m_passHCPt_subl     = (sublHCandPt > (0.333333*m4j - 73.3333) ); 
  m_passHCPt_lead     = (leadHCandPt > (0.513333*m4j - 103.333) );

  m_passHCPt          = m_passHCPt_lead && m_passHCPt_subl;

  m_passHCdEta = fabs(m_dEta)<1.5;
  m_passHCdPhi = true;
  m_passHCdR = true;

  m_pass_ggVeto = m_sublGC->m_dRjj > 235.242/(m4j+70)+0.1162996;

  //
  //  Set Regions
  //

  m_passSignal     = (m_xhh < radius_SR);  
  m_passSignal_in  = (m_xhh < 1.0);
  m_passSignal_out = m_passSignal && !m_passSignal_in;
  m_passLMVR       = (m_xLM < radius_SR);
  m_passHMVR       = (m_xHM < radius_SR);

  bool passCRVeto = !m_passSignal;
  m_passControl   = passCRVeto &&  (sqrt( pow(leadHCandMass - leadMass_SR*CR_shift,2) +  pow(sublHCandMass - sublMass_SR*CR_shift,2) ) < radius_CR );
  m_passControlD  = !(m_xhh < radius_SR*1.25) && m_passControl;
  
  m_passSideband = !m_passSignal && !m_passControl && passCRVeto &&
    ( sqrt( pow(leadHCandMass - leadMass_SR*SB_shift,2) +  pow(sublHCandMass - sublMass_SR*SB_shift,2) ) < radius_SB );
  
  
  m_passLeadHC = fabs(leadMass_SR - leadHCandMass) < 10;
  m_passSublHC = fabs(sublMass_SR - sublHCandMass) < 10;

  //
  // Determine if 
  //
  
  m_randViewWeight = m_randGen->Uniform();//random weight for studies where I want to pick a random event view

  return; 
}



float EventView::GetBTagSF(unsigned int btagSFItr) const
{
  float totalSF = 1.0;
  
  if(m_leadHC->m_leadJet->MV2c20_isFix70)
    totalSF *= m_leadHC->m_leadJet->MV2c20_sfFix70.at(btagSFItr);

  if(m_leadHC->m_sublJet->MV2c20_isFix70)
    totalSF *= m_leadHC->m_sublJet->MV2c20_sfFix70.at(btagSFItr);

  if(m_sublHC->m_leadJet->MV2c20_isFix70)
    totalSF *= m_sublHC->m_leadJet->MV2c20_sfFix70.at(btagSFItr);

  if(m_sublHC->m_sublJet->MV2c20_isFix70)
    totalSF *= m_sublHC->m_sublJet->MV2c20_sfFix70.at(btagSFItr);
  
  return totalSF;
}


