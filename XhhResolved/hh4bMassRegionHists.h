#ifndef XhhResolved_hh4bMassRegionHists_H
#define XhhResolved_hh4bMassRegionHists_H

#include <TH1F.h>
#include "XhhResolved/hh4bEvent.h"
#include "XhhResolved/hh4bHists.h"

#include <xAODAnaHelpers/HistogramManager.h>

class hh4bMassRegionHists : public HistogramManager
{
 public:

  hh4bMassRegionHists(const std::string& name, const std::string& detailStr, const std::string& signalExtras = "", bool doTagCategories = false, bool doJetCategories = false);
  ~hh4bMassRegionHists();

  virtual void record(EL::Worker *wk);

  bool m_debug;
  bool m_fast;
  bool m_doTagCategories;
  bool m_doJetCategories;
  virtual StatusCode initialize();
  StatusCode execute(const EventComb* eventComb, const hh4bEvent* event, float eventWeight);
  virtual StatusCode finalize();

  using HistogramManager::book;    // make other overloaded version of book() to show up in subclass
  using HistogramManager::execute; // make other overloaded version of execute() to show up in subclass

 private:


  hh4bHists*       h_Inclusive;
  hh4bHists*       h_NoSR;
  hh4bHists*       h_Sideband;
  hh4bHists*       h_Control;
  //hh4bHists*       h_ControlD;
  hh4bHists*       h_Signal;
  //hh4bHists*       h_Signal_in;
  //hh4bHists*       h_Signal_out;
  hh4bHists*       h_LMVR;
  hh4bHists*       h_HMVR;
  hh4bHists*       h_FullMassPlane;
  //hh4bHists*       h_LowDhh;
  /* hh4bHists*       h_SidebandTwoTagSplit; */
  /* hh4bHists*       h_SidebandLeadTag; */
  /* hh4bHists*       h_SidebandSublTag; */
  /* hh4bHists*       h_ControlTwoTagSplit; */
  /* hh4bHists*       h_ControlLeadTag; */
  /* hh4bHists*       h_ControlSublTag; */
  /* hh4bHists*       h_SignalTwoTagSplit; */
  /* hh4bHists*       h_SignalLeadTag; */
  /* hh4bHists*       h_SignalSublTag; */

  hh4bHists*       h_Sideband_nJet4;
  hh4bHists*       h_Sideband_nJet5;

  hh4bHists*       h_Control_nJet4;
  hh4bHists*       h_Control_nJet5;

  hh4bHists*       h_Signal_nJet4;
  hh4bHists*       h_Signal_nJet5;

  hh4bHists*       h_FullMassPlane_nJet4;
  hh4bHists*       h_FullMassPlane_nJet5;

  hh4bHists*       h_NoSR_nJet4;
  hh4bHists*       h_NoSR_nJet5;

  std::string m_signalHistExtraFlags;
};


#endif // XhhResolved_EventComb_H
