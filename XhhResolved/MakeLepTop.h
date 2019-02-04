#ifndef MakeLepTop_MakeLepTop_H
#define MakeLepTop_MakeLepTop_H

#include <EventLoop/Algorithm.h>
#include "xAODRootAccess/Init.h"
#include "xAODRootAccess/TEvent.h"
#include "xAODRootAccess/TStore.h"

// used to make histograms
#include <TH1.h>

class MakeLepTop : public EL::Algorithm
{

  // variables that don't get filled at submission time should be
  // protected from being send from the submission node to the worker
  // node (done by the //!)
 public:

  std::string m_name;

  xAOD::TEvent *m_event; //!
  xAOD::TStore *m_store; //!
  bool        m_debug; 
  float       m_lepTopPtCut; 
  float       m_muonJetDrCut; 
  std::string m_outLepTopName; 
  std::string m_inJetName; 
  std::string m_inMuonName; 
  std::string m_inMetName; 
  std::string m_MetType; 
  std::string m_inputAlgo;
  std::string m_outputAlgo;

 private:

  //
  //  No //! for these guys as they are configuration
  //
  
  EL::StatusCode makeLepTops (std::string jetSystName, std::string muonSystName="");
  
  EL::StatusCode selected    (std::string jetSystName, std::string muonSystName);
  EL::StatusCode selectUnique(std::string jetSystName, std::string muonSystName);

 public:

  // this is a standard constructor
  MakeLepTop ();

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

  // these are the functions not inherited from Algorithm
  virtual EL::StatusCode configure ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(MakeLepTop, 1);
};

#endif
