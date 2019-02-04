#ifndef XhhResolved_topCand_H
#define XhhResolved_topCand_H

#include <TTree.h>
#include <TLorentzVector.h>

#include <xAODAnaHelpers/Jet.h>
#include <vector>
#include <string>

class topCand
{
 public:

  topCand(std::vector<const xAH::Jet*>& jets_tag, std::vector<const xAH::Jet*>& jets_non);

  ~topCand();

  float mW;
  float mT;
  float w_sig;
  float t_sig;
  float m_xwt;

  //
  //
  const xAH::Jet* m_bjet;
  std::vector<const xAH::Jet*> m_wjets;
  

 private:
  void noMV2Order(const std::vector<const xAH::Jet*>& jets_tag, const std::vector<const xAH::Jet*>& jets_non);
  void MV2Order  (std::vector<const xAH::Jet*>& jets_tag, std::vector<const xAH::Jet*>& jets_non);

};


#endif // XhhResolved_topCand_H
