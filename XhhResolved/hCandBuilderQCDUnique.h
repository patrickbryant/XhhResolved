#ifndef XhhResolved_hCandBuilderQCDUnique_H
#define XhhResolved_hCandBuilderQCDUnique_H

//#include "TRandom3.h"
#include "TSystem.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include <string>
#include <XhhResolved/hCandBuilderBase.h>

struct tagPermutation {
  std::vector<int>  tagIndices;
  float        prob;
  unsigned int nTag;
  float        totalProb;
};

class hCandBuilderQCDUnique : public hCandBuilderBase
{
  // put your configuration variables here as public variables.
  // that way they can be set directly from CINT and python.
public:
  
  // this is a standard constructor
  hCandBuilderQCDUnique ();
  ~hCandBuilderQCDUnique () ;

  EL::StatusCode initialize();

  // these are the functions inherited from Algorithm
  virtual EL::StatusCode buildHCands ();

  // this is needed to distribute the algorithm to the workers
  ClassDef(hCandBuilderQCDUnique, 1);

  float m_singleTagProb;
  std::string m_factorFile;
  std::string m_bTagEfficiencyFile;

 private:

  TRandom3* m_randGen = nullptr;
  TF1* m_fit_f2_dR = nullptr;
  TF1* m_fit_f2_pt = nullptr;
  float m_fit_f2_pt_min = 0;
  TF1* m_fit_f2_eta = nullptr;
  TGraphErrors* m_f2_m2j = nullptr;
  TGraphErrors* m_bTagEfficiency = nullptr;
  void store_bTagEfficiency(std::string file);
  void store_factor(std::string file);
 
  std::vector<tagPermutation> buildPossiblePermutations(unsigned int nNonTaggedJets, 
							unsigned int minTagJets, 
							float        singleTagProb);

  std::vector<tagPermutation> addJet(unsigned int jetIndex, std::vector<tagPermutation> input, float f);

  tagPermutation selectPermutation(std::vector<tagPermutation> allPerms);

};

#endif
