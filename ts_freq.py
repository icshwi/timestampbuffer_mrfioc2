import numpy as np
import sys
from collections import OrderedDict
import os
import time
import pdb
import subprocess as sp

Freqs = []
Delays = []
EvtNo = []
FlshNo = []
TotalFreqs = 0

#pdb.set_trace()
with open("freq.cfg","r") as FreqFile:
	for x in FreqFile:
		if x[0] != "#" and int(x[0]) > 0:
			Freqs.append(int(x.split(",")[0]))
			Delays.append(int(x.split(",")[1]))
			EvtNo.append(int(x.split(",")[2]))
			FlshNo.append(int(x.split(",")[3]))
			TotalFreqs = TotalFreqs +1

#pdb.set_trace()

def CalcDiff():
	# calc diff
	global TSString, TSSplitString, TSList, TSDiffList, MaxDiff, MinDiff
	TSSplitString = []
	TSDiffList = []
	TSList = []
	MaxDiff = -1
	MinDiff = -1
	TSString = sp.getoutput('caget MDTST{evr:1-ts:1}TS-I')
#	print (TSString)
	TSSplitString = TSString.split(" ")
	for i in range(2,len(TSSplitString)):
		try:
			TSDiff = int(TSSplitString[i])
#			print (TSDiff)
			if TSDiff < 0:
				TSList.append(TSDiff)
			if i > 2:
				TSDiffList.append(TSList[i-2]-TSList[i-3])
		except:
			pass
	for i in TSDiffList:
		if i > MaxDiff:
			MaxDiff = i
		if i < MinDiff or MinDiff == -1:
			MinDiff = i
		print (i)
	print ("Mindiff: ", MinDiff)
	print ("Maxdiff: ", MaxDiff)
	print ("SP freq: ", Freqs[0], "Act freq :", len(TSList)*14, "No of TS: ", len(TSList))
	
	
def main():
	global LowFreq, BaseTicks, TotalSeqTicks
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/caput Utgard:MDS:TS-EVG-01:Mxc1-Prescaler-SP " +str(88052500/Freqs[0]))
	time.sleep(1)
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/caput MDTST{evr:1-SoftSeq:0}Commit-Cmd" +" 1")
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/caput MDTST{evr:1-ts:1}CptEvt-SP " +str(EvtNo[0]))
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/caput MDTST{evr:1-ts:1}FlshEvt-SP " +str(FlshNo[0]))
	time.sleep(1)	


	CalcDiff()

if __name__ == "__main__":
	main()
