#include <XhhResolved/hCandBuilderQCDUnique.h>
#include <xAODAnaHelpers/HelperFunctions.h>
 
#include <algorithm>

using namespace std;

// this is needed to distribute the algorithm to the workers
ClassImp(hCandBuilderQCDUnique)


hCandBuilderQCDUnique :: hCandBuilderQCDUnique () 
: hCandBuilderBase(),     
  m_singleTagProb(0.05),
  m_factorFile(""),
  m_bTagEfficiencyFile(""),
  m_randGen    (new TRandom3()),
  m_bTagEfficiency(nullptr)
{
  Info("hCandBuilderQCDUnique()", "Calling constructor");
}

void hCandBuilderQCDUnique :: store_bTagEfficiency(string file){
  Info("hCandBuilderQCDUnique()","store_bTagEfficiency");
  string fullString = gSystem->ExpandPathName( file.c_str() );
  cout << "bTagEfficiency File: " << fullString << endl;
  if (access( fullString.c_str(), F_OK ) == 0 && fullString != "") {
    cout << "Found File: " << fullString << endl;
    TFile *file = new TFile(fullString.c_str(), "READ");
    m_bTagEfficiency = (TGraphErrors*)file->Get("TGraphEfficiency");
  } else {
    cout << "Did not find file:" << file << endl;
  }
  return;
}

void hCandBuilderQCDUnique :: store_factor(string file){
  string fullString = gSystem->ExpandPathName( file.c_str() );
  cout << "factor File: " << fullString << endl;
  if (access( fullString.c_str(), F_OK ) == 0 && fullString != "") {
    cout << "Found File: " << fullString << endl;
    TFile *file = new TFile(fullString.c_str(), "READ");
    m_fit_f2_dR     = (TF1*)file->Get("fit_f2_dR");
    m_fit_f2_pt     = (TF1*)file->Get("fit_f2_pt");
    m_fit_f2_pt_min = m_fit_f2_pt->GetParameter(0);
    m_fit_f2_eta    = (TF1*)file->Get("fit_f2_eta");
    m_f2_m2j        = (TGraphErrors*)file->Get("TGraphErrors_f2_m2j");
  } else {
    cout << "Did not find file:" << file << endl;
  }
  return;
}

EL::StatusCode hCandBuilderQCDUnique :: initialize ()
{
  hCandBuilderBase::initialize();
  Info("initialize()", "Succesfully initialized! \n");
  if(m_bTagEfficiencyFile != "")
    store_bTagEfficiency(m_bTagEfficiencyFile);
  if(m_factorFile != "")
    store_factor(m_factorFile);

  return EL::StatusCode::SUCCESS;
}


hCandBuilderQCDUnique :: ~hCandBuilderQCDUnique () 
{ 
  Info("hCandBuilderQCDUnique()","Calling Destructor");
  delete m_randGen;
}


EL::StatusCode hCandBuilderQCDUnique :: buildHCands ()
{
  if(m_debug) Info("execute()", "Processing Event");

  if(m_debug) cout << " Number of combs before " << m_combList->size() << endl;

  unsigned int nNonTaggedJets    = m_eventData->m_nonTaggedJets->at("NonTagged").size();  
  //unsigned int nNonTaggedJets    = m_eventData->m_qcdTightJets->size();  

  std::vector<tagPermutation> tagPermutationList = buildPossiblePermutations(nNonTaggedJets, 2, m_singleTagProb);
  if(m_debug)
    cout << "Have " << nNonTaggedJets << " nonTagged JEts " 
	 << " and " << tagPermutationList.size() << " Permutations " 
	 << endl;

  tagPermutation selectedPermutation            = selectPermutation(tagPermutationList);

  if(m_debug){
    cout << "Selected permutation has " << selectedPermutation.nTag << " prob " << selectedPermutation.prob << endl;
    for(int iTag : selectedPermutation.tagIndices)
      cout << "\t"<<iTag << endl;
  }

  //
  // Add btagged jets
  //
  JetVec pseudoTaggedJets;
  JetVec pseudoNonTaggedJets;
  for(const xAH::Jet* tJet : *m_eventData->m_taggedJets){
    pseudoTaggedJets.push_back(tJet);
  }


  //
  // Loop over non-tagged jets and assign them to ps-tagged or untagged
  //
  vector<int>& tagIndices = selectedPermutation.tagIndices;
  for(unsigned int iNonTag = 0; iNonTag < nNonTaggedJets; ++iNonTag){
    if(std::find(tagIndices.begin(), tagIndices.end(), iNonTag) != tagIndices.end()) 
      pseudoTaggedJets.push_back(m_eventData->m_nonTaggedJets->at("NonTagged").at(iNonTag));
    else
      pseudoNonTaggedJets.push_back(m_eventData->m_nonTaggedJets->at("NonTagged").at(iNonTag));
  }
  

  assert(pseudoTaggedJets.size() > 3 && "Size of higgs candidate jets must be bigger than 3");

  //
  // Sort Jets by MV2
  //
  std::sort(pseudoTaggedJets.begin(), pseudoTaggedJets.end(), MV2_greater_than());

  // 
  // Take the first 4 "tagged" jets.
  //
  std::vector<const xAH::Jet*> HCJets;

  for(const xAH::Jet* tJet : pseudoTaggedJets){
    if(HCJets.size() < 4) HCJets   .push_back(tJet);
  }

  std::vector<const xAH::Jet*> nonHCJets = overlapRemove(HCJets, *(m_eventData->m_baselineJets));

  addEvent(HCJets, nonHCJets, m_randGen);
  
  if(m_combList->back()->m_selectedView){
    if(m_debug) cout << "nNonTaggedJets " << nNonTaggedJets << " qcd_weight " << selectedPermutation.totalProb << endl;
    m_combList->back()->m_selectedView->m_qcd_weight = selectedPermutation.totalProb;
    m_combList->back()->m_selectedView->m_nJetWeight = selectedPermutation.totalProb;
    m_combList->back()->m_pseudoTaggedJets    = pseudoTaggedJets;
    m_combList->back()->m_pseudoNonTaggedJets = pseudoNonTaggedJets;

    if(m_bTagEfficiencyFile != ""){
      float l_jet1_weight = m_bTagEfficiency->Eval(pseudoTaggedJets.at(2)->p4.Pt());
      float l_jet2_weight = m_bTagEfficiency->Eval(pseudoTaggedJets.at(3)->p4.Pt());
      if(m_debug) cout << "bTagEfficiency weights: " << l_jet1_weight << " " << l_jet2_weight << endl; 
      m_combList->back()->m_selectedView->m_qcd_weight = m_combList->back()->m_selectedView->m_qcd_weight * l_jet1_weight * l_jet2_weight;
    }
      ////
      ////  ADD exclusive QCD if 
      ////
      //hCand* leadHCand = eventCombsQCD->back()->m_selectedView->m_leadHCand;
      //std::vector<const xAH::Jet*>* taggedJets = m_eventData->m_taggedJets;
      //bool leadHCand_leadJet_isTagged = find(taggedJets->begin(), taggedJets->end(), leadHCand->m_leadJet) != taggedJets->end();
      //bool leadHCand_sublJet_isTagged = find(taggedJets->begin(), taggedJets->end(), leadHCand->m_sublJet) != taggedJets->end();
      //bool leadHCand_doubleTag        =  leadHCand_leadJet_isTagged &&  leadHCand_sublJet_isTagged;
      //bool leadHCand_noTag            = !leadHCand_leadJet_isTagged && !leadHCand_sublJet_isTagged;
      //
      //if(leadHCand_doubleTag || leadHCand_noTag)
      //  eventCombsQCDExclusive->push_back(eventCombsQCD->back());
  }


  if(m_debug) cout << " Number of combs after " << m_combList->size() << endl;  
  return EL::StatusCode::SUCCESS;
}


std::vector<tagPermutation> hCandBuilderQCDUnique::buildPossiblePermutations(unsigned int nNonTaggedJets, 
									     unsigned int minTagJets, 
									     float        singleTagProb)
{
  std::vector<tagPermutation> allPermutations;
  for(unsigned int iNonTag = 0; iNonTag < nNonTaggedJets; ++iNonTag){
    allPermutations = addJet(iNonTag, allPermutations, singleTagProb);
  }

  std::vector<tagPermutation> permWithTwoOrMoreTags;
  for(tagPermutation i_perm : allPermutations){
    if(i_perm.nTag < minTagJets) continue;

    permWithTwoOrMoreTags.push_back(i_perm);
  }

  return permWithTwoOrMoreTags;
}


std::vector<tagPermutation>  hCandBuilderQCDUnique::addJet(unsigned int jetIndex, std::vector<tagPermutation> input, float f)
{
  vector<tagPermutation> output;

  if(input.size()){
    
    for(tagPermutation inPer : input){
      //
      // Case: Input Jet tagged
      //
      output.push_back(tagPermutation());
      output.back().prob       = (inPer.prob * f);

      output.back().tagIndices = inPer.tagIndices;
      output.back().tagIndices.push_back(jetIndex);

      output.back().nTag       = (inPer.nTag + 1);      

      //
      // Case: Input Jet not tagged
      //
      output.push_back(tagPermutation());
      output.back().prob       = (inPer.prob * (1-f));

      output.back().tagIndices = inPer.tagIndices;

      output.back().nTag       = (inPer.nTag);
    }

  }else{
    
    //
    // Case input jet is tagged
    //
    output.push_back(tagPermutation());
    output.back().prob       = f;

    output.back().tagIndices = vector<int>();
    output.back().tagIndices.push_back(jetIndex);

    output.back().nTag       = 1;

    //
    // Case input jet is not tagged
    //
    output.push_back(tagPermutation());
    output.back().prob       = (1-f);

    output.back().tagIndices = vector<int>();

    output.back().nTag       = 0;

  }

  return output;
}


tagPermutation hCandBuilderQCDUnique::selectPermutation(vector<tagPermutation> allPerms)
{

  float totalProb = 0;
  for(tagPermutation i_perm : allPerms){
    totalProb += i_perm.prob;
  }

  float thisProb = m_randGen->Uniform();

  float sumProb = 0;
  for(tagPermutation i_perm : allPerms){
    sumProb += i_perm.prob/totalProb;
    if(sumProb > thisProb){
      i_perm.totalProb = totalProb;
      return i_perm;
    }
  }
  cout << "error did not return permulation " <<endl;
  return allPerms.back();
}
