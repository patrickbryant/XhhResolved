//#include <EventLoop/Job.h>
//#include <EventLoop/Worker.h>
//#include <EventLoop/OutputStream.h>
//
//#include <AsgTools/MessageCheck.h>
//
//#include <XhhResolved/topCandBuilderKLFitter.h>
//
//#include <xAODAnaHelpers/HelperFunctions.h>
//#include <xAODAnaHelpers/tools/ReturnCheck.h>
//
//#include "TFile.h"
//#include "TH1D.h"
//#include "TKey.h"
//#include "TLorentzVector.h"
//#include "TSystem.h"
//
//#include <utility>      
//#include <iostream>
//#include <fstream>
//#include <assert.h>     /* assert */
//#include <math.h>
//
//
//#include "KLFitter/Fitter.h"
//#include "KLFitter/Permutations.h"
//#include "KLFitter/LikelihoodBase.h"
//#include "KLFitter/DetectorAtlas_7TeV.h"
//#include "KLFitter/LikelihoodTopAllHadronic.h"
//#include "KLFitter/PhysicsConstants.h"
//
//
//using namespace std;
//using xAH::Jet;
//
//// this is needed to distribute the algorithm to the workers
//ClassImp(topCandBuilderKLFitter)
//
//
//topCandBuilderKLFitter :: topCandBuilderKLFitter () 
//: m_combName(""),
//  m_fitter(0)
//{
//  Info("topCandBuilderKLFitter()", "Calling constructor");
//}
//
//EL::StatusCode topCandBuilderKLFitter :: setupJob (EL::Job& /*job*/)
//{
//  return EL::StatusCode::SUCCESS;
//}
//
//
//
//EL::StatusCode topCandBuilderKLFitter :: histInitialize ()
//{
//  Info("histInitialize()", "Calling histInitialize \n");
//
//  //
//  // data model
//  //
//  m_eventData=hh4bEvent::global();
//
//  return EL::StatusCode::SUCCESS;
//}
//
//
//
//EL::StatusCode topCandBuilderKLFitter :: fileExecute ()
//{
//  // Here you do everything that needs to be done exactly once for every
//  // single file, e.g. collect a list of all lumi-blocks processed
//  return EL::StatusCode::SUCCESS;
//}
//
//EL::StatusCode topCandBuilderKLFitter :: initialize ()
//{
//  Info("initialize()", "Succesfully initialized! \n");
//
//  m_fitter = new KLFitter::Fitter();
//
//  // set detector configuration (still 7 TeV setup)
//  std::string detConfig = Form("%s/data/KLFitter/transferfunctions/7TeV/ttbar/mc11c",gSystem->Getenv("ROOTCOREBIN"));
//  KLFitter::DetectorBase * myDetector = new KLFitter::DetectorAtlas_7TeV( detConfig );
//  if ( ! m_fitter->SetDetector(myDetector) ) {
//    Error("KLFitterTool::initialize()","Couldn't set detector!"); 
//    return EL::StatusCode::FAILURE;
//  }
//
//  // set likelihood
//  KLFitter::LikelihoodTopAllHadronic * myLikelihood = new KLFitter::LikelihoodTopAllHadronic();
//  myLikelihood->SetBTagging(KLFitter::LikelihoodBase::kNotag); // kNotag, kVetoFitLight, kVetoFitBoth
//  myLikelihood->PhysicsConstants()->SetMassTop(172.5);
//  myLikelihood->SetFlagTopMassFixed(false); // allow top mass to float in fit
//  myLikelihood->SetFlagIntegrate(false); // used for calculating event probability - not used here...
//  if ( ! m_fitter->SetLikelihood(myLikelihood) ) {
//    Error("KLFitterTool::initialize()","Couldn't set likelihood!"); 
//    return EL::StatusCode::FAILURE;
//  }
//
//
//
//  return EL::StatusCode::SUCCESS;
//}
//
//
//EL::StatusCode topCandBuilderKLFitter :: execute ()
//{
//  if(m_debug) Info("execute()", "Processing Event");
//
//  // check if initialize was called
//  if ( ! m_fitter ) {
//    Error("KLFitterTool::processEvent()","KLFitter is not initialized!");
//    return EL::StatusCode::FAILURE;
//  }
//  
//  float metPt  = m_eventData->m_met->m_metFinalTrk;
//  float metPhi = m_eventData->m_met->m_metFinalTrkPhi;
//  if ( ! m_fitter->SetET_miss_XY_SumET(metPt*cos(metPhi), metPt*sin(metPhi), m_eventData->m_met->m_metFinalTrkSumEt) ) {
//    Warning("KLFitterTool::processEvent()","Couldn't set met!");
//    return EL::StatusCode::SUCCESS;
//  }
//
//  vector<vector<const xAH::Jet*> > allTTbarCombs;
//  float maxLogL = -99;
//
//  EventCombVec* eventCombs = m_eventData->m_eventComb->at(m_combName);
//
//  for(EventComb* thisComb : *eventCombs){
//
//    EventView* thisView = thisComb->m_selectedView;
//
//    //
//    // Only consider combinations with a valid event view
//    //
//    if(!thisView) continue;
//
//    if(m_debug) cout << "NJets_tag (PS)  " << thisComb->m_pseudoTaggedJets.size() << " NJets_non (PS)  " << thisComb->m_pseudoNonTaggedJets.size() << endl;
//    allTTbarCombs   = makeAllTTJetCombs(*thisComb->m_HCJets, *thisComb->m_nonHCJets);
//
//    if(m_debug) cout << "NTop Cands  " << allTTbarCombs.size() << endl;
//
//
//    //cout << "NJets_tag (PS)  " << thisComb->m_pseudoTaggedJets.size() << " NJets_non (PS)  " << thisComb->m_pseudoNonTaggedJets.size() << endl;
//    //cout << "NTop Cands  " << allTTbarCombs.size() << endl;
//
//    for(vector<const xAH::Jet*> thisTTBarComb : allTTbarCombs){
//      assert( (thisTTBarComb.size() == 6) && "Have number of cands differnt than 6");
//
//      if(m_debug) cout << "Building Partilces " << endl;
//      KLFitter::Particles particles;
//      int ijet = 0;
//      for(const xAH::Jet* ttJet : thisTTBarComb){
//	++ijet;
//
//	bool isTagged = (find(thisComb->m_pseudoTaggedJets.begin(), thisComb->m_pseudoTaggedJets.end(), ttJet ) != thisComb->m_pseudoTaggedJets.end());
//	TLorentzVector* tlv = const_cast<TLorentzVector*>(&ttJet->p4);
//	particles.AddParticle(tlv, ttJet->p4.Eta(), KLFitter::Particles::kParton, "", ijet, isTagged);
//      }
//
//      // pass particles to fitter
//      if ( ! m_fitter->SetParticles(&particles) ) {
//	Warning("KLFitterTool::processEvent()","Couldn't set particles!");
//	continue;
//      }
//
//      // loop over all permutations 
//      for (int iperm = 0; iperm < m_fitter->Permutations()->NPermutations(); ++iperm) {
//
//	// fit 
//	if ( m_fitter->Fit(iperm) != 1 ) {
//	  Warning("KLFitterTool::processEvent()","Couldn't set fit permutation %d!", iperm);
//	  continue;
//	}
//
//	// print fit info
//	//if ( doPrint ) print();
//
//	// check convergence
//	unsigned int ConvergenceStatusBitWord = m_fitter->ConvergenceStatus();
//	if ( (ConvergenceStatusBitWord & m_fitter->MinuitDidNotConvergeMask)                 != 0 ||
//	     (ConvergenceStatusBitWord & m_fitter->FitAbortedDueToNaNMask)                   != 0 ||
//	     (ConvergenceStatusBitWord & m_fitter->InvalidTransferFunctionAtConvergenceMask) != 0 ) {
//	  continue;
//	}
//	if ( (ConvergenceStatusBitWord & m_fitter->AtLeastOneFitParameterAtItsLimitMask) != 0 ) {
//	  continue;
//	}
//	
//	// get logl
//	float logl = m_fitter->Likelihood()->LogLikelihood(m_fitter->Likelihood()->GetBestFitParameters());
//	if ( logl > maxLogL ) {
//	  maxLogL = logl;
//	}  
//
//      }// permutations
//
//    }// All 6 jet combinations
//
//
//      
//  }    
//  if(m_debug) cout << "Leaving " << endl;
//  return EL::StatusCode::SUCCESS;
//}
//  
//EL::StatusCode topCandBuilderKLFitter :: postExecute ()
//{
//  return EL::StatusCode::SUCCESS;
//}
//
//
//
//EL::StatusCode topCandBuilderKLFitter :: finalize ()
//{
//
//  if ( m_fitter ) {
//    delete m_fitter->Detector();
//    delete dynamic_cast<KLFitter::LikelihoodTopAllHadronic *>( m_fitter->Likelihood() );
//    delete m_fitter;
//  }
//
//  return EL::StatusCode::SUCCESS;
//}
//
//
//
//
//EL::StatusCode topCandBuilderKLFitter :: histFinalize ()
//{
//  return EL::StatusCode::SUCCESS;
//}
//
//vector<vector<const xAH::Jet*> >  topCandBuilderKLFitter::makeAllTTJetCombs(const std::vector<const xAH::Jet*>& inJets_tag,
//									    const std::vector<const xAH::Jet*>& inJets_non)
//{
//  vector<vector<const xAH::Jet*> > output;  
//
//  vector<const xAH::Jet*> inJets_all;
//  for(const xAH::Jet* jet_tag : inJets_tag) inJets_all.push_back(jet_tag);
//  for(const xAH::Jet* jet_non : inJets_non) inJets_all.push_back(jet_non);
//  unsigned int nJets_all = inJets_all.size();
//
//  if(nJets_all < 6) return output;
//
//  for(unsigned int j1 = 0; j1<nJets_all; ++j1){
//
//    for(unsigned int j2 = j1; j2<nJets_all; ++j2){
//      if(j2 == j1) continue;
//
//      for(unsigned int j3 = j2; j3<nJets_all; ++j3){
//	if(j3 == j2) continue;
//
//	for(unsigned int j4 = j3; j4<nJets_all; ++j4){
//	  if(j4 == j3) continue;
//
//	  for(unsigned int j5 = j4; j5<nJets_all; ++j5){
//	    if(j5 == j4) continue;
//
//	    for(unsigned int j6 = j5; j6<nJets_all; ++j6){
//	      if(j6 == j5) continue;
//	      
//	      output.push_back(vector<const xAH::Jet*>() );
//	      output.back().push_back(inJets_all.at(j1));
//	      output.back().push_back(inJets_all.at(j2));
//	      output.back().push_back(inJets_all.at(j3));
//	      output.back().push_back(inJets_all.at(j4));
//	      output.back().push_back(inJets_all.at(j5));
//	      output.back().push_back(inJets_all.at(j6));
//	      
//	    }//j6
//	  }//j5
//	}//j4
//      }//j3
//    }//j2
//  }//j1
//
//
//  return output;
//}
//
//
//
