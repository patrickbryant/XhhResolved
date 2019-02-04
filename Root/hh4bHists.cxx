#include "XhhResolved/hh4bHists.h"
#include "xAODAnaHelpers/HelperFunctions.h"
#include "xAODAnaHelpers/Muon.h"

using std::cout;  using std::endl; 
using xAH::Jet;   using xAH::Muon;

hh4bHists :: hh4bHists (const std::string& name, const std::string& detailStr)
  : HistogramManager(name, detailStr), m_debug(false), 
    m_lhh_reweightFile(0),
    h_leadHC(0), h_sublHC(0), 
    h_HCJet1(0), h_HCJet2(0), h_HCJet3(0), h_HCJet4(0), 
    h_jetsHC(0), h_jetsOther(0),
    h_muons(0), h_promptMuons(0), h_elecs(0),
    h_preSelJets(0)
{ 
  m_doReweight = HelperFunctions::has_exact(detailStr, "doReweight");
  m_doBTagSF   = HelperFunctions::has_exact(detailStr, "doBTagSF");
}

hh4bHists :: ~hh4bHists () 
{ }

StatusCode hh4bHists::initialize()
{
  //
  // Event Level
  //
  h_NPV            = book(m_name, "NPV",         "NPV",           50,     -0.5,    49.5 );
  h_mu_ave         = book(m_name, "mu_ave",      "mu_ave",        50,     -0.5,    49.5 );
  h_nJetOther      = book(m_name, "nJetOther",   "nJetsOther",    10,     -0.5,     9.5 );
  h_nJetOther_u    = book(m_name, "nJetOther_u", "nJetsOther",    10,     -0.5,     9.5 );
  h_nJetOther_l    = book(m_name, "nJetOther_l", "nJetsOther",    20,     -0.5,    19.5 );
  h_nMuons         = book(m_name, "nMuons",      "nMuons",    10,     -0.5,     9.5 );
  h_nPromptMuons   = book(m_name, "nPromptMuons","nPromptMuons",    10,     -0.5,     9.5 );
  h_nPromptElecs   = book(m_name, "nPromptElecs","nPromptElecs",    10,     -0.5,     9.5 );
  h_nLooseOther    = book(m_name, "nLooseOther", "nJetsOther (Loose Tag)",    10,     -0.5,     9.5 );
  h_m4j            = book(m_name, "m4j",         "m4j [GeV]",    100,      100,    1000 );
  h_m4j10          = book(m_name, "m4j10",       "m4j [GeV]",    190,      100,    2000 );
  h_m4j25          = book(m_name, "m4j25",       "m4j [GeV]",    120,       0,    3000 );
  h_m4j50          = book(m_name, "m4j50",       "m4j [GeV]",     60,       0 ,    3000 );
  h_m4j_l          = book(m_name, "m4j_l",       "m4j [GeV]",    190,      100,    2000 );
  h_m_4j           = book(m_name, "m_4j",        "m_4j [GeV]",    60,       0,    3000 ); 
  h_m4j_cor        = book(m_name, "m4j_cor",         "m4j (corrected) [GeV]",    100,        0,    1000 );
  h_m4j_cor_l      = book(m_name, "m4j_cor_l",       "m4j (corrected) [GeV]",    190,      100,    2000 );
  h_m4j_cor_1      = book(m_name, "m4j_cor_1",       "m4j (corrected) [GeV]",    750,     250,    1000 );

  Double_t bins[] = {150, 250, 262, 275, 288, 302, 317, 332, 348, 365, 383, 402, 422, 443, 465, 488, 512, 537, 563, 591, 620, 651, 683, 717, 752, 789, 828, 869, 912, 957,
		     1004, 1054, 1106, 1161, 1219, 1279, 1342, 1409, 1479, 1552, 1629, 1710, 1795, 1884, 1978, 2076};
  h_m4j_cor_v      = book(m_name, "m4j_cor_v",       "m4j (corrected) [GeV]",    45, bins);
  h_m4j_cor_f      = book(m_name, "m4j_cor_f",       "bin", 45, 0,45);

  Double_t bins_s[] = {150, 250, 255, 260, 265, 270, 275, 280, 285, 290, 295, 300, 306, 312, 318, 324, 330, 336, 342, 348, 354, 361, 368, 375, 382, 389, 396, 403, 411, 419, 
		       427, 435, 443, 451, 460, 469, 478, 487, 496, 505, 515, 525, 535, 545, 555, 566, 577, 588, 599, 610, 622, 634, 646, 658, 671, 684, 697, 710, 724, 738, 
		       752, 767, 782, 797, 812, 828, 844, 860, 877, 894, 911, 929, 947, 965, 984, 1003, 1023, 1043, 1063, 1084, 1105, 1127, 1149, 1171, 1194, 1217, 1241, 
		       1265, 1290, 1315, 1341, 1367, 1394, 1421, 1449, 1477, 1506, 1536, 1566, 1597, 1628, 1660, 1693, 1726, 1760, 1795, 1830, 1866, 1903, 1941, 1979, 2018};

  //h_m4j_cor_v_s    = book(m_name, "m4j_cor_v_s",  "m4j (corrected) [GeV]",    111, bins_s);
  //hist for stat tools with constant bin width. Bins correspond to bins of h_m4j_cor_v
  //h_m4j_cor_f_s      = book(m_name, "m4j_cor_f_s",       "bin", 111, 0,111);

  h_Ht4j_l      = book(m_name, "Ht4j_l",       "Ht 4j [GeV]",    190,      100,    2000 );
  h_R_pt_4j_l   = book(m_name, "R_pt_4j_l",    "#sqrt{#Sigma (pt-40)^2} 4j [GeV]",    100,      0,    1000 );

  //Split by high/low HCJet Ht in order to define high and low mass shape systematic NPs
  h_lowHt_m4j_cor_l      = book(m_name, "lowHt_m4j_cor_l",       "m4j (corrected) [GeV]",    190,      100,    2000 );
  h_lowHt_m4j_cor_v      = book(m_name, "lowHt_m4j_cor_v",       "m4j (corrected) [GeV]",    45, bins);
  h_lowHt_m4j_cor_f      = book(m_name, "lowHt_m4j_cor_f",       "bin", 45, 0,45);
  //h_lowHt_m4j_cor_v_s      = book(m_name, "lowHt_m4j_cor_v_s",       "m4j (corrected) [GeV]",    111, bins_s);
  //h_lowHt_m4j_cor_f_s      = book(m_name, "lowHt_m4j_cor_f_s",       "bin", 111, 0,111);
  h_lowHt_m12m34         = book(m_name,"lowHt_m12m34",        "Lead HC mass",      60,   0,    300, "Subl HC mass",          60, 0, 300);

  h_highHt_m4j_cor_l      = book(m_name, "highHt_m4j_cor_l",       "m4j (corrected) [GeV]",    190,      100,    2000 );
  h_highHt_m4j_cor_v      = book(m_name, "highHt_m4j_cor_v",       "m4j (corrected) [GeV]",    45, bins);
  h_highHt_m4j_cor_f      = book(m_name, "highHt_m4j_cor_f",       "bin", 45, 0,45);
  //h_highHt_m4j_cor_v_s      = book(m_name, "highHt_m4j_cor_v_s",       "m4j (corrected) [GeV]",    111, bins_s);
  //h_highHt_m4j_cor_f_s      = book(m_name, "highHt_m4j_cor_f_s",       "bin", 111, 0,111);
  h_highHt_m12m34         = book(m_name,"highHt_m12m34",        "Lead HC mass",      60,   0,    300, "Subl HC mass",          60, 0, 300);
  
  h_m4j_cor_l_tSF_up   = book(m_name, "m4j_cor_l_tSF_up"  ,       "m4j (corrected) [GeV]",    190,      100,    2000 );
  h_m4j_cor_l_tSF_down = book(m_name, "m4j_cor_l_tSF_down",       "m4j (corrected) [GeV]",    190,      100,    2000 );
  h_m4j_cor_1_tSF_up      = book(m_name, "m4j_cor_1_tSF_up",       "m4j (corrected) [GeV]",    750,     250,    1000 );
  h_m4j_cor_1_tSF_down      = book(m_name, "m4j_cor_1_tSF_down",       "m4j (corrected) [GeV]",    750,     250,    1000 );
  h_m4j_cor_v_tSF_up   = book(m_name, "m4j_cor_v_tSF_up"  ,       "m4j (corrected) [GeV]",    45, bins );
  h_m4j_cor_v_tSF_down = book(m_name, "m4j_cor_v_tSF_down",       "m4j (corrected) [GeV]",    45, bins );
  h_m4j_cor_f_tSF_up   = book(m_name, "m4j_cor_f_tSF_up"  ,                         "bin",    45, 0,45 );
  h_m4j_cor_f_tSF_down = book(m_name, "m4j_cor_f_tSF_down",                         "bin",    45, 0,45 );

  //h_m4j_cor_v_s_tSF_up   = book(m_name, "m4j_cor_v_s_tSF_up"  ,       "m4j (corrected) [GeV]",    111, bins_s );
  //h_m4j_cor_v_s_tSF_down = book(m_name, "m4j_cor_v_s_tSF_down",       "m4j (corrected) [GeV]",    111, bins_s );
  //h_m4j_cor_f_s_tSF_up   = book(m_name, "m4j_cor_f_s_tSF_up"  ,                         "bin",    111, 0,111 );
  //h_m4j_cor_f_s_tSF_down = book(m_name, "m4j_cor_f_s_tSF_down",                         "bin",    111, 0,111 );

  if(m_doBTagSF){
    m_nBTagSFVar = 51;
    h_m4j_cor_l_bSF = new std::vector<TH1F*>();
    h_m4j_cor_1_bSF = new std::vector<TH1F*>();
    h_m4j_cor_v_bSF = new std::vector<TH1F*>();
    h_m4j_cor_f_bSF = new std::vector<TH1F*>();
    //h_m4j_cor_v_s_bSF = new std::vector<TH1F*>();
    //h_m4j_cor_f_s_bSF = new std::vector<TH1F*>();
    for(unsigned int i = 1; i < m_nBTagSFVar; ++i){
      h_m4j_cor_l_bSF->push_back(book(m_name, "m4j_cor_l_bSF"+std::to_string(i),"m4j (corrected) [GeV]", 190, 100, 2000));
      h_m4j_cor_1_bSF->push_back(book(m_name, "m4j_cor_1_bSF"+std::to_string(i),"m4j (corrected) [GeV]", 750,250, 1000));
      h_m4j_cor_v_bSF->push_back(book(m_name, "m4j_cor_v_bSF"+std::to_string(i),"m4j (corrected) [GeV]", 45, bins));
      h_m4j_cor_f_bSF->push_back(book(m_name, "m4j_cor_f_bSF"+std::to_string(i),                  "bin", 45, 0,45));
      //h_m4j_cor_v_s_bSF->push_back(book(m_name, "m4j_cor_v_s_bSF"+std::to_string(i),"m4j (corrected) [GeV]", 111, bins_s));
      //h_m4j_cor_f_s_bSF->push_back(book(m_name, "m4j_cor_f_s_bSF"+std::to_string(i),                  "bin", 111, 0,111));
    }
  }

  h_m_4j_cor       = book(m_name, "m_4j_cor",        "m_4j (corrected) [GeV]",    60,        0,    3000 );
  h_m4j25_cor      = book(m_name, "m4j25_cor",       "m4j [GeV]",    120,      0,    3000 );
  h_m4j50_cor      = book(m_name, "m4j50_cor",       "m4j [GeV]",     60,      0,    3000 );
  h_m4j_diff       = book(m_name, "m4j_diff",         "m4j (corrected diff) [GeV]",    100,        -500,    500 );

  h_trigBits       = book(m_name, "trigBits", "Trigger Combination", 16,0,16);

  h_m4j_cor_Z        = book(m_name, "m4j_cor_Z",         "m4j (Z-corrected) [GeV]",    100,        0,    1000 );
  h_m4j_cor_Z_l      = book(m_name, "m4j_cor_Z_l",       "m4j (Z-corrected) [GeV]",    190,      100,    2000 );
  Double_t binsZ[] = {150, 182, 191, 200, 210, 220, 231, 242, 254, 266, 279, 292, 306, 321, 337, 353, 370, 388, 407, 427, 448, 470, 493, 517, 542, 569, 597, 626, 657, 
		      689, 723, 759, 796, 835, 876, 919, 964, 1012, 1062, 1115, 1170, 1228, 1289, 1353, 1420, 1491, 1565, 1643, 1725, 1811, 1901, 1996, 2095};
  h_m4j_cor_Z_v      = book(m_name, "m4j_cor_Z_v",       "m4j (Z-corrected) [GeV]",    52, binsZ);
  h_m4j_cor_Z_f      = book(m_name, "m4j_cor_Z_f",       "bin", 52, 0,52);

  h_m4j_cor_H        = book(m_name, "m4j_cor_H",         "m4j (H-corrected) [GeV]",    100,        0,    1000 );
  h_m4j_cor_H_l      = book(m_name, "m4j_cor_H_l",       "m4j (H-corrected) [GeV]",    190,      100,    2000 );
  Double_t binsH[] = {150, 310, 325, 341, 358, 375, 393, 412, 432, 453, 475, 498, 522, 548, 575, 603, 633, 664, 697, 731, 767, 805, 845, 887, 931, 977, 1025, 1076, 
		      1129, 1185, 1244, 1306, 1371, 1439, 1510, 1585, 1664, 1747, 1834, 1925, 2021};
  h_m4j_cor_H_v      = book(m_name, "m4j_cor_H_v",       "m4j (H-corrected) [GeV]",    40, binsH);
  h_m4j_cor_H_f      = book(m_name, "m4j_cor_H_f",       "bin", 40, 0,40);

  h_dEta_hh      = book(m_name, "dEta_hh",    "dEta hh",   120,       -6,       6 );
  h_abs_dEta_hh  = book(m_name, "abs_dEta_hh","|dEta hh|",  70,        0,       7 );
  h_dPhi_hh      = book(m_name, "dPhi_hh",    "dPhi hh",   100,     -0.2,     3.8 );
  h_dR_hh        = book(m_name, "dR_hh",      "dR hh",     140,        0,       7 );
  h_Pt_hh        = book(m_name, "Pt_hh",      "pt hh",     100,        0,      300 );

  h_dEta_gg      = book(m_name, "dEta_gg",    "dEta gg",   120,       -6,       6 );
  h_abs_dEta_gg  = book(m_name, "abs_dEta_gg","|dEta gg|",  70,        0,       7 );
  h_dPhi_gg      = book(m_name, "dPhi_gg",    "dPhi gg",   100,     -0.2,     3.8 );
  h_dR_gg        = book(m_name, "dR_gg",      "dR gg",     140,        0,       7 );
  h_Pt_gg        = book(m_name, "Pt_gg",      "pt gg",     100,        0,      300 );

  h_R_dRdR       = book(m_name, "R_dRdR",    "R_{dR_{1}dR_{2}}", 305, -0.1,  6);
  h_R_dRdR_gg    = book(m_name, "R_dRdR_gg", "R_{dR_{1}dR_{2}}", 305, -0.1,  6);

  h_GCdR_diff    = book(m_name, "GCdR_diff", "dR_{2}-dR_{1}", 275, -0.5,  5);
  h_GCdR_sum     = book(m_name, "GCdR_sum",  "dR_{2}+dR_{1}", 325,  0.5,  7);

  h_HCdR_diff    = book(m_name, "HCdR_diff", "dR_{2}-dR_{1}", 160, -4,  4);
  h_HCdR_sum     = book(m_name, "HCdR_sum",  "dR_{2}+dR_{1}", 170,  0.5, 9);

  h_nbjets         = book(m_name, "nbJetsOther",   "nbJets Other",    10,     -0.5,     9.5 );
  h_njets          = book(m_name, "nJets",   "nJets",    10,     -0.5,     9.5 );
  //  h_nbjetsInHCs    = book(m_name, "nbjetsInHCs",      "nbjetsInHCs",         5,     -0.5,     4.5 );
  h_ht             = book(m_name, "ht",          "ht [GeV]",     100,      0,    1000 );
  h_ht_l           = book(m_name, "ht_l",        "ht [GeV]",     100,      0,    2000 );
  h_mht             = book(m_name, "mht",          "mht [GeV]",     100,      0,    100 );
  h_mht_l           = book(m_name, "mht_l",        "mht [GeV]",     100,      0,    500 );

  h_xhh            = book(m_name, "xhh",         "Xhh",           50,        0,      12 );
  h_dhh            = book(m_name, "dhh",         "Dhh [GeV]",           30,        0,      150 );
  h_lhh            = book(m_name, "lhh",         "Lhh [GeV]",           50,        50,     300 );
  h_rhh            = book(m_name, "rhh",         "Rhh [GeV]",          100,         0,     500 );
  h_rhhMin         = book(m_name, "rhhMin","Rhh (Min) [GeV]",          100,         0,     500 );

  h_hhJetEtaSum2   = book(m_name, "hhJetEtaSum2","hhJetEtaSum2",        50,        0,       25 );
  h_HCJetAbsEta    = book(m_name, "HCJetAbsEta", "<|HC Jet #eta|>",     80,        0,        4 );
  h_HCJetAR        = book(m_name, "HCJetAR",     "HC Jets sqrt( #Sigma(1-P_{t}/E)^{2} )",        55,        0,       1.1 );

  h_HCJetPtE1      = book(m_name, "HCJetPtE1",     "HC Jets <P_{t}/E>",        55,        0,       1.1 );
  h_HCJetPtE2      = book(m_name, "HCJetPtE2",     "HC Jets <(P_{t}/E)^{2}>/<P_{t}/E>",        55,        0,       1.1 );

  h_xwt            = book(m_name, "xwt",         "Xwt",           48,        0,      12 );
  h_xwt_ave        = book(m_name, "xwt_ave",     "Xwt_ave",       48,        0,      12 );
  h_xtt            = book(m_name, "xtt",         "Xtt",           48,        0,      12 );
  h_minSum_xtt_1   = book(m_name, "minSum_xtt_1","minSum_xtt_1",       50,        0,      12 );
  h_minSum_xtt_2   = book(m_name, "minSum_xtt_2","minSum_xtt_2",       50,        0,      12 );
  h_nTopCands      = book(m_name, "nTopCands"   ,"nTopCands",    100,     -0.5,    99.5 );
  h_nTopCands3     = book(m_name, "nTopCands3"  ,"nTopCands3",   30,     -0.5,     29.5 );
  h_nTopCandsAll   = book(m_name, "nTopCandsAll","nTopCands (All)",    100,     -0.5,    499.5 );


  h_xtt_2j         = book(m_name, "xtt_2j",      "Xtt (2-jet)",           50,        0,      12 );
  h_xtt_2j_ave     = book(m_name, "xtt_2j_ave",  "Xtt_ave (2-jet)",       50,        0,      12 );
  h_nTopCands_2j   = book(m_name, "nTopCands_2j"   ,"nTopCands (2-jet)",   100,     -0.5,    99.5 );
  h_nTopCands3_2j  = book(m_name, "nTopCands3_2j"  ,"nTopCands3 (2-jet)",  30,     -0.5,     29.5 );
  h_nTopCandsAll_2j= book(m_name, "nTopCandsAll_2j","nTopCands All (2-jets)",    100,     -0.5,    499.5 );

  h_m12m34         = book(m_name,"m12m34",        "Lead HC mass",      60,   0,    300, "Subl HC mass",          60, 0, 300);
  h_GC_m12m34      = book(m_name,"GC_m12m34",     "Lead GC mass",      60,   0,    300, "Subl GC mass",          60, 0, 300);
  h_dR12dR34       = book(m_name,"dR12dR34",      "Lead HC dRjj",      40,   0,      4, "Subl HC dRjj",          40, 0, 4  );
  h_GC_dR12dR34    = book(m_name,"GC_dR12dR34",   "Lead GC dRjj",      40,   0,      4, "Subl GC dRjj",          40, 0, 4  );
  h_m4jnJetOther   = book(m_name,"m4jnJetOther"  ,"m4j",              100, 100,   1100, "nJetOther",      10, -0.5, 9.5);
  h_m4jLeadHCandPt = book(m_name,"m4jLeadHCandPt","m4j",              100, 100,   1100, "Lead HC Pt",     45, 0, 450);
  h_m4jSublHCandPt = book(m_name,"m4jSublHCandPt","m4j",              100, 100,   1100, "Subl HC Pt",     30, 0, 300);
  h_m4jHCdEta      = book(m_name,"m4jHCdEta"     ,"m4j",              100, 100,   1100, "HC dEta",       180, 0, 1.8);
  h_m4jHCdPhi      = book(m_name,"m4jHCdPhi"     ,"m4j",              100, 100,   1100, "HC dPhi",        80, 0, 4.0);
  h_m4jLeadHCdRjj  = book(m_name,"m4jLeadHCdRjj" ,"m4j",              100, 100,   1100, "Lead HC dRjj",   40, 0, 4  );
  h_m4jSublHCdRjj  = book(m_name,"m4jSublHCdRjj" ,"m4j",              100, 100,   1100, "Subl HC dRjj",   40, 0, 4  );

  h_m4jLeadGCdRjj  = book(m_name,"m4jLeadGCdRjj" ,"m4j",              100, 100,   1100, "Lead GC dRjj",   40, 0, 4  );
  h_m4jSublGCdRjj  = book(m_name,"m4jSublGCdRjj" ,"m4j",              100, 100,   1100, "Subl GC dRjj",   40, 0, 4  );

  h_m4jLeadPtHCandPt = book(m_name,"m4jLeadPtHCandPt","m4j",    100, 100,   1100, "LeadPt HC Pt",     45, 0, 450);
  h_m4jSublPtHCandPt = book(m_name,"m4jSublPtHCandPt","m4j",    100, 100,   1100, "SublPt HC Pt",     30, 0, 300);
  h_m4jLeadPtHCdRjj  = book(m_name,"m4jLeadPtHCdRjj" ,"m4j",    100, 100,   1100, "LeadPt HC dRjj",   40, 0, 4  );
  h_m4jSublPtHCdRjj  = book(m_name,"m4jSublPtHCdRjj" ,"m4j",    100, 100,   1100, "SublPt HC dRjj",   40, 0, 4  );

  h_m4j_nViews     = book(m_name,"m4j_nViews" ,"m4j",    120, 100,   1200, "nViews",   4, 0.5, 4.5  );

  h_pt2pt4         = book(m_name,"pt2pt4","pt2", 10,40,140, "pt4", 10,40,80);

  h_leadHC        = new hCandidateHists(m_name+"leadHC_", "leadHC", m_detailStr);
  h_leadHC->initialize();

  h_sublHC        = new hCandidateHists(m_name+"sublHC_", "sublHC", m_detailStr);
  h_sublHC->initialize();

  h_leadGC        = new hCandidateHists(m_name+"leadGC_", "leadGC", m_detailStr);
  h_leadGC->initialize();

  h_sublGC        = new hCandidateHists(m_name+"sublGC_", "sublGC", m_detailStr);
  h_sublGC->initialize();

  h_HCJet1        = new JetHists(m_name+"HCJet1_", "flavorTag", "", "HCJet1 ");
  h_HCJet2        = new JetHists(m_name+"HCJet2_", "flavorTag", "", "HCJet2 ");
  h_HCJet3        = new JetHists(m_name+"HCJet3_", "flavorTag", "", "HCJet3 ");
  h_HCJet4        = new JetHists(m_name+"HCJet4_", "flavorTag", "", "HCJet4 ");
  h_HCJet1->initialize();
  h_HCJet2->initialize();
  h_HCJet3->initialize();
  h_HCJet4->initialize();

  h_jetsHC        = new JetHists(m_name+"HC_jets_" , "flavorTag", "", "HC_jet ");
  h_jetsHC->initialize();

  h_jetsOther        = new JetHists(m_name+"otherJets_" , "flavorTag", "", "otherJet ");
  h_jetsOther->initialize();

  h_muons        = new MuonHists(m_name+"Muons_" , "kinematic quality isolation", "", "muons");
  h_muons->initialize();

  h_promptMuons        = new MuonHists(m_name+"PromptMuons_" , "kinematic quality isolation", "", "prompt Muons");
  h_promptMuons->initialize();

  h_elecs        = new ElectronHists(m_name+"Elecs_" , "kinematic PID isolation");
  h_elecs->initialize();

  h_preSelJets        = new JetHists(m_name+"preSelJets_" , "flavorTag", "", "preSelJet ");
  h_preSelJets->initialize();

  if(true){
    h_nTruthElec   = book(m_name, "nTruthElec",    "nTruthElec",      3,     -0.5,     2.5 );
    h_nTruthMuon   = book(m_name, "nTruthMuon",    "nTruthMuon",      3,     -0.5,     2.5 );
    h_nTruthTau    = book(m_name, "nTruthTau",     "nTruthTau",       3,     -0.5,     2.5 );
    h_nTruthElMu   = book(m_name, "nTruthElMu",    "nTruthElMu",      3,     -0.5,     2.5 );
    h_nTruthLep    = book(m_name, "nTruthLep",     "nTruthLep",       3,     -0.5,     2.5 );
    h_nTruthCharm  = book(m_name, "nTruthCharm",   "nTruthCharm",     3,     -0.5,     2.5 );
    h_nTruthLF     = book(m_name, "nTruthLF",      "nTruthLF",        6,     -0.5,     5.5 );
  }

  h_eventWeight_s      = book(m_name, "eventWeight_s", "Event Weight",          400,        0,      0.2 );
  h_eventWeight_m      = book(m_name, "eventWeight_m", "Event Weight",           50,     -0.1,      0.5 );
  h_eventWeight_l      = book(m_name, "eventWeight_l", "Event Weight",           50,       -1,     10 );

  //tagging rates
  // h_TaggedBJets_pt       = book(m_name,"TaggedBJets_pt",     "TaggedBJets_pt",      200, 0 , 1000);
  // h_TruthBJets_pt        = book(m_name,"TruthBJets_pt",      "TruthBJets_pt",       200, 0 , 1000);
  // h_TaggedTruthBJets_pt  = book(m_name,"TaggedTruthBJets_pt","TaggedTruthBJets_pt", 200, 0 , 1000);

  
  h_metClusEt      = book(m_name, "met_clusEt",   "metClusEt",    100,     0,     100 );
  h_metClusEt_l    = book(m_name, "met_clusEt_l", "metClusEt",    100,     0,     500 );
  h_metClusPhi     = book(m_name, "met_clusPhi",  "metClusPhi",   100,    -3.2,     3.2 );

  h_metTrkEt       = book(m_name, "met_trkEt",   "metTrkEt",    100,     0,     100 );
  h_metTrkEt_l     = book(m_name, "met_trkEt_l", "metTrkEt",    100,     0,     500 );
  h_metTrkPhi      = book(m_name, "met_trkPhi",  "metTrkPhi",   100,    -3.2,     3.2 );

  h_m4j_l_truth    = book(m_name, "m4j_l_truth",  "m4j [GeV]",    190,      100,    2000 );

  if(m_doReweight){

    h_m4j_l_lhh00    = book(m_name, "m4j_l_lhh00",       "m4j [GeV]",    190,      100,    2000 );
    h_m4j_l_lhh02    = book(m_name, "m4j_l_lhh02",       "m4j [GeV]",    190,      100,    2000 );
    h_m4j_l_lhh10    = book(m_name, "m4j_l_lhh10",       "m4j [GeV]",    190,      100,    2000 );

    h_m4j_cor_l_lhh00      = book(m_name, "m4j_cor_l_lhh00",       "m4j (corrected) [GeV]",    190,      100,    2000 );
    h_m4j_cor_v_lhh00      = book(m_name, "m4j_cor_v_lhh00",       "m4j (corrected) [GeV]",    45, bins);
    h_m4j_cor_f_lhh00      = book(m_name, "m4j_cor_f_lhh00",       "bin", 45, 0,45);
    h_m4j_cor_l_lhh02      = book(m_name, "m4j_cor_l_lhh02",       "m4j (corrected) [GeV]",    190,      100,    2000 );
    h_m4j_cor_v_lhh02      = book(m_name, "m4j_cor_v_lhh02",       "m4j (corrected) [GeV]",    45, bins);
    h_m4j_cor_f_lhh02      = book(m_name, "m4j_cor_f_lhh02",       "bin", 45, 0,45);
    h_m4j_cor_l_lhh10      = book(m_name, "m4j_cor_l_lhh10",       "m4j (corrected) [GeV]",    190,      100,    2000 );
    h_m4j_cor_v_lhh10      = book(m_name, "m4j_cor_v_lhh10",       "m4j (corrected) [GeV]",    45, bins);
    h_m4j_cor_f_lhh10      = book(m_name, "m4j_cor_f_lhh10",       "bin", 45, 0,45);
    
    m_lhh_reweightFile = new TFile("$ROOTCOREBIN/data/XhhResolved/LambdaWeight.root", "READ");
  }

  h_mZmumu    = book(m_name, "mZmumu",  "m_{Z->#mu#mu} [GeV]",    40,      0,    200 );
  

  h_eventsPerRun = book(m_name, "eventsPerRun", "eventsPerRun", 1, 1, 2);
  h_eventsPerRun->SetCanExtend(TH1::kAllAxes);
  TFile* iLumiHistFile = new TFile("$ROOTCOREBIN/data/XhhResolved/ilumiHist2016.root", "READ");
  TH1F* lumi_histo = (TH1F*)iLumiHistFile->Get("lumi_histo");
  for(int bin = 1; bin<lumi_histo->GetNbinsX(); bin++) h_eventsPerRun->Fill(lumi_histo->GetXaxis()->GetBinLabel(bin),0);
  iLumiHistFile->Close();

  return StatusCode::SUCCESS;
}


void hh4bHists::record(EL::Worker* wk)
{
  HistogramManager::record(wk);
  h_leadHC     ->record(wk);
  h_sublHC     ->record(wk);

  h_leadGC     ->record(wk);
  h_sublGC     ->record(wk);

  h_HCJet1     ->record(wk);
  h_HCJet2     ->record(wk);
  h_HCJet3     ->record(wk);
  h_HCJet4     ->record(wk);

  h_jetsOther     ->record(wk);
  h_jetsHC        ->record(wk);

  h_muons         ->record(wk);
  h_promptMuons   ->record(wk);
  h_elecs         ->record(wk);

  h_preSelJets    ->record(wk);
}



//void hh4bHists::execute
StatusCode hh4bHists::execute(const EventComb* eventComb, const hh4bEvent* event, float eventWeight)
{
  ANA_CHECK(HistogramManager::execute() );
  if(m_debug) std::cout << "hh4bHists::execute()" << std::endl;
  
  //const EventView* eventView = eventComb->m_selectedView;
  
  h_NPV            ->Fill(event->m_eventInfo->m_npv               , eventWeight);
  h_mu_ave         ->Fill(event->m_eventInfo->m_averageMu , eventWeight);

  //unsigned int nJetPtCut = event->m_taggedJets->size() + event->m_nonTaggedJets->at("NonTagged").size();
  h_nJetOther      ->Fill(eventComb->m_nonHCJets->size()          , eventWeight);
  h_nJetOther_u    ->Fill(eventComb->m_nonHCJets->size()          , eventWeight/eventComb->m_selectedView->m_nJetWeight);
  h_nJetOther_l    ->Fill(eventComb->m_nonHCJets->size()          , eventWeight);
  h_nMuons         ->Fill(event->m_muons->size()                  , eventWeight);
  h_nPromptMuons   ->Fill(event->m_promptMuons->size()            , eventWeight);
  h_nPromptElecs   ->Fill(event->m_elecs->size()            , eventWeight);
  h_nLooseOther    ->Fill(event->m_looseTaggedJets->size()-4      , eventWeight);

  float m4j    = eventComb->m_selectedView->hhp4->M();
  float m4jcor = eventComb->m_selectedView->hhp4cor->M();
  h_m4j            ->Fill(m4j                           , eventWeight);
  h_m4j10          ->Fill(m4j                           , eventWeight);
  h_m4j25          ->Fill(m4j                           , eventWeight);
  h_m4j50          ->Fill(m4j                           , eventWeight);
  h_m4j_l          ->Fill(m4j                           , eventWeight);

  h_m_4j           ->Fill(m4j                           , eventWeight);
  h_m4j_cor        ->Fill(m4jcor                           , eventWeight);
  h_m4j_cor_l      ->Fill(m4jcor                           , eventWeight);
  h_m4j_cor_1      ->Fill(m4jcor                           , eventWeight);

  h_m4j_cor_v      ->Fill(m4jcor                           , eventWeight);
  int m4j_cor_f_bin = h_m4j_cor_v->GetXaxis()->FindBin(m4jcor);
  h_m4j_cor_f      ->Fill(m4j_cor_f_bin, eventWeight);

  //h_m4j_cor_v_s      ->Fill(m4jcor                           , eventWeight);
  //int m4j_cor_f_s_bin = h_m4j_cor_v_s->GetXaxis()->FindBin(m4jcor);
  //h_m4j_cor_f_s      ->Fill(m4j_cor_f_s_bin, eventWeight);

  h_Ht4j_l   ->Fill(eventComb->m_selectedView->m_Ht4j   , eventWeight);
  h_R_pt_4j_l->Fill(eventComb->m_selectedView->m_R_pt_4j, eventWeight);
  if(eventComb->m_selectedView->m_Ht4j < 300){
    h_lowHt_m4j_cor_l      ->Fill(m4jcor                           , eventWeight);
    h_lowHt_m4j_cor_v      ->Fill(m4jcor                           , eventWeight);
    h_lowHt_m4j_cor_f      ->Fill(m4j_cor_f_bin, eventWeight);
    //h_lowHt_m4j_cor_v_s      ->Fill(m4jcor                           , eventWeight);
    //h_lowHt_m4j_cor_f_s      ->Fill(m4j_cor_f_s_bin, eventWeight);
    h_lowHt_m12m34        ->Fill(eventComb->m_selectedView->m_leadHC->p4->M(), eventComb->m_selectedView->m_sublHC->p4->M(),  eventWeight);
  }else{
    h_highHt_m4j_cor_l      ->Fill(m4jcor                           , eventWeight);
    h_highHt_m4j_cor_v      ->Fill(m4jcor                           , eventWeight);
    h_highHt_m4j_cor_f      ->Fill(m4j_cor_f_bin, eventWeight);
    //h_highHt_m4j_cor_v_s      ->Fill(m4jcor                           , eventWeight);
    //h_highHt_m4j_cor_f_s      ->Fill(m4j_cor_f_s_bin, eventWeight);
    h_highHt_m12m34        ->Fill(eventComb->m_selectedView->m_leadHC->p4->M(), eventComb->m_selectedView->m_sublHC->p4->M(),  eventWeight);
  }

  //b-tag systematic variations
  if(m_doBTagSF){
    float nomSF = eventComb->m_selectedView->GetBTagSF(0);
    if(nomSF>0){
      float weightNoSF = eventWeight/nomSF;
      float newWeight = 1.0;
      for(unsigned int i=1; i<m_nBTagSFVar; i++){
	newWeight = weightNoSF*eventComb->m_selectedView->GetBTagSF(i);
	h_m4j_cor_l_bSF->at(i-1)->Fill(m4jcor       ,newWeight);
	h_m4j_cor_1_bSF->at(i-1)->Fill(m4jcor       ,newWeight);
	h_m4j_cor_v_bSF->at(i-1)->Fill(m4jcor       ,newWeight);
	h_m4j_cor_f_bSF->at(i-1)->Fill(m4j_cor_f_bin,newWeight);
	//h_m4j_cor_v_s_bSF->at(i-1)->Fill(m4jcor       ,newWeight);
	//h_m4j_cor_f_s_bSF->at(i-1)->Fill(m4j_cor_f_s_bin,newWeight);
      }
    }
  }
  
  //trig SF variations
  if(eventComb->m_trigSF){
    float trigSFUp   = (eventComb->m_trigSF + eventComb->m_trigSFErr);
    float trigSFDown = (eventComb->m_trigSF - eventComb->m_trigSFErr);
    if(trigSFUp   > 1) trigSFUp   = 1.0;
    if(trigSFDown < 0) trigSFDown = 0.0;

    float weight_trigSFUp   = (eventWeight/eventComb->m_trigSF * trigSFUp);
    float weight_trigSFDown = (eventWeight/eventComb->m_trigSF * trigSFDown);
    h_m4j_cor_l_tSF_up  ->Fill(m4jcor       , weight_trigSFUp  );
    h_m4j_cor_l_tSF_down->Fill(m4jcor       , weight_trigSFDown);
    h_m4j_cor_1_tSF_up  ->Fill(m4jcor       , weight_trigSFUp  );
    h_m4j_cor_1_tSF_down->Fill(m4jcor       , weight_trigSFDown);
    h_m4j_cor_v_tSF_up  ->Fill(m4jcor       , weight_trigSFUp  );
    h_m4j_cor_v_tSF_down->Fill(m4jcor       , weight_trigSFDown);
    h_m4j_cor_f_tSF_up  ->Fill(m4j_cor_f_bin, weight_trigSFUp  );
    h_m4j_cor_f_tSF_down->Fill(m4j_cor_f_bin, weight_trigSFDown);

    //h_m4j_cor_v_s_tSF_up  ->Fill(m4jcor       , weight_trigSFUp  );
    //h_m4j_cor_v_s_tSF_down->Fill(m4jcor       , weight_trigSFDown);
    //h_m4j_cor_f_s_tSF_up  ->Fill(m4j_cor_f_s_bin, weight_trigSFUp  );
    //h_m4j_cor_f_s_tSF_down->Fill(m4j_cor_f_s_bin, weight_trigSFDown);
  }

  h_m_4j_cor       ->Fill(m4jcor                           , eventWeight);
  h_m4j25_cor      ->Fill(m4jcor                           , eventWeight);
  h_m4j50_cor      ->Fill(m4jcor                           , eventWeight);

  h_m4j_diff        ->Fill(m4jcor-m4j                           , eventWeight);

  float m4jcorZ = eventComb->m_selectedView->hhp4corZ->M();
  h_m4j_cor_Z        ->Fill(m4jcorZ                           , eventWeight);
  h_m4j_cor_Z_l      ->Fill(m4jcorZ                           , eventWeight);
  h_m4j_cor_Z_v      ->Fill(m4jcorZ                           , eventWeight);
  int m4j_cor_Z_f_bin = h_m4j_cor_Z_v->GetXaxis()->FindBin(m4jcorZ);
  h_m4j_cor_Z_f      ->Fill(m4j_cor_Z_f_bin, eventWeight);


  float m4jcorH = eventComb->m_selectedView->hhp4corH->M();
  h_m4j_cor_H        ->Fill(m4jcorH                           , eventWeight);
  h_m4j_cor_H_l      ->Fill(m4jcorH                           , eventWeight);
  h_m4j_cor_H_v      ->Fill(m4jcorH                           , eventWeight);
  int m4j_cor_H_f_bin = h_m4j_cor_H_v->GetXaxis()->FindBin(m4jcorH);
  h_m4j_cor_H_f      ->Fill(m4j_cor_H_f_bin, eventWeight);

  h_trigBits->Fill(eventComb->m_trigBits, eventWeight);



  h_dEta_hh      ->Fill(eventComb->m_selectedView->m_dEta                           , eventWeight);
  h_abs_dEta_hh  ->Fill(fabs(eventComb->m_selectedView->m_dEta)                     , eventWeight);
  h_dPhi_hh      ->Fill(fabs(eventComb->m_selectedView->m_dPhi)                     , eventWeight);
  h_dR_hh        ->Fill(eventComb->m_selectedView->m_dR                             , eventWeight);
  h_Pt_hh        ->Fill(eventComb->m_selectedView->hhp4->Pt()                       , eventWeight);
  h_R_dRdR       ->Fill(eventComb->m_selectedView->m_R_dRdR                         , eventWeight);
  
  h_dEta_gg      ->Fill(eventComb->m_selectedView->m_dEta_gg                           , eventWeight);
  h_abs_dEta_gg  ->Fill(fabs(eventComb->m_selectedView->m_dEta_gg)                     , eventWeight);
  h_dPhi_gg      ->Fill(fabs(eventComb->m_selectedView->m_dPhi_gg)                     , eventWeight);
  h_dR_gg        ->Fill(eventComb->m_selectedView->m_dR_gg                             , eventWeight);
  h_Pt_gg        ->Fill(eventComb->m_selectedView->ggp4->Pt()                          , eventWeight);
  h_R_dRdR_gg    ->Fill(eventComb->m_selectedView->m_R_dRdR_gg                         , eventWeight);  

  h_GCdR_diff    ->Fill(eventComb->m_selectedView->m_GCdR_diff                         , eventWeight);
  h_GCdR_sum     ->Fill(eventComb->m_selectedView->m_GCdR_sum                          , eventWeight);

  h_HCdR_diff    ->Fill(eventComb->m_selectedView->m_HCdR_diff                         , eventWeight);
  h_HCdR_sum     ->Fill(eventComb->m_selectedView->m_HCdR_sum                          , eventWeight);

  h_nbjets         ->Fill(eventComb->m_pseudoTaggedJets.size()-4                           , eventWeight);
  h_njets          ->Fill(event->m_jets->size()                           , eventWeight);
  h_ht             ->Fill(event->m_ht                           , eventWeight);
  h_ht_l           ->Fill(event->m_ht                           , eventWeight);
  h_mht             ->Fill(event->m_mht                           , eventWeight);
  h_mht_l           ->Fill(event->m_mht                           , eventWeight);
  h_xhh            ->Fill(eventComb->m_selectedView->m_xhh                           , eventWeight);
  h_dhh            ->Fill(eventComb->m_selectedView->m_dhh                           , eventWeight);
  h_lhh            ->Fill(eventComb->m_selectedView->m_lhh                           , eventWeight);
  h_rhh            ->Fill(eventComb->m_selectedView->m_rhh                           , eventWeight);
  h_rhhMin         ->Fill(eventComb->m_RhhMinView->m_rhh             , eventWeight);

  h_hhJetEtaSum2   ->Fill(eventComb->m_selectedView->m_hhJetEtaSum2                  , eventWeight);
  h_HCJetAbsEta    ->Fill(eventComb->m_selectedView->m_HCJetAbsEta                   , eventWeight);
  h_HCJetAR        ->Fill(eventComb->m_selectedView->m_HCJetAR                       , eventWeight);

  h_HCJetPtE1      ->Fill(eventComb->m_selectedView->m_HCJetPtE1                     , eventWeight);
  h_HCJetPtE2      ->Fill(eventComb->m_selectedView->m_HCJetPtE2                     , eventWeight);

  float xwt_limited = (event->m_xwt < 12) ? event->m_xwt : 12;
  h_xwt            ->Fill(xwt_limited    , eventWeight);
  h_xwt_ave        ->Fill(event->m_xwt_ave                           , eventWeight);
  h_xtt            ->Fill(event->m_xtt                           , eventWeight);

  // if(eventComb->m_nonHCJets->size() > 1){
  //   h_xtt_2j            ->Fill(eventComb->m_xtt                           , eventWeight);
  //   h_xtt_2j_ave        ->Fill(eventComb->m_xtt_ave                           , eventWeight);
  //   h_nTopCandsAll_2j   ->Fill(eventComb->m_nTopCandsAll             , eventWeight);
  //   h_nTopCands_2j      ->Fill(eventComb->m_nTopCands                , eventWeight);
  //   h_nTopCands3_2j     ->Fill(eventComb->m_nTopCands3                , eventWeight);
  // }
  
  h_m12m34        ->Fill(eventComb->m_selectedView->m_leadHC->p4->M(), eventComb->m_selectedView->m_sublHC->p4->M(),  eventWeight);
  h_GC_m12m34     ->Fill(eventComb->m_selectedView->m_leadGC->p4->M(), eventComb->m_selectedView->m_sublGC->p4->M(),  eventWeight);
  h_dR12dR34      ->Fill(eventComb->m_selectedView->m_leadHC->m_dRjj,  eventComb->m_selectedView->m_sublHC->m_dRjj,   eventWeight);
  h_GC_dR12dR34   ->Fill(eventComb->m_selectedView->m_leadGC->m_dRjj,  eventComb->m_selectedView->m_sublGC->m_dRjj,   eventWeight);

  h_m4jnJetOther  ->Fill(m4j, eventComb->m_nonHCJets->size(), eventWeight);
  h_m4jLeadHCandPt->Fill(m4j, eventComb->m_selectedView->m_leadHC->p4->Pt(), eventWeight);
  h_m4jSublHCandPt->Fill(m4j, eventComb->m_selectedView->m_sublHC->p4->Pt(), eventWeight);
  h_m4jHCdEta     ->Fill(m4j, fabs(eventComb->m_selectedView->m_dEta),        eventWeight);
  h_m4jHCdPhi     ->Fill(m4j, fabs(eventComb->m_selectedView->m_dPhi),        eventWeight);
  h_m4jLeadHCdRjj ->Fill(m4j, eventComb->m_selectedView->m_leadHC->m_dRjj, eventWeight);
  h_m4jSublHCdRjj ->Fill(m4j, eventComb->m_selectedView->m_sublHC->m_dRjj, eventWeight);

  h_m4jLeadGCdRjj ->Fill(m4j, eventComb->m_selectedView->m_leadGC->m_dRjj, eventWeight);
  h_m4jSublGCdRjj ->Fill(m4j, eventComb->m_selectedView->m_sublGC->m_dRjj, eventWeight);

  h_m4jLeadPtHCandPt->Fill(m4j, eventComb->m_selectedView->m_leadPtHC->p4->Pt(), eventWeight);
  h_m4jSublPtHCandPt->Fill(m4j, eventComb->m_selectedView->m_sublPtHC->p4->Pt(), eventWeight);
  h_m4jLeadPtHCdRjj ->Fill(m4j, eventComb->m_selectedView->m_leadPtHC->m_dRjj, eventWeight);
  h_m4jSublPtHCdRjj ->Fill(m4j, eventComb->m_selectedView->m_sublPtHC->m_dRjj, eventWeight);

  h_m4j_nViews    ->Fill(m4j, eventComb->m_nViews, eventWeight);

  h_pt2pt4->Fill(eventComb->m_HCJets->at(1)->p4.Pt(),eventComb->m_HCJets->at(3)->p4.Pt(), eventWeight);

  h_leadHC     ->execute(*(eventComb->m_selectedView->m_leadHC)     , eventWeight);
  h_sublHC     ->execute(*(eventComb->m_selectedView->m_sublHC)     , eventWeight);

  h_leadGC     ->execute(*(eventComb->m_selectedView->m_leadGC)     , eventWeight);
  h_sublGC     ->execute(*(eventComb->m_selectedView->m_sublGC)     , eventWeight);

  h_HCJet1->execute(eventComb->m_HCJets->at(0), eventWeight);
  h_HCJet2->execute(eventComb->m_HCJets->at(1), eventWeight);
  h_HCJet3->execute(eventComb->m_HCJets->at(2), eventWeight);
  h_HCJet4->execute(eventComb->m_HCJets->at(3), eventWeight);

  // if(eventComb->m_HCJets->at(3)->p4.Pt()<40 && 
  //    fabs(eventComb->m_HCJets->at(3)->p4.Pz())<10) {
  //   cout << "Pt: " << eventComb->m_HCJets->at(3)->p4.Pt() << " Pz: " << eventComb->m_HCJets->at(3)->p4.Pz() << " E: " << eventComb->m_HCJets->at(3)->p4.E() << endl;
  // }

  for(const Jet* hJet : *eventComb->m_HCJets)
    h_jetsHC      ->execute(hJet   , eventWeight);

  for(const Jet* oJet : *eventComb->m_nonHCJets)
    h_jetsOther   ->execute(oJet   , eventWeight);

  for(unsigned int iMuon = 0; iMuon < event->m_muons->size(); ++iMuon){
    const xAH::Muon* thisMuon = &(event->m_muons->at(iMuon));
    h_muons   ->execute(thisMuon   , eventWeight);
  }

  for(const xAH::Muon* pMuon : *event->m_promptMuons)
    h_promptMuons   ->execute(pMuon   , eventWeight);

  for(unsigned int iElec = 0; iElec < event->m_elecs->size(); ++iElec){
    const xAH::Electron* thisElec = &(event->m_elecs->at(iElec));
    h_elecs   ->execute(thisElec   , eventWeight);
  }


  for(unsigned int iJet = 0; iJet < event->m_jets->size(); ++iJet){
    Jet* jet = &(event->m_jets->at_nonConst(iJet));
    h_preSelJets      ->execute(jet   , eventWeight);
  }

  h_eventWeight_s->Fill(eventWeight, 1);
  h_eventWeight_m->Fill(eventWeight, 1);
  h_eventWeight_l->Fill(eventWeight, 1);

  float metClusEt = event->m_met->m_metFinalClus;
  h_metClusEt    ->Fill(metClusEt,  eventWeight);
  h_metClusEt_l  ->Fill(metClusEt,  eventWeight);
  h_metClusPhi   ->Fill(event->m_met->m_metFinalClusPhi, eventWeight);

  float metTrkEt = event->m_met->m_metFinalTrk;
  h_metTrkEt    ->Fill(metTrkEt, eventWeight);
  h_metTrkEt_l  ->Fill(metTrkEt, eventWeight);
  h_metTrkPhi   ->Fill(event->m_met->m_metFinalTrkPhi, eventWeight);


  
  if(event->m_mc && false){
      
    //
    // Get the two higgs indices
    //
    unsigned int hIndex1 = 0;
    unsigned int hIndex2 = 0;
    unsigned int nHiggs  = 0;
    for(unsigned int iTruth = 0; iTruth < event->m_truth->size(); ++iTruth){
      const xAH::TruthPart& thisTruth = event->m_truth->at(iTruth);
      int thisPDGID = thisTruth.pdgId;
      
      if(thisPDGID == 25){
	if(nHiggs == 0)  hIndex1 = iTruth;
	if(nHiggs == 1)  hIndex2 = iTruth;
	++nHiggs;
      }
      
    }

    if(nHiggs == 2){
      float mhh_truth = (event->m_truth->at(hIndex1).p4+event->m_truth->at(hIndex2).p4).M();
      h_m4j_l_truth      ->Fill(mhh_truth, eventWeight);
      
      if(m_doReweight){
	TH1F* hist_l00    = (TH1F*)(m_lhh_reweightFile->Get("Weight_mHH_lambda00"));
	TH1F* hist_l02    = (TH1F*)(m_lhh_reweightFile->Get("Weight_mHH_lambda02"));
	TH1F* hist_l10    = (TH1F*)(m_lhh_reweightFile->Get("Weight_mHH_lambda10"));
	int mhh_truth_bin = hist_l00->FindBin(mhh_truth);
	
	float weight_l00  = hist_l00->GetBinContent(mhh_truth_bin);
	float weight_l02  = hist_l02->GetBinContent(mhh_truth_bin);
	float weight_l10  = hist_l10->GetBinContent(mhh_truth_bin);
	cout << "Setting Truth" << endl;
	h_m4j_l_lhh00          ->Fill(m4j                           , eventWeight*weight_l00);
	h_m4j_l_lhh02          ->Fill(m4j                           , eventWeight*weight_l02);
	h_m4j_l_lhh10          ->Fill(m4j                           , eventWeight*weight_l10);

	h_m4j_cor_l_lhh00      ->Fill(m4jcor                        , eventWeight*weight_l00);
	h_m4j_cor_l_lhh02      ->Fill(m4jcor                        , eventWeight*weight_l02);
	h_m4j_cor_l_lhh10      ->Fill(m4jcor                        , eventWeight*weight_l10);

	h_m4j_cor_v_lhh00      ->Fill(m4jcor                        , eventWeight*weight_l00);
	h_m4j_cor_v_lhh02      ->Fill(m4jcor                        , eventWeight*weight_l02);
	h_m4j_cor_v_lhh10      ->Fill(m4jcor                        , eventWeight*weight_l10);

	h_m4j_cor_f_lhh00      ->Fill(m4j_cor_f_bin                 , eventWeight*weight_l00);
	h_m4j_cor_f_lhh02      ->Fill(m4j_cor_f_bin                 , eventWeight*weight_l02);
	h_m4j_cor_f_lhh10      ->Fill(m4j_cor_f_bin                 , eventWeight*weight_l10);

      }
      
    }else{
      //cout << "ERROR::nHiggs " << nHiggs << endl;;
    }
    
  }


  if(event->m_mc){
    unsigned int nElec  = 0;
    unsigned int nMuon  = 0;
    unsigned int nTau   = 0;
    unsigned int nCharm = 0;
    unsigned int nLF    = 0;

    for(unsigned int iTruth = 0; iTruth < event->m_truth->size(); ++iTruth){
      const xAH::TruthPart* thisTruth = &(event->m_truth->at(iTruth));
      unsigned int absPdgId = abs(thisTruth->pdgId);
      if(absPdgId == 11)  ++nElec;
      if(absPdgId == 13)  ++nMuon;
      if(absPdgId == 15)  ++nTau;
      if(absPdgId ==  4)  ++nCharm;
      //if(absPdgId ==  5)  cout << " Have a bjet" << endl;

      if(absPdgId  <  4)  ++nLF;
    }

    h_nTruthElec   -> Fill( nElec , eventWeight);
    h_nTruthMuon   -> Fill( nMuon , eventWeight);
    h_nTruthTau    -> Fill( nTau  , eventWeight);    
    h_nTruthElMu   -> Fill( (nElec + nMuon) , eventWeight);
    h_nTruthLep    -> Fill( (nElec + nMuon + nTau) , eventWeight);
    h_nTruthCharm  -> Fill( nCharm , eventWeight);
    h_nTruthLF     -> Fill( nLF    , eventWeight);

  }


  //cout << eventWeight << endl;


  // for(const Jet* jet : *event->m_taggedJets)
  //   h_TaggedBJets_pt->Fill(jet->p4.Pt(), eventWeight);  

  // for(const Jet* jet : *event->m_TruthBJets)
  //   h_TruthBJets_pt->Fill(jet->p4.Pt(), eventWeight);

  // for(const Jet* jet : *event->m_TaggedTruthBJets)
  //   h_TaggedTruthBJets_pt->Fill(jet->p4.Pt(), eventWeight);

  h_mZmumu->Fill(event->m_mZmumu, eventWeight);

  h_eventsPerRun->Fill(std::to_string(event->m_eventInfo->m_runNumber).c_str(),eventWeight);

  return StatusCode::SUCCESS;
}


StatusCode hh4bHists::finalize()
{
  if(m_debug) std::cout << "hh4bHists::finalize()" << std::endl;
  
  HistogramManager::finalize();

  h_leadHC     ->finalize();
  delete h_leadHC;

  h_sublHC     ->finalize();
  delete h_sublHC;

  h_leadGC     ->finalize();
  delete h_leadGC;

  h_sublGC     ->finalize();
  delete h_sublGC;

  h_HCJet1->finalize();
  delete h_HCJet1;
  h_HCJet2->finalize();
  delete h_HCJet2;
  h_HCJet3->finalize();
  delete h_HCJet3;
  h_HCJet4->finalize();
  delete h_HCJet4;

  h_jetsHC->finalize();
  delete h_jetsHC;

  h_jetsOther   ->finalize();
  delete h_jetsOther;

  h_muons   ->finalize();
  delete h_muons;

  h_promptMuons   ->finalize();
  delete h_promptMuons;

  h_elecs ->finalize();
  delete h_elecs;

  h_preSelJets->finalize();
  delete h_preSelJets;

  return StatusCode::SUCCESS;
}
