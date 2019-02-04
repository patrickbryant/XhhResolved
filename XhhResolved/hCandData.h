#ifndef XHHRESOLVED_HCANDDATA_H
#define XHHRESOLVED_HCANDDATA_H

#include <vector>
using namespace std;

//
// hCandData
//
class hCandData{

 public:

  float pt;
  float ht;
  float eta;
  float phi;
  float m;
  float shiftedMass;

  float alpha;

  float dRjj;
  jetData* leadJet;
  jetData* sublJet;
  TLorentzVector tvector;
  TLorentzVector tvectorMhCorrected;
  TLorentzVector tvectorMZCorrected;
  TLorentzVector tvectorMHCorrected;

  float pt_cor;

  float mW;
  float WdRjj;
  float TdRwb;
  float mTop;
  float Xtt;
  int   nTags;
  unsigned int leadJetIdx;
  unsigned int sublJetIdx;

  hCandData(const vector<int>& b_jet_asso_idx_in_resolvedJets, 
	    const vector<float>& b_resolvedJets_pt, 
	    const vector<float>& b_resolvedJets_eta, 
	    const vector<float>& b_resolvedJets_phi, 
	    const vector<float>& b_resolvedJets_E, 
	    const vector<float>& b_resolvedJets_MV2, 
	    const vector<float>& b_resolvedJets_Jvt,   
	    const vector<int>& b_resolvedJets_clean_passLooseBad,
	    const vector<vector<float> >* b_resolvedJets_MV2_SF = 0
	    ){ 
    leadJetIdx = b_jet_asso_idx_in_resolvedJets.at(0);
    leadJet = new jetData(b_resolvedJets_pt    .at(leadJetIdx),
                          b_resolvedJets_eta   .at(leadJetIdx), 
                          b_resolvedJets_phi   .at(leadJetIdx), 
                          b_resolvedJets_E     .at(leadJetIdx),
                          b_resolvedJets_MV2.at(leadJetIdx));



    leadJet->Jvt = b_resolvedJets_Jvt.at(leadJetIdx);
    leadJet->clean_passLooseBad = b_resolvedJets_clean_passLooseBad.at(leadJetIdx);
    if(b_resolvedJets_MV2_SF)
      leadJet->btagSF = &(b_resolvedJets_MV2_SF->at(leadJetIdx));

    TLorentzVector leadJetVec = leadJet->vec();
    sublJetIdx = b_jet_asso_idx_in_resolvedJets.at(1);
    sublJet = new jetData(b_resolvedJets_pt    .at(sublJetIdx),
                          b_resolvedJets_eta   .at(sublJetIdx), 
                          b_resolvedJets_phi   .at(sublJetIdx), 
                          b_resolvedJets_E     .at(sublJetIdx),
                          b_resolvedJets_MV2.at(sublJetIdx));
    sublJet->Jvt = b_resolvedJets_Jvt.at(sublJetIdx);
    sublJet->clean_passLooseBad = b_resolvedJets_clean_passLooseBad.at(sublJetIdx);
    if(b_resolvedJets_MV2_SF)
      sublJet->btagSF = &(b_resolvedJets_MV2_SF->at(sublJetIdx));

    TLorentzVector sublJetVec = sublJet->vec();
    
    dRjj = leadJetVec.DeltaR(sublJetVec);

    mW     = -1;
    WdRjj  = -1;
    TdRwb  = -1;
    mTop   = -1;
    Xtt    = 99;
    nTags  = -1;
    calcHCandKinematics();
  }

  TLorentzVector vec() const{
    return tvector;
  }

  TLorentzVector vecMhCorrected() const{
    return tvectorMhCorrected;
  }

  TLorentzVector vecMZCorrected() const{
    return tvectorMZCorrected;
  }

  TLorentzVector vecMHCorrected() const{
    return tvectorMHCorrected;
  }

  void calcHCandKinematics(){
    tvector = (leadJet->vec() + sublJet->vec());
    pt  = tvector.Pt();
    ht  = leadJet->pt + sublJet->pt;
    eta = tvector.Eta();
    phi = tvector.Phi();
    m   = tvector.M();

    jetData* oldLead = leadJet;
    jetData* oldSubl = sublJet;
    if(leadJet->pt < sublJet->pt){
      leadJet = oldSubl;
      sublJet = oldLead;
    }
      

    alpha = m ? 125.0/m : 1.0;
    tvectorMhCorrected = alpha * tvector;

    float alpha_Z = m ? 91.2/m : 1.0;
    tvectorMZCorrected = alpha_Z * tvector;

    float alpha_H = m ? 165.0/m : 1.0;
    tvectorMHCorrected = alpha_H * tvector;

    pt_cor = tvectorMhCorrected.Pt();

    return;
  }

  void calcTTBarX(const vector<jetData*> otherJets){
	jetData* highMV2Jet = leadJet;
	jetData* lowMV2Jet  = sublJet;
	  
	if(lowMV2Jet->MV2 > highMV2Jet->MV2){
	  highMV2Jet = sublJet;
	  lowMV2Jet  = leadJet;
	}
	
	for(const jetData* ojet : otherJets){//pick jet that minimizes fabs(mW - 80.4)
	  TLorentzVector oVec = ojet->vec();

	  //if(oVec.DeltaR(tvector) > 1.5) continue;

	  float this_mW    = (oVec + lowMV2Jet->vec()).M();
	  float this_WdRjj = oVec.DeltaR(lowMV2Jet->vec());
	  float this_mTop  = (oVec + tvector).M();
	  float this_TdRwb = (oVec + lowMV2Jet->vec()).DeltaR(highMV2Jet->vec());

	  float w_sig    = (this_mW   -  80.4)/(0.1*this_mW);
	  float top_sig  = (this_mTop - 172.5)/(0.1*this_mTop);
	  float this_Xtt = sqrt(w_sig*w_sig + top_sig*top_sig);
	  
	  /* if((Xtt < 0) || (this_Xtt < Xtt)){ */
	  /*   Xtt  = this_Xtt; */
	  /*   mW   = this_mW; */
	  /*   mTop = this_mTop; */
	  /* } */
	  if(fabs(this_mW - 80.4) < fabs(mW - 80.4)){
	    Xtt    = this_Xtt;
	    mW     = this_mW;
	    WdRjj  = this_WdRjj;
	    mTop   = this_mTop;
	    TdRwb  = this_TdRwb;
	  }
	  
	}

  }

  bool canMakeDiJet(const jetData& oneJet, const jetData& thirdJet) const{
    if(oneJet.vec().DeltaR(thirdJet.vec()) < 1.5){
      if((oneJet.vec() + thirdJet.vec()).Pt() > 150){
	return true;
      }
    }
    return false;
  }

  bool canMakeDiJet(const jetData& thirdJet) const{
    if(canMakeDiJet(*leadJet, thirdJet)) return true;
    if(canMakeDiJet(*sublJet, thirdJet)) return true;
    return false;
  }

  ~hCandData(){
    if (leadJet) delete leadJet;
    if (sublJet) delete sublJet;
  }

};
#endif

