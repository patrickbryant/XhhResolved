#include <EventLoop/Job.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <AsgTools/MessageCheck.h>

#include <XhhResolved/topCandBuilder.h>
#include <xAODAnaHelpers/HelperFunctions.h>

#include "TFile.h"
#include "TH1D.h"
#include "TKey.h"
#include "TLorentzVector.h"
#include "TSystem.h"

#include <utility>      
#include <iostream>
#include <fstream>
#include <assert.h>     /* assert */

using namespace std;
using xAH::Jet;

// this is needed to distribute the algorithm to the workers
ClassImp(topCandBuilder)


topCandBuilder :: topCandBuilder () 
: m_combName("")
{
  Info("topCandBuilder()", "Calling constructor");
}

EL::StatusCode topCandBuilder :: setupJob (EL::Job& /*job*/)
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode topCandBuilder :: histInitialize ()
{
  Info("histInitialize()", "Calling histInitialize \n");

  //
  // data model
  //
  m_eventData=hh4bEvent::global();

  return EL::StatusCode::SUCCESS;
}



EL::StatusCode topCandBuilder :: fileExecute ()
{
  // Here you do everything that needs to be done exactly once for every
  // single file, e.g. collect a list of all lumi-blocks processed
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode topCandBuilder :: initialize ()
{
  Info("initialize()", "Succesfully initialized! \n");
  return EL::StatusCode::SUCCESS;
}


EL::StatusCode topCandBuilder :: execute ()
{
  if(m_debug) Info("execute()", "Processing Event");

  vector<vector<topCand> > topCands;

  EventCombVec* eventCombs = m_eventData->m_eventComb->at(m_combName);

  for(EventComb* thisComb : *eventCombs){

    EventView* thisView = thisComb->m_selectedView;

    //
    // Only consider combinations with a valid event view
    //
    if(!thisView) continue;

    if(m_debug) cout << "NJets_tag (PS)  " << thisComb->m_pseudoTaggedJets.size() << " NJets_non (PS)  " << thisComb->m_pseudoNonTaggedJets.size() << endl;
    topCands   = makeAllTopCands(*thisComb->m_HCJets, *thisComb->m_nonHCJets);

    if(m_debug) cout << "NTop Cands  " << topCands.size() << endl;

    float minXwt      = 9999;
    float minOtherXwt = 9999;
    float minSumXwt   = 9999;
    float minXtt      = 9999;
  
    unsigned int nTopCandsMax = 0;
    unsigned int nTopCandsMax3 = 0;


    for(vector<topCand> thisTopPairing : topCands){
      if(m_debug) cout << thisTopPairing.size() << endl;
    
      assert( (thisTopPairing.size() > 0 ) && "Have non-zero top pairing size");
      float thisXwt = thisTopPairing.at(0).m_xwt;
    
      if(m_debug) cout << "\t\t " << thisXwt << endl;
      //if(thisXwt > 10.0) continue;

      //First find best top candidate
      if(thisXwt < minXwt){
	minXwt    = thisXwt;
      }

      unsigned int nTopCandsThisParing = 1;
      unsigned int nTopCandsThisParing3 = 0;
      if(thisXwt < 3.0){
	++nTopCandsThisParing3;
      }
      
      //if more than one top candiate, find second best
      if(thisTopPairing.size() > 1){

	for(unsigned int iOtherTop = 1; iOtherTop < thisTopPairing.size(); ++iOtherTop){

	  if(thisTopPairing.at(iOtherTop).m_xwt > 10.0) continue;

	  float otherXwt = thisTopPairing.at(iOtherTop).m_xwt;

	  if( otherXwt < minOtherXwt){
	    minOtherXwt = otherXwt;
	    minSumXwt   = thisXwt + otherXwt;
	    minXtt      = sqrt( thisXwt*thisXwt + otherXwt*otherXwt );
	  }
	  
	  ++nTopCandsThisParing;
	  if(otherXwt < 3.0){
	    ++nTopCandsThisParing3;
	  }
	    
	}

      }

      if(nTopCandsThisParing  > nTopCandsMax ) nTopCandsMax  = nTopCandsThisParing;
      if(nTopCandsThisParing3 > nTopCandsMax3) nTopCandsMax3 = nTopCandsThisParing3;    
    }

    if(m_debug) cout << "NJets " << (thisComb->m_pseudoTaggedJets.size() + thisComb->m_pseudoNonTaggedJets.size())<< " NTop Cands " << topCands.size() << " xtt_ave " << (minSumXwt/2) <<  endl;
      
    thisComb->m_nTopCands    = nTopCandsMax;
    thisComb->m_nTopCands3   = nTopCandsMax3;
    thisComb->m_nTopCandsAll = topCands.size();

    m_eventData->m_xwt     = minXwt;
    m_eventData->m_xwt_ave = (minSumXwt/2);
    m_eventData->m_xtt     = minXtt;
    m_eventData->m_passXtt = (minXtt > 5) && (minXwt > 1);
    m_eventData->m_passAllhadVeto = (minXwt > 1.50);
    
    if(m_debug) cout << minXwt << " " << minSumXwt/2 << endl;
  }    
  if(m_debug) cout << "Leaving " << endl;
  return EL::StatusCode::SUCCESS;
}
  
EL::StatusCode topCandBuilder :: postExecute ()
{
  return EL::StatusCode::SUCCESS;
}



EL::StatusCode topCandBuilder :: finalize ()
{
  return EL::StatusCode::SUCCESS;
}




EL::StatusCode topCandBuilder :: histFinalize ()
{
  return EL::StatusCode::SUCCESS;
}

std::vector<vector<topCand> > topCandBuilder::makeAllTopCands(const std::vector<const xAH::Jet*>& inJets_tag,
							      const std::vector<const xAH::Jet*>& inJets_non)
{
  vector<vector<topCand> > output;

  vector<const xAH::Jet*> inJets_all;
  for(const xAH::Jet* jet_tag : inJets_tag) inJets_all.push_back(jet_tag);
  for(const xAH::Jet* jet_non : inJets_non) inJets_all.push_back(jet_non);
  unsigned int nJets_all = inJets_all.size();


  //
  // Top Cand 1
  //
  for(unsigned int t1_j1 = 0; t1_j1<nJets_all; ++t1_j1){
    
    for(unsigned int t1_j2 = t1_j1; t1_j2<nJets_all; ++t1_j2){
      if(t1_j2 == t1_j1) continue;
      
      for(unsigned int t1_j3 = t1_j2; t1_j3<nJets_all; ++t1_j3){
	if(t1_j3 == t1_j2) continue;

	vector<const xAH::Jet*> t1_tag_jets;
	vector<const xAH::Jet*> t1_non_jets;
	
	const Jet* t1_jet1 = inJets_all.at(t1_j1);
	if(find(inJets_tag.begin(), inJets_tag.end(), t1_jet1) != inJets_tag.end()) t1_tag_jets.push_back(t1_jet1);
	else                                                                        t1_non_jets.push_back(t1_jet1);

	const Jet* t1_jet2 = inJets_all.at(t1_j2);
	if(find(inJets_tag.begin(), inJets_tag.end(), t1_jet2) != inJets_tag.end()) t1_tag_jets.push_back(t1_jet2);
	else                                                                           t1_non_jets.push_back(t1_jet2);

	const Jet* t1_jet3 = inJets_all.at(t1_j3);
	if(find(inJets_tag.begin(), inJets_tag.end(), t1_jet3) != inJets_tag.end()) t1_tag_jets.push_back(t1_jet3);
	else                                                                           t1_non_jets.push_back(t1_jet3);

	//if(m_debug) cout << "Makding cand1  "  << t1_j1 << " " << t1_j2 << " " << t1_j3 << endl;
	//if(m_debug) cout << "\t"  << inJets_tag.size() << " + " << inJets_non->size() << endl;
	topCand cand1 = topCand(t1_tag_jets, t1_non_jets);
	output.push_back(vector<topCand>());
	output.back().push_back(cand1);
	
	//
	// Top Cand 2
	//
	// Start at t1_j1 to avoid double counting
	for(unsigned int t2_j1 = t1_j1; t2_j1<nJets_all; ++t2_j1){
	  if(t2_j1 == t1_j1) continue;
	  if(t2_j1 == t1_j1 || t2_j1 == t1_j2 || t2_j1 == t1_j3) continue;

	  for(unsigned int t2_j2 = t2_j1; t2_j2<nJets_all; ++t2_j2){
	    if(t2_j2 == t2_j1) continue;
	    if(t2_j2 == t1_j1 || t2_j2 == t1_j2 || t2_j2 == t1_j3) continue;

	    for(unsigned int t2_j3 = t2_j2; t2_j3<nJets_all; ++t2_j3){
	      if(t2_j3 == t2_j2) continue;	  
	      if(t2_j3 == t1_j1 || t2_j3 == t1_j2 || t2_j3 == t1_j3) continue;

	      vector<const Jet*> t2_tag_jets;
	      vector<const Jet*> t2_non_jets;
	
	      const Jet* t2_jet1 = inJets_all.at(t2_j1);
	      if(find(inJets_tag.begin(), inJets_tag.end(), t2_jet1) != inJets_tag.end()) t2_tag_jets.push_back(t2_jet1);
	      else                                                                           t2_non_jets.push_back(t2_jet1);

	      const Jet* t2_jet2 = inJets_all.at(t2_j2);
	      if(find(inJets_tag.begin(), inJets_tag.end(), t2_jet2) != inJets_tag.end()) t2_tag_jets.push_back(t2_jet2);
	      else                                                                           t2_non_jets.push_back(t2_jet2);

	      const Jet* t2_jet3 = inJets_all.at(t2_j3);
	      if(find(inJets_tag.begin(), inJets_tag.end(), t2_jet3) != inJets_tag.end()) t2_tag_jets.push_back(t2_jet3);
	      else                                                                           t2_non_jets.push_back(t2_jet3);

	      //cout << "Makding cand1  "  << t1_j1 << " " << t1_j2 << " " << t1_j3 << endl;
	      topCand cand2 = topCand(t2_tag_jets, t2_non_jets);
	      output.back().push_back(cand2);
	      

	    }//t2_j3
	  }//t2_j2
	}//t2_j1

      }//t1_j3
    }//t1_jet2
  }//t1_jet1
  
  return output;
}



