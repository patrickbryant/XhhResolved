#ifndef XhhResolved_hh4bEventBuilder_H
#define XhhResolved_hh4bEventBuilder_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
#include <EventLoop/Worker.h>
#include "TRandom3.h"

// rootcore includes
#include "GoodRunsLists/GoodRunsListSelectionTool.h"

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"


// our histogramming code
#include <XhhResolved/hh4bEvent.h>


#include <XhhResolved/CutflowHists.h>



class hh4bEventBuilder : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  
  //configuration variables
  bool m_mc;
  bool m_doMCNorm;
  std::string m_tagger;
  float m_MV2CutValue;
  float m_MV2CutValueTightQCD;
  float m_minJetPtCut;

  std::string m_eventDetailStr;
  std::string m_triggerDetailStr;
  std::string m_truthDetailStr;
  std::string m_jetDetailStr;
  std::string m_muonDetailStr;
  std::string m_elecDetailStr;
  std::string m_metDetailStr;
  
  float m_lumi;                   // Lumi we are scaling to
  float m_mcEventWeight;

  float m_nevents;           
  bool m_useWeighted;
  bool m_useMhhWeight;
  std::string m_hhReweightFile;
  bool m_doPUReweight;
  bool m_doCleaning;

  // GRL
  bool m_applyGRL;
  std::string m_GRLxml;

  bool m_promoteMuons;

private:

  GoodRunsListSelectionTool*   m_grl          = nullptr;       //!

  // Cutflow
  CutflowHists *m_cutflow; //!
  int m_cf_init;
  int m_cf_grl;
  int m_cf_trigger;
  int m_cf_less4Jets;
  int m_cf_less2BJets;
  int m_cf_jetcleaning;

  float m_nJetsAbove3;
  float m_nBJetsAll;
  float m_nBJetsAbove3;
  float m_nBJetsEqual4;

  // Event data
  hh4bEvent* m_eventData; //!

  TH1F* h_metaDataOutput;
  TTree* m_skim; //!

  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
public:

  // this is a standard constructor
  hh4bEventBuilder ();

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

  // this is needed to distribute the algorithm to the workers
  ClassDef(hh4bEventBuilder, 1);

};

#endif
