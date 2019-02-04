import time
import os, re
import sys
sys.path.insert(0, 'XhhResolved/plotting/')
import rootFiles
import subprocess
import shlex
from bTagSyst import getBTagSFName
from setupConfig import setLumi


import optparse
parser = optparse.OptionParser()
parser.add_option('-r',            action="store_true", dest="run",       default=False, help="Run data/ttbar")
parser.add_option('-z',            action="store_true", dest="zbb",       default=False, help="Run data driven Zbb")
parser.add_option('-s',            action="store_true", dest="signal",    default=False, help="Run signal")
parser.add_option('-t',            action="store_true", dest="doTrig",    default=False, help="make hists for trigger and acceptance")
parser.add_option('--pt',          action="store_true", dest="plotTrig",  default=False, help="plot hists for trigger and acceptance")
parser.add_option('-w',            action="store_true", dest="weights",   default=False, help="Make weights but don't run iterations")
parser.add_option('-p',            action="store_true", dest="plot",      default=False, help="Make plots")
parser.add_option('-l',            action="store_true", dest="limit",     default=False, help="Make limit inputs")
parser.add_option('--noSyst',      action="store_false",dest="doSyst",    default=True,  help="don't make shape systematic limit inputs")
parser.add_option('--pl',          action="store_true", dest="plotLimitInputs",     default=False, help="Plot limit inputs")
parser.add_option('--pf',          action="store_true", dest="plotFit",             default=False, help="Plot fit stuff")
parser.add_option('-i',                                 dest="iterations",default="",    help="comma separated list of iterations")
parser.add_option('-e',            action="store_true", dest="execute",   default=False, help="Execute commands. Default is to just print them")
parser.add_option('-f',                                 dest="fast",      default="",    help="comma separated list of iterations to run in fast mode for reweighting.")
o, a = parser.parse_args()

#
# Config
#
condor     = True
script     = "config_hh4bCombUnique.py"
nTuple     = "02-03-04"
tagger     = "MV2c10"
var        = "Nominal"
#ttbarVariation="ttbar_hard2b_xwt"
ttbarVariation=""

weightRegion="Sideband"
weightSet  = "redo"+("_"+ttbarVariation if ttbarVariation else "")+("_CR" if weightRegion == "Control" else "")
#weightSet  = "noLowMDR"+("_"+ttbarVariation if ttbarVariation else "")+("_CR" if weightRegion == "Control" else "")
year       = "2016"
outdir     = "hists_"+year+"_"+weightSet

files = rootFiles.getFiles("0",nTuple, outdir, year)
injectFile = None
injectMu   = None
# injectFile = files["H280"]
# injectMu   = "0.04"

iterations      = [int(i) for i in o.iterations.split(",")] if o.iterations else []
fast_iterations = [int(i) for i in o.      fast.split(",")] if o.fast       else []
iterations      = sorted(iterations+fast_iterations)
plot_iterations = iterations
applyWeight = True
#limitVariable = "m4j_cor_f"
limitVariable = "m4j_cor_Z_f"
#limitCut = "PassAllhadVeto"
limitCut = "PassHCdEta"
#limitCut = "Pass_ggVeto"
blind = False
trigSF = True
detectorSyst=True
if detectorSyst:
    NPs = ["",
           # "Resolved_JET_GroupedNP_1__1up",
           # "Resolved_JET_GroupedNP_1__1down",
           # "Resolved_JET_GroupedNP_2__1up",
           # "Resolved_JET_GroupedNP_2__1down",
           # "Resolved_JET_GroupedNP_3__1up",
           # "Resolved_JET_GroupedNP_3__1down",
           # "Resolved_JET_EtaIntercalibration_NonClosure__1up",
           # "Resolved_JET_EtaIntercalibration_NonClosure__1down",
           # "Resolved_JET_JER_SINGLE_NP__1up",
           ]
else:
    NPs = [""]

# File lists for data and ttbar
dataFileList   = "XhhResolved/filelists/data_"+year+".hh4b-"+nTuple+".txt"
ttbarFileList  = "XhhResolved/filelists/ttbar.hh4b-"+nTuple+".txt"
zbbFileList    = "XhhResolved/filelists/zbb_"+year+".hh4b-"+nTuple+".txt"
signalFileList = "XhhResolved/filelists/signal.hh4b-"+nTuple+(".txt" if not detectorSyst else "s.txt")

# def getDSName(f):
#     f = f.replace(".root","")
#     f = f.replace("group.phys-exotics.","")
#     f = f.replace(".physics_Main.","")
#     f = re.sub("hh4b-\d{2}-\d{2}-\d{2}","",f)
#     f = f.replace("_MiniNTuple","")
#     return f

def getDSNickName(f):
    if ".txt" in f: 
        f = f.replace("XhhResolved/filelists/","")
        return f.replace("_hh4b-"+nTuple+".txt","")
    if "hack" in f: return "data.periodF"
    if nTuple+"z" in f or "02-03-05z" in f: return "zbb"+f[f.find(".period"):f.find(".period")+8]
    if "Zbb" in f: # data
        f = "zbb"+f[f.find("data1")+4:f.find("data1")+6]+f[f.find(".period"):f.find(".period")+8]
        return f
    f = f.replace(".root","")
    f = f.replace("group.phys-exotics.","")
    f = f.replace(".physics_Main.","")
    f = re.sub("hh4b-\d{2}-\d{2}-\d{2}","",f)
    if "/share/" in f: 
        f = f[f.find("mc15_13TeV"):]
        f = f[:f.find(".merge")]

    f = f.replace("_MiniNTuple","")
    f = f.replace("_MiniNTupl","")

    if "RS_G" in f: #Graviton sample
        f = "RSG"+f[f.find("_c"):f.find("_c")+4]+f[f.find("_M"):].replace("M","m")
    if "CT10ME_Xhh" in f: #Narrow Width Scalar sample
        if "aMcAtNlo" in f:
            f = "NWS_NLO"+f[f.find("Xhh_m")+3:]
        else:
            f = "NWS"+f[f.find("Xhh_m")+3:]
        f = f.replace("_4b","")
    if "CT10ME_hh_4b" in f: #Standard Model Non-resonant hh sample
        f = "SMNR"
    if "data" in f: # data
        f = "data"+f[f.find(".period"):]
        return f
    if   "nonallhad" in f: #nonallhad ttbar
        f = "nonallhad"
    elif "allhad" in f or "AllHadron" in f: #allhad ttbar
        f = "allhad"
    if "N1N1_directHG" in f: #SUSY Higgsino sample
        f= "N1N1_m"+f[f.find("A14N23LO_")+9:f.find("_N1N1")]
    if "BBS" in f:
        f= f[f.find("BBS"):f.find(".hh4b")].replace("M","m")
    if f[-1] == ".": f = f[:-1]
    if f[-1] == "_": f = f[:-1]
    f = f.replace(".s","")
    f = f.replace(".","")
    return f

def getDSLimitName(f):
    f = f.replace(".root","")
    f = f.replace("group.phys-exotics.","")
    f = f.replace(".physics_Main.","")
    f = re.sub("hh4b-\d{2}-\d{2}-\d{2}","",f)
    f = f.replace("_MiniNTuple","")
    if "/share/" in f: 
        f = f[f.find("mc15_13TeV"):]
        f = f[:f.find(".merge")]

    if "RS_G" in f: #Graviton sample
        f = "g_hh"+f[f.find("_M"):].replace("M","m")+f[f.find("_c"):f.find("_c")+4]
    if "CT10ME_Xhh" in f: #Narrow Width Scalar sample
        f = "s_hh"+f[f.find("Xhh_m")+3:]
        f = f.replace("_4b","")
    if "CT10ME_hh_4b" in f: #Standard Model Non-resonant hh sample
        f = "sm_hh"
    if "data" in f: # data
        f = "data"+f[f.find(".period"):]
    if   "nonallhad" in f: #nonallhad ttbar
        f = "nonallhad"
    elif "allhad" in f: #allhad ttbar
        f = "allhad"
    if f[-1] == "_": f = f[:-1]
    f = f.replace(".s","")
    f = f.replace(".","")
    

    return f
    

def execute(command): # use to run command like a normal line of bash
    print command
    if o.execute: os.system(command)

def watch(command): # use to run a command and keep track of the thread, ie to run something when it is done
    print command
    if o.execute: return (command, subprocess.Popen(shlex.split(command)))

def babySit(job):
    tries = 1
    code = job[1].wait()
    print "Command: "
    print "Exited with: ",code
    while code and tries < 3:
        tries += 1
        print "-----------------------------------------"
        print "RELAUNCH JOB (ATTEMPT #"+str(tries)+"):"
        code = watch(job[0])[1].wait()

def waitForJobs(jobs,failedJobs):
    for job in jobs:
        code = job[1].wait()
        if code: failedJobs.append(job)
    return failedJobs

def relaunchJobs(jobs):
    print "--------------------------------------------"
    print "RELAUNCHING JOBS"
    newJobs = []
    for job in jobs: newJobs.append(watch(job[0]))
    return newJobs

def mkdir(directory):
    if not o.execute: 
        print "mkdir",directory
        return
    if not os.path.isdir(directory):
        os.mkdir(directory)
    else:
        print directory,"already exists"

def rmdir(directory):
    if not o.execute: 
        print "rm -r",directory
        return
    if "*" in directory:
        execute("rm -r "+directory)
        return
    if os.path.isdir(directory):
        execute("rm -r "+directory)
    elif os.path.exists(directory):
        execute("rm "+directory)
    else:
        print directory,"does not exist"



def doSignal():
    signalJobs = []

    mkdir(outdir)

    #
    # Submit signal samples to condor
    #
    BR   = 0.5824**2
    k    = 1
    lumi = setLumi(year)

    signal_ds_list = open(signalFileList,"r")
    for ds in signal_ds_list:
        thisDS = ds.rstrip()
        if not len(thisDS):  continue
        if thisDS[0] == "#": continue
        if thisDS[0] == "/" or ".txt" in thisDS: inputRucio = False
        else:                inputRucio = True
        if ".txt" in thisDS: inputList = " --inputList "
        else:                inputList = ""
        if thisDS[0] == "/": inputList = ""
        else:                inputList = " --rucioMakeList "

        if   "NWS_m270"     in getDSNickName(thisDS): k = 190.000
        elif "NWS_m280"     in getDSNickName(thisDS): k = 208.550
        elif "NWS_m290"     in getDSNickName(thisDS): k = 217.400
        elif "RSG_c10_m260" in getDSNickName(thisDS): k = 0.272210
        elif "RSG_c10_m270" in getDSNickName(thisDS): k = 0.464770
        elif "RSG_c10_m280" in getDSNickName(thisDS): k = 0.728720
        elif "RSG_c10_m290" in getDSNickName(thisDS): k = 1.024000
        elif "RSG_c20_m260" in getDSNickName(thisDS): k = 8.72
        elif "RSG_c20_m280" in getDSNickName(thisDS): k = 9.138
        else: k = 1.0


        # Deal with SMNR norm in post processing
        if "SMNR" == getDSNickName(thisDS) or detectorSyst: #detector syst ntuples sometimes split into multiple files. Normalize after processing
            lumiSF = "--noMCNorm"
            # if "SMNR" == getDSNickName(thisDS):
            #     lumiSF += " --useMhhWeight " #" --useMhhWeight --uselhhWeight "
        else: 
            lumiSF = "--lumiSF "+str(BR*k)

        if trigSF: doTrigSF = " --doTrigSF "
        else:      doTrigSF = ""

        # need to check what BR is used in SUSY/VLQ samples
        if "N1N1" in getDSNickName(thisDS) or "BBS" in getDSNickName(thisDS):
            lumiSF = "--lumiSF 1"

        cmds=[]
        for NP in NPs:
            submitDir = " --submitDir "+outdir+"/"+getDSNickName(thisDS)+("_"+NP if NP else "")
            cmd  = "xAH_run.py "
            cmd += " --files "+thisDS+inputList
            cmd += " --config XhhResolved/scripts/"+script+" "
            cmd += " --extraOptions='--tagger "+tagger+" --year "+year+" "+lumiSF+" --signal "+doTrigSF+("--doBTagSF" if detectorSyst and not NP else "")+"' "
            cmd += submitDir
            cmd += " --isMC "
            cmd += " -f "
            cmd += " --treeName XhhMiniNtuple"+NP+" "
            if inputRucio:
                cmd += " --inputRucio "
            if condor:
                cmd += " condor --optFilesPerWorker 1 --optBatchWait  "
            else:
                cmd += " direct "
            
            
            signalJobs.append(watch(cmd))
            if "SMNR" == getDSNickName(thisDS):#run again with finite mTop correction using truth Mhh weight function
                newSubmitDir = " --submitDir "+outdir+"/"+getDSNickName(thisDS)+"_MhhWeight"+("_"+NP if NP else "")
                signalJobs.append(watch(cmd.replace("--signal","--signal --useMhhWeight").replace(submitDir,newSubmitDir)))

        failedJobs = []
        if condor and detectorSyst and o.execute and len(signalJobs)>39:#avoid overloading the interactive node when launching too many jobs
            failedJobs = waitForJobs(signalJobs, failedJobs)
            tries = 0
            while failedJobs and tries < 2:
                newJobs = relaunchJobs(failedJobs)
                newFailedJobs = []
                failedJobs = waitForJobs(newJobs, newFailedJobs)
                tries += 1

            while len(signalJobs): signalJobs.pop()
            rmdir(outdir+"/*/fetch")
            rmdir(outdir+"/*/submit/RootCore.par")

    # wait for jobs to finish
    failedJobs = []
    if o.execute:
        failedJobs = waitForJobs(signalJobs, failedJobs)
        
    tries = 0
    while failedJobs and tries < 2:
        newJobs = relaunchJobs(failedJobs)
        newFailedJobs = []
        failedJobs = waitForJobs(newJobs, newFailedJobs)
        tries += 1

    #delete the huge fetch/ and submit/RootCore.par
    rmdir(outdir+"/*/fetch")
    rmdir(outdir+"/*/submit/RootCore.par")
 
    signal_ds_list.seek(0)
    for ds in signal_ds_list:
        thisDS = ds.rstrip()
        if not len(thisDS):  continue
        if thisDS[0] == "#": continue

        for NP in NPs:
            if "SMNR" == getDSNickName(thisDS) or detectorSyst: 
                if "SMNR" == getDSNickName(thisDS):k = 33.45/25.3 # scale to new xs calculation: 
                else: k = 1.0
                
                if   "NWS_m270"     in getDSNickName(thisDS): k = 190.000
                elif "NWS_m280"     in getDSNickName(thisDS): k = 208.550
                elif "NWS_m290"     in getDSNickName(thisDS): k = 217.400
                elif "RSG_c10_m260" in getDSNickName(thisDS): k = 0.272210
                elif "RSG_c10_m270" in getDSNickName(thisDS): k = 0.464770
                elif "RSG_c10_m280" in getDSNickName(thisDS): k = 0.728720
                elif "RSG_c10_m290" in getDSNickName(thisDS): k = 1.024000
                elif "RSG_c20_m260" in getDSNickName(thisDS): k = 8.72
                elif "RSG_c20_m280" in getDSNickName(thisDS): k = 9.138

                submitDir = outdir+"/"+getDSNickName(thisDS)+("_"+NP if NP else "")
                cmd = "python "
                cmd += "XhhResolved/scripts/applyMiniTreeEventCountWeight.py "
                cmd += submitDir
                cmd += " --scale "+str(lumi*BR*k)
                cmd += "  -w "
                if applyWeight: 
                    execute(cmd)
                    if "SMNR" == getDSNickName(thisDS):
                        newSubmitDir = outdir+"/"+getDSNickName(thisDS)+"_MhhWeight"+("_"+NP if NP else "")
                        execute(cmd.replace(submitDir,newSubmitDir))

            cmd = "mv "+outdir+"/"+getDSNickName(thisDS)+("_"+NP if NP else "")+"/hist-*.root "+outdir+"/"+getDSNickName(thisDS)+("_"+NP if NP else "")+"/hists.root"
            execute(cmd)
            if "SMNR" == getDSNickName(thisDS):
                execute(cmd.replace(submitDir,newSubmitDir))

    rmdir(outdir+"/*/orig")


def doIteration(iteration):
    dataJobs   = []
    ttbarJobs  = []

    mkdir(outdir)
    if iteration in fast_iterations: fast = " --fast "
    else:                            fast = " "
    #
    # Submit data to condor
    #
    data_ds_list = open(dataFileList,"r")
    for ds in data_ds_list:
        thisDS = ds.rstrip()
        if not len(thisDS):  continue
        if thisDS[0] == "#": continue
        if ".txt" in thisDS: inputList = " --inputList "
        else:                inputList = ""
        inputList = " --rucioMakeList "

        cmd  = "xAH_run.py "
        cmd += " --files "+thisDS+inputList
        cmd += " --config XhhResolved/scripts/"+script+" "
        cmd += " --extraOptions='"+fast+" --tagger "+tagger+" --weights "+weightSet+" --variation "+var+" --iteration "+str(iteration)+" --year "+year+" ' "
        cmd += " --submitDir "+outdir+"/"+getDSNickName(thisDS)+"_iter"+str(iteration)
        cmd += " -f "
        cmd += " --treeName XhhMiniNtuple "
        #cmd += " --inputRucio "
        if condor:
            cmd += " condor --optFilesPerWorker 7 --optBatchWait  "
        else:
            cmd += " direct "

        if not o.weights:
            dataJobs.append(watch(cmd))

    #
    # Submit ttbar to condor
    #
    ttbar_ds_list = open(ttbarFileList,"r")
    for ds in ttbar_ds_list:
        thisDS = ds.rstrip()
        if not len(thisDS):  continue
        if thisDS[0] == "#": continue
        if ".txt" in thisDS: inputList = " --inputList "
        else:                inputList = ""
        inputList = " --rucioMakeList "

        #apply ttbar variations only to 
        # QCD in allhad_shape
        #  4b in nonallhad
        if ttbarVariation:
            ttbarVariationStr=" --ttbarVariation "+ttbarVariation+" "
            if "allhad" == getDSNickName(thisDS):
                ttbarVariationStr += "--ttbarVariationCombName QCD "
            else:
                ttbarVariationStr += "--ttbarVariationCombName 4b "
            
        
        # first run ttbar with same njet factor as data. Used to subtract ttbar from 2b data
        cmd  = "xAH_run.py "
        cmd += " --files "+thisDS+inputList
        cmd += " --config XhhResolved/scripts/"+script+" "
        cmd += " --extraOptions='"+fast+" --tagger "+tagger+" --weights "+weightSet+" --variation "+var+" --iteration "+str(iteration)+" --year "+year
        if "allhad" != getDSNickName(thisDS) and ttbarVariation and "xwt" not in ttbarVariation: cmd += ttbarVariationStr
        if "allhad" == getDSNickName(thisDS) and "2b" in ttbarVariation: cmd += ttbarVariationStr
        cmd += " --noMCNorm' "
        cmd += " --submitDir "+outdir+"/"+getDSNickName(thisDS)+"_iter"+str(iteration)
        cmd += " --isMC "
        cmd += " -f "
        cmd += " --treeName XhhMiniNtuple "
        #cmd += " --inputRucio "
        if condor:
            cmd += " condor --optFilesPerWorker 1 --optBatchWait  "
        else:
            cmd += " direct "

        if not o.weights:
            ttbarJobs.append(watch(cmd))

        # next run allhad ttbar with njet factor tuned to get njet spectrum right for ttbar. 
        #  Difference is due to increased charm component. Used for allhad shape in qcd estimate
        if "allhad" == getDSNickName(thisDS):
            cmd  = "xAH_run.py "
            cmd += " --files "+thisDS+inputList
            cmd += " --config XhhResolved/scripts/"+script+" "
            cmd += " --extraOptions='"+fast+" --tagger "+tagger+" --weights "+weightSet+" --variation "+var+" --iteration "+str(iteration)+" --year "+year
            if ttbarVariation and "2b" not in ttbarVariation: cmd += ttbarVariationStr
            cmd += " --allhad --noMCNorm' "
            cmd += " --submitDir "+outdir+"/"+getDSNickName(thisDS)+"_shape_iter"+str(iteration)
            cmd += " --isMC "
            cmd += " -f "
            cmd += " --treeName XhhMiniNtuple "
            #cmd += " --inputRucio "
            if condor:
                cmd += " condor --optFilesPerWorker 1 --optBatchWait  "
            else:
                cmd += " direct "

            if not o.weights:
                ttbarJobs.append(watch(cmd))


    # wait for jobs to finish
    failedJobs = []
    if o.execute and not o.weights:
        failedJobs = waitForJobs(dataJobs, failedJobs)
        # for job in dataJobs:
        #     babySit(job)
    
    if o.execute and not o.weights:
        failedJobs = waitForJobs(ttbarJobs, failedJobs)
        # for job in ttbarJobs:
        #     babySit(job)

    tries = 0
    while failedJobs and tries < 2:
        newJobs = relaunchJobs(failedJobs)
        newFailedJobs = []
        failedJobs = waitForJobs(newJobs, newFailedJobs)
        tries += 1
        

    #delete the huge fetch/ and submit/RootCore.par
    if not o.weights: 
        rmdir(outdir+"/*/submit/RootCore.par")
        failed = os.popen('find '+outdir+'/ -name "fail*" ')
        failedList = []
        for line in failed: failedList.append(line.replace("\n",""))
        rmdir(outdir+"/*/fetch")
        if len(failedList):
            for fail in failedList: print fail
            return 1
    
    #
    #  ttbar normalization for lumi applied after subjobs have been merged
    #
    lumi = setLumi(year)
    k = 1.2
    
    cmd = "python "
    cmd += "XhhResolved/scripts/applyMiniTreeEventCountWeight.py "
    cmd += outdir+"/nonallhad_iter"+str(iteration)
    cmd += " --scale "+str(lumi*k)
    if not o.weights and applyWeight: execute(cmd)
    
    cmd = "python "
    cmd += "XhhResolved/scripts/applyMiniTreeEventCountWeight.py "
    cmd += outdir+"/allhad_iter"+str(iteration)
    cmd += " --scale "+str(lumi*k)
    cmd += "  -w "
    if not o.weights and applyWeight: execute(cmd)

    cmd = "python "
    cmd += "XhhResolved/scripts/applyMiniTreeEventCountWeight.py "
    cmd += outdir+"/allhad_shape_iter"+str(iteration)
    cmd += " --scale "+str(lumi*k)
    cmd += "  -w "
    if not o.weights and applyWeight: execute(cmd)
        

    # hadd together the data periods
    if not o.weights:
        mkdir(outdir+"/data_iter"+str(iteration))
        cmd = "hadd -f "+outdir+"/data_iter"+str(iteration)+"/hists.root   "
        cmd += outdir+"/data.period*_iter"+str(iteration)+"/hist*MiniNTuple.root.root"
        execute(cmd)
    
    # simplify ttbar file names
    if not o.weights: 
        execute("mv "+outdir+   "/allhad_iter"      +str(iteration)+"/hist-*.root "+outdir+   "/allhad_iter"      +str(iteration)+"/hists.root ")
        execute("mv "+outdir+"/nonallhad_iter"      +str(iteration)+"/hist-*.root "+outdir+"/nonallhad_iter"      +str(iteration)+"/hists.root ")
        execute("mv "+outdir+   "/allhad_shape_iter"+str(iteration)+"/hist-*.root "+outdir+   "/allhad_shape_iter"+str(iteration)+"/hists.root ")

    #
    # Make weights for this iteration. 
    #
    mkdir(outdir+"/qcd_iter"+str(iteration))
    cmd =  "python XhhResolved/scripts/makeWeights.py -i "+str(iteration)
    cmd += " -w _"+weightSet+"_"+year+"_"+var+"_"
    cmd += " -r "+weightRegion
    cmd += " -d "+outdir+"/data_iter"+str(iteration)+"/hists.root "
    cmd += " -a "+outdir+"/allhad_iter"+str(iteration)+"/hists.root "
    cmd += " -s "+outdir+"/allhad_shape_iter"+str(iteration)+"/hists.root "
    cmd += " -n "+outdir+"/nonallhad_iter"+str(iteration)+"/hists.root "
    cmd += " -q "+outdir+"/qcd_iter"+str(iteration)+"/hists.root "
    cmd += " -o "+outdir+"/ "
    if iteration < 1: cmd += " --noFitWeight 1.0 "
    if injectFile and injectMu: cmd += " --injectFile "+injectFile+" --injectMu "+injectMu+" "
    execute(cmd)

    if not o.weights: execute("rc make_par")#add newest weights files to .par submitted to worker nodes

    return 0

def doZbb():
    zbbJobs = []

    mkdir(outdir)
    #
    # Submit zbb selection in data to condor. Muons promoted to b-jets
    #
    zbb_ds_list = open(zbbFileList,"r")
    for ds in zbb_ds_list:
        thisDS = ds.rstrip()
        if not len(thisDS):  continue
        if thisDS[0] == "#": continue
        
        cmd  = "xAH_run.py "
        cmd += " --files "+thisDS
        cmd += " --config XhhResolved/scripts/"+script+" "
        cmd += " --extraOptions='--tagger "+tagger+" --variation "+var+" --year "+year
        cmd += " --promoteMuons --scale4b 2.2 '" #BR(Z->bb)/BR(Z->mumu)*WP^2 = 15.12/3.37*(0.7^2) gives rough scale factor
        cmd += " --submitDir "+outdir+"/"+getDSNickName(thisDS)
        cmd += " -f "
        cmd += " --treeName XhhMiniNtuple "
        cmd += " --inputRucio "
        if condor:
            cmd += " condor --optFilesPerWorker 7 --optBatchWait  "
        else:
            cmd += " direct "

        zbbJobs.append(watch(cmd))

    # wait for jobs to finish
    if o.execute:
        for zbbJob in zbbJobs:
            zbbJob.wait()

    #delete the huge fetch/ and submit/RootCore.par
    rmdir(outdir+"/*/fetch")
    rmdir(outdir+"/*/submit/RootCore.par")
    
    # hadd together the data periods
    mkdir(outdir+"/zbb")
    cmd = "hadd -f "+outdir+"/zbb/hists.root   "
    cmd += outdir+"/zbb.period*/hist*MiniNTuple.root.root"
    execute(cmd)

    return 
    

def doPlot(iteration):
    #rmdir(outdir+"/plots_"+year+"_"+weightSet+"_iter"+str(iteration))

    cmd  = "python XhhResolved/plotting/studyhh4bComb.py  "
    cmd += " --doMain --outDir "+outdir+"/plots_"+year+"_"+weightSet+"_iter"+str(iteration)+"/"
    cmd += " --inDir "+outdir
    cmd += "  -i "+str(iteration)+" -y "+str(year)+" --variation "+var+" -v "+nTuple
    cmd += " --weights "+weightSet
    execute(cmd)

    if not blind:
        cmd = "tar -C "+outdir+" -zcf  "+outdir+"/plots_"+year+"_"+weightSet+"_iter"+str(iteration)+"_UNBLINDED.tar plots_"+year+"_"+weightSet+"_iter"+str(iteration)+"_UNBLINDED"
    else:
        cmd = "tar -C "+outdir+" -zcf  "+outdir+"/plots_"+year+"_"+weightSet+"_iter"+str(iteration)+".tar plots_"+year+"_"+weightSet+"_iter"+str(iteration)
    execute(cmd)

def doPlotLimitInputs(iteration):
    rmdir(outdir+"/LimitInputs_"+year+"_"+weightSet+"_iter"+str(iteration))

    cmd  = "python XhhResolved/plotting/studyhh4bComb.py  "
    cmd += " --doLimitInputs --outDir "+outdir+"/LimitInputs_"+year+"_"+weightSet+"_iter"+str(iteration)+"/"
    cmd += " --inDir "+outdir
    cmd += "  -i "+str(iteration)+" -y "+str(year)+" --variation "+var+" -v "+nTuple
    cmd += " --weights "+weightSet
    execute(cmd)    

def doTrigAccep(iteration):
    cmd  = "python XhhResolved/scripts/makeCutflowPlots.py --out "+outdir+"/efficiencies_acceptances.root"
    cmd += " -i "+str(iteration)+" -v "+nTuple+" -y "+str(year)+" --inDir "+outdir
    execute(cmd)

def plotTrigAccep(iteration):
    cmd  = "python XhhResolved/plotting/studyhh4bComb.py  "
    cmd += " --doTrigger --outDir "+outdir+"/trigger_"+year+"_"+weightSet+"/"
    cmd += " --inDir "+outdir
    cmd += "  -i "+str(iteration)+" -y "+str(year)+" --variation "+var+" -v "+nTuple
    cmd += " --weights "+weightSet
    execute(cmd)    

def doLimitInputs(iteration):
    mkdir("LimitSettingInputs_"+weightSet+"_iter"+str(iteration))
    rmdir("LimitSettingInputs_"+weightSet+"_iter"+str(iteration)+"/resolved_4bSR_"+year+".root")
    cmd  = "python XhhResolved/scripts/shapeSystematics.py"
    cmd += " --weights "+weightSet+" -i "+str(iteration)+" --variation "+var+" -v "+nTuple+" -y "+year
    cmd += " -c "+limitCut
    cmd += " --var "+limitVariable    
    cmd += " --limitFile LimitSettingInputs_"+weightSet+"_iter"+str(iteration)+"/resolved_4bSR_"+year+".root"
    if not o.doSyst: cmd += " --noSyst"
    execute(cmd)
    execute(cmd.replace(limitVariable,limitVariable.replace("_f","_v"))+" --nameSuffix _v")
    #execute(cmd.replace(limitVariable,"m4j_cor_l")+" --nameSuffix _l")
    #execute(cmd.replace(limitVariable,"m4j_cor_1")+" --nameSuffix _1")
    #execute(cmd.replace(limitVariable,"xwt")+" --nameSuffix _xwt --noSyst")

    signal_ds_list = open(signalFileList,"r")
    for ds in signal_ds_list:
        cmds = []
        thisDS = ds.rstrip()
        if not len(thisDS):  continue
        if thisDS[0] == "#": continue

        submitDir = outdir+"/"+getDSNickName(thisDS)+"/hists.root"
        cmd  = "python XhhResolved/scripts/makeLimitInputs.py -i "+submitDir
        cmd += " -o LimitSettingInputs_"+weightSet+"_iter"+str(iteration)+"/resolved_4bSR_"+year+".root"
        cmd += " -n "+getDSLimitName(thisDS)
        cmd += " -c "+limitCut
        cmd += " --var "+limitVariable
        if detectorSyst: cmd += " --bTagSyst --trigSyst --jetSyst "
        execute(cmd)
        if "SMNR" == getDSNickName(thisDS):
            newSubmitDir = outdir+"/"+getDSNickName(thisDS)+"_MhhWeight/hists.root"
            execute(cmd.replace(submitDir,newSubmitDir).replace(getDSLimitName(thisDS),"smrwMhh_hh"))

        # if detectorSyst:
        #     for NP in NPs:
        #         if not NP: continue
        #         cmd  = "python XhhResolved/scripts/makeLimitInputs.py -i "+outdir+"/"+getDSNickName(thisDS)+"_"+NP+"/hists.root"
        #         cmd += " -o LimitSettingInputs_"+weightSet+"_iter"+str(iteration)+"/resolved_4bSR_"+year+".root"
        #         cmd += " -n "+getDSLimitName(thisDS)+"_"+NP
        #         cmd += " -c PassAllhadVeto"
        #         cmd += " --var "+limitVariable
        #         execute(cmd)
        

def setLimits():#this is not really an automatted procedure yet. Here are some commands you can run.
    cmd  = "svn co svn+ssh://svn.cern.ch/reps/atlasphys-exo/Physics/Exotic/JDM/hh4b/Run2/Code/StatAnalysis/pbryant StatAnalysis"
    cmd  = "cp LimitSettingInputs/resolved_4bSR_"+year+".root StatAnalysis/HistFiles/"
    cmd  = "cd StatAnalysis/Code"
    #./bin/MakeWorkspaces_Resolved --sigModel sm --region CR --channel resolved_4b_2016 --syst BackSyst --unblind
    #./bin/FitCrossCheckForLimits ../Workspaces/sm_CR_resolved_4b_2016_BackSyst_combined_hh4b_model.root Results_Fit_CR_BackSyst --unblind
    cmd  = "./bin/MakeWorkspaces_Resolved --sigModel sm --region hh --syst QCDShape --channel resolved_4b_2016"
    cmd  = "./bin/MakeWorkspaces_Resolved --sigModel s  --region hh --syst QCDShape --channel resolved_4b_2016"
    cmd  = "python RunAsymptotics.py sm_hh resolved_4b_2016 combined QCDShape"
    cmd  = "python RunAsymptotics.py  s_hh resolved_4b_2016 combined QCDShape"
    cmd  = "python PlotAsymptoticLimits.py Results_Asymptotics/s_hh_resolved_4b_2016_QCDShape/ NWS resolved_4b_2016" 
    #source runCombined.sh does this:
    #./bin/MakeWorkspaces_combined --sigModel g --syst NoSyst
    #python RunAsymptotics.py g_hh combined combined NoSyst
    #python RunAsymptotics.py g_hh combined combined_r15_hh NoSyst
    #python RunAsymptotics.py g_hh combined combined_r16_hh NoSyst
    #python RunAsymptotics.py g_hh combined combined_b4b_hh NoSyst
    #python RunAsymptotics.py g_hh combined combined_b3b_hh NoSyst
    #python RunAsymptotics.py g_hh combined combined_b2b_hh NoSyst
    #python PlotAsymptoticLimits.py Results_Asymptotics/g_hh_combined_NoSyst_combined/ RSGC10 combined

def doPlotFit(iteration):
    rmdir(outdir+"/LimitOutputs_"+year+"_"+weightSet+"_iter"+str(iteration))

    cmd  = "python XhhResolved/plotting/studyhh4bComb.py  "
    cmd += " --doPostFit --outDir "+outdir+"/LimitOutputs_"+year+"_"+weightSet+"_iter"+str(iteration)+"/"
    cmd += " --inDir "+outdir
    cmd += "  -i "+str(iteration)+" -y "+str(year)+" --variation "+var+" -v "+nTuple
    cmd += " --weights "+weightSet
    execute(cmd)

#
# Run analysis
#
if o.signal:
    doSignal()

if o.run: 
    for i in iterations:  
        failed = doIteration(i)
        while failed:
            raw_input("FOUND FAILURES! Run again?")
            failed = doIteration(i)

if o.zbb:
    doZbb()

if o.plot: 
    for i in plot_iterations:
        doPlot(i)

if o.doTrig:
    for i in plot_iterations:
        doTrigAccep(i)

if o.plotTrig:
    plotTrigAccep("0")

if o.limit:
    doLimitInputs(iterations[-1])

if o.plotLimitInputs:
    for i in plot_iterations:
        doPlotLimitInputs(i)

if o.plotFit:
    for i in plot_iterations:
        doPlotFit(i)
