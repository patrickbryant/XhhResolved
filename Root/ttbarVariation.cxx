#include <EventLoop/Job.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <AsgTools/MessageCheck.h>

#include <XhhResolved/ttbarVariation.h>
#include <xAODAnaHelpers/HelperFunctions.h>

#include "TFile.h"
#include "TKey.h"
#include "TLorentzVector.h"
#include "TSystem.h"

#include <utility>      
#include <iostream>
#include <fstream>

#include <string>
#include <sstream>
#include <vector>

using namespace std;

// this is needed to distribute the algorithm to the workers
ClassImp(ttbarVariation)

ttbarVariation :: ttbarVariation () :
  m_debug(false),
  m_doKinematicWeights(true),
  m_combName(""),
  m_weightsFile(""),
  m_variation("ttbar_hard"),
  m_function(nullptr),
  m_doM4j(false),
  m_doXwt(false)
{
  Info("ttbarVariation()", "Calling constructor");
}

EL::StatusCode ttbarVariation :: histInitialize ()
{
  Info("histInitialize()", "Calling histInitialize \n");

  //
  // data model
  m_event = hh4bEvent::global();

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode ttbarVariation :: initialize ()
{
  storeKinematicWeights(m_weightsFile);

  //Check what variable is being weighted
  unsigned int pos = m_variation.find("xwt");
  if(pos<m_variation.size()) m_doXwt = true;
  else m_doM4j = true;

  if(m_debug) Info("initialize()", "Calling initialize");
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode ttbarVariation :: execute ()
{
  if(m_debug) Info("execute()", "Processing Event");

  EventCombVec* eventCombs = m_event->m_eventComb->at(m_combName);

  for(const EventComb* thisComb : *eventCombs){

    EventView* thisView = thisComb->m_selectedView;

    //
    // Only correct views with a valid event view
    //
    if(!thisView) continue;

    
    if(m_doM4j) setKinematicWeights(thisView->hhp4->M(),   thisView);
    if(m_doXwt) setKinematicWeights(m_event->m_xwt,        thisView);

  }// EventComb

  return EL::StatusCode::SUCCESS;
}


void ttbarVariation::storeKinematicWeights(string file){
  string fullString = gSystem->ExpandPathName( file.c_str() );
  cout << "Weights File: " << fullString << endl;
  if (access( fullString.c_str(), F_OK ) == 0 && fullString != "") {
    cout << "Found Weights File: " << fullString << endl;

    TFile *weightsFile = new TFile(fullString.c_str(), "READ");
    m_function = (TF1*)weightsFile->Get(m_variation.c_str());

  } else {
    cout << "Not using a weights file. Will do nothing" << endl;
  }

  return;
}


void ttbarVariation::setKinematicWeights(float value, EventView* thisView){
  if (m_debug){
    cout << " In Set Kinematic Weights. " << value << endl;
  }

  if ((m_weightsFile != "") && m_doKinematicWeights){
    if (m_debug)
      cout << " Applying weight " << endl;

    float eval = 1.0;
    
    eval = m_function->Eval(value);

    if(m_debug) cout << "eval " << eval << endl;

    thisView->m_qcd_weight *= eval; //update qcd weight

  } else {
    if (m_debug ) cout << " No weights file or config file doesnt have m_doKinematicWeights = True, do not change weight " << endl;
  }

  return;
}



EL::StatusCode ttbarVariation :: histFinalize ()
{
  return EL::StatusCode::SUCCESS;
}

