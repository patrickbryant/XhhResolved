#include <XhhResolved/CutflowHists.h>
#include <sstream>

CutflowHists :: CutflowHists (const std::string& name, const std::string& detailStr)
  : HistogramManager(name, detailStr), m_debug(false)
{ }

CutflowHists :: ~CutflowHists () 
{ }

int CutflowHists::addCut(const std::string& cut)
{
  int binN=m_cutflow ->GetXaxis()->FindBin(cut.c_str());
  int binW=m_cutflowW->GetXaxis()->FindBin(cut.c_str());

  if(binN!=binW)
    std::cout << "Warning! nEvents and sumW bins don't match for " << cut << std::endl;

  return binN;
}

StatusCode CutflowHists::initialize() 
{
  // These plots are always made
  m_cutflow   = book(m_name, "cutflow", "cutflow", 1, 1, 2);
  m_cutflow ->SetCanExtend(TH1::kAllAxes);
  m_cutflowW  = book(m_name, "cutflow_weighted", "cutflow_weighted", 1, 1, 2);
  m_cutflowW->SetCanExtend(TH1::kAllAxes);

  m_cutflow ->GetXaxis()->FindBin("all");
  m_cutflowW->GetXaxis()->FindBin("all");
 
  return StatusCode::SUCCESS;
}

StatusCode CutflowHists::initialize(TH1F *cutflow, TH1F */*cutflowW*/) 
{
  // These plots are always made
  m_cutflow   = book(m_name, "cutflow", "cutflow", 1, 1, 2);
  m_cutflow ->SetCanExtend(TH1::kAllAxes);
  m_cutflowW  = book(m_name, "cutflow_weighted", "cutflow_weighted", 1, 1, 2);
  m_cutflowW->SetCanExtend(TH1::kAllAxes);

  for(int i=1; i<cutflow->GetNbinsX()+1; ++i)
    {
      const char* label=cutflow->GetXaxis()->GetBinLabel(i);
      if(label[0]=='\0') continue;
      m_cutflow ->GetXaxis()->FindBin(label);
      m_cutflowW->GetXaxis()->FindBin(label);
    }

  return StatusCode::SUCCESS;
}

StatusCode CutflowHists::executeInitial(float totalNevents, float totalWeight, std::string name)
{
  m_cutflow ->Fill(name.c_str(), totalNevents);
  m_cutflowW->Fill(name.c_str(), totalWeight);

  return StatusCode::SUCCESS;
}

StatusCode CutflowHists::executeInitial(TH1F *cutflow, TH1F *cutflowW)
{
  int bin_all=cutflow->GetXaxis()->FindBin("all");
  float totalNevents=cutflow ->GetBinContent(bin_all);
  float totalWeight =cutflowW->GetBinContent(bin_all);

  m_cutflow ->Fill("all", totalNevents);
  m_cutflowW->Fill("all", totalWeight);

  return StatusCode::SUCCESS;
}

StatusCode CutflowHists::execute(const std::string& cut, float eventWeight, float mcEventWeight)
{
  ANA_CHECK(HistogramManager::execute() );

  m_cutflow ->Fill(cut.c_str(), mcEventWeight);
  m_cutflowW->Fill(cut.c_str(), eventWeight);

  return StatusCode::SUCCESS;
}

StatusCode CutflowHists::execute(const std::string& cut, float eventWeight, float mcEventWeight, EventComb* thisComb)
{
  ANA_CHECK( HistogramManager::execute() );

  m_cutflow ->Fill(cut.c_str(), mcEventWeight);
  m_cutflowW->Fill(cut.c_str(), eventWeight);

  float eventWeightTrig = eventWeight * thisComb->m_trigSF;

  for(auto trig : *(thisComb->m_passedL1Triggers)){
    if(m_debug) std::cout << "CutflowHists::execute trig " << trig << std::endl;
    m_cutflow ->Fill((cut+"_"+trig).c_str(), mcEventWeight);
    m_cutflowW->Fill((cut+"_"+trig).c_str(), eventWeight);
  }

  for(auto trig : *(thisComb->m_passedTriggers)){
    if(m_debug) std::cout << "CutflowHists::execute trig " << trig << std::endl;
    m_cutflow ->Fill((cut+"_"+trig).c_str(), mcEventWeight);
    m_cutflowW->Fill((cut+"_"+trig).c_str(), eventWeightTrig);
  }

  if(thisComb->m_passHLTTrig){
    m_cutflow ->Fill((cut+"_HLT").c_str(), mcEventWeight);
    m_cutflowW->Fill((cut+"_HLT").c_str(), eventWeightTrig);

    float trigSFUp   = (thisComb->m_trigSF + thisComb->m_trigSFErr);
    float trigSFDown = (thisComb->m_trigSF - thisComb->m_trigSFErr);
    if(trigSFUp   > 1) trigSFUp   = 1.0;
    if(trigSFDown < 0) trigSFDown = 0.0;
    float eventWeightTrigUp   = eventWeight * trigSFUp;
    float eventWeightTrigDown = eventWeight * trigSFDown;
    m_cutflowW->Fill((cut+"_HLT_SF_up"  ).c_str(), eventWeightTrigUp);    
    m_cutflowW->Fill((cut+"_HLT_SF_down").c_str(), eventWeightTrigDown);    
  }

  return StatusCode::SUCCESS;
}

StatusCode CutflowHists::execute(int cut, float eventWeight, float mcEventWeight)
{
  ANA_CHECK( HistogramManager::execute() );

  m_cutflow ->Fill(cut, mcEventWeight);
  m_cutflowW->Fill(cut, eventWeight);

  return StatusCode::SUCCESS;
}

StatusCode CutflowHists::finalize(TH1F *cutflow, TH1F *cutflowW) 
{
  ANA_CHECK( HistogramManager::finalize() );

  // These plots are always made
  for(int i=1; i<cutflow->GetNbinsX()+1; ++i)
    {
      const char* label=cutflow->GetXaxis()->GetBinLabel(i);
      if(label[0]=='\0') continue;
      m_cutflow ->SetBinContent(i, cutflow ->GetBinContent(i));
      m_cutflowW->SetBinContent(i, cutflowW->GetBinContent(i));
    }

  return StatusCode::SUCCESS;
}
