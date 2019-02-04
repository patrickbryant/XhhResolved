#include <XhhResolved/hCandBuilderMVSort.h>
#include <xAODAnaHelpers/HelperFunctions.h>

#include <algorithm>

using namespace std;

// this is needed to distribute the algorithm to the workers
ClassImp(hCandBuilderMVSort)


hCandBuilderMVSort :: hCandBuilderMVSort ()
: hCandBuilderBase(),
  m_randGen    (new TRandom3())
{
  Info("hCandBuilderMVSort()", "Calling constructor");
}

hCandBuilderMVSort :: ~hCandBuilderMVSort () 
{ 
  delete m_randGen;
}

EL::StatusCode hCandBuilderMVSort :: buildHCands ()
{
  if(m_debug) Info("buildHCands()", "Processing Event");

  //
  // Sort Jets by MV2
  //
  std::vector<const xAH::Jet*>* taggedJets      = m_eventData->m_taggedJets;
  std::sort(taggedJets->begin(), taggedJets->end(), MV2_greater_than());

  std::vector<const xAH::Jet*>* nonTaggedJets   = &(m_eventData->m_nonTaggedJets->at(m_nonTaggedName));
  std::sort(nonTaggedJets->begin(), nonTaggedJets->end(), MV2_greater_than());

  // 
  // Take the first 4 tagged jets.
  //
  std::vector<const xAH::Jet*> HCJets;
  JetVec pseudoTaggedJets;
  JetVec pseudoNonTaggedJets;

  for(const xAH::Jet* tJet : *taggedJets){
    if(HCJets.size() < 4) HCJets   .push_back(tJet);
    pseudoTaggedJets.push_back(tJet);
  }

  for(const xAH::Jet* ntJet : *nonTaggedJets){
    if(HCJets.size() < 4) HCJets   .push_back(ntJet);
    pseudoNonTaggedJets.push_back(ntJet);
  }

  std::vector<const xAH::Jet*> nonHCJets = overlapRemove(HCJets, *(m_eventData->m_baselineJets));

  assert(HCJets.size() == 4 && "Size of higgs candidate jets must be 4");

  addEvent(HCJets, nonHCJets, m_randGen);

  if(m_combList->back()->m_selectedView){
    m_combList->back()->m_pseudoTaggedJets    = pseudoTaggedJets;
    m_combList->back()->m_pseudoNonTaggedJets = pseudoNonTaggedJets;
  }
  
  if(m_debug) Info("buildHCands()", "Processed Event");
  return EL::StatusCode::SUCCESS;
}


