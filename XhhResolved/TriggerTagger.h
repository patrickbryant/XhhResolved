#ifndef XhhResolved_TriggerTagger_H
#define XhhResolved_TriggerTagger_H

#include <string>
#include <vector>
#include "TGraphAsymmErrors.h"
#include "TRandom3.h"

namespace XhhResolved{

  struct jetTrigInfo{

    float pt;
    float pt_weight;
    float tag_weight;
  };

}


//
//  Trigger emulation
//
class TriggerTagger 
{

 private:

  std::string  m_name;
  bool         m_doTag;  
  float        m_scaleFactor;

  struct ptThreshold {
    float              m_plateau;
    unsigned int       m_n;    
    TGraphAsymmErrors* m_ptEff;

    ptThreshold(TGraphAsymmErrors* ptEff, float plateau, unsigned int n = 0)
    {
      m_ptEff=ptEff;
      m_plateau=plateau; 
      m_n=n; 
    }

  };

  TGraphAsymmErrors* m_eff_tag;
  TGraphAsymmErrors* m_sf_tag;


 public:


  TriggerTagger(std::string m_name, bool m_doTag, 
		TGraphAsymmErrors* eff_tag ,
		TGraphAsymmErrors* sf_tag ,
		TGraphAsymmErrors* eff_j35 ,
		TGraphAsymmErrors* eff_j45 ,
		TGraphAsymmErrors* eff_j50 ,
		TGraphAsymmErrors* eff_j55 ,
		TGraphAsymmErrors* eff_j60 ,
		TGraphAsymmErrors* eff_j65 ,
		TGraphAsymmErrors* eff_j70 ,
		TGraphAsymmErrors* eff_j75 ,
		TGraphAsymmErrors* eff_j100,
		TGraphAsymmErrors* eff_j150,
		TGraphAsymmErrors* eff_j175,
		TGraphAsymmErrors* eff_j225,
		TGraphAsymmErrors* eff_j275,
		TGraphAsymmErrors* eff_j300,
		TGraphAsymmErrors* eff_j360,
		float scaleFactor = 1.0);

  void SetDecisions(const std::vector<XhhResolved::jetTrigInfo>& jetInfos, float bjetSmearFactor = 1.0, bool debug = false);

  ptThreshold m_j35;
  ptThreshold m_j45 ;
  ptThreshold m_j50 ;
  ptThreshold m_j55 ;
  ptThreshold m_j60 ;
  ptThreshold m_j65 ;
  ptThreshold m_j70 ;
  ptThreshold m_j75 ;
  ptThreshold m_j100 ;
  ptThreshold m_j150 ;
  ptThreshold m_j175 ;
  ptThreshold m_j225 ;
  ptThreshold m_j275 ;
  ptThreshold m_j300 ;
  ptThreshold m_j360 ;


 private:

  void count(ptThreshold& thisThreshold, const XhhResolved::jetTrigInfo& jetInfo, float smearFactor, bool debug = false);
  void clearCounters();

  // EFficeincies and Uncertianties
  std::vector<float> m_highBinEdge;
  std::vector<float> m_eff;
  std::vector<float> m_effErr;

};

#endif
