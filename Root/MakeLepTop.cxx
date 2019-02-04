#include <EventLoop/Job.h>
#include <EventLoop/StatusCode.h>
#include <EventLoop/Worker.h>
#include <XhhResolved/MakeLepTop.h>

// EDM includes:
#include "AthContainers/ConstDataVector.h"
#include "xAODEventInfo/EventInfo.h"
#include "xAODAnaHelpers/HelperFunctions.h"

// Jet xAOD EDM container
#include "xAODJet/JetContainer.h"
#include "xAODJet/JetAuxContainer.h"
#include "xAODMuon/MuonContainer.h"
#include "xAODMissingET/MissingETContainer.h"

// Particle 
#include "xAODParticleEvent/Particle.h"
#include "xAODParticleEvent/ParticleContainer.h"
#include "xAODParticleEvent/ParticleAuxContainer.h"

#include <TSystem.h> // used to define JERTool calibration path
#include "TEnv.h"

// this is needed to distribute the algorithm to the workers
ClassImp(MakeLepTop)

using std::cout;   using std::endl;
using std::string; using std::vector;

struct LepTop_ptSort
{
  bool operator()(const xAOD::Particle*  a, const xAOD::Particle* b) const
  {
    return a->pt() > b->pt();
  }
};


MakeLepTop :: MakeLepTop ():
  Algorithm(),
  m_name(""),
  m_debug(false),
  m_lepTopPtCut(120e3),
  m_muonJetDrCut(1.5),
  m_outLepTopName(""),
  m_inJetName(""),
  m_inMuonName(""),
  m_inMetName(""),
  m_MetType("FinalTrk"),
  m_inputAlgo(""),
  m_outputAlgo("")
{
}


EL::StatusCode MakeLepTop :: setupJob (EL::Job& job)
{  
  job.useXAOD();

  xAOD::Init("MakeLepTop").ignore(); // call before opening first file

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode MakeLepTop :: histInitialize ()
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode MakeLepTop :: fileExecute ()
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode MakeLepTop :: changeInput (bool /*firstFile*/)
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode MakeLepTop :: configure ()
{
  return EL::StatusCode::SUCCESS;
}


EL::StatusCode MakeLepTop :: initialize ()
{
  if ( this->configure() == EL::StatusCode::FAILURE ) {
    Error("initialize()", "Failed to properly configure. Exiting." );
    return EL::StatusCode::FAILURE;
  }

  m_event = wk()->xaodEvent();
  m_store = wk()->xaodStore();

  if ( m_outputAlgo.empty() ) {
    m_outputAlgo = m_inputAlgo + "_FindTop4WithBJetPrecedence";
  }

  cout << endl;
  cout << "MakeLepTops: "  << endl; 
  cout << "\tcreating: "  << m_outLepTopName << " <--  "<< m_inJetName << " " << m_inMuonName << endl;
  cout << "\t  ptcut:  "  << m_lepTopPtCut <<endl;
  cout << "\t  dR-cut: "  << m_muonJetDrCut <<endl;
  cout << endl;

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode MakeLepTop :: execute ()
{
  if(m_debug) cout << "In MakeLepTop" << endl;

  //
  // No systematics
  //
  if ( m_inputAlgo.empty() ) {

    makeLepTops("");

  //
  // Do Systemaitcs
  //
  }else{
    
    // get vector of string giving the names
    vector<string>* systNames(nullptr);
    ANA_CHECK( HelperFunctions::retrieve(systNames, m_inputAlgo, 0, m_store, msg()) );

    // loop over systematics
    vector< string >* vecOutContainerNames = new vector< string >;
    for ( string& systName : *systNames ) {
      
      if(m_debug) Info("execute",  "systName %s", systName.c_str());
      
      makeLepTops(systName);
      
      vecOutContainerNames->push_back( systName );
    }

    // save list of systs that should be considered down stream
    ANA_CHECK( m_store->record( vecOutContainerNames, m_outputAlgo) );
  }


  return EL::StatusCode::SUCCESS;
}

EL::StatusCode MakeLepTop :: postExecute ()
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode MakeLepTop :: finalize ()
{
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode MakeLepTop :: histFinalize ()
{
  return EL::StatusCode::SUCCESS;
}


EL::StatusCode MakeLepTop::makeLepTops(string jetSystName, string muonSystName){

  // Make all lepTops
  selected(jetSystName,    muonSystName);
  
  // Unique
  selectUnique(jetSystName, muonSystName);

  return EL::StatusCode::SUCCESS;
}


//
//  Select lepTops function
//
EL::StatusCode MakeLepTop::selected(string jetSystName, string muonSystName)
{
  if(m_debug) cout << "In selected" << endl;

  string systName = "";
  if(!jetSystName.empty())  systName = jetSystName;
  if(!muonSystName.empty()) systName = muonSystName;


  //
  // Create the new container and its auxiliary store.
  //
  xAOD::ParticleContainer*     lepTopsAll    = new xAOD::ParticleContainer();
  xAOD::ParticleAuxContainer*  lepTopsAllAux = new xAOD::ParticleAuxContainer();
  lepTopsAll->setStore( lepTopsAllAux ); //< Connect the two

  //
  //  get the Input containers
  //
  if(m_debug) cout << "Getting Jets: " << m_inJetName+jetSystName << endl;
  const xAOD::JetContainer* jets(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(jets,  m_inJetName+jetSystName,   m_event, m_store, msg()) );

  if(m_debug) cout << "Getting Muons" << m_inMuonName+muonSystName << endl;
  const xAOD::MuonContainer* muons(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(muons, m_inMuonName+muonSystName, m_event, m_store, msg()) );

  if(m_debug) cout << "Getting Met" << m_inMetName << endl;
  const xAOD::MissingETContainer* metcontainer(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(metcontainer, m_inMetName, m_event, m_store, msg()) );

  const xAOD::MissingET* met = *metcontainer->find(m_MetType); 

  //
  // Loop on input muons
  //
  unsigned int nMuon = muons->size();
  unsigned int nJets = jets->size();
  if(m_debug) cout << "Looping nMuons: " << nMuon << " nJets: " << nJets << endl;

  for(unsigned int iMu = 0; iMu < nMuon; ++iMu){
    const xAOD::Muon& thisMuon = *muons->at(iMu);

    //  Only allow input muon to belong to one lepTop
    xAOD::Particle* thisLepTop = 0;

    for(unsigned int iJet = 0; iJet < nJets; ++iJet){
    
      const xAOD::Jet& thisJet = *jets->at(iJet);
      
      //
      // Build the Lep-Top Candidate
      //
      float dRmj = thisMuon.p4().DeltaR(thisJet.p4());

      //
      // dR muon -jet cut
      //
      if ( dRmj > m_muonJetDrCut) continue;
      if(m_debug) cout << " Pass dRmj " << endl;
      
      //
      // PT-LepTop cut
      //
      // Need to get meT calculation
      float metx     = met->mpx();
      float mety     = met->mpy();
      float pXLepTop = thisJet.p4().Px() + metx + thisMuon.p4().Px();
      float pYLepTop = thisJet.p4().Py() + mety + thisMuon.p4().Py();
      float pTLepTop = sqrt(pXLepTop*pXLepTop+ pYLepTop*pYLepTop);
      if( pTLepTop < m_lepTopPtCut) continue;
      if(m_debug) cout << " Pass ptLepTop " << endl;

      // 
      // We create a lepTop if:
      //   a) there is none built yet, 
      //   or
      //   b) the drmj of this one is smaller than before
      //
      bool buildNewLepTop = (!thisLepTop || dRmj < thisLepTop->auxdata<float>("dRmj"));

      //
      // if not building a lepTop continue
      //
      if(!buildNewLepTop) continue;

      if(m_debug) cout << " Building LepTop " << endl;
      
      //
      //  If were replacing one, clean up the old one.
      //
      if(thisLepTop) delete thisLepTop;

      thisLepTop = new xAOD::Particle();
      thisLepTop->makePrivateStore();
      float pZLepTop = thisJet.p4().Pz() + thisMuon.p4().Pz(); // Solve for pZ using mW constaint ?
      float mTop = 175.*1000;
      float eLepTop = sqrt(pXLepTop*pXLepTop + pYLepTop*pYLepTop + pZLepTop*pZLepTop + mTop*mTop );

      if(m_debug) cout << " Set PxPyPzE: " << pXLepTop << " " << pYLepTop  << " " << pZLepTop << " " << eLepTop << endl;
      thisLepTop->setPxPyPzE(pXLepTop,pYLepTop,pZLepTop,eLepTop);

      //
      // Set LepTop Vars
      //
      if(m_debug) cout << " Setting Vars " << endl;
      thisLepTop->auxdecor<float>("dRmj") = dRmj;

      float metet  = met->met();
      float metPhi = met->phi();
      float muonPhi = thisMuon.p4().Phi();
      float DPhi = (metPhi - muonPhi);
      if(DPhi > 3.14) 	DPhi -= 2*3.14;
      if(DPhi < -3.14)  DPhi += 2*3.14;
      thisLepTop->auxdecor<float>("dPhiMuonMet") = DPhi;
      
      float mt2 = 2*thisMuon.p4().Pt()*metet*(1-cos(DPhi));
      thisLepTop->auxdecor<float>("Mt") = sqrt(mt2);
      thisLepTop->auxdecor<float>("Met") = metet;
      thisLepTop->auxdecor<float>("MetPhi") = metPhi;

      thisLepTop->auxdecor< const xAOD::Jet*  >("Jet")  = (&thisJet);      
      thisLepTop->auxdecor< const xAOD::Muon* >("Muon") = (&thisMuon);      
      
    }//iJet2
    
    // If we sucsessfully built a lep-top, add it.
    if(thisLepTop){
      if(m_debug) cout << " Add output Leptop " << endl;
      lepTopsAll->push_back( thisLepTop );
    }

  }//iMuon 

  if(m_debug) cout << "Recording " << m_outLepTopName+systName+"All   " << lepTopsAll->size() << endl;
  ANA_CHECK( m_store->record( lepTopsAll,    m_outLepTopName+systName+"All")     );
  ANA_CHECK( m_store->record( lepTopsAllAux, m_outLepTopName+systName+"AllAux.") );

  return EL::StatusCode::SUCCESS;
}

//select unique lepTops (don't share jets)
EL::StatusCode MakeLepTop::selectUnique(string jetSystName, string muonSystName)
{
  if(m_debug) cout << "In selectUnique" << endl;

  string systName = "";
  if(!jetSystName.empty())  systName = jetSystName;
  if(!muonSystName.empty()) systName = muonSystName;

  //
  // Create the new container and its auxiliary store.
  //
  xAOD::ParticleContainer*     lepTops    = new xAOD::ParticleContainer();
  xAOD::ParticleAuxContainer*  lepTopsAux = new xAOD::ParticleAuxContainer();
  lepTops->setStore( lepTopsAux ); //< Connect the two

  if(m_debug) cout << "Getting " << m_outLepTopName+systName+"All" << endl;
  const xAOD::ParticleContainer* lepTopsAll(nullptr);
  ANA_CHECK( HelperFunctions::retrieve(lepTopsAll, m_outLepTopName+systName+"All", m_event, m_store, msg()) );

  unsigned int nLepTopIn = lepTopsAll->size();
  if(m_debug) cout << "Looping nLepTopIn: " << nLepTopIn << endl;
  for(unsigned int lepTopItA = 0; lepTopItA < nLepTopIn; ++lepTopItA){
    const xAOD::Particle& lepTopA = *lepTopsAll->at(lepTopItA);
    bool lepTopAIsUnique = true;
    
    for(unsigned int lepTopItB = 0; lepTopItB < nLepTopIn; ++lepTopItB){
      const xAOD::Particle& lepTopB = *lepTopsAll->at(lepTopItB);
      if(lepTopItA == lepTopItB) continue; //lepTopA is lepTopB

      // the Muons are unique by construction
      const xAOD::Jet* jetA = lepTopA.auxdata< const xAOD::Jet* >("Jet");
      const xAOD::Jet* jetB = lepTopB.auxdata< const xAOD::Jet* >("Jet");

      if(jetB == jetA){
	//lepTopA and lepTopB share a jet, only use the one with the higher mass
	if(lepTopA.p4().M() < lepTopB.p4().M()) lepTopAIsUnique = false;
      }

    }// Over B

    if(lepTopAIsUnique){
      xAOD::Particle* newlepTop = new xAOD::Particle();
      newlepTop->makePrivateStore( lepTopA );
      lepTops->push_back( newlepTop );
    }
  } // Over A

  std::sort(lepTops->begin(), lepTops->end(), LepTop_ptSort());

  if(m_debug) cout << "Recording " << m_outLepTopName+systName << endl;
  ANA_CHECK( m_store->record( lepTops,    m_outLepTopName+systName)       );
  ANA_CHECK( m_store->record( lepTopsAux, m_outLepTopName+systName+"Aux."));
  
  return EL::StatusCode::SUCCESS;
}
