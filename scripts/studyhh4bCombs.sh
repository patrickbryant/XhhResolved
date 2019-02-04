#!/bin/bash
##############################################
## Top Level Resolved hh4b Analysis Script. ##
##############################################
## Analysis Outline:
##     1. Create nTuples
##         a. Data
##         b. MC (RSG, 2HDM, ttbar, Z+jets)
##     2. Download nTuples
##     3. Process Signal nTuples
##         a. Generate file list
##         b. Process Signal Samples in parallel 
##              (run RSG masses in parallel for each coupling, run nonResonant files separately, combine weighted by nEventsInFile/nEventsInSample)
##     4. Process Data/ttbar MC
##         a. Process Data/ttbar files in parallel
##         b. Combine hists for each sample 
##              (for data just hadd them, for MC, need to weight by nEventsInFile/nEventsInSample)
##         c. Calculate mu_qcd and kinematic weights
##         d. Iterate a-c ~2-3x
##     5. Make plots
##     6. Make limit setting inputs (m4j distributions with systematic variations for background and signal)
##         
#---------------------------------------------------------------------------------------------------------------------------------------

runCommands=true #Set false to echo all commands that will be run if this is true.


# nTuple=01-02-06
# outDir=hists_SB45CR30_GC_pt40_fq0.066_ft0.033
nTuple=02-02-00
weights=pt1_pt4_eta_sumdiffdR_vecMDC7
outDir=hists_${weights}
threeTag=''
outDir="${outDir}${threeTag}"

script=config_hh4bCombUnique.py
tagger=MV2c10
years=( 2016 )
scope=group.phys-exotics
mod=''

# 1.---------------------------------------------------------------------------
nTupleSubmitData=false
nTupleSubmitMC=false
# 2.---------------------------------------------------------------------------
download=false
# 3.---------------------------------------------------------------------------
runSignal=false
signalIndices=( 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 ) #signal samples to be run. See below
#signalIndices=( 20 21 22 23 24 25 )
#signalIndices=( 0 ) #signal samples to be run. See below
# 4.---------------------------------------------------------------------------
runData=false
weightsOnly=false
iterations=( 0 1 2 3 4 ) #iterations to run
variations=( "Nominal" )
# 5.---------------------------------------------------------------------------
plotIterations=( 0 4 )
plotMC=false
plotData=false
plotVariations=( "Nominal" )
# 6.---------------------------------------------------------------------------
runShapeSystematics=false
runLimitInputs=false
plotLimitInputs=true
# 7.---------------------------------------------------------------------------
setLimits=false

### Configuration ###
# Paths to nTuples and working directory for hists and plots
t3data=/share/t3data3/johnda/samples/XhhOutput
workDir=$PWD


function runCommand { #first argument is command to be run. If env var runCommands, run the command, otherwise, just print it for debugging
    echo $1
    echo
    if $runCommands; then
	eval $1
    fi
    echo $1 >> runLog.txt #Log all commands to check progress
}
rm runLog.txt
#---------------------------------------------------------------------------------------------------------------------------------------

#########################################
## 1. Submit nTuple production to grid ##
#########################################
if $nTupleSubmitData; then
    runCommand "xAH_run.py --files XhhCommon/scripts/grid_samples_EXOT8_data.txt --inputList \
                           --config XhhCommon/scripts/miniNTuple_config.py \
                           -f --inputDQ2 prun \
                           --optGridOutputSampleName='group.phys-exotics.%in:name[1]%.%in:name[2]%.%in:name[3]%.hh4b-$nTuple' --optSubmitFlags='--official'"
fi

if $nTupleSubmitMC; then
    runCommand "xAH_run.py --files XhhCommon/scripts/grid_samples_EXOT8_mc.txt --isMC --inputList \
  	                   --config XhhCommon/scripts/miniNTuple_config.py \
                           -f --inputDQ2 prun \
                           --optGridOutputSampleName='group.phys-exotics.%in:name[1]%.%in:name[2]%.%in:name[3]%.hh4b-$nTuple' --optSubmitFlags='--official'"
fi

#---------------------------------------------------------------------------------------------------------------------------------------

#########################
## 2. Download nTuples ##
#########################

RSG300c10=group.phys-exotics.mc15_13TeV.301488.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M300.hh4b-${nTuple}_MiniNTuple.root
RSG400c10=group.phys-exotics.mc15_13TeV.301489.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M400.hh4b-${nTuple}_MiniNTuple.root
RSG500c10=group.phys-exotics.mc15_13TeV.301490.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M500.hh4b-${nTuple}_MiniNTuple.root
RSG600c10=group.phys-exotics.mc15_13TeV.301491.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M600.hh4b-${nTuple}_MiniNTuple.root
RSG700c10=group.phys-exotics.mc15_13TeV.301492.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M700.hh4b-${nTuple}_MiniNTuple.root
RSG800c10=group.phys-exotics.mc15_13TeV.301493.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M800.hh4b-${nTuple}_MiniNTuple.root
RSG900c10=group.phys-exotics.mc15_13TeV.301494.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M900.hh4b-${nTuple}_MiniNTuple.root
RSG1000c10=group.phys-exotics.mc15_13TeV.301495.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1000.hh4b-${nTuple}_MiniNTuple.root
RSG1100c10=group.phys-exotics.mc15_13TeV.301496.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1100.hh4b-${nTuple}_MiniNTuple.root
RSG1200c10=group.phys-exotics.mc15_13TeV.301497.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1200.hh4b-${nTuple}_MiniNTuple.root
RSG=( $RSG300c10 $RSG400c10 $RSG500c10 $RSG600c10 $RSG700c10 $RSG800c10 $RSG900c10 $RSG1000c10 $RSG1100c10 $RSG1200c10 )

HDM260=group.phys-exotics.mc15_13TeV.343394.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m260_4b.hh4b-${nTuple}_MiniNTuple.root
HDM300=group.phys-exotics.mc15_13TeV.343395.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m300_4b.hh4b-${nTuple}_MiniNTuple.root
HDM400=group.phys-exotics.mc15_13TeV.343396.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m400_4b.hh4b-${nTuple}_MiniNTuple.root
HDM500=group.phys-exotics.mc15_13TeV.343397.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m500_4b.hh4b-${nTuple}_MiniNTuple.root
HDM600=group.phys-exotics.mc15_13TeV.343398.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m600_4b.hh4b-${nTuple}_MiniNTuple.root
HDM700=group.phys-exotics.mc15_13TeV.343399.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m700_4b.hh4b-${nTuple}_MiniNTuple.root
HDM800=group.phys-exotics.mc15_13TeV.343400.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m800_4b.hh4b-${nTuple}_MiniNTuple.root
HDM900=group.phys-exotics.mc15_13TeV.343401.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m900_4b.hh4b-${nTuple}_MiniNTuple.root
HDM1000=group.phys-exotics.mc15_13TeV.343402.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m1000_4b.hh4b-${nTuple}_MiniNTuple.root
HDM1100=group.phys-exotics.mc15_13TeV.343403.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m1100_4b.hh4b-${nTuple}_MiniNTuple.root
HDM1200=group.phys-exotics.mc15_13TeV.343404.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m1200_4b.hh4b-${nTuple}_MiniNTuple.root
HDM=( $HDM260 $HDM300 $HDM400 $HDM500 $HDM600 $HDM700 $HDM800 $HDM900 $HDM1000 $HDM1100 $HDM1200 )

SMNR=group.phys-exotics.mc15_13TeV.342619.aMcAtNloHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_hh_4b.hh4b-${nTuple}_MiniNTuple.root

ttbarAllHad=${scope}.mc15_13TeV.410007.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_allhad.hh4b-${nTuple}_MiniNTuple.root
ttbarNonAllHad=${scope}.mc15_13TeV.410000.PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_nonallhad.hh4b-${nTuple}_MiniNTuple.root


dataD=${scope}.data15_13TeV.periodD.physics_Main.hh4b-${nTuple}_MiniNTuple.root
dataE=${scope}.data15_13TeV.periodE.physics_Main.hh4b-${nTuple}_MiniNTuple.root
dataF=${scope}.data15_13TeV.periodF.physics_Main.hh4b-${nTuple}_MiniNTuple.root
dataG=${scope}.data15_13TeV.periodG.physics_Main.hh4b-${nTuple}_MiniNTuple.root
dataH=${scope}.data15_13TeV.periodH.physics_Main.hh4b-${nTuple}_MiniNTuple.root
dataJ=${scope}.data15_13TeV.periodJ.physics_Main.hh4b-${nTuple}_MiniNTuple.root
data=( $dataD $dataE $dataF $dataG $dataH $dataJ )

dataA=${scope}.data16_13TeV.periodA.physics_Main.hh4b-${nTuple}_MiniNTuple.root
dataB=${scope}.data16_13TeV.periodB.physics_Main.hh4b-${nTuple}_MiniNTuple.root
data2016=( $dataA $dataB )


if $download; then
    if [ ! -d "$t3data/$nTuple" ]; then
        runCommand "mkdir $t3data/$nTuple"
    fi
    
    runCommand "cd $t3data/$nTuple"

    for sample in "${RSG[@]}"; do
        runCommand "rucio download group.phys-exotics:$sample"
    done

    for sample in "${HDM[@]}"; do
	runCommand "rucio download group.phys-exotics:$sample"
    done

    runCommand "rucio download group.phys-exotics:$SMNR"
    runCommand "hadd nonResonant.hh4b-${nTuple}_MiniNTuple.root $SMNR/*"

    runCommand "rucio download group.phys-exotics:$ttbarAllHad"

    runCommand "rucio download group.phys-exotics:$ttbarNonAllHad"

    for sample in "${data[@]}"; do
	runCommand "rucio download group.phys-exotics:$sample"
    done

    periods=( D E F G H J )
    for period in "${periods[@]}"
    do
	runCommand "hadd period$period.hh4b-${nTuple}_MiniNTuple.root group.phys-exotics.data15_13TeV.period$period.physics_Main.hh4b-${nTuple}_MiniNTuple.root/*"
    done

    runCommand "cd $workDir"

fi


#---------------------------------------------------------------------------------------------------------------------------------------

###############################
## 3. Process Signal nTuples ##
###############################
HDM260=${scope}.mc15_13TeV.343394.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m260_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM300=${scope}.mc15_13TeV.343395.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m300_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM400=${scope}.mc15_13TeV.343396.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m400_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM500=${scope}.mc15_13TeV.343397.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m500_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM600=${scope}.mc15_13TeV.343398.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m600_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM700=${scope}.mc15_13TeV.343399.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m700_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM800=${scope}.mc15_13TeV.343400.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m800_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM900=${scope}.mc15_13TeV.343401.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m900_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM1000=${scope}.mc15_13TeV.343402.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m1000_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM1100=${scope}.mc15_13TeV.343403.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m1100_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM1200=${scope}.mc15_13TeV.343404.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m1200_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM1300=${scope}.mc15_13TeV.343405.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m1300_4b.hh4b-${nTuple}_MiniNTuple.root/*
HDM1400=${scope}.mc15_13TeV.343406.MadGraphHerwigppEvtGen_UEEE5_CTEQ6L1_CT10ME_Xhh_m1400_4b.hh4b-${nTuple}_MiniNTuple.root/*

RSG300=${scope}.mc15_13TeV.301488.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M300.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG400=${scope}.mc15_13TeV.301489.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M400.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG500=${scope}.mc15_13TeV.301490.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M500.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG600=${scope}.mc15_13TeV.301491.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M600.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG700=${scope}.mc15_13TeV.301492.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M700.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG800=${scope}.mc15_13TeV.301493.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M800.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG900=${scope}.mc15_13TeV.301494.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M900.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG1000=${scope}.mc15_13TeV.301495.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1000.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG1100=${scope}.mc15_13TeV.301496.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1100.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG1200=${scope}.mc15_13TeV.301497.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1200.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG1300=${scope}.mc15_13TeV.301498.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1300.hh4b${mod}-${nTuple}_MiniNTuple.root/*
RSG1400=${scope}.mc15_13TeV.301499.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1400.hh4b${mod}-${nTuple}_MiniNTuple.root/*
nonResonant=nonResonant.hh4b-${nTuple}_MiniNTuple.root

signalSamples=( $RSG300 $RSG400 $RSG500 $RSG600 $RSG700 $RSG800 $RSG900 $RSG1000 $RSG1100 $RSG1200 $nonResonant $HDM260 $RSG1300 $RSG1400 
                $HDM300 $HDM400 $HDM500 $HDM600 $HDM700 $HDM800 $HDM900 $HDM1000 $HDM1100 $HDM1200 $HDM1300 $HDM1400 )
signalNames=( RSG300 RSG400 RSG500 RSG600 RSG700 RSG800 RSG900 RSG1000 RSG1100 RSG1200 nonResonant HDM260 RSG1300 RSG1400 
              HDM300 HDM400 HDM500 HDM600 HDM700 HDM800 HDM900 HDM1000 HDM1100 HDM1200 HDM1300 HDM1400 )


if [ ! -d "$outDir-$nTuple" ]; then
    runCommand "mkdir $outDir-$nTuple"
fi

if $runSignal; then
for year in "${years[@]}"; do
for i in "${signalIndices[@]}"; do
    runCommand "xAH_run.py  --files $t3data/$nTuple/${signalSamples[i]} \
                            --config XhhResolved/scripts/${script} \
                            --extraOptions='--tagger ${tagger} --year ${year} ${threeTag}'
                            --submitDir $outDir-$nTuple/${signalNames[i]}_${year}_hists \
                            --isMC \
                            -f \
                            --treeName XhhMiniNtuple \
                            direct &"
done
wait

for i in "${signalIndices[@]}"
do
    runCommand "mv $outDir-$nTuple/${signalNames[i]}_${year}_hists/hist-*.root $outDir-$nTuple/${signalNames[i]}_${year}_hists/hists.root &"
done
wait
done
fi

if [ ! -d "plots" ]; then
    runCommand "mkdir plots"
fi

#plot signal stuff
if $plotMC; then
    runCommand "rm -r plots/signal-${nTuple}"
    runCommand "python XhhResolved/plotting/triggerStudyHCandAlgos.py --outFile $outDir-$nTuple/efficiency_acceptance -v $nTuple &"
    runCommand "python XhhResolved/plotting/studyHCandAlgos.py --doSignalOnly --outDir plots/signal-${nTuple}/ -i 0 -v $nTuple"
    wait
    runCommand "tar -C plots -zcf plots/signal-${nTuple}.tar signal-${nTuple}"
fi

#---------------------------------------------------------------------------------------------------------------------------------------

###############################
## 4. data/ttbar reweighting ##
###############################

nonallhadparts=( 0 1 2 3 )
allhadparts=( 0 1 )

if $runData; then
for year in "${years[@]}"; do

if [ "$year" -eq "2015" ]; then 
    periods=( data15.periodD data15.periodE data15.periodF data15.periodG data15.periodH data15.periodJ )
fi

if [ "$year" -eq "2016" ]; then 
    # periods=( data16.periodA \
    #           data16.periodB0 data16.periodB1 \
    #           data16.periodC1 data16.periodC2 data16.periodC3_0 data16.periodC3_1 data16.periodC4 \
    #           data16.periodD0 data16.periodD1 data16.periodD2 data16.periodD3 )
    periods=( data16.periodA \
              data16.periodB data16.periodC \
              data16.periodD data16.periodE data16.periodF data16.periodG data16.periodI \
              data16.periodK data16.periodL )
fi

for var  in "${variations[@]}"; do
for iter in "${iterations[@]}"; do

    if ! ${weightsOnly}; then
    for period in "${periods[@]}"; do    
    	runCommand "xAH_run.py  --files /share/t3data3/johnda/samples/XhhOutput/$nTuple/$period.hh4b-${nTuple}_MiniNTuple.root \
                                --config XhhResolved/scripts/${script} \
                                --extraOptions='--tagger ${tagger} --weights ${weights} --variation ${var} --iteration ${iter} --year ${year} ${threeTag}' \
                                --submitDir $outDir-$nTuple/Data.${period}_${year}_hists_${var}_iter$iter \
                                -f \
                                --treeName XhhMiniNtuple \
                                direct & "

    done ## data

    for part in "${nonallhadparts[@]}"; do
    	nonallhad=nonallhad_${part}.hh4b-${nTuple}_MiniNTuple.root

    	runCommand "xAH_run.py  --files $t3data/$nTuple/$nonallhad \
                                --config XhhResolved/scripts/${script} \
                                --extraOptions='--tagger ${tagger} --weights ${weights} --variation ${var} --iteration ${iter} --year ${year} --lumiSF 1.2 ${threeTag}' \
                                --submitDir $outDir-$nTuple/nonallhad_${part}_${year}_hists_${var}_iter$iter \
                                --isMC \
                                -f \
                                --treeName XhhMiniNtuple \
                                direct &"

    	runCommand "xAH_run.py  --files $t3data/$nTuple/$nonallhad \
                                --config XhhResolved/scripts/${script} \
                                --extraOptions='--tagger ${tagger} --weights ${weights} --variation ${var} --iteration ${iter} --year ${year} --lumiSF 1.2 --ttbar ${threeTag}' \
                                --submitDir $outDir-$nTuple/nonallhadShape_${part}_${year}_hists_${var}_iter$iter \
                                --isMC \
                                -f \
                                --treeName XhhMiniNtuple \
                                direct &"

    done ## non all hadronic ttbar

    for part in "${allhadparts[@]}"; do
    	allhad=allhad_${part}.hh4b-${nTuple}_MiniNTuple.root
	
    	runCommand "xAH_run.py  --files $t3data/$nTuple/$allhad \
                                --config XhhResolved/scripts/${script} \
                                --extraOptions='--tagger ${tagger} --weights ${weights} --variation ${var} --iteration ${iter} --year ${year} --lumiSF 1.2 ${threeTag}' \
                                --submitDir $outDir-$nTuple/allhad_${part}_${year}_hists_${var}_iter$iter \
                                --isMC \
                                -f \
                                --treeName XhhMiniNtuple \
                                direct &"

    	runCommand "xAH_run.py  --files $t3data/$nTuple/$allhad \
                                --config XhhResolved/scripts/${script} \
                                --extraOptions='--tagger ${tagger} --weights ${weights} --variation ${var} --iteration ${iter} --year ${year} --lumiSF 1.2 --ttbar ${threeTag}' \
                                --submitDir $outDir-$nTuple/allhadShape_${part}_${year}_hists_${var}_iter$iter \
                                --isMC \
                                -f \
                                --treeName XhhMiniNtuple \
                                direct &"

    done ## all hadronic ttbar
    wait

    runCommand "rm -r $outDir-$nTuple/Data_${year}_hists_${var}_iter$iter"
    runCommand "mkdir $outDir-$nTuple/Data_${year}_hists_${var}_iter$iter"
    runCommand "hadd  $outDir-$nTuple/Data_${year}_hists_${var}_iter$iter/hists.root $outDir-$nTuple/Data.*_${year}_hists_${var}_iter$iter/hist-$nTuple.root"

    runCommand "mkdir   $outDir-$nTuple/ttbar_${year}_hists_${var}_iter$iter"
    runCommand "hadd -f $outDir-$nTuple/ttbar_${year}_hists_${var}_iter$iter/hists.root $outDir-$nTuple/*had_*_${year}_hists_${var}_iter$iter/hist-*.root"

    runCommand "mkdir   $outDir-$nTuple/ttbarShape_${year}_hists_${var}_iter$iter"
    runCommand "hadd -f $outDir-$nTuple/ttbarShape_${year}_hists_${var}_iter$iter/hists.root $outDir-$nTuple/*hadShape_*_${year}_hists_${var}_iter$iter/hist-*.root"
    fi

    ## Make weights and qcd background hists
    runCommand "mkdir $outDir-$nTuple/qcd_${year}_hists_${var}_iter$iter/"
    runCommand "cd XhhResolved/scripts/"
    runCommand "python makeWeightshh4bComb.py -i $iter \
                                              -n _${weights}_${year}_${var}_ \
                                              -d ../../$outDir-$nTuple/Data_${year}_hists_${var}_iter$iter/hists.root \
                                              -t           ../../$outDir-$nTuple/ttbar_${year}_hists_${var}_iter$iter/hists.root \
                                              --ttbarShape ../../$outDir-$nTuple/ttbarShape_${year}_hists_${var}_iter$iter/hists.root \
                                              -q ../../$outDir-$nTuple/qcd_${year}_hists_${var}_iter$iter/hists.root \
                                              ${threeTag}"
    runCommand "cd $workDir"
done ##iteration
done ##variations
done ##year
fi

#---------------------------------------------------------------------------------------------------------------------------------------

#################
## 5. Plotting ##
#################

if $plotData; then
for year in "${years[@]}"; do
    for var  in "${plotVariations[@]}"; do
    for iter in "${plotIterations[@]}"; do
    	runCommand "rm -r plots/${outDir}-${var}-iter${iter}-${nTuple}_${year}"
    done
    wait
    for iter in "${plotIterations[@]}"; do
	runCommand "python XhhResolved/plotting/studyhh4bComb.py   --doMain --outDir plots/${outDir}-${var}-iter${iter}-${nTuple}_${year}/ --weights ${weights} -i ${iter} --variation ${var} -v $nTuple -y $year --inDir $outDir &"
        #runCommand "python XhhResolved/plotting/sensitivityStudyHCandAlgos.py --outFile plots/iter${iter}-${nTuple}/sensitivity \
        #                                                                      --mu XhhResolved/data/mu_qcd_StudyHCandAlgos-${iter}.txt -i ${iter} -v $nTuple &"
    done 
    wait

    #for iter in "${plotIterations[@]}"; do
    #    runCommand "mkdir plots/iter${iter}-${nTuple}/tables"
    #	runCommand "python XhhResolved/plotting/tablesStudyHCandAlgos.py --sampleComp    plots/iter${iter}-${nTuple}/tables/sampleComp.tex \
    #                                                                     --muTable       plots/iter${iter}-${nTuple}/tables/mu_qcd_iter${iter}.tex \
    #                                                                     --cutflow_table plots/iter${iter}-${nTuple}/tables/cutflow.tex \
    #	                                                                 --bkgSR         plots/iter${iter}-${nTuple}/tables/bkgSR.tex \
    #                                                                     --data hists-${nTuple}/Data_${year}_hists_${var}_iter${iter}/hists.root \
    #                                                                     --m300  $outDir-$nTuple/RSG300_${year}_hists_${var}/hists.root \
    #                                                                     --m700  $outDir-$nTuple/RSG700_${year}_hists_${var}/hists.root \
    #                                                                     --m1100 $outDir-$nTuple/RSG1100_${year}_hists_${var}/hists.root \
    #                                                                     --ttbar hists-${nTuple}/ttbar_${year}_hists_${var}_iter${iter}/hists.root \
    #                                                                     --mu XhhResolved/data/mu_qcd_StudyHCandAlgos-${iter}.txt"
    #done

    for iter in "${plotIterations[@]}"; do
    	runCommand "tar -C plots -zcf plots/${outDir}-${var}-iter${iter}-${nTuple}_${year}.tar ${outDir}-${var}-iter${iter}-${nTuple}_${year} &"
    done
    wait
    done #variation
done #year
fi


#---------------------------------------------------------------------------------------------------------------------------------------

#############################
## 6. Limit Setting Inputs ##
#############################

# QCD
if $runLimitInputs; then
    runCommand "rm -r LimitSettingInputs"
    runCommand "mkdir LimitSettingInputs"
    runCommand "mkdir plots/${outDir}-Nominal-iter4-${nTuple}_2016_shapeSpace/"
    runCommand "python XhhResolved/scripts/shapeSpace.py --outDir plots/${outDir}-Nominal-iter4-${nTuple}_2016_shapeSpace/ \
                                                         --weights ${weights} -i 4 --variation Nominal -v $nTuple -y 2016 --inDir $outDir \
                                                         --limitFile LimitSettingInputs/resolved_4bSR.root "

    # runCommand "python XhhResolved/scripts/makeLimitInputs.py -i $outDir-$nTuple/qcd_2016_hists_Nominal_iter4/hists.root \
    #                                                           -d $outDir-$nTuple/Data_2016_hists_Nominal_iter4/hists.root \
    #                                                           -t $outDir-${nTuple}/ttbarShape_2016_hists_Nominal_iter4/hists.root \
    #                                                           -o LimitSettingInputs/resolved_4bSR.root \
    #                                                           -n qcd_hh \
    #                                                           -u XhhResolved/data/mu_qcd_FourTag_${weights}_2016_Nominal_4.txt
    #                                                           --type qcd" #\
    # 							     #--shape true"

    # runCommand "python XhhResolved/scripts/makeLimitInputs.py -i $outDir-$nTuple/ttbarShape_2016_hists_Nominal_iter4/hists.root \
    #                                                           -o LimitSettingInputs/resolved_4bSR.root \
    #                                                           -n ttbar_hh \
    #                                                           -u XhhResolved/data/mu_qcd_FourTag_${weights}_2016_Nominal_4.txt
    #                                                           --type ttbar" #\
    # 							     #--shape true"

    # runCommand "python XhhResolved/scripts/makeLimitInputs.py -i $outDir-$nTuple/Data_2016_hists_Nominal_iter4/hists.root \
    #                                                           -o LimitSettingInputs/resolved_4bSR.root \
    #                                                           -n data_hh \
    #                                                           --type data "

fi

## Signal sample names for limit setting input hists:
#               0             1             2             3             4             5             6              7              8              9    10        11
n=( g_hh_m300_c10 g_hh_m400_c10 g_hh_m500_c10 g_hh_m600_c10 g_hh_m700_c10 g_hh_m800_c10 g_hh_m900_c10 g_hh_m1000_c10 g_hh_m1100_c10 g_hh_m1200_c10 sm_hh s_hh_m260 
    g_hh_m1300_c10 g_hh_m1400_c10 
    s_hh_m300     s_hh_m400     s_hh_m500     s_hh_m600     s_hh_m700     s_hh_m800     s_hh_m900     s_hh_m1000     s_hh_m1100     s_hh_m1200     s_hh_m1300     s_hh_m1400)

syst=( 
XhhMiniNtuple 
XhhMiniNtupleResolved_JET_GroupedNP_1__1up 
XhhMiniNtupleResolved_JET_GroupedNP_1__1down 
XhhMiniNtupleResolved_JET_GroupedNP_2__1up 
XhhMiniNtupleResolved_JET_GroupedNP_2__1down 
XhhMiniNtupleResolved_JET_GroupedNP_3__1up 
XhhMiniNtupleResolved_JET_GroupedNP_3__1down 
XhhMiniNtupleResolved_JET_JER_SINGLE_NP__1up 
) 

systIndices=( 0 )
if $runLimitInputs; then
    for i in "${signalIndices[@]}"; do

	name=( 
	    ${n[$i]} 
	    ${n[$i]}_JET_GroupedNP_1Up 
	    ${n[$i]}_JET_GroupedNP_1Down 
	    ${n[$i]}_JET_GroupedNP_2Up 
	    ${n[$i]}_JET_GroupedNP_2Down 
	    ${n[$i]}_JET_GroupedNP_3Up 
	    ${n[$i]}_JET_GroupedNP_3Down 
	    ${n[$i]}_JET_JER_SINGLE_NPUp 
	    ) 
	echo $name
	echo $i
	echo ${n[$i]}
	runCommand "python XhhResolved/scripts/makeLimitInputs.py -i $outDir-$nTuple/${signalNames[i]}_2016_hists/hists.root \
                                                                  -o LimitSettingInputs/resolved_4bSR.root \
                                                                  -n ${name[0]} \
                                                                  --type signal"
    done
fi

if $plotLimitInputs; then
    runCommand "python XhhResolved/plotting/studyhh4bComb.py --doLimitInputs --outDir plots/${outDir}-LimitInputs-${nTuple}/ --weights $weights -i 4 -v $nTuple -y 2016 --inDir $outDir"

fi

#    for j in "${systIndices[@]}"; do

# 	if [ -e systematics-${nTuple}/RSGM${m[$i]}_${syst[$j]}-1/hists.root ]; then 

# 	    runCommand "python makeLimitInputs.py -i systematics-${nTuple}/RSGM${m[$i]}_${syst[$j]}-1/hists.root \
#                                                   -o LimitSettingInputs/resolved_4bSR.root -n ${name[$j]}  -f TTVetoFourTag_Signal"

# 	fi
#     done
# done

# #
# # ttbar
# #
# name=( \
# ttbar_hh \
# ttbar_hh_JET_GroupedNP_1Up \
# ttbar_hh_JET_GroupedNP_1Down \
# ttbar_hh_JET_GroupedNP_2Up \
# ttbar_hh_JET_GroupedNP_2Down \
# ttbar_hh_JET_GroupedNP_3Up \
# ttbar_hh_JET_GroupedNP_3Down \
# ttbar_hh_JET_JER_SINGLE_NPUp \
# ) 

# for i in `seq 0 0`; do 

#     if [ -e systematics-${nTuple}/ttbar_allhad_${syst[$i]}-1/hists.root ];then

# 	if [ -e systematics-${nTuple}/ttbar_nonallhad_${syst[$i]}-1/hists.root ]; then
	    
# 	    if ! [ -e systematics-${nTuple}/ttbar_${syst[$i]}-1/hists.root ]; then
# 		runCommand "mkdir systematics-${nTuple}/ttbar_${syst[$i]}-1"
# 	    fi 

# 	    runCommand "hadd systematics-${nTuple}/ttbar_${syst[$i]}-1/hists.root \
#                              systematics-${nTuple}/ttbar_allhad_${syst[$i]}-1/hists.root \
#                              systematics-${nTuple}/ttbar_nonallhad_${syst[$i]}-1/hists.root"

# 	    runCommand "python makeLimitInputs.py -i systematics-${nTuple}/ttbar_${syst[$i]}-1/hists.root \
#                                                   -o LimitSettingInputs/resolved_4bSR.root -n ${name[$i]} -f TTVetoTwoTag_Signal"

# 	fi
#     fi
# done

if $setLimits; then
    runCommand "cp LimitSettingInputs/resolved_4bSR.root StatAnalysis/HistFiles/resolved_4bSR_2016.root"
    runCommand "cd StatAnalysis/Code"
    
    runCommand "./bin/MakeWorkspaces_Resolved --sigModel sm_hh --syst QCDShape --channel resolved_4b_2016"
    runCommand "./bin/MakeWorkspaces_Resolved --sigModel s_hh --syst QCDShape --channel resolved_4b_2016"

    runCommand "./bin/FitCrossCheckForLimits ../Workspaces/sm_hh_resolved_4b_2016_QCDShape_combined_hh4b_model.root Results_Fit/Test"

    #SM cross section x BR from nTuple is 8.42. Actual SM value is 11.3. 8.42/11.3 ~ 0.75 
    runCommand "python RunAsymptotics.py sm_hh resolved_4b_2016 QCDShape"

fi