#ifndef XhhResolved_CutflowHists_H
#define XhhResolved_CutflowHists_H

#include "xAODAnaHelpers/HistogramManager.h"
#include "xAODAnaHelpers/HelperClasses.h"
#include "XhhResolved/EventComb.h"

class CutflowHists : public HistogramManager
{
public:

  CutflowHists(const std::string& name, const std::string& detailStr);
  virtual ~CutflowHists() ;

  bool m_debug;
  virtual StatusCode initialize();
  virtual StatusCode initialize(TH1F *cutflow, TH1F *cutflow_weighted);

  int addCut(const std::string& cut);

  StatusCode executeInitial(float totalNevents, float totalWeight, std::string name = "all");
  StatusCode executeInitial(TH1F *cutflow, TH1F *cutflow_weighted);
  StatusCode execute( int cutflow, float eventWeight, float mcEventWeight=1.0);
  StatusCode execute( const std::string& cutflow, float eventWeight, float mcEventWeight=1.0);
  StatusCode execute( const std::string& cutflow, float eventWeight, float mcEventWeight, EventComb* thisComb);

  virtual StatusCode finalize(TH1F *cutflow, TH1F *cutflow_weighted);

  using HistogramManager::book;     // make other overloaded version of book() to show up in subclass
  using HistogramManager::execute;  // make other overloaded version of execute() to show up in subclass
  using HistogramManager::finalize; // make other overloaded version of finalize() to show up in subclass

private:
  //histograms
  TH1F* m_cutflow;             //!
  TH1F* m_cutflowW;            //!
};

#endif
