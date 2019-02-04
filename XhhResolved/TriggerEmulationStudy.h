#ifndef XhhResolved_TriggerEmulationStudy_H
#define XhhResolved_TriggerEmulationStudy_H

#include <EventLoop/StatusCode.h>
#include <EventLoop/Algorithm.h>
#include <EventLoop/Worker.h>

//algorithm wrapper
#include "xAODAnaHelpers/Algorithm.h"

// our histogramming code
#include <XhhResolved/hh4bEvent.h>
#include <XhhResolved/TriggerEmulation.h>

//#include <XhhResolved/CutflowHists.h>
#include <XhhResolved/hh4bMassRegionHists.h>

// ROOT include(s):
#include "TH1D.h"
#include "TH2D.h"
#include "TProfile.h"
#include "TLorentzVector.h"

#include <sstream>
#include <vector>

#include <XhhResolved/CutflowHists.h>


using namespace std;

class TriggerEmulationStudy : public xAH::Algorithm
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  
  //configuration variables
  bool m_debug;
  bool m_printTriggers;
  bool m_printEmulatedTriggers;
  bool m_doAll;
 
  // switches
  std::string m_combName;

private:

  //
  // Cutflow
  int m_cf_all    ;
  int m_cf_view   ;
  int m_cf_HCPt   ;
  int m_cf_HCdEta ;
  int m_cf_signal ;

  std::map<std::string, int> m_trigMap;
  std::map<std::string, int> m_emulated_trigMap;
  std::map<std::string, int> m_emulated_BJetMap;

  TriggerEmulation* m_trigEmulation          = nullptr; //!
  TriggerEmulation* m_trigEmulationData      = nullptr; //!
  TriggerEmulation* m_trigEmulation_2015     = nullptr; //!
  TriggerEmulation* m_trigEmulation_2015Data = nullptr; //!

  void addTrig(std::string trigName);
  void checkTrigBits(const std::string& trigName, float eventWeight);
  void checkTrigEmulation(const std::string& trigName, bool passTrig, float eventWeight);

  struct SFCalcHists {

    std::string m_name;

  SFCalcHists(const std::string& name):
    m_name(name) {
    }

    void initialize(){
    }

    void fill(){
    }

  }; // struct

protected:

  // Cutflow data
  CutflowHists *m_cutflow; //!
  CutflowHists *m_passTrig; //!
  CutflowHists *m_passTrigEmu; //!
  CutflowHists *m_passBJetEmu; //!

  // Event data
  hh4bEvent *m_event; //!


public:

  // this is a standard constructor
  TriggerEmulationStudy ();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode histInitialize ();
  virtual EL::StatusCode initialize ();
  virtual EL::StatusCode execute ();
  virtual EL::StatusCode histFinalize ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(TriggerEmulationStudy, 1);
};

#endif
