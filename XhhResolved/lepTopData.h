#ifndef XHHRESOLVED_LEPTOPDATA_H
#define XHHRESOLVED_LEPTOPDATA_H

#include <vector>
using namespace std;

//
// lepTop Cand
//
class lepTopData{

 public:
  float pt;
  float eta;
  float phi;
  float m;
  float drmj;
  jetData* jet;
  muonData* muon;
  TLorentzVector tvector;
  TLorentzVector tvector_mub;

  float met;
  float metphi;
  float dPhiMuonMet;
  float Mt;
  unsigned int jetIdx;  
  
  lepTopData(float dRmj,
	     //float b_jet_asso_pt, 
	     int   b_jet_idx_in_lepTopJets, 
	     const vector<float>& b_lepTopJets_pt,      const vector<float>& b_lepTopJets_eta, const vector<float>& b_lepTopJets_phi,const vector<float>& b_lepTopJets_E,
	     const vector<float>& b_lepTopJets_MV2c20,  const vector<float>& b_lepTopJets_Jvt, const vector<int>& b_lepTopJets_clean_passLooseBad, 
	     float b_lTop_muon_pt, float b_lTop_muon_eta, float b_lTop_muon_phi, float b_lTop_muon_m, float b_lTop_muon_ptcone20,
	     float b_lTop_met, float b_lTop_metphi, float b_lTop_dPhimmet, float b_lTop_Mt,
	     bool debug
	     ){ 
    if(debug) cout << "In lepTopData " << endl;
    drmj        = dRmj;
    met         = b_lTop_met;
    metphi      = b_lTop_metphi;
    dPhiMuonMet = b_lTop_dPhimmet;
    Mt          = b_lTop_Mt;

    //
    // Temporary hack to patch v5 ntupls
    //
    jetIdx = b_jet_idx_in_lepTopJets;
    //int hack_idx = -1;
    //for(unsigned int idx = 0; idx < b_lepTopJets_pt.size(); ++idx){
    //  if(b_lepTopJets_pt.at(idx) == b_jet_asso_pt){
    //	hack_idx = idx;
    //  }
    //}
    //
    //if(hack_idx<0){
    //  cout << "ERROR setting hack_idx to " << 0 << endl;
    //  cout << " Matching " << b_jet_asso_pt << endl;
    //  for(unsigned int idx = 0; idx < b_lepTopJets_pt.size(); ++idx){
    //	cout << "\t" << b_lepTopJets_pt.at(idx) <<endl;
    //  }
    //
    //  hack_idx = 0;
    //}

    //
    // Jet
    // 
    jet = new jetData(b_lepTopJets_pt     .at(jetIdx), 
		      b_lepTopJets_eta    .at(jetIdx), 
		      b_lepTopJets_phi    .at(jetIdx), 
		      b_lepTopJets_E      .at(jetIdx), 
		      b_lepTopJets_MV2c20 .at(jetIdx));
    jet->Jvt = b_lepTopJets_Jvt.at(jetIdx);
    jet->clean_passLooseBad = b_lepTopJets_clean_passLooseBad.at(jetIdx);
    //TLorentzVector jetVec = jet->vec();

    //
    // Muon
    //
    muon = new muonData(b_lTop_muon_pt, b_lTop_muon_eta, b_lTop_muon_phi, b_lTop_muon_m);
    muon->ptcone20 =   b_lTop_muon_ptcone20;

    calcLepTopKinematics();
    if(debug) cout << "Left lepTopData " << endl;
  }

  void calcLepTopKinematics(){
    TLorentzVector jetVec  = jet ->vec();
    TLorentzVector muonVec = muon->vec();

    //
    // Calculating the rescaled pt (muon+b)
    //
    tvector_mub = (muonVec + jetVec);

    float metx     = met * cos(metphi);
    float mety     = met * sin(metphi);

    float pXLepTop = jetVec.Px() + metx + muonVec.Px();
    float pYLepTop = jetVec.Py() + mety + muonVec.Py();
    float pZLepTop = jetVec.Pz() + muonVec.Pz(); // Solve for pZ using mW constaint ?
    float mTop = 175.*1000;
    float eLepTop = sqrt(pXLepTop*pXLepTop + pYLepTop*pYLepTop + pZLepTop*pZLepTop + mTop*mTop );

    tvector.SetPxPyPzE(pXLepTop,pYLepTop,pZLepTop,eLepTop);

    pt  = tvector.Pt();
    eta = tvector.Eta();
    phi = tvector.Phi();
    m   = tvector.M();
    return;
  }


  TLorentzVector vec() const{
    return tvector;
  }

  TLorentzVector vec_mub() const{
    return tvector_mub;
  }

  
};
#endif
