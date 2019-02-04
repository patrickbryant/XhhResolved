#include <XhhResolved/TriggerTagger.h>
#include <assert.h>

#include <iostream>
using std::vector; 
using std::cout; using std::endl;

TriggerTagger :: TriggerTagger (std::string name, bool doTag,
                                TGraphAsymmErrors* eff_tag ,
                                TGraphAsymmErrors* sf_tag  ,
                                TGraphAsymmErrors* eff_j35 ,
                                TGraphAsymmErrors* eff_j45 ,
                                TGraphAsymmErrors* eff_j50 ,
                                TGraphAsymmErrors* eff_j55 ,
                                TGraphAsymmErrors* eff_j60 ,
                                TGraphAsymmErrors* eff_j65 ,
                                TGraphAsymmErrors* eff_j70 ,
                                TGraphAsymmErrors* eff_j75 ,
                                TGraphAsymmErrors* eff_j100,
                                TGraphAsymmErrors* eff_j150,
                                TGraphAsymmErrors* eff_j175,
                                TGraphAsymmErrors* eff_j225,
                                TGraphAsymmErrors* eff_j275,
                                TGraphAsymmErrors* eff_j300,
                                TGraphAsymmErrors* eff_j360,
                                float scaleFactor
                                ) :
  m_name(name),
  m_doTag(doTag),
  m_scaleFactor(scaleFactor),
  //m_j35Plateau  (35.0  ),
  //m_j45Plateau  (45.0  ),
  //m_j50Plateau  (50.0  ),
  //m_j55Plateau  (55.0  ),
  //m_j60Plateau  (60.0  ),
  //m_j65Plateau  (65.0  ),
  //m_j70Plateau  (70.0  ),
  //m_j75Plateau  (75.0  ),
  //m_j100Plateau (100.0 ),
  //m_j150Plateau (150.0 ),
  //m_j175Plateau (175.0 ),
  //m_j225Plateau (225.0 ),
  //m_j275Plateau (275.0 ),
  //m_j300Plateau (300.0 ),
  //m_j360Plateau (360.0 ),

  m_eff_tag(eff_tag),
  m_sf_tag (sf_tag),
  m_j35    (eff_j35 , 0),
  m_j45    (eff_j45 , 0),
  m_j50    (eff_j50 , 0),
  m_j55    (eff_j55 , 0),
  m_j60    (eff_j60 , 70.),
  m_j65    (eff_j65 , 0),
  m_j70    (eff_j70 , 85.),
  //m_j75    (eff_j75 , 85.),
  m_j75    (eff_j75 , 0),
  m_j100   (eff_j100, 0),
  m_j150   (eff_j150, 0),
  m_j175   (eff_j175, 0),
  m_j225   (eff_j225, 0),
  m_j275   (eff_j275, 0),
  m_j300   (eff_j300, 0),
  m_j360   (eff_j360, 0)
{

  //
  // Init the Eff and 
  //
  if(m_doTag && m_eff_tag){

    //cout << "Loading Efficeincies " << m_name << endl;
    if(m_sf_tag){
      //cout << "\t and scale factors " << endl;

      unsigned int nBins = m_sf_tag->GetN();
      for(unsigned int iBin = 0; iBin<nBins; ++iBin){
        double sf_eff, sf_pt;
        m_sf_tag->GetPoint(iBin, sf_pt, sf_eff);
        //float sf_pt_low   = m_sf_tag->GetErrorXlow(iBin);
        //float sf_pt_high  = m_sf_tag->GetErrorXhigh(iBin);
        //cout << "\tiBin " << iBin << " pt: " << sf_pt-sf_pt_low << " - " << sf_pt << " - " << sf_pt+sf_pt_high
        //     << endl;
      }
      //cout << m_eff_tag->GetN()  << " vs " << m_sf_tag->GetN() << endl;
      assert(m_eff_tag->GetN() == m_sf_tag->GetN());
    }

    unsigned int nBins = m_eff_tag->GetN();
    for(unsigned int iBin = 0; iBin<nBins; ++iBin){
      double eff, pt;
      m_eff_tag->GetPoint(iBin, pt, eff);
      //float pt_low   = m_eff_tag->GetErrorXlow(iBin);
      float pt_high  = m_eff_tag->GetErrorXhigh(iBin);
      float err_low  = m_eff_tag->GetErrorYlow(iBin);
      float err_high = m_eff_tag->GetErrorYhigh(iBin);
      float err_ave  = (err_low+err_high)/2;
      float error_total = err_ave;

      if(sf_tag){
        double sf, ptSF;
        m_sf_tag->GetPoint(iBin, ptSF, sf);     
        //float ptSF_low   = m_sf_tag->GetErrorXlow(iBin);
        //float ptSF_high  = m_sf_tag->GetErrorXhigh(iBin);
        float errSF_low  = m_sf_tag->GetErrorYlow(iBin);
        float errSF_high = m_sf_tag->GetErrorYhigh(iBin);
        float errSF_ave  = (errSF_low+errSF_high)/2;
        
        eff *= sf;
        error_total = sqrt(err_ave*err_ave + errSF_ave*errSF_ave);
      }

      //cout << "\tiBin " << iBin << " pt: " << pt-pt_low << " - " << pt << " - " << pt+pt_high
      //     << " eff: " << eff << " +/- " << error_total 
      //     << endl;
      m_highBinEdge.push_back(pt+pt_high);
      m_eff        .push_back(eff);
      m_effErr     .push_back(error_total);
    }

  }// doTag and eff_tag

}


void TriggerTagger::count(ptThreshold& thisThreshold, const XhhResolved::jetTrigInfo& jetInfo, float smearFactor, bool debug)
{
  if(debug) cout << "In count" << m_name << endl;


  //
  //  See if on plateua (if using a plataue)
  //
  if(jetInfo.pt < thisThreshold.m_plateau){
    return;
  }
    
  //
  // Evaluate the turn on
  //
  float thisPtEff = 1.0;
  if(thisThreshold.m_ptEff){
    if(jetInfo.pt>700)  thisPtEff = thisThreshold.m_ptEff->Eval(600);
    else                thisPtEff = thisThreshold.m_ptEff->Eval(jetInfo.pt);
  }
    
  //
  // Simlate pt inefficiency
  //
  if(jetInfo.pt_weight > thisPtEff) {
    // Fails pt requirement
    return;
  }


  if(m_doTag){

    //thisTagEff = tagEff->Eval(pt)*scaleFactor;
    float eff    = -99;
    float sf     = -99;
    float effErr = -99;
    
    if(jetInfo.pt > 700){
      eff        = m_eff_tag->Eval(600);
      sf         = m_sf_tag ? m_sf_tag->Eval(600) : 1.0;
      eff        *= sf;
      effErr     = m_effErr.back();
    } else {
      eff        = m_eff_tag->Eval(jetInfo.pt);
      sf         = m_sf_tag ? m_sf_tag->Eval(jetInfo.pt) : 1.0;
      eff        *= sf;
    }
    
    for(unsigned int iBin = 0; iBin< m_highBinEdge.size(); ++iBin){
      if(jetInfo.pt < m_highBinEdge.at(iBin)){
        effErr = m_effErr.at(iBin);
        break;
      }
    }
    if(effErr < 0) {
      effErr = m_effErr.back();
    }
    assert((effErr > 0) && "ERROR effErr < 0");


    float thisTagEff = eff + effErr*smearFactor;

    if(jetInfo.tag_weight < thisTagEff){
      ++thisThreshold.m_n;
    }

  }else{
    //
    // only check threshold
    //
    ++thisThreshold.m_n;
  }

  if(debug) cout << "Leftcount" << endl;
  return;
}

void TriggerTagger::SetDecisions(const vector<XhhResolved::jetTrigInfo>& jetInfos, float bjetSmearFactor, bool debug){

  //
  // clear previous decision
  //
  clearCounters();

  for(const XhhResolved::jetTrigInfo& thisJet: jetInfos){
    count (  m_j35 , thisJet, bjetSmearFactor, debug);
    //count (  m_j45 , thisJet, bjetSmearFactor, debug);
    //count (  m_j50 , thisJet, bjetSmearFactor, debug);
    count (  m_j55 , thisJet, bjetSmearFactor, debug);
    //count (  m_j60 , thisJet, bjetSmearFactor, debug);
    //count (  m_j65 , thisJet, bjetSmearFactor, debug);
    //count (  m_j70 , thisJet, bjetSmearFactor, debug);
    //count (  m_j75 , thisJet, bjetSmearFactor, debug);
    count (  m_j100, thisJet, bjetSmearFactor, debug);
    //count (  m_j150, thisJet, bjetSmearFactor, debug);
    //count (  m_j175, thisJet, bjetSmearFactor, debug);
    count (  m_j225, thisJet, bjetSmearFactor, debug);
    //count (  m_j275, thisJet, bjetSmearFactor, debug);
    //count (  m_j300, thisJet, bjetSmearFactor, debug);
    //count (  m_j360, thisJet, bjetSmearFactor, debug);
  }
  
  return;
}

void TriggerTagger::clearCounters()
{
  m_j35  .m_n = 0;
  m_j45  .m_n = 0;
  m_j50  .m_n = 0;
  m_j55  .m_n = 0;
  m_j60  .m_n = 0;
  m_j65  .m_n = 0;
  m_j70  .m_n = 0;
  m_j75  .m_n = 0;
  m_j100 .m_n = 0;
  m_j150 .m_n = 0;
  m_j175 .m_n = 0;
  m_j225 .m_n = 0;
  m_j275 .m_n = 0;
  m_j300 .m_n = 0;
  m_j360 .m_n = 0;

}
