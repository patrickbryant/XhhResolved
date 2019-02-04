#ifndef XhhResolved_hh4bHistsAlgo_H
#define XhhResolved_hh4bHistsAlgo_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
#include <EventLoop/Worker.h>

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

// our histogramming code
#include <XhhResolved/hh4bEvent.h>

#include <XhhResolved/CutflowHists.h>
#include <XhhResolved/hh4bMassRegionHists.h>

// ROOT include(s):
#include "TH1D.h"
#include "TH2D.h"
#include "TProfile.h"
#include "TLorentzVector.h"

#include <sstream>
#include <vector>

using namespace std;

class hh4bHistsAlgo : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  
  //configuration variables
  bool m_debug;
  bool m_fast;
  bool m_mc;

  // switches
  std::string m_histDetailStr;
  std::string m_jetDetailStr;
  std::string m_combName;
  std::string m_trigRequirement;
  std::string m_signalHistExtraFlags;
  float m_scale;
  float m_maxDr;
  float m_minDr;
  float m_minMeT;
  float m_maxDphi;
  int  m_detailLevel;
  bool m_doTruthOnly;
  bool m_doBlind;   
  bool m_doTagCategories;
  bool m_doJetCategories;

  // trigger config
  //bool m_doTrigger;  
  //std::string m_trigger;

  // Kinematic selection
//  float m_reso0PtCut;
//  float m_reso0PtCutMax;
//  float m_reso1PtCut;
//  float m_YStarCut;
//  float m_YBoostCut;
//  float m_dRISRclosejCut;
//  float m_dPhiISRclosejCut;
//  float m_YStarISRjjCut;
//  float m_mjjCut;

private:

//  //
//  // Cutflow
//  int m_cf_trigger;
//  int m_cf_cleaning;
//  // ISR cuts
//  int m_cf_reso0;
//  int m_cf_reso0_max;
//  int m_cf_reso1;
//  int m_cf_ystar;
//  int m_cf_yboost;
//  int m_cf_drisrclosej;
//  int m_cf_dphiisrclosej;
//  int m_cf_ystarisrjj;
//  int m_cf_mjj;

  //
  // Triggers
  std::vector<std::string> m_triggers;

  //
  // Histograms
  hh4bMassRegionHists* hIncl; //!
  hh4bMassRegionHists* hPassHCPt; //!
  hh4bMassRegionHists* hPassHCdEta; //!
  hh4bMassRegionHists* hPassAllhadVeto; //!
  hh4bMassRegionHists* hPass_ggVeto; //!
  hh4bMassRegionHists* hExcess; //!
  hh4bMassRegionHists* hNotExcess; //!
  //hh4bMassRegionHists* hPassXtt; //!
  hh4bMassRegionHists* hPassVbbVeto; //!

protected:

  // Cutflow data
  CutflowHists *m_cutflow; //!

  // Event data
  hh4bEvent *m_event; //!

  //  selection
//  Jet m_reso0;    //!
//  Jet m_reso1;    //!
//  Particle m_isr; //!

  //
  // functions
//  void initISRCutflow();
//  bool doISRCutflow(float eventWeight) ;

public:

  // this is a standard constructor
  hh4bHistsAlgo ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode histFinalize ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(hh4bHistsAlgo, 1);
};

#endif
