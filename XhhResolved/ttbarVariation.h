#ifndef XhhResolved_ttbarVariation_H
#define XhhResolved_ttbarVariation_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
#include <EventLoop/Worker.h>

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

// our histogramming code
#include <XhhResolved/hh4bEvent.h>

//#include <XhhResolved/CutflowHists.h>
#include <XhhResolved/hh4bMassRegionHists.h>

// ROOT include(s):
#include "TF1.h"
#include "TSpline.h"

#include <sstream>
#include <vector>

using namespace std;

class ttbarVariation : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  
  //configuration variables
  bool m_debug;

  // switches
  bool m_doKinematicWeights;
  string m_combName;
  string m_weightsFile;
  string m_variation;
  bool m_doM4j;
  bool m_doXwt;


private:

  TF1*      m_function;

protected:

  // Event data
  hh4bEvent *m_event; //!

public:

  // this is a standard constructor
  ttbarVariation ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode histFinalize ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(ttbarVariation, 1);

  void setKinematicWeights(float value, EventView* thisView);
  void storeKinematicWeights(std::string file);
};

#endif
