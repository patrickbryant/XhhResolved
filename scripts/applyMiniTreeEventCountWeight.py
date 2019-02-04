#!/usr/bin/env python

import ROOT

import sys
import glob
import os, os.path
import shutil
import argparse
import multiprocessing

def rescale_file(rootfile):
    # Check if backup file exists
    origrootfile='%s/orig/%s'%(args.sampledir,os.path.basename(rootfile))
    if not os.path.exists(origrootfile): # Create backup
        shutil.copyfile(rootfile,origrootfile)

    fh_out =ROOT.TFile.Open(rootfile,'recreate')
    fh_hist=ROOT.TFile.Open(origrootfile)

    # Get event counts
    eventCountHist = fh_hist.Get('MetaData_EventCount_XhhMiniNtuple')

    if "0x(nil)" in str(eventCountHist): 
        print "ERROR: Did not find MetaData_EventCount_XhhMiniNtuple"
        #fh_hist.ls()
        print "Try using EventLoop_EventCount"

        eventCountHist = fh_hist.Get('EventLoop_EventCount')
        if "0x(nil)" in str(eventCountHist): 
            print "ERROR: Did not find EventLoop_EventCount"

    if not args.weighted:
        EventCount=eventCountHist.GetBinContent(1)
    else:
        EventCount=eventCountHist.GetBinContent(3)

    recursive_rescale(fh_hist,fh_out,EventCount,float(args.scale))

    fh_out .Close()
    fh_hist.Close()

    return (rootfile,EventCount,args.scale)

def recursive_rescale(indir,outdir,EventCount,scale):
    keys=indir.GetListOfKeys()

    for key in keys:
        name=key.GetName()
        obj=key.ReadObj()
        if obj.InheritsFrom(ROOT.TH1.Class()):
            outdir.cd()
            if(EventCount!=0 and obj.GetName()!="cutflow" and obj.GetName()!="MetaData_EventCount_XhhMiniNtuple"): obj.Scale(scale/EventCount)
            obj.Write()
        elif obj.InheritsFrom(ROOT.TDirectoryFile.Class()):
            newoutdir=outdir.mkdir(obj.GetName())
            recursive_rescale(obj,newoutdir,EventCount,scale)
        obj.Delete()

parser = argparse.ArgumentParser(description="Normalize histograms by number of events")
parser.add_argument('sampledir',help="Path of sampledir containing histograms.")
parser.add_argument('-w','--weighted',action='store_true',help="Normalize using weighted cutflow.")
parser.add_argument('-s','--scale',  default=1.0,help="scale fector (usually just lumi in pb)")
args = parser.parse_args()

# Check if backup directory exists
if not os.path.isdir('%s/orig'%args.sampledir):
    print '%s/orig'%args.sampledir
    os.makedirs('%s/orig'%args.sampledir)

rootfiles=glob.glob('%s/hist-*.root'%args.sampledir)

workers = multiprocessing.Pool(6)
for result in workers.imap_unordered(rescale_file,rootfiles):
    print(result)
# for rootfile in rootfiles:
#     print(rescale_file(rootfile))
