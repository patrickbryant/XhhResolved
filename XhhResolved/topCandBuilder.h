#ifndef XhhResolved_topCandBuilder_H
#define XhhResolved_topCandBuilder_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
#include <EventLoop/Worker.h>
#include "TRandom3.h"

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

#include <XhhResolved/hh4bEvent.h>
#include <XhhResolved/topCand.h>


#include <XhhResolved/CutflowHists.h>


class topCandBuilder : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  
  std::string m_combName;

private:


  // Event data
  hh4bEvent* m_eventData; //!

  std::vector<std::vector<topCand> > makeAllTopCands(const std::vector<const xAH::Jet*>& inJets_tag,
						     const std::vector<const xAH::Jet*>& inJets_non);
  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
public:
  // Tree *myTree; //!
  // TH1 *myHist; //!

  // this is a standard constructor
  topCandBuilder ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode setupJob (EL::Job& job);
  virtual EL::StatusCode fileExecute ();
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode postExecute ();
  virtual EL::StatusCode finalize ();
  virtual EL::StatusCode histFinalize ();


  // this is needed to distribute the algorithm to the workers
  ClassDef(topCandBuilder, 1);
};

#endif
