#include <XhhResolved/TriggerEmulation.h>

#include "TFile.h"
#include "TSystem.h"

#include <utility>      
#include <iostream>
#include <fstream>

using namespace std;


TriggerEmulation :: TriggerEmulation (bool do2015, bool debug, bool doData, bool doDetailed) :
  m_debug(debug),
  m_do2015(do2015),
  m_doData(doData),
  m_doDetailed(doDetailed),
  m_trigTurnOnFile_pt(nullptr),
  m_trigTurnOnFile(nullptr),
  m_trigTurnOnFile_Signal(nullptr),
  m_trigTurnOnFile2015(nullptr),
  m_trigTurnOnFile2015_MC(nullptr),
  m_trigTurnOnFile2015_SF(nullptr),
  m_trigTurnOnFile2015_Signal(nullptr),
  m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25         (false),
  m_pass_HLT_2j35_bperf_2j35_L14J15_0ETA25         (false),
  m_pass_HLT_j70_bmedium_3j70_L14J15_0ETA25         (false),
  m_pass_HLT_j70_bperf_3j70_L14J15_0ETA25           (false),
  m_pass_HLT_j225_bloose                            (false),
  m_pass_HLT_j225_bperf                             (false),
  m_pass_HLT_j100_2j55_bmedium                      (false),
  m_pass_HLT_j100_2j55_bperf                        (false),
  m_pass_HLT_2j45_bmedium_split_2j45_L14J15_0ETA25 (false),
  m_pass_HLT_j175_bmedium_split_j60_bmedium_split  (false),
  m_pass_HLT_2j55_bmedium_split_2j55_L13J25_0ETA23 (false),
  m_pass_HLT_2j35_btight_split_2j35_L14J15_0ETA25  (false),
  m_pass_HLT_2j45_btight_split_2j45_L13J25_0ETA23  (false),
  m_pass_HLT_j225_bloose_split                     (false),
  m_pass_HLT_j300_bloose_split                     (false),
  m_pass_HLT_hh4b2015_OR                           (false),
  m_pass_HLT_j225_bmv2c2060_split                   (false),
  m_pass_HLT_j100_2j55_bmv2c2060_split              (false),
  m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25(false),
  m_pass_HLT_j175_bmv2c2077_split(false), 
  m_pass_HLT_j175_bmv2c2085_split(false), 
  m_pass_HLT_j75_bmv2c2070_split_3j75_L14J15_0ETA25(false), 
  m_pass_HLT_j75_boffperf_split_3j75_L14J15_0ETA25(false), 
  m_pass_HLT_j65_bperf_split_3j65_L14J15_0ETA25    (false),
  m_pass_HLT_j65_bmv2c2070_split_3j65_L13J25_0ETA23(false),
  m_pass_HLT_j70_bmv2c2070_split_3j70_L13J25_0ETA23(false),
  m_pass_HLT_j70_bmv2c2077_split_3j70_L14J15_0ETA25(false), 
  m_pass_HLT_j75_bmv2c2077_split_3j75_L13J25_0ETA23(false), 
  m_pass_HLT_2j65_bmv2c2070_split_j65(false),
  m_pass_HLT_2j70_bmv2c2077_split_j70(false),
  m_pass_HLT_2j70_bmv2c2070_split_j70(false),
  m_pass_HLT_2j75_bmv2c2077_split_j75(false),
  m_pass_HLT_2j35_bmv2c2070_split_2j35_L14J15_0ETA25(false),
  m_pass_HLT_2j45_bmv2c2070_split_2j45_L13J25_0ETA23(false),
  m_pass_HLT_2j45_bmv2c2077_split_2j45_L14J15_0ETA25(false),
  m_pass_HLT_2j55_bmv2c2077_split_2j55_L13J25_0ETA23(false),
  m_pass_HLT_hh4b_OR                           (false),
  m_randGen    (new TRandom3()),
  m_notTagged    (nullptr),
  m_offBTag      (nullptr),
  m_allJets      (nullptr),
  m_allJets_eta25(nullptr),
  m_looseTags    (nullptr),
  m_mediumTags   (nullptr),
  m_tightTags    (nullptr),
  m_hlt40Tags    (nullptr),
  m_hlt50Tags    (nullptr),
  m_hlt60Tags    (nullptr),
  m_hlt70Tags    (nullptr),
  m_hlt77Tags    (nullptr),
  m_hlt85Tags    (nullptr)

{
  m_trigTurnOnFile2015    = new TFile(gSystem->ExpandPathName("$ROOTCOREBIN/data/XhhResolved/BJetTurnOnFile_emu_ttbar_Data.root"),"READ"); 
  m_trigTurnOnFile2015_MC = new TFile(gSystem->ExpandPathName("$ROOTCOREBIN/data/XhhResolved/BJetTurnOnFile_emu_ttbar_MC.root"),"READ"); 
  m_trigTurnOnFile2015_SF = new TFile(gSystem->ExpandPathName("$ROOTCOREBIN/data/XhhResolved/2015BJetTriggerSF.root"),"READ");
  m_trigTurnOnFile2015_Signal = new TFile(gSystem->ExpandPathName("$ROOTCOREBIN/data/XhhResolved/2015SignalEff.root"),"READ"); 
  m_trigTurnOnFile_pt     = new TFile(gSystem->ExpandPathName("$ROOTCOREBIN/data/XhhResolved/BJetTurnOnFile_2016.root"),"READ"); 
  m_trigTurnOnFile        = new TFile(gSystem->ExpandPathName("$ROOTCOREBIN/data/XhhResolved/BJetTriggerEfficiencies-00-02-01_wMC.root"),"READ");
  m_trigTurnOnFile_Signal = new TFile(gSystem->ExpandPathName("$ROOTCOREBIN/data/XhhResolved/2016BJetTriggerSignalEff.root"),"READ");

  TGraphAsymmErrors* m_ptEff35   = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_35GeV_MC"));
  TGraphAsymmErrors* m_ptEff45   = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_45GeV_MC"));
  TGraphAsymmErrors* m_ptEff50   = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_50GeV_MC"));
  TGraphAsymmErrors* m_ptEff55   = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_55GeV_MC"));
  TGraphAsymmErrors* m_ptEff60   = (TGraphAsymmErrors*)(m_trigTurnOnFile2015->Get("jet_Pt_rebin_ratio_offBTag_hasJet60"));
  TGraphAsymmErrors* m_ptEff65   = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_65GeV_MC"));
  TGraphAsymmErrors* m_ptEff70   = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_70GeV_MC"));
  TGraphAsymmErrors* m_ptEff75   = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_75GeV_MC"));
  TGraphAsymmErrors* m_ptEff100  = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_100GeV_MC"));
  TGraphAsymmErrors* m_ptEff150  = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_150GeV_MC"));
  TGraphAsymmErrors* m_ptEff175  = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_175GeV_MC"));
  TGraphAsymmErrors* m_ptEff225  = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_225GeV_MC"));
  TGraphAsymmErrors* m_ptEff275  = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_275GeV_MC"));
  TGraphAsymmErrors* m_ptEff300  = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_300GeV_MC"));
  TGraphAsymmErrors* m_ptEff360  = (TGraphAsymmErrors*)(m_trigTurnOnFile_pt->Get("boffperf_split_offJets85_match_hlt_360GeV_MC"));

  m_notTagged     = new TriggerTagger("notTagged",  false,       nullptr,  nullptr,
                                      m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
                                      m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
                                      m_ptEff275,  m_ptEff300, m_ptEff360);
                  
  m_offBTag       = new TriggerTagger("offBTag",    false,  nullptr, nullptr,
                                      m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
                                      m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
                                      m_ptEff275,  m_ptEff300, m_ptEff360);
                  
  m_allJets       = new TriggerTagger("allJets",    false,  nullptr, nullptr,
                                      m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
                                      m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
                                      m_ptEff275,  m_ptEff300, m_ptEff360);

  m_allJets_eta25 = new TriggerTagger("allJets_eta25",    false,  nullptr, nullptr,
                                      m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
                                      m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
                                      m_ptEff275,  m_ptEff300, m_ptEff360);



  if(m_do2015){

    TGraphAsymmErrors* effLoose = (TGraphAsymmErrors*)(m_trigTurnOnFile2015_Signal->Get("off70_match_hltLoose_jetPt_rebin_ratio"));
    TGraphAsymmErrors* sfLoose = nullptr;
    if(m_doData) sfLoose = (TGraphAsymmErrors*)(m_trigTurnOnFile2015_SF ->Get("Pt_offBTag70_bLoose_Total_SF"));

    m_looseTags  = new TriggerTagger("loose",  true,  effLoose, sfLoose,
                                     m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
                                     m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
                                     m_ptEff275,  m_ptEff300, m_ptEff360,
                                     1.0 );

    TGraphAsymmErrors* effMedium = (TGraphAsymmErrors*)(m_trigTurnOnFile2015_Signal->Get("off70_match_hltMedium_jetPt_rebin_ratio"));
    TGraphAsymmErrors* sfMedium  = nullptr;
    if(m_doData) sfMedium = (TGraphAsymmErrors*)(m_trigTurnOnFile2015_SF   ->Get("Pt_offBTag70_bMedium_Total_SF"));

    m_mediumTags = new TriggerTagger("medium", true,  effMedium, sfMedium,
                                     m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
                                     m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
                                     m_ptEff275,  m_ptEff300, m_ptEff360,
                                     1.0 );

    TGraphAsymmErrors* effTight = (TGraphAsymmErrors*)(m_trigTurnOnFile2015_Signal->Get("off70_match_hltTight_jetPt_rebin_ratio"));
    TGraphAsymmErrors* sfTight = nullptr;
    if(m_doData) sfTight = (TGraphAsymmErrors*)(m_trigTurnOnFile2015_SF   ->Get("Pt_offBTag70_bTight_Total_SF"));
    
    m_tightTags  = new TriggerTagger("tight",  true,  effTight, sfTight,
                                     m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
                                     m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
                                     m_ptEff275,  m_ptEff300, m_ptEff360,
                                     1.0 );
  }else{

    //
    // Event-level correction
    //
    if(m_doData){
      m_eventLevelCorrection = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_Eff_Event_leadingJet_jetEta"));

      //
      // Init the Eff and Error
      //
      if(m_debug)
	cout << "Loading Efficeincies in TriggerEmulation " << endl;

      unsigned int nBins = m_eventLevelCorrection->GetN();
      for(unsigned int iBin = 0; iBin<nBins; ++iBin){
	double eff, eta;
	m_eventLevelCorrection->GetPoint(iBin, eta, eff);
	float eta_low   = m_eventLevelCorrection->GetErrorXlow(iBin);
	float eta_high  = m_eventLevelCorrection->GetErrorXhigh(iBin);
	float err_low  = m_eventLevelCorrection->GetErrorYlow(iBin);
	float err_high = m_eventLevelCorrection->GetErrorYhigh(iBin);
	float err_ave  = (err_low+err_high)/2;
	float error_total = err_ave;
	
	if(m_debug)
	  cout << "\tiBin " << iBin << " eta: " << eta-eta_low << " - " << eta << " - " << eta+eta_high
	       << " eff: " << eff << " +/- " << error_total 
	       << endl;
	m_highBinEdge.push_back(eta+eta_high);
	m_eff        .push_back(eff);
	m_effErr     .push_back(error_total);
      }

    }

    //TGraphAsymmErrors* effHLT40(nullptr);
    //if(m_doData) effHLT40 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_Eff_offJets70_match_hlt_match_hlt40_jetPt"));
    //else         effHLT40 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_EffMC_offJets70_match_hlt_match_hlt40_jetPt"));
    //
    //
    //m_hlt40Tags  = new TriggerTagger("hlt40",  true,  effHLT40, nullptr,
    //                               m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
    //                               m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
    //                               m_ptEff275,  m_ptEff300, m_ptEff360,
    //                               1.0 );
    //
    //
    //TGraphAsymmErrors* effHLT50(nullptr);
    //if(m_doData) effHLT50 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_Eff_offJets70_match_hlt_match_hlt50_jetPt"));
    //else         effHLT50 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_EffMC_offJets70_match_hlt_match_hlt50_jetPt"));
    //
    //m_hlt50Tags  = new TriggerTagger("hlt50",  true,  effHLT50, nullptr,
    //                               m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
    //                               m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
    //                               m_ptEff275,  m_ptEff300, m_ptEff360,
    //                               1.0 );
    //

    TGraphAsymmErrors* effHLT60 = (TGraphAsymmErrors*)(m_trigTurnOnFile_Signal->Get("off70_match_hlt60_jetPt_rebin_ratio"));
    TGraphAsymmErrors* sfHLT60 = nullptr;
    if(m_doData) sfHLT60 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_SF_offJets70_match_hlt_match_hlt60_jetPt"));
    
    m_hlt60Tags  = new TriggerTagger("hlt60",  true,  effHLT60, sfHLT60,
				     m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
				     m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
				     m_ptEff275,  m_ptEff300, m_ptEff360 );
				     
    
    //TGraphAsymmErrors* effHLT70(nullptr);
    //if(m_doData) effHLT70 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_Eff_offJets70_match_hlt_match_hlt70_jetPt"));
    //else         effHLT70 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_EffMC_offJets70_match_hlt_match_hlt70_jetPt"));
    //
    //m_hlt70Tags  = new TriggerTagger("hlt70",  true,  effHLT70, nullptr,
    //                                 m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
    //                                 m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
    //                                 m_ptEff275,  m_ptEff300, m_ptEff360,
    //                                 1.0 );
    //
    //TGraphAsymmErrors* effHLT77(nullptr);
    //if(m_doData) effHLT77 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_Eff_offJets70_match_hlt_match_hlt77_jetPt"));
    //else         effHLT77 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_EffMC_offJets70_match_hlt_match_hlt77_jetPt"));
    //
    //m_hlt77Tags  = new TriggerTagger("hlt77",  true,  effHLT77, nullptr,
    //                                 m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
    //                                 m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
    //                                 m_ptEff275,  m_ptEff300, m_ptEff360,
    //                                 1.0 );
    //
    //TGraphAsymmErrors* effHLT85(nullptr);
    //if(m_doData) effHLT85 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_Eff_offJets70_match_hlt_match_hlt85_jetPt"));
    //else         effHLT85 = (TGraphAsymmErrors*)(m_trigTurnOnFile->Get("g_EffMC_offJets70_match_hlt_match_hlt85_jetPt"));
    //
    //m_hlt85Tags  = new TriggerTagger("hlt85",  true,  effHLT85, nullptr,
    //                                 m_ptEff35,   m_ptEff45,  m_ptEff50,  m_ptEff55,  m_ptEff60,  m_ptEff65,
    //                                 m_ptEff70,   m_ptEff75,  m_ptEff100, m_ptEff150, m_ptEff175, m_ptEff225,
    //                                 m_ptEff275,  m_ptEff300, m_ptEff360,
    //                                 1.0 );
  }

}

TriggerEmulation :: ~TriggerEmulation () 
{ 
  m_trigTurnOnFile->Close();
  delete m_trigTurnOnFile;

  delete m_randGen;
}


void TriggerEmulation::fillWeights(const hh4bEvent* event, float seedOffset)
{
  //
  //  clear weights
  //
  m_tag_jet.clear();
  m_all_jet.clear();

  if(m_doDetailed){
    m_all_eta25_jet.clear();
  }

  m_nontag_jet.clear();

  int seed;
  for(const xAH::Jet* tagJet : *event->m_taggedJets){
    seed = (int)(tagJet->p4.Pt()*1000 * seedOffset);
    m_randGen->SetSeed(seed);
    float this_pt_weight     = m_randGen->Uniform();
    float this_pt_tag_weight = m_randGen->Uniform();
    // float this_pt_weight = 0;
    // float this_pt_tag_weight = 0;
    
    m_tag_jet.push_back(XhhResolved::jetTrigInfo());
    m_tag_jet.back().pt         = tagJet->p4.Pt();
    m_tag_jet.back().pt_weight  = this_pt_weight;
    m_tag_jet.back().tag_weight = this_pt_tag_weight;

    m_all_jet.push_back(XhhResolved::jetTrigInfo());
    m_all_jet.back().pt         = tagJet->p4.Pt();
    m_all_jet.back().pt_weight  = this_pt_weight;
    m_all_jet.back().tag_weight = -99;

    if(m_doDetailed){
      if(fabs(tagJet->p4.Eta()) < 2.5){
        m_all_eta25_jet.push_back(XhhResolved::jetTrigInfo());
        m_all_eta25_jet.back().pt             = tagJet->p4.Pt();
        m_all_eta25_jet.back().pt_weight      = this_pt_weight;
        m_all_eta25_jet.back().tag_weight     = -99;
      }
    }

  }


  for(const xAH::Jet* nonTagJet : event->m_nonTaggedJets->at("NonTagged")){
    seed = (int)(nonTagJet->p4.Pt()*1000 * seedOffset);
    m_randGen->SetSeed(seed);
    float this_pt_weight  = m_randGen->Uniform();
    //float this_pt_weight = 0;

    m_nontag_jet.push_back(XhhResolved::jetTrigInfo());
    m_nontag_jet.back().pt         = nonTagJet->p4.Pt();
    m_nontag_jet.back().pt_weight  = this_pt_weight;
    m_nontag_jet.back().tag_weight = -99;

    m_all_jet.push_back(XhhResolved::jetTrigInfo());    
    m_all_jet.back().pt         = nonTagJet->p4.Pt();
    m_all_jet.back().pt_weight  = this_pt_weight;
    m_all_jet.back().tag_weight = -99;

    if(m_doDetailed){
      if(fabs(nonTagJet->p4.Eta()) < 2.5){
        m_all_eta25_jet.push_back(XhhResolved::jetTrigInfo());
        m_all_eta25_jet.back().pt         = nonTagJet->p4.Pt();
        m_all_eta25_jet.back().pt_weight  = this_pt_weight;
        m_all_eta25_jet.back().tag_weight = -99;
      }
    }
  }

  return;
}


void TriggerEmulation::emulateTrigger2015(const hh4bEvent* event, float seedOffset, float smearFactor)
{
                                          
  if(m_debug) cout << " In emulateTrigger2015" << endl;

  clearDecisions();

  fillWeights(event, seedOffset);

  m_looseTags     ->SetDecisions(m_tag_jet,     smearFactor, m_debug);
  m_mediumTags    ->SetDecisions(m_tag_jet,     smearFactor, m_debug);
  m_tightTags     ->SetDecisions(m_tag_jet,     smearFactor, m_debug);
  m_notTagged     ->SetDecisions(m_nontag_jet,  smearFactor, m_debug);
  m_allJets       ->SetDecisions(m_all_jet,     smearFactor, m_debug);

  bool pass_L1_4J150ETA25 = event->passTrig("L1_4J15.0ETA25");
  m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25 = (pass_L1_4J150ETA25 && (m_tightTags->m_j35.m_n > 1)   && (m_allJets->m_j35.m_n > 3)  );
  m_pass_HLT_2j35_bperf_2j35_L14J15_0ETA25 = (pass_L1_4J150ETA25 && (m_allJets->m_j35.m_n > 3)  );
  //bool pass_HLT_2j45_bmedium_2j45_L13J25.0ETA23 = (m_event->passTrig("L1_3J25.0ETA23") && (m_mediumTags->n45 > 1)  && (m_allJets->n45 > 3)  );
  //m_pass_HLT_j70_bmedium_3j70_L14J15_0ETA25 = (pass_L1_4J150ETA25 && (m_mediumTags->m_j70.m_n > 0)  && (m_allJets->m_j70.m_n > 3)  );
  //m_pass_HLT_j70_bperf_3j70_L14J15_0ETA25 = (pass_L1_4J150ETA25 && (m_allJets->m_j70.m_n > 3)  );
  /* HLT.at("HLT_2j35_btight_2j35_L14J15.0ETA25")  = (L1.at("L1_4J15.0ETA25") && (m_tightTags->n35 > 1)   && (m_allJets->n35 > 3)  ); */
  /* HLT.at("HLT_2j45_bmedium_2j45_L14J15.0ETA25") = (L1.at("L1_4J15.0ETA25") && (m_mediumTags->n45 > 1)  && (m_allJets->n45 > 3)  ); */
  /* HLT.at("HLT_j70_bmedium_3j70_L14J15.0ETA25")  = (L1.at("L1_4J15.0ETA25") && (m_mediumTags->n70 > 0)  && (m_allJets->n70 > 3)  ); */
  //HLT.at("HLT_j175_bmedium_j60_bmedium")        = (L1.at("L1_J100")        && (m_mediumTags->n175 > 0) && (m_mediumTags->n60 > 1) );
  bool pass_L1_J100 = event->passTrig("L1_J100");
  m_pass_HLT_j225_bloose                     = (pass_L1_J100        && (m_looseTags->m_j225.m_n > 0) );
  m_pass_HLT_j225_bperf                     = (pass_L1_J100        && (m_allJets->m_j225.m_n > 0) );
  bool pass_L1_J75_3J20 = event->passTrig("L1_J75_3J20");
  m_pass_HLT_j100_2j55_bmedium               = (pass_L1_J75_3J20    &&  (m_allJets->m_j55.m_n > 2) &&
                                                (  (m_mediumTags->m_j55.m_n > 1)  && (m_allJets->m_j100.m_n > 0)  )
                                                );

  m_pass_HLT_hh4b2015_OR = (m_pass_HLT_j225_bloose || m_pass_HLT_j100_2j55_bmedium || m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25);

  m_pass_HLT_j100_2j55_bperf               = (pass_L1_J75_3J20    &&  (m_allJets->m_j55.m_n > 2) &&
                                              ( (m_allJets->m_j100.m_n > 0) ) 
                                              );
                                        
  //m_pass_HLT_2j45_bmedium_split_2j45_L14J15_0ETA25 = (pass_L1_4J150ETA25 && (m_mediumTags->m_j45.m_n > 1) && (m_allJets->m_j45.m_n > 3));
  //m_pass_HLT_j175_bmedium_split_j60_bmedium_split  = (pass_L1_J100 && (m_mediumTags->m_j60.m_n > 1) && (m_mediumTags->m_j175.m_n > 0));
  //m_pass_HLT_2j55_bmedium_split_2j55_L13J25_0ETA23 = (event->passTrig("L1_3J25.0ETA23") && (m_mediumTags->m_j55.m_n > 1) && (m_allJets->m_j55.m_n > 3));
  //m_pass_HLT_2j35_btight_split_2j35_L14J15_0ETA25  = (pass_L1_4J150ETA25 && (m_tightTags->m_j35.m_n > 1) && (m_allJets->m_j35.m_n > 3));
  //m_pass_HLT_2j45_btight_split_2j45_L13J25_0ETA23  = (event->passTrig("L1_3J25.0ETA23") && (m_tightTags->m_j45.m_n > 1) && (m_allJets->m_j45.m_n > 3));
  //m_pass_HLT_j225_bloose_split                     = (event->passTrig("L1_J100") && (m_looseTags->m_j225.m_n > 0));
  //m_pass_HLT_j300_bloose_split                     = (event->passTrig("L1_J100") && (m_looseTags->m_j300.m_n > 0));

  return;
}


void TriggerEmulation::emulateTriggerSF2015(const hh4bEvent* event, float& trigSF, float& trigSFError)
{
                                          
  if(m_debug) cout << " In emulateTrigger2015" << endl;

  unsigned int nToys             = 40;
  unsigned int nThrows           = 50;
  //float eventLevelUncertianty    = 0.05; 

  unsigned int nPassTotal_2j35_bt_2j35  = 0;
  unsigned int sumPassToy2_2j35_bt_2j35 = 0;

  //unsigned int nPassTotal_j70_bm_3j70  = 0;
  //unsigned int sumPassToy2_j70_bm_3j70 = 0;

  unsigned int nPassTotal_j225_bl  = 0;
  unsigned int sumPassToy2_j225_bl = 0;

  unsigned int nPassTotal_j100_2j55_bm  = 0;
  unsigned int sumPassToy2_j100_2j55_bm = 0;

  unsigned int nPassTotal_OR  = 0;
  unsigned int sumPassToy2_OR = 0;

  for(unsigned int iToy = 0; iToy < nToys; ++iToy){

    float nPassToy_2j35_bt_2j35 = 0;
    //float nPassToy_j70_bm_3j70  = 0;
    float nPassToy_j225_bl  = 0;
    float nPassToy_j100_2j55_bm  = 0;
    float nPassToy_OR  = 0;

    m_randGen->SetSeed(iToy);
    float bjetSmearFactor = m_randGen->Gaus(0,1);

    for(unsigned int iThrow = 0; iThrow < nThrows; ++iThrow){

      emulateTrigger2015(event, iThrow*iToy, bjetSmearFactor);

      if(m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25){
        ++nPassTotal_2j35_bt_2j35;
        ++nPassToy_2j35_bt_2j35;
      }
      
      //if(m_pass_HLT_j70_bmedium_3j70_L14J15_0ETA25){
      //        ++nPassTotal_j70_bm_3j70;
      //        ++nPassToy_j70_bm_3j70;
      //}

      if(m_pass_HLT_j225_bloose){
        ++nPassTotal_j225_bl;
        ++nPassToy_j225_bl;
      }


      if(m_pass_HLT_j100_2j55_bmedium){
        ++nPassTotal_j100_2j55_bm;
        ++nPassToy_j100_2j55_bm;
      }

      if(m_pass_HLT_j100_2j55_bmedium || m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25 || m_pass_HLT_j225_bloose){
        ++nPassTotal_OR;
        ++nPassToy_OR;
      }

    }// throws
    
    sumPassToy2_2j35_bt_2j35 += (nPassToy_2j35_bt_2j35 * nPassToy_2j35_bt_2j35);
    //sumPassToy2_j70_bm_3j70  += (nPassToy_j70_bm_3j70  * nPassToy_j70_bm_3j70 );
    sumPassToy2_j225_bl      += (nPassToy_j225_bl      * nPassToy_j225_bl );
    sumPassToy2_j100_2j55_bm += (nPassToy_j100_2j55_bm * nPassToy_j100_2j55_bm );
    sumPassToy2_OR           += (nPassToy_OR           * nPassToy_OR );

  }

  //float w_ave_2j35_bt_2j35 = nPassTotal_2j35_bt_2j35/(nToys*nThrows);
  //float w_var_2j35_bt_2j35 = 1./nToys * sumPassToy2_2j35_bt_2j35/(nThrows*nThrows)  - (w_ave_2j35_bt_2j35*w_ave_2j35_bt_2j35);
  //
  ////float w_ave_j70_bm_3j70  = nPassTotal_j70_bm_3j70/(nToys*nThrows);
  ////float w_var_j70_bm_3j70  = 1./nToys * sumPassToy2_j70_bm_3j70/(nThrows*nThrows)  - (w_ave_j70_bm_3j70*w_ave_j70_bm_3j70);
  //
  //float w_ave_j225_bl  = nPassTotal_j225_bl/(nToys*nThrows);
  //float w_var_j225_bl  = 1./nToys * sumPassToy2_j225_bl/(nThrows*nThrows)  - (w_ave_j225_bl*w_ave_j225_bl);
  //
  //float w_ave_j100_2j55_bm  = nPassTotal_j100_2j55_bm/(nToys*nThrows);
  //float w_var_j100_2j55_bm  = 1./nToys * sumPassToy2_j100_2j55_bm/(nThrows*nThrows)  - (w_ave_j100_2j55_bm*w_ave_j100_2j55_bm);

  float w_ave_OR  = float(nPassTotal_OR)/(nToys*nThrows);
  float w_var_OR  = 1./nToys * float(sumPassToy2_OR)/(nThrows*nThrows)  - (w_ave_OR*w_ave_OR);

  trigSF           *=  w_ave_OR;
  float newTrigSFError = sqrt(trigSFError*trigSFError + w_var_OR);
  trigSFError = newTrigSFError;

  //
  // Add a 5% in quadrature
  //
  //float e_2j35_bt_2j35 = sqrt(w_var_2j35_bt_2j35 + (eventLevelUncertianty*w_ave_2j35_bt_2j35)*(eventLevelUncertianty*w_ave_2j35_bt_2j35));
  ////float e_j70_bm_3j70  = sqrt(w_var_j70_bm_3j70  + (eventLevelUncertianty*w_ave_j70_bm_3j70 )*(eventLevelUncertianty*w_ave_j70_bm_3j70 ));
  //float e_j225_bl      = sqrt(w_var_j225_bl      + (eventLevelUncertianty*w_ave_j225_bl     )*(eventLevelUncertianty*w_ave_j225_bl     ));
  //float e_j100_2j55_bm = sqrt(w_var_j100_2j55_bm + (eventLevelUncertianty*w_ave_j100_2j55_bm)*(eventLevelUncertianty*w_ave_j100_2j55_bm));
  //
  //// Calculate the or efficeincy from the input efficeincies
  //trigSF           =  1 - ( (1-w_ave_2j35_bt_2j35) * (1-w_ave_j225_bl) * (1-w_ave_j100_2j55_bm));
  //float e_OR_t1    =  ( (1-w_ave_j225_bl)      * (1-w_ave_j100_2j55_bm) ) * e_2j35_bt_2j35;
  //float e_OR_t2    =  ( (1-w_ave_2j35_bt_2j35) * (1-w_ave_j100_2j55_bm) ) * e_j225_bl;
  //float e_OR_t3    =  ( (1-w_ave_2j35_bt_2j35) * (1-w_ave_j225_bl     ) ) * e_j100_2j55_bm;
  //trigSFError      = sqrt( e_OR_t1*e_OR_t1 + e_OR_t2*e_OR_t2 + e_OR_t3*e_OR_t3  );

  return;
}


void TriggerEmulation::emulateTrigger2016(const hh4bEvent* event, float seedOffset, float smearFactor)
{
  clearDecisions();

  fillWeights(event, seedOffset);

  //m_hlt40Tags     ->SetDecisions(m_tag_jet_pts,         m_tag_jet_tag_weights,       m_tag_jet_pt_weights,           m_debug);
  //m_hlt50Tags     ->SetDecisions(m_tag_jet_pts,         m_tag_jet_tag_weights,       m_tag_jet_pt_weights,           m_debug);
  m_hlt60Tags     ->SetDecisions(m_tag_jet,   smearFactor,    m_debug);
  //m_hlt70Tags     ->SetDecisions(m_tag_jet,      smearFactor,      m_debug);
  //m_hlt77Tags     ->SetDecisions(m_tag_jet,      smearFactor,      m_debug);
  //m_hlt85Tags     ->SetDecisions(m_tag_jet_pts,         m_tag_jet_tag_weights,       m_tag_jet_pt_weights,           m_debug);
  m_notTagged     ->SetDecisions(m_nontag_jet,     smearFactor,     m_debug);
  m_allJets       ->SetDecisions(m_all_jet,        smearFactor,    m_debug);

  // Data Emulation 2016 triggers
  //single b (good to 1.5e34)
  //HLT.at("HLT_j175_bmv2c2040_split") = (L1.at("L1_J100") && (hlt40Tags_data->n175 > 0) );
  bool pass_L1_J100 = event->passTrig("L1_J100");
  m_pass_HLT_j225_bmv2c2060_split = (pass_L1_J100 && (m_hlt60Tags->m_j225.m_n > 0) );

  bool pass_L1_J75_3J20 = event->passTrig("L1_J75_3J20");
  m_pass_HLT_j100_2j55_bmv2c2060_split              = ( pass_L1_J75_3J20   && ( m_allJets->m_j55.m_n > 2) &&
                                                        ( (m_hlt60Tags->m_j55.m_n > 1)  && (m_allJets->m_j100.m_n > 0) )
                                                          );
  m_pass_HLT_j100_2j55_bperf                        = ( pass_L1_J75_3J20   && ( m_allJets->m_j55.m_n > 2) &&
							(m_allJets->m_j100.m_n > 0)
							);

  bool pass_L1_4J15_0ETA25 = event->passTrig("L1_4J15.0ETA25");
  m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25  = (pass_L1_4J15_0ETA25 && (m_hlt60Tags->m_j35.m_n > 1) && (m_allJets->m_j35.m_n > 3)  );

  //m_pass_HLT_j75_bmv2c2070_split_3j75_L14J15_0ETA25 = (pass_L1_4J15_0ETA25 && (m_hlt70Tags->m_j75.m_n > 0) && (m_allJets->m_j75.m_n > 3));
  //m_pass_HLT_j75_boffperf_split_3j75_L14J15_0ETA25 = (pass_L1_4J15_0ETA25 &&  (m_allJets->m_j75.m_n > 3));

  m_pass_HLT_hh4b_OR = (m_pass_HLT_j225_bmv2c2060_split || m_pass_HLT_j100_2j55_bmv2c2060_split || m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25);


  //bool pass_HLT_j275_bmv2c2070_split = (event->passTrig("L1_J100") && (m_hlt70Tags->m_j275.m_n > 0) );
  //HLT.at("HLT_j300_bmv2c2077_split") = (L1.at("L1_J100") && (hlt77Tags_data->n300 > 0) );
  //HLT.at("HLT_j360_bmv2c2085_split") = (L1.at("L1_J100") && (hlt85Tags_data->n360 > 0) );
  
  //single b+X (good to 1.5e34)
  //HLT.at("HLT_j55_bmv2c2060_split_ht500_L14J15") = (L1.at("L1_4J15.0ETA25") && (hlt60Tags_data->n55 > 0) && (ht > 550) );

  //HLT.at("HLT_j75_bmv2c2077_split_3j75_L14J15")  = (L1.at("L1_4J15.0ETA25") && (hlt77Tags_data->n75 > 0) && (m_allJets->n75 > 3) );
  
  //2b+X (good to 1.5e34)
  //bool pass_HLT_2j70_bmv2c2050_split_j70                 = (event->passTrig("L1_3J25.0ETA23") && (m_hlt50Tags->m_j70.m_n > 1)  && (m_allJets->m_j70.m_n > 2) );
  //\HLT.at("HLT_2j75_bmv2c2060_split_j75")                 = (L1.at("L1_3J25.0ETA23") && (hlt60Tags_data->n75 > 1)  && (m_allJets->n75 > 2) );
  //bool pass_HLT_j150_bmv2c2060_split_j50_bmv2c2060_split = (event->passTrig("L1_J100")        && (m_hlt60Tags->m_j150.m_n > 0) && (m_hlt60Tags->m_j50.m_n > 1) );

  //HLT.at("HLT_2j55_bmv2c2060_split_ht300_L14J15")        = (L1.at("L1_4J15.0ETA25") && (hlt60Tags_data->n55 > 1) && (ht > 350) );
  //HLT.at("HLT_2j45_bmv2c2077_split_3j45_L14J15.0ETA25")  = (L1.at("L1_4J15.0ETA25") && (hlt77Tags_data->n45 > 1) && (m_allJets->n45 > 4)  );

  if(m_doDetailed){
    m_allJets_eta25 ->SetDecisions(m_all_eta25_jet, 1.0, m_debug);

    m_pass_HLT_j175_bmv2c2077_split                     = (pass_L1_J100        && (m_hlt77Tags->m_j175.m_n > 0) );
    m_pass_HLT_j175_bmv2c2085_split                     = (pass_L1_J100        && (m_hlt77Tags->m_j175.m_n > 0) );
  
    bool pass_L1_3J25_0ETA23 = event->passTrig("L1_3J25.0ETA23");
    m_pass_HLT_j65_bmv2c2070_split_3j65_L13J25_0ETA23 = (pass_L1_3J25_0ETA23 && (m_hlt70Tags->m_j65.m_n > 0) && (m_allJets->m_j65.m_n > 3));
    m_pass_HLT_j70_bmv2c2070_split_3j70_L13J25_0ETA23 = (pass_L1_3J25_0ETA23 && (m_hlt70Tags->m_j70.m_n > 0) && (m_allJets->m_j70.m_n > 3));
    m_pass_HLT_j70_bmv2c2077_split_3j70_L14J15_0ETA25 = (pass_L1_4J15_0ETA25 && (m_hlt77Tags->m_j70.m_n > 0) && (m_allJets->m_j70.m_n > 3));
    m_pass_HLT_j75_bmv2c2077_split_3j75_L13J25_0ETA23 = (pass_L1_3J25_0ETA23 && (m_hlt77Tags->m_j75.m_n > 0) && (m_allJets->m_j75.m_n > 3));
    m_pass_HLT_j65_bperf_split_3j65_L14J15_0ETA25     = (pass_L1_4J15_0ETA25 && (m_allJets_eta25->m_j65.m_n > 3));
  
    m_pass_HLT_2j65_bmv2c2070_split_j65 = (pass_L1_3J25_0ETA23 && (m_hlt70Tags->m_j65.m_n > 1) && (m_allJets->m_j65.m_n > 2));
    m_pass_HLT_2j70_bmv2c2070_split_j70 = (pass_L1_3J25_0ETA23 && (m_hlt70Tags->m_j70.m_n > 1) && (m_allJets->m_j70.m_n > 2));
    m_pass_HLT_2j70_bmv2c2077_split_j70 = (pass_L1_3J25_0ETA23 && (m_hlt77Tags->m_j70.m_n > 1) && (m_allJets->m_j70.m_n > 2));
    m_pass_HLT_2j75_bmv2c2077_split_j75 = (pass_L1_3J25_0ETA23 && (m_hlt77Tags->m_j75.m_n > 1) && (m_allJets->m_j75.m_n > 2));
  
    m_pass_HLT_2j35_bmv2c2070_split_2j35_L14J15_0ETA25 = (pass_L1_4J15_0ETA25 && (m_hlt70Tags->m_j35.m_n > 1) && (m_allJets->m_j35.m_n > 3));
    m_pass_HLT_2j45_bmv2c2070_split_2j45_L13J25_0ETA23 = (pass_L1_3J25_0ETA23 && (m_hlt70Tags->m_j45.m_n > 1) && (m_allJets->m_j45.m_n > 3));
    m_pass_HLT_2j45_bmv2c2077_split_2j45_L14J15_0ETA25 = (pass_L1_4J15_0ETA25 && (m_hlt77Tags->m_j45.m_n > 1) && (m_allJets->m_j45.m_n > 3));
    m_pass_HLT_2j55_bmv2c2077_split_2j55_L13J25_0ETA23 = (pass_L1_3J25_0ETA23 && (m_hlt77Tags->m_j55.m_n > 1) && (m_allJets->m_j55.m_n > 3));
  }
  
  return;
}


void TriggerEmulation::emulateTriggerSF2016(const hh4bEvent* event, float& trigSF, float& trigSFError)
{

  unsigned int nToys             = 40;
  unsigned int nThrows           = 50;
  //float eventLevelUncertianty    = 0.05; 

  float nPassTotal_2j35_b60_2j35  = 0;
  float sumPassToy2_2j35_b60_2j35 = 0;
  
  float nPassTotal_j225_b60  = 0;
  float sumPassToy2_j225_b60 = 0;
  
  float nPassTotal_j100_j255_b60  = 0;
  float sumPassToy2_j100_j255_b60 = 0;

  float nPassTotal_OR  = 0;
  float sumPassToy2_OR = 0;

  for(unsigned int iToy = 0; iToy < nToys; ++iToy){

    float nPassToy_2j35_b60_2j35 = 0;
    float nPassToy_j225_b60  = 0;
    float nPassToy_j100_j255_b60  = 0;
    float nPassToy_OR       = 0;

    m_randGen->SetSeed(iToy);
    float bjetSmearFactor = m_randGen->Gaus(0,1);
    
    for(unsigned int iThrow = 0; iThrow < nThrows; ++iThrow){

      emulateTrigger2016(event, iThrow*iToy, bjetSmearFactor);

      if(m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25){
        ++nPassTotal_2j35_b60_2j35;
        ++nPassToy_2j35_b60_2j35;
      }
      
      if(m_pass_HLT_j225_bmv2c2060_split){
        ++nPassTotal_j225_b60;
        ++nPassToy_j225_b60;
      }


      if(m_pass_HLT_j100_2j55_bmv2c2060_split){
        ++nPassTotal_j100_j255_b60;
        ++nPassToy_j100_j255_b60;
      }

      if(m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25 || 
         m_pass_HLT_j225_bmv2c2060_split    ||
         m_pass_HLT_j100_2j55_bmv2c2060_split){
        ++nPassTotal_OR;
        ++nPassToy_OR;
      }



    }// throws
    
    sumPassToy2_2j35_b60_2j35 += (nPassToy_2j35_b60_2j35 * nPassToy_2j35_b60_2j35);
    sumPassToy2_j225_b60      += (nPassToy_j225_b60      * nPassToy_j225_b60 );
    sumPassToy2_j100_j255_b60 += (nPassToy_j100_j255_b60 * nPassToy_j100_j255_b60 );
    sumPassToy2_OR            += (nPassToy_OR            * nPassToy_OR );
  }

  //float w_ave_2j35_b60_2j35 = nPassTotal_2j35_b60_2j35/(nToys*nThrows);
  //float w_var_2j35_b60_2j35 = 1./nToys * sumPassToy2_2j35_b60_2j35/(nThrows*nThrows)  - (w_ave_2j35_b60_2j35*w_ave_2j35_b60_2j35);
  //
  //float w_ave_j225_b60  = nPassTotal_j225_b60/(nToys*nThrows);
  //float w_var_j225_b60  = 1./nToys * sumPassToy2_j225_b60/(nThrows*nThrows)  - (w_ave_j225_b60*w_ave_j225_b60);
  //
  //float w_ave_j100_j255_b60  = nPassTotal_j100_j255_b60/(nToys*nThrows);
  //float w_var_j100_j255_b60  = 1./nToys * sumPassToy2_j100_j255_b60/(nThrows*nThrows)  - (w_ave_j100_j255_b60*w_ave_j100_j255_b60);

  //cout << "nPassTotal_OR " << nPassTotal_OR << endl;
  //cout << "sumPassToy2_OR " << sumPassToy2_OR << endl;
  float w_ave_OR  = float(nPassTotal_OR)/(nToys*nThrows);
  float w_var_OR  = 1./nToys * float(sumPassToy2_OR)/(nThrows*nThrows)  - (w_ave_OR*w_ave_OR);

  //cout << "w_ave_OR " << w_ave_OR << endl;
  trigSF           *=  w_ave_OR;
  float newTrigSFError = sqrt(trigSFError*trigSFError + w_var_OR);
  trigSFError = newTrigSFError;

  return;
}

void TriggerEmulation::apply2016PVEff(const hh4bEvent* event, float& trigSF, float& trigSFError)
{

  if(m_doData){
    // get lead jet eta
    float leadJetPt  = -99;
    float leadJetEta = -99;
    for(const xAH::Jet* tagJet : *event->m_taggedJets){
      if(tagJet->p4.Pt() > leadJetPt) {
	leadJetPt  = tagJet->p4.Pt();
	leadJetEta = tagJet->p4.Eta();
      }
    }

    // get eff and error assocated with lead jet eta
    float eventEff    = -99;
    float eventEffErr = -99;
    for(unsigned int iBin = 0; iBin< m_highBinEdge.size(); ++iBin){
      if(leadJetEta < m_highBinEdge.at(iBin)){
	eventEff    = m_eff   .at(iBin);
	eventEffErr = m_effErr.at(iBin);
	break;
      }
    }

    if(eventEff < 0) {
      eventEff    = m_eff.back();
      eventEffErr = m_effErr.back();
    }
    assert((eventEffErr > 0) && (eventEff > 0) && "ERROR effErr < 0");
    
    trigSF      *= eventEff;
    float newTrigSFError = sqrt(trigSFError*trigSFError + eventEffErr*eventEffErr);
    trigSFError = newTrigSFError;
  }// do data
  
  return;
}

void TriggerEmulation :: clearDecisions ()
{

  //
  // 2015
  //
  m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25  = false;
  m_pass_HLT_2j35_bperf_2j35_L14J15_0ETA25  = false;
  m_pass_HLT_j70_bmedium_3j70_L14J15_0ETA25  = false;
  m_pass_HLT_j70_bperf_3j70_L14J15_0ETA25  = false;
  m_pass_HLT_j225_bloose                     = false;
  m_pass_HLT_j225_bperf                     = false;
  m_pass_HLT_j100_2j55_bmedium               = false;
  m_pass_HLT_j100_2j55_bperf               = false;
  m_pass_HLT_hh4b2015_OR = false;

  m_pass_HLT_2j45_bmedium_split_2j45_L14J15_0ETA25  = false;
  m_pass_HLT_j175_bmedium_split_j60_bmedium_split   = false;
  m_pass_HLT_2j55_bmedium_split_2j55_L13J25_0ETA23  = false;
  m_pass_HLT_2j35_btight_split_2j35_L14J15_0ETA25   = false;
  m_pass_HLT_2j45_btight_split_2j45_L13J25_0ETA23   = false;
  m_pass_HLT_j225_bloose_split                      = false;
  m_pass_HLT_j300_bloose_split                      = false;


  //
  //  2016 
  //
  m_pass_HLT_j225_bmv2c2060_split                     = false;
  m_pass_HLT_j100_2j55_bmv2c2060_split                = false;
  m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25  = false;

  m_pass_HLT_j175_bmv2c2077_split = false; 
  m_pass_HLT_j175_bmv2c2085_split = false; 
  m_pass_HLT_j75_bmv2c2070_split_3j75_L14J15_0ETA25 = false; 
  m_pass_HLT_j75_boffperf_split_3j75_L14J15_0ETA25 = false; 
  m_pass_HLT_j65_bperf_split_3j65_L14J15_0ETA25     = false;
  m_pass_HLT_j65_bmv2c2070_split_3j65_L13J25_0ETA23 = false;
  m_pass_HLT_j70_bmv2c2070_split_3j70_L13J25_0ETA23 = false;
  m_pass_HLT_j70_bmv2c2077_split_3j70_L14J15_0ETA25 = false; 
  m_pass_HLT_j75_bmv2c2077_split_3j75_L13J25_0ETA23 = false; 
  m_pass_HLT_2j65_bmv2c2070_split_j65 = false;
  m_pass_HLT_2j70_bmv2c2077_split_j70 = false;
  m_pass_HLT_2j70_bmv2c2070_split_j70 = false;
  m_pass_HLT_2j75_bmv2c2077_split_j75 = false;


  m_pass_HLT_2j65_bmv2c2070_split_j65 = false;
  m_pass_HLT_2j70_bmv2c2070_split_j70 = false;
  m_pass_HLT_2j70_bmv2c2077_split_j70 = false;
  m_pass_HLT_2j75_bmv2c2077_split_j75 = false;
  m_pass_HLT_hh4b_OR = false;

}



