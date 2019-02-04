#ifndef XhhResolved_hh4bEventBuilderAll_H
#define XhhResolved_hh4bEventBuilderAll_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
#include <EventLoop/Worker.h>

// rootcore includes
#include "GoodRunsLists/GoodRunsListSelectionTool.h"

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

// our histogramming code
#include <XhhResolved/hh4bEvent.h>

#include <XhhResolved/CutflowHists.h>

#include "TRandom3.h"

class hh4bEventBuilderAll : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  
  //configuration variables
  bool m_mc;
  bool m_doTrigEmulation;
  float m_minJetPtCut;
  std::string m_triggerDetailStr;

  std::string m_jetDetailStr;

  float m_leadMass_SR;
  float m_sublMass_SR;
  float m_radius_SR;
  float m_radius_CR;
  float m_radius_SB;
  float m_CR_shift;
  float m_SB_shift;
  
  float m_lumi;                   // Lumi we are scaling to
  float m_mcEventWeight;                   // Lumi we are scaling to

  float m_sampleEvents;      
  float m_nevents;           
  bool m_useWeighted;
  bool m_doPUReweight;
  bool m_doCleaning;

  // GRL
  bool m_applyGRL;
  std::string m_GRLxml;
  
  TRandom3* m_randGen;

private:

  GoodRunsListSelectionTool*   m_grl;       //!

  // Cutflow
  CutflowHists *m_cutflow; //!
  int m_cf_init;
  int m_cf_grl;
  int m_cf_trigger;
  int m_cf_less4Jets;
  int m_cf_less2BJets;
  int m_cf_jetcleaning;
  int m_cf_comb_4b  ;
  int m_cf_drjj_4b  ;
  int m_cf_dphi_4b  ;
  int m_cf_comb_QCD ;
  int m_cf_drjj_QCD ;
  int m_cf_dphi_QCD ;

  float m_nJetsAbove3;
  float m_nBJetsAll;
  float m_nBJetsAbove3;
  float m_nBJetsEqual4;

  // Event data
  hh4bEvent* m_eventData; //!

  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
public:
  // Tree *myTree; //!
  // TH1 *myHist; //!

  // this is a standard constructor
  hh4bEventBuilderAll ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);
  virtual EL::StatusCode fileExecute ();
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode changeInput (bool firstFile);
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode postExecute ();
  virtual EL::StatusCode finalize ();
  virtual EL::StatusCode histFinalize ();

  float getEventWeight();

  // this is needed to distribute the algorithm to the workers
  ClassDef(hh4bEventBuilderAll, 1);
};

#endif
