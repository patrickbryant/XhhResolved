#include <EventLoop/Job.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <AsgTools/MessageCheck.h>

#include <XhhResolved/hh4bReweightAlgo.h>
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
ClassImp(hh4bReweightAlgo)

hh4bReweightAlgo :: hh4bReweightAlgo () :
  m_debug(false),
  m_doKinematicWeights(true),
  m_combName(""),
  m_weightsFile(""),
  m_variables(nullptr),
//m_hists(nullptr),
  m_MV2CutValue(0.8244),
//m_functions(nullptr),
  m_splines(nullptr)
{
  Info("hh4bReweightAlgo()", "Calling constructor");
}

EL::StatusCode hh4bReweightAlgo :: histInitialize ()
{
  Info("histInitialize()", "Calling histInitialize \n");

  //
  // data model
  m_event = hh4bEvent::global();

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode hh4bReweightAlgo :: initialize ()
{
  storeKinematicWeights(m_weightsFile);

  if(m_debug) Info("initialize()", "Calling initialize");
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode hh4bReweightAlgo :: execute ()
{
  if(m_debug) Info("execute()", "Processing Event");

  EventCombVec* eventCombs = m_event->m_eventComb->at(m_combName);

  for(const EventComb* thisComb : *eventCombs){

    EventView* thisView = thisComb->m_selectedView;

    //
    // Only correct views with a valid event view
    //
    if(!thisView) continue;
    
    // setKinematicWeights("sublGC_sublJet_Pt_m", thisView->m_sublGC->m_sublJet->p4.Pt(), thisView);
    // setKinematicWeights("leadGC_Pt",   thisView->m_leadGC->p4->Pt(), thisView);

    //setKinematicWeights("R_dRdR",      thisView->m_R_dRdR,           thisView);
    //setKinematicWeights("R_dRdR_gg",   thisView->m_R_dRdR_gg,        thisView);
    //setKinematicWeights("HCdR_diff",   thisView->m_HCdR_diff,        thisView);
    //setKinematicWeights("HCdR_sum",    thisView->m_HCdR_sum,         thisView);
    //setKinematicWeights("GCdR_diff",   thisView->m_GCdR_diff,        thisView);
    //setKinematicWeights("GCdR_sum",    thisView->m_GCdR_sum,         thisView);
    setKinematicWeights("leadGC_dRjj", thisView->m_leadGC->m_dRjj,   thisView);
    setKinematicWeights("sublGC_dRjj", thisView->m_sublGC->m_dRjj,   thisView);
    //setKinematicWeights("leadGC_Pt_m", thisView->m_leadGC->p4->Pt(), thisView);
    //setKinematicWeights("Pt_hh",       thisView->hhp4->Pt(),         thisView);
    //setKinematicWeights("hhJetEtaSum2",thisView->m_hhJetEtaSum2,     thisView);
    // for(const xAH::Jet* j : *thisView->m_HCJets){
    //   setKinematicWeights("HC_jets_Pt_m",        j->p4.Pt()  , thisView);
    //   setKinematicWeights("HC_jets_AbsEta", fabs(j->p4.Eta()), thisView);
    // }
    setKinematicWeights("HCJetAbsEta", thisView->m_HCJetAbsEta,            thisView);
    //setKinematicWeights("HCJet1_Pt",   thisView->m_HCJets->at(0)->p4.Pt(), thisView);
    setKinematicWeights("HCJet2_Pt",   thisView->m_HCJets->at(1)->p4.Pt(), thisView);
    //setKinematicWeights("HCJet3_Pt_s", thisView->m_HCJets->at(2)->p4.Pt(), thisView);
    setKinematicWeights("HCJet4_Pt_s", thisView->m_HCJets->at(3)->p4.Pt(), thisView);

    //setKinematicWeights("trigBits", thisComb->m_trigBits, thisView);

    // setKinematicWeights("leadGC_Pt",   thisView->m_leadGC->p4->Pt(),        thisView);

    // setKinematicWeights("HCJetBottomTwoMV2_Pt_m", thisComb->m_HCJets_mv2Sort->at(2)->p4.Pt(), thisView);
    // setKinematicWeights("HCJetBottomTwoMV2_Pt_m", thisComb->m_HCJets_mv2Sort->at(3)->p4.Pt(), thisView);

    // setKinematicWeights("HCJetBottomTwoMV2_AbsEta", fabs(thisComb->m_HCJets_mv2Sort->at(2)->p4.Eta()), thisView);
    // setKinematicWeights("HCJetBottomTwoMV2_AbsEta", fabs(thisComb->m_HCJets_mv2Sort->at(3)->p4.Eta()), thisView);

    // setKinematicWeights("HCJetTopTwoMV2_Pt_m", thisComb->m_HCJets_mv2Sort->at(0)->p4.Pt(), thisView);
    // setKinematicWeights("HCJetTopTwoMV2_Pt_m", thisComb->m_HCJets_mv2Sort->at(1)->p4.Pt(), thisView);

    // setKinematicWeights("HCJetTopTwoMV2_AbsEta", fabs(thisComb->m_HCJets_mv2Sort->at(0)->p4.Eta()), thisView);
    // setKinematicWeights("HCJetTopTwoMV2_AbsEta", fabs(thisComb->m_HCJets_mv2Sort->at(1)->p4.Eta()), thisView);


    //setKinematicWeights("leadGC_dRjj", thisView->m_leadGC->m_dRjj,   thisView);
    //setKinematicWeights("abs_dEta_hh", fabs(thisView->m_dEta),       thisView);
    //setKinematicWeights("abs_dEta_gg", fabs(thisView->m_dEta_gg),    thisView);

  }// EventComb

  return EL::StatusCode::SUCCESS;
}


void hh4bReweightAlgo::storeKinematicWeights(string file){
  string fullString = gSystem->ExpandPathName( file.c_str() );
  cout << "Weights File: " << fullString << endl;
  if (access( fullString.c_str(), F_OK ) == 0 && fullString != "") {
    cout << "Found Weights File: " << fullString << endl;

    //Get Iteration info.
    int pos = fullString.find(".root");
    string substring = fullString.substr(pos-1,1);
    int iMax = atoi( substring.c_str() );

    //Set variables to reweight
    m_variables = new vector<string>;
    //m_variables->push_back("GCdR_diff");
    //m_variables->push_back("GCdR_sum");
    m_variables->push_back("leadGC_dRjj");
    m_variables->push_back("sublGC_dRjj");
    //m_variables->push_back("leadGC_Pt_m");
    //m_variables->push_back("HCJet1_Pt");
    m_variables->push_back("HCJet2_Pt");
    m_variables->push_back("HCJet4_Pt_s");
    m_variables->push_back("HCJetAbsEta");

    //initialize functions map
    //m_hists     = new map<string,vector<TH1F*>*>;
    //m_functions = new map<string,vector<TF1*>*>;
    m_splines   = new map<string,vector<TSpline3*>*>;
    for (auto & variable : *m_variables){
      if(m_debug) cout << "init m_splines "<< variable <<endl;
      //(*m_hists)    [variable] = new vector<TH1F*>;
      //(*m_functions)[variable] = new vector<TF1*>;
      (*m_splines  )[variable] = new vector<TSpline3*>;
    }

    //Loop over files from all iterations up to current

    for (int i = 1; i <= iMax; ++i) {
      fullString.replace(pos-1,1,to_string(i));
      TFile *weightsFile = new TFile(fullString.c_str(), "READ");

      for(uint v = 0; v < m_variables->size(); v++){	
	//Now get kinematic weight functions
	//m_hists    ->at(m_variables->at(v))->push_back(  (TH1F*)    weightsFile->Get( (m_variables->at(v)+"_4b_ratio").c_str() )  );
	//m_functions->at(m_variables->at(v))->push_back(  (TF1*)     weightsFile->Get( ("fit_"+m_variables->at(v)).c_str() )  );
	m_splines  ->at(m_variables->at(v))->push_back(  (TSpline3*)weightsFile->Get( ("spline_"+m_variables->at(v)).c_str() )  );
      }
    }

  } else {
    cout << "Not using a weights file. Setting all weights to 1" << endl;
    //m_weight_4bTo2b = 1;
  }

  return;
}


void hh4bReweightAlgo::setKinematicWeights(std::string variable, float value, EventView* thisView){
  float stepSize = 0.5;
  if (m_debug){
    cout << " In Set Kinematic Weights. " << variable << " " << value << endl;
  }

  if ((m_weightsFile != "") && m_doKinematicWeights){
    if (m_debug)
      cout << " Applying weight " << endl;

    float weight = 1.0;
    float eval = 1.0;
    
    for (unsigned int i = 0; i < m_splines->at(variable)->size(); ++i) { 
      // if(variable == "trigBits")
      // 	eval = m_hists  ->at(variable)->at(i)->GetBinContent(value+1); //bin 2 is m_trigBits = 1 because root hists have bin 0 as underflow
      // else
      eval = m_splines->at(variable)->at(i)->Eval(value);

      if(m_debug) cout << "eval " << eval << endl;
      eval   = (eval - 1)*stepSize + 1;//make step size half the weight to reduce overshooting and oscillatory behaviour in iterations
      eval   = eval > 0.5 ? eval : 0.5;//limit weights at 50% to keep them above zero
      eval   = eval < 1.5 ? eval : 1.5;//limit weights at 150% to keep them from blowing up
      weight = weight * eval;
      //update step size to increase convergance rate as reweighting functions approach 1
      stepSize = stepSize + pow(0.5, i+2);// stepSize per iteration = 1/2, 3/4, 7/8, etc...
    }

    thisView->m_qcd_weight *= weight; //update qcd weight

    

    if (m_debug || (  (thisView->m_qcd_weight < 0) && (m_event->m_totalWeight > 0) )){
      cout << "weight: " << weight << " at " << value << endl;

      cout << "thisEvent.qcdweight  = " << thisView->m_qcd_weight << endl;
      if (thisView->m_qcd_weight < 0) cout << "ERROR: Weight is negative" << endl;
    }

  } else {
    if (m_debug ) cout << " No weights file or config file doesnt have m_doKinematicWeights = True, do not change weight " << endl;
  }

  return;
}



EL::StatusCode hh4bReweightAlgo :: histFinalize ()
{
  return EL::StatusCode::SUCCESS;
}

