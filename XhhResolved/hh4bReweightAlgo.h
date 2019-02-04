#ifndef XhhResolved_hh4bReweightAlgo_H
#define XhhResolved_hh4bReweightAlgo_H

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

class hh4bReweightAlgo : public xAH::Algorithm
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
  string m_stringOfVariables;
  vector<string>* m_variables;
  float m_MV2CutValue;


private:

  //map<string,vector<TH1F*>*>*     m_hists;
  //map<string,vector<TF1*>*>*      m_functions;
  map<string,vector<TSpline3*>*>* m_splines;

protected:

  // Event data
  hh4bEvent *m_event; //!

public:

  // this is a standard constructor
  hh4bReweightAlgo ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode histFinalize ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(hh4bReweightAlgo, 1);

  void setKinematicWeights(std::string variable, float value, EventView* thisView);
  //void setKinematicWeights(const EventComb* thisComb, EventView* thisView);
  void storeKinematicWeights(std::string file);
};

#endif
