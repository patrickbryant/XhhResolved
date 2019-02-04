#ifndef XhhResolved_TriggerEmulation_H
#define XhhResolved_TriggerEmulation_H

// our histogramming code
#include <XhhResolved/hh4bEvent.h>
#include <XhhResolved/TriggerTagger.h>

#include "TRandom3.h"

#include <sstream>
#include <vector>


class TriggerEmulation
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
   
  //configuration variables
  bool m_debug;
  bool m_do2015;
  bool m_doData;
  bool m_doDetailed;

  TFile* m_trigTurnOnFile_pt;
  TFile* m_trigTurnOnFile;
  TFile* m_trigTurnOnFile_Signal;
  TFile* m_trigTurnOnFile2015;
  TFile* m_trigTurnOnFile2015_MC;
  TFile* m_trigTurnOnFile2015_SF;
  TFile* m_trigTurnOnFile2015_Signal;

public:

  // this is a standard constructor
  TriggerEmulation (bool do2015, bool debug = false, bool doData = true, bool doDetailed = false);
  ~TriggerEmulation();

  void emulateTrigger2015(const hh4bEvent* event, float seedOffset = 1.0, float smearFactor = 1.0);
  void emulateTriggerSF2015(const hh4bEvent* event, float& trigSF, float& trigSFError);

  void emulateTrigger2016  (const hh4bEvent* event, float seedOffset = 1.0, float smearFactor = 1.0);
  void emulateTriggerSF2016(const hh4bEvent* event, float& trigSF, float& trigSFError);
  void apply2016PVEff      (const hh4bEvent* event, float& trigSF, float& trigSFError);

  // 2015 
  bool m_pass_HLT_2j35_btight_2j35_L14J15_0ETA25         ;
  bool m_pass_HLT_2j35_bperf_2j35_L14J15_0ETA25         ;
  bool m_pass_HLT_j70_bmedium_3j70_L14J15_0ETA25	 ;
  bool m_pass_HLT_j70_bperf_3j70_L14J15_0ETA25	 ;
  bool m_pass_HLT_j225_bloose                   	 ;
  bool m_pass_HLT_j225_bperf                   	 ;
  bool m_pass_HLT_j100_2j55_bmedium             	 ;
  bool m_pass_HLT_j100_2j55_bperf             	 ;
  bool m_pass_HLT_2j45_bmedium_split_2j45_L14J15_0ETA25 ;
  bool m_pass_HLT_j175_bmedium_split_j60_bmedium_split  ;
  bool m_pass_HLT_2j55_bmedium_split_2j55_L13J25_0ETA23 ;
  bool m_pass_HLT_2j35_btight_split_2j35_L14J15_0ETA25  ;
  bool m_pass_HLT_2j45_btight_split_2j45_L13J25_0ETA23  ;
  bool m_pass_HLT_j225_bloose_split                     ;
  bool m_pass_HLT_j300_bloose_split                     ;
  bool m_pass_HLT_hh4b2015_OR                     ;
  

  // 2016
  bool m_pass_HLT_j225_bmv2c2060_split          	 ;
  bool m_pass_HLT_j100_2j55_bmv2c2060_split              ; 
  bool m_pass_HLT_2j35_bmv2c2060_split_2j35_L14J15_0ETA25; 
  bool m_pass_HLT_j175_bmv2c2077_split; 
  bool m_pass_HLT_j175_bmv2c2085_split; 
  bool m_pass_HLT_j75_bmv2c2070_split_3j75_L14J15_0ETA25;
  bool m_pass_HLT_j75_boffperf_split_3j75_L14J15_0ETA25;
  bool m_pass_HLT_j65_bperf_split_3j65_L14J15_0ETA25    ;
  bool m_pass_HLT_j65_bmv2c2070_split_3j65_L13J25_0ETA23;
  bool m_pass_HLT_j70_bmv2c2070_split_3j70_L13J25_0ETA23;
  bool m_pass_HLT_j70_bmv2c2077_split_3j70_L14J15_0ETA25;
  bool m_pass_HLT_j75_bmv2c2077_split_3j75_L13J25_0ETA23;
  bool m_pass_HLT_2j65_bmv2c2070_split_j65;
  bool m_pass_HLT_2j70_bmv2c2077_split_j70;
  bool m_pass_HLT_2j70_bmv2c2070_split_j70;
  bool m_pass_HLT_2j75_bmv2c2077_split_j75;
  bool m_pass_HLT_2j35_bmv2c2070_split_2j35_L14J15_0ETA25;
  bool m_pass_HLT_2j45_bmv2c2070_split_2j45_L13J25_0ETA23;
  bool m_pass_HLT_2j45_bmv2c2077_split_2j45_L14J15_0ETA25;
  bool m_pass_HLT_2j55_bmv2c2077_split_2j55_L13J25_0ETA23;
  bool m_pass_HLT_hh4b_OR                     ;

 private:

  void fillWeights    (const hh4bEvent* event, float seedOffset);
  void clearDecisions ();  

  TRandom3* m_randGen;

  TriggerTagger* m_notTagged; //!
  TriggerTagger* m_offBTag;   //!
  TriggerTagger* m_allJets;   //!
  TriggerTagger* m_allJets_eta25;   //!
  
  // 2015
  TriggerTagger* m_looseTags;  //!
  TriggerTagger* m_mediumTags; //!
  TriggerTagger* m_tightTags;  //!

  // 2016
  TriggerTagger* m_hlt40Tags;  //!
  TriggerTagger* m_hlt50Tags;  //!
  TriggerTagger* m_hlt60Tags;  //!
  TriggerTagger* m_hlt70Tags;  //!
  TriggerTagger* m_hlt77Tags;  //!
  TriggerTagger* m_hlt85Tags;  //!

  // Event-level correction
  TGraphAsymmErrors* m_eventLevelCorrection = nullptr;
  std::vector<float> m_highBinEdge;
  std::vector<float> m_eff        ;
  std::vector<float> m_effErr     ;

  std::vector<XhhResolved::jetTrigInfo> m_tag_jet;
  std::vector<XhhResolved::jetTrigInfo> m_all_jet;
  std::vector<XhhResolved::jetTrigInfo> m_all_eta25_jet;
  std::vector<XhhResolved::jetTrigInfo> m_nontag_jet;


};

#endif
