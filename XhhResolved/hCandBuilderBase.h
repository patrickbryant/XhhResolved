#ifndef XhhResolved_hCandBuilderBase_H
#define XhhResolved_hCandBuilderBase_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
#include <EventLoop/Worker.h>
#include "TRandom3.h"

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

// our histogramming code
#include <XhhResolved/hh4bEvent.h>
#include <XhhResolved/TriggerEmulation.h>

#include <XhhResolved/CutflowHists.h>

#include "TRandom3.h"

class hCandBuilderBase : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  
  //configuration variables
  bool m_debug;
  bool m_mc;
  bool m_doTrigEmulation;
  bool m_useTrigSF;
  bool m_promoteMuons;
  std::string m_year;
  std::string m_tagger;
  std::string m_combName;
  std::string m_nonTaggedName;
  unsigned int m_minTagJets;
  unsigned int m_maxTagJets;
  unsigned int m_minTotalJets;


  float m_leadMass_SR;
  float m_sublMass_SR;
  float m_radius_SR;
  float m_radius_CR;
  float m_radius_SB;
  float m_CR_shift;
  float m_SB_shift;

private:

  bool m_do2015;

 protected:

  // Cutflow
  CutflowHists *m_cutflow; //!
  int m_cf_comb  ;
  int m_cf_drjj  ;
  int m_cf_dphi  ;
  int m_cf_passMinNTagJets;
  int m_cf_passMaxNTagJets;
  int m_cf_passMinNTotalJet;

  bool m_pass_drjj;
  bool m_pass_dphi;

  TriggerEmulation* m_trigEmulation; //!

  // 
  // Local handles to event data info
  //
  EventCombVec*     m_combList;

  // Event data
  hh4bEvent* m_eventData; //!

  void addEvent (const std::vector<const xAH::Jet*>& HCJets, const std::vector<const xAH::Jet*>& nonHCJets, TRandom3* rand);

  const std::vector<const xAH::Jet*> overlapRemove(const std::vector<const xAH::Jet*>& HCJets, const std::vector<const xAH::Jet*>& allJets);

public:


  // this is a standard constructor
  hCandBuilderBase ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);
  virtual EL::StatusCode fileExecute ();
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode postExecute ();
  virtual EL::StatusCode finalize ();
  virtual EL::StatusCode histFinalize ();

  virtual EL::StatusCode buildHCands () = 0;

  // this is needed to distribute the algorithm to the workers
  ClassDef(hCandBuilderBase, 1);

};

#endif
