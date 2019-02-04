#ifndef XhhResolved_skimTree_H
#define XhhResolved_skimTree_H

#include <TTree.h>
#include "XhhResolved/hh4bEvent.h"
#include <EventLoop/Worker.h>

//#include <xAODAnaHelpers/HistogramManager.h>

class skimTree// : public HistogramManager
{
 public:

  skimTree(const std::string& name, const std::string& detailStr, bool debug);
  virtual ~skimTree();

  virtual void record(EL::Worker *wk);


  std::string m_name;
  std::string m_detailStr;
  bool m_debug;

  virtual StatusCode initialize();
  StatusCode execute(const EventComb* eventComb, const hh4bEvent* event, float eventWeight);
  virtual StatusCode finalize();

 private:
  TTree*       skimmedTree;

  int*   m_NPV = new int();
  float* m_eventWeight = new float();
  float* m_leadHC_M = new float();
  float* m_sublHC_M = new float();
  float* m_leadHC_dRjj = new float();
  float* m_sublHC_dRjj = new float();
  float* m_Xhh = new float();
  float* m_m4j = new float();


};


#endif //
