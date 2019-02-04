
def setGRL(year=""):
    GRL = "$ROOTCOREBIN/data/XhhResolved/data15_13TeV.periodAllYear_DetStatus-v79-repro20-02_DQDefects-00-02-02_PHYS_StandardGRL_All_Good.xml"
    if year == "2016":
        GRL = "$ROOTCOREBIN/data/XhhResolved/data16_13TeV.periodAllYear_DetStatus-v87-pro20-20_DQDefects-00-02-04_PHYS_StandardGRL_All_Good_25ns_BjetHLT.xml"
    return GRL

def setLumi(year="2015"):
    lumi = 3237.49
    if year == "2016":
        lumi = 24321.9
    return lumi

def setTagger(tagger):
    if tagger == "MV2c20":#these are from 2015 recommendations for mc15a/b
        MV2CutValue    = -0.0436
        MV2CutValueQCD = -0.7887
    if tagger == "MV2c10":#these are from 2016 recommendations for mc15c
        #https://twiki.cern.ch/twiki/bin/view/AtlasProtected/BTaggingBenchmarks#MV2c10_tagger_added_on_11th_May
        MV2CutValue    = 0.8244273
        #MV2CutValueQCD = 0.1758
        MV2CutValueQCD = -1.1
    return (MV2CutValue, MV2CutValueQCD)

#retrieve cut values for input to optimizeMDCs.cxx
def getCuts(cutFile):#cutFile contains comma delimited lists of each variable in the MDC optimization with newline char at end of each line
    f = open(cutFile)
    leadPtCuts   = f.readline()[:-1]
    sublPtCuts   = f.readline()[:-1]
    hCandEtaCuts = f.readline()[:-1]
    return (leadPtCuts, sublPtCuts, hCandEtaCuts)

def setRegions(variation):
    leadMass_SR = 120.0
    sublMass_SR = 110.0
    radius_SR = 1.6
    radius_CR = 30.0 #Nominal
    #radius_CR = 27.0 #Small
    radius_SB = 45.0
    inner_SB  = 0.0

    # radius_SB = 85
    # radius_CR = 40
    
    CR_shift  = 1.03
    SB_shift  = 1.05

    # CR_shift  = 1.03
    # SB_shift  = 1.17

    doTightQCDTag = False
    doLooseQCDTag = False
    leadHCmassCut = 0.0
    sublHCmassCut = 0.0
    DhhCut        = 10000.0

    if variation == "LowMass":
        CR_shift = 1.1
    if variation == "HighMass":
        CR_shift = 0.9
    if variation == "Tight":
        doTightQCDTag = True
    if variation == "Loose":
        doLooseQCDTag = True
    if variation == "UnrestrictedSB":
        radius_SB     = 10000.0
    if variation == "CloseSB":
        radius_SB = 58.0
    if variation == "FarSB":
        inner_SB = 58.0
    return (leadMass_SR, sublMass_SR, radius_SR, radius_CR, radius_SB, inner_SB, CR_shift, SB_shift, doTightQCDTag, doLooseQCDTag, leadHCmassCut, sublHCmassCut, DhhCut)

    #return (leadMass_SR, sublMass_SR, radius_SR, radius_CR, radius_SB, CR_shift, SB_shift)
        
