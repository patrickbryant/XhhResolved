#include <EventLoop/Job.h>
#include <EventLoop/Worker.h>
#include <EventLoop/OutputStream.h>

#include <AsgTools/MessageCheck.h>

#include <XhhResolved/hh4bHistsAlgo.h>
#include <xAODAnaHelpers/HelperFunctions.h>

#include "TFile.h"
#include "TKey.h"
#include "TLorentzVector.h"
#include "TSystem.h"

#include <utility>      
#include <iostream>
#include <fstream>

using namespace std;

// this is needed to distribute the algorithm to the workers
ClassImp(hh4bHistsAlgo)

hh4bHistsAlgo :: hh4bHistsAlgo () :
  m_debug(false),
  m_fast(false),
  m_mc(false),
  m_histDetailStr(""),
  m_jetDetailStr(""),
  m_combName(""),
  m_trigRequirement(""),
  m_signalHistExtraFlags(""),
  m_scale(1.0),
  m_maxDr  (1000.),
  m_minDr  (-1000.),
  m_minMeT (-1000.),
  m_maxDphi(1000.),
  m_detailLevel(0),
  m_doBlind(false),
  m_doTagCategories(false),
  m_doJetCategories(false),
  hIncl(nullptr),
  hPassHCPt(nullptr),
  hPassHCdEta(nullptr),
  hPassAllhadVeto(nullptr),
  hPass_ggVeto(nullptr),
  hPassVbbVeto(nullptr),
  hExcess(nullptr),
  hNotExcess(nullptr)
//hPassXtt(nullptr)
{
  Info("hh4bHistsAlgo()", "Calling constructor");
}

EL::StatusCode hh4bHistsAlgo :: histInitialize ()
{
  Info("histInitialize()", "Calling histInitialize \n");

  //
  // data model
  m_event = hh4bEvent::global();
  //wk()->addOutput(m_event->m_skim);

  if(!m_fast){
    hIncl         = new hh4bMassRegionHists("Inclusive_"+m_name+"_", "");
    ANA_CHECK(hIncl->initialize());
    hIncl->record(wk());
  }

  if(m_detailLevel > 0) {
    hPassHCPt      = new hh4bMassRegionHists("PassHCPt_"+m_name+"_", "");
    ANA_CHECK(hPassHCPt->initialize());
    hPassHCPt->record(wk());
  }

  hPassHCdEta     = new hh4bMassRegionHists("PassHCdEta_"    +m_name+"_", "", m_signalHistExtraFlags, m_doTagCategories, m_doJetCategories);
  ANA_CHECK(hPassHCdEta->initialize());
  hPassHCdEta->record(wk());
  hPassHCdEta->m_debug = m_debug;
  hPassHCdEta->m_fast = m_fast; //Background model derived prior to top veto
  

  if(!m_fast){
    hPassAllhadVeto = new hh4bMassRegionHists("PassAllhadVeto_"+m_name+"_", "", m_signalHistExtraFlags, m_doTagCategories, m_doJetCategories);
    ANA_CHECK(hPassAllhadVeto->initialize());
    hPassAllhadVeto->record(wk());
    hPassAllhadVeto->m_fast = m_fast; //only need sideband hists for reweighting

    hPass_ggVeto = new hh4bMassRegionHists("Pass_ggVeto_"+m_name+"_", "", m_signalHistExtraFlags, m_doTagCategories, m_doJetCategories);
    ANA_CHECK(hPass_ggVeto->initialize());
    hPass_ggVeto->record(wk());
    hPass_ggVeto->m_fast = m_fast; //only need sideband hists for reweighting

    // hExcess = new hh4bMassRegionHists("Excess_"+m_name+"_", "", m_signalHistExtraFlags, m_doTagCategories, m_doJetCategories);
    // ANA_CHECK(hExcess->initialize());
    // hExcess->record(wk());
    // hExcess->m_fast = m_fast; //only need sideband hists for reweighting

    // hNotExcess = new hh4bMassRegionHists("NotExcess_"+m_name+"_", "", m_signalHistExtraFlags, m_doTagCategories, m_doJetCategories);
    // ANA_CHECK(hNotExcess->initialize());
    // hNotExcess->record(wk());
    // hNotExcess->m_fast = m_fast; //only need sideband hists for reweighting

    // hPassVbbVeto = new hh4bMassRegionHists("PassVbbVeto_"+m_name+"_", "", m_signalHistExtraFlags, m_doTagCategories, m_doJetCategories);
    // ANA_CHECK(hPassVbbVeto->initialize());
    // hPassVbbVeto->record(wk());
    // hPassVbbVeto->m_fast = m_fast; //only need sideband hists for reweighting
  }



  //
  // Cutflow
  //
  m_cutflow=new CutflowHists(m_name, "");
  m_cutflow->m_debug=m_debug;
  ANA_CHECK(m_cutflow->initialize() );
  m_cutflow->record(wk());

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode hh4bHistsAlgo :: initialize ()
{
  if(m_debug) Info("initialize()", "Calling initialize");
  return EL::StatusCode::SUCCESS;
}

EL::StatusCode hh4bHistsAlgo :: execute ()
{
  if(m_debug) Info("execute()", "Processing Event");
  float eventWeight = m_event->getEventWeight();
  m_cutflow->execute("execute",eventWeight*m_scale,1);


  //
  // Check that there are 4 HC Jets. (There will always be an eventComb if there are 4 HC Jets)
  // 
  if(m_debug) cout << " Check for 4 HC Jets" << endl;
  if(m_event->m_eventComb->at(m_combName)->size()==0){
    if(m_debug) cout << " Fail nJets/nbJets" << endl;
    return EL::StatusCode::SUCCESS;
  }

  EventComb* thisComb = m_event->m_eventComb->at(m_combName)->at(0);
  float combWeight = eventWeight*thisComb->m_btagSF*m_scale;
  m_cutflow->execute("passHCJetSelection",combWeight,1,thisComb);

 
  //
  // Only fill combinations with a valid event view - requires a jet pairing passes MDRs
  //
  if(m_debug) cout << " Get EventView" << endl;
  EventView* thisView = thisComb->m_selectedView;
  if(!thisView)   return EL::StatusCode::SUCCESS;
  float viewWeight = combWeight * thisView->m_qcd_weight;
  float viewWeightTrig = viewWeight * thisComb->m_trigSF;
  m_cutflow->execute("passHCJetPairing",viewWeight,1,thisComb);

  // //test a dhh cut
  // if(thisView->m_dhh>20) return EL::StatusCode::SUCCESS;

  //
  //  Blind Signal Region in 4b Data
  //
  if(m_debug) cout << " Check Blinding" << endl;
  bool blindEvent = (m_doBlind && !m_mc && thisView->m_passSignal);
  if(blindEvent){
    if(m_debug) cout << " Fail blinding " << endl;
    return EL::StatusCode::SUCCESS;
  }


  //
  // Fill cutflow before trigger cut. Cutflow hists also check triggers and HLTOR
  // 
  if(m_debug) cout << " Fill Cutflow" << endl;
  if(thisView->m_passHCPt){
    m_cutflow->execute("passHCPt",viewWeight,1,thisComb);
    if(thisView->m_passHCdEta){
      m_cutflow->execute("passHCdEta",viewWeight,1,thisComb);
      if(thisView->m_passSignal){
	m_cutflow->execute("passSignalBeforeAllhadVeto",viewWeight,1,thisComb);
      }
      if(m_event->m_passAllhadVeto){
	m_cutflow->execute("passAllhadVeto",viewWeight,1,thisComb);
	if(thisView->m_passSignal){
	  m_cutflow->execute("passSignal",viewWeight,1,thisComb);
	  if(thisView->m_pass_ggVeto){
	    m_cutflow->execute("pass_ggVeto",viewWeight,1,thisComb);
	    if(thisView->m_passVbbVeto)
	      m_cutflow->execute("passVbbVeto",viewWeight,1,thisComb);
	  }
	}
      }
    }
  }
  if(m_debug) cout << " Check Trigger" << endl;


  //
  // Trigger Req.
  //
  if(!thisComb->passTrig(m_trigRequirement)){
    if(m_debug) cout << " Fail Trigger" << endl;
    return EL::StatusCode::SUCCESS;
  }
  if(m_debug) cout << "PassTrigger " << endl;
  if(!m_fast) hIncl->execute(thisComb, m_event, viewWeightTrig);


  //
  // MDCs
  //
  if(!thisView->m_passHCPt){
    if(m_debug) cout << " Fail HC Pt" << endl;
    return EL::StatusCode::SUCCESS;
  }
  if(m_detailLevel > 0) hPassHCPt->execute(thisComb, m_event, viewWeightTrig);	

  if(!thisView->m_passHCdEta){
    if(m_debug) cout << " Fail HC dEta" << endl;
    return EL::StatusCode::SUCCESS;
  }
  hPassHCdEta->execute(thisComb, m_event, viewWeightTrig);

  if(m_fast) return EL::StatusCode::SUCCESS;

  //
  // Top Veto
  //
  if(!m_event->m_passAllhadVeto){
    if(m_debug) cout << " Fail Allhad veto" << endl;
    return EL::StatusCode::SUCCESS;
  }
  hPassAllhadVeto->execute(thisComb, m_event, viewWeightTrig);

  //
  // gluon,gluon Veto
  //
  if(!thisView->m_pass_ggVeto){
    if(m_debug) cout << " Fail gluon gluon veto" << endl;
    return EL::StatusCode::SUCCESS;
  }
  hPass_ggVeto->execute(thisComb, m_event, viewWeightTrig);

  //if(thisView->hhp4cor->M() > 262 && thisView->hhp4cor->M() < 288) hExcess->execute(thisComb, m_event, viewWeightTrig);
  // else hNotExcess->execute(thisComb, m_event, viewWeightTrig);
  // if(m_combName == "4b" && thisView->m_xhh < 1){
  //   if((thisView->hhp4cor->M() > 262 && thisView->hhp4cor->M() < 288) || thisView->hhp4cor->M() > 1000){
  //     cout << "    Run: " << m_event->m_eventInfo->m_runNumber << endl;
  //     cout << "  Event: " << m_event->m_eventInfo->m_eventNumber << endl;
  //     cout << "    Xhh: " << thisView->m_xhh << endl;
  //     cout << "    m4j: " << thisView->hhp4->M() << endl;
  //     cout << "m4j_cor: " << thisView->hhp4cor->M() << endl;
  //     cout << "  nJets: " << thisComb->m_nonHCJets->size()+4 << endl;
  //   }
  // }


  // //
  // // Z/W+bbar veto
  // //
  // if(!thisView->m_passVbbVeto){
  //   if(m_debug) cout << " Fail Vbb veto" << endl;
  //   return EL::StatusCode::SUCCESS;
  // }
  // hPassVbbVeto->execute(thisComb, m_event, viewWeightTrig);

  //m_event->m_skim->Fill();

  return EL::StatusCode::SUCCESS;
}

EL::StatusCode hh4bHistsAlgo :: histFinalize ()
{
  Info("hh4bHistsAlgo()", "histFinalize");

  ANA_CHECK(m_cutflow->finalize());
  delete m_cutflow;


  if(m_detailLevel > 0){
    ANA_CHECK(hPassHCPt->finalize());  delete hPassHCPt;
  }

  ANA_CHECK(hPassHCdEta->finalize());  delete hPassHCdEta;

  if(!m_fast){
    ANA_CHECK(hIncl->finalize());  delete hIncl;
    ANA_CHECK(hPassAllhadVeto->finalize());  delete hPassAllhadVeto;
    ANA_CHECK(hPass_ggVeto->finalize());  delete hPass_ggVeto;
    // ANA_CHECK(hExcess->finalize());  delete hExcess;
    // ANA_CHECK(hNotExcess->finalize());  delete hNotExcess;
    // ANA_CHECK(hPassVbbVeto->finalize());  delete hPassVbbVeto;
  }

  //write out skimmed tree
  //m_event->m_skim->AutoSave();
  return EL::StatusCode::SUCCESS;
}

