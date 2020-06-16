import numpy as np
import sys
from collections import OrderedDict
import os
import time
import pdb
import subprocess as sp

BaseTicks = 1572366 #int(round(88051900/14)) #88052500/14.000000636  # 6289424
TotalSeqTicks = 0
TotalFreqs = 0
LowFreq = 14.0
RiseEdge = []
Freqs = []
Delays = []
EvtNo = []
FlshNo = []
#SYSTEM = MDTST{evr:1-DlyGen:2}Evt:Trig0-SP
#DEVICE = {evr:1
#SYSTEM = "LabS-Utgard-VIP:"
#DEVICE = "TS-EVR-1:"
SEQEVTCODE = "SoftSeq0-EvtCode-SP"
SEQEVTTICK = "SoftSeq0-Timestamp-SP"
COMMIT = "SoftSeq0-Commit-Cmd"


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
#print Freqs
#print Delays
#print EvtNo

def CreateTickList(NoOfEvtsArr):
	RetTickArr = [] #[] for i in range(TotalFreqs)]
	for NoOfEvts in NoOfEvtsArr:
		RiseEdge = []
		if NoOfEvts > -1 :
			EvtTickListArr = np.linspace(0, TotalSeqTicks-TotalSeqTicks/NoOfEvts, NoOfEvts)

			for x in EvtTickListArr:
				rounded =  int(round(x))
				RiseEdge.append(rounded)
			RetTickArr.append(RiseEdge)
		else :
			RetTickArr.append(-1)
	return RetTickArr

def CreateOutput(SeqTicks, SeqEvt, NumOfPulsesX):
	# Add one event to total no of events, event 127, to indicate sequence finished
	
	# Add all events to epics command"
	EvtString = ' '.join(str(x) for x in SeqEvt)
#	CaputCmdEvt = "caput -a " +SYSTEM +DEVICE +SEQEVTCODE +" " +str(NumOfPulsesX+1) +" " +EvtString +" 127"
	CaputCmdEvt = "caput -a MDTST{evr:1-SoftSeq:0}EvtCode-SP" +" " +str(NumOfPulsesX+1) +" " +EvtString +" 127"
	
	TickString = ' '.join(str(x) for x in SeqTicks)
#	CaputCmdTicks = "caput -a " +SYSTEM +DEVICE +SEQEVTTICK +" " +str(NumOfPulsesX+1) +" " +TickString +" " +str(TotalSeqTicks-3)
	CaputCmdTicks = "caput -a MDTST{evr:1-SoftSeq:0}Timestamp-SP" +" " +str(NumOfPulsesX+1) +" " +TickString +" " +str(TotalSeqTicks-3)


	return CaputCmdTicks, CaputCmdEvt

def CreateSequence(TickArrs):
	TicksList = []
	EvtList = []
	ArrNo = 0
	EvtNoTmp = 0
	# Create arrays of each event number from input file
	for SubArr in TickArrs:
		EvtNoTmp = EvtNo[ArrNo]
		ArrNo = ArrNo + 1
		for Event in range(0,len(SubArr)):
			EvtList.append(EvtNoTmp)
		TicksList = TicksList + SubArr
	#pdb.set_trace()
	# connect the events to number of ticks in a tuplet
	TickEvtZipTup = zip(TicksList, EvtList)
	
	return TickEvtZipTup

def ResolveConflicts(EvtTicksTuple):
	RetSeqTicks = ()
	UnsortedList = EvtTicksTuple
	SortedList = sorted(UnsortedList, key=lambda ticks: ticks[0])
	TicksTuple, EventsTuple = zip(*SortedList)

	i = 1	
	while i < len(TicksTuple):
		if TicksTuple[i-1] == TicksTuple[i]:
			TicksList = list(TicksTuple)
			TicksList[i] = TicksList[i]+1
			if TicksList[i] > (TotalSeqTicks - 3):
				TicksList[i] = 0
			TicksTuple = tuple(TicksList)
			UnsortedList = zip(TicksTuple, EventsTuple)
			SortedList = sorted(UnsortedList, key=lambda ticks: ticks[0])
			TicksTuple, EventsTuple = zip(*SortedList)
			i = 0
		i+=1
	
	RetSeqTicks = SortedList

	return RetSeqTicks		

def DelayEvents(ArgTicks2D):
	for Index1, Item1 in enumerate(ArgTicks2D): #TicksListArr in ArgTicks2D:
		
		for  Index2, Item2 in enumerate(Item1): #TicksListArr):
			Item1[Index2] += Delays[Index1]
		ArgTicks2D[Index1] = Item1 #[Index2] #TicksListArr
		
	return ArgTicks2D
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
	MinInFreq = 14.0
	NumOfPulses = [] 
	TotNumOfPulses = 0
	#if any frequency is lower than 14, set number of ticks to 12*baseTicks
	MinInFreq = min(Freqs)
	TotalSeqTicks = BaseTicks
	
	if MinInFreq < 14:
		TotalSeqTicks = BaseTicks * 12
		LowFreq = 14.0/12.0
	
	for events in Freqs:
		NumOfPulses.append(int(round(int(events)/LowFreq)))
		TotNumOfPulses += int(round(int(events)/LowFreq))
		
	#pdb.set_trace()
	TickList2D = CreateTickList(NumOfPulses)
	
	#pdb.set_trace()
	DelayedSeqTicks = DelayEvents(TickList2D)	
	
	##pdb.set_trace()
	EvtTicksTup = CreateSequence(DelayedSeqTicks)
	
	#pdb.set_trace()
	NoConflictSeqTicks = ResolveConflicts(EvtTicksTup)

	SeqTicks, SeqEvt = zip(*NoConflictSeqTicks)

	Ticks, Events = CreateOutput(list(SeqTicks), list(SeqEvt), TotNumOfPulses)

	print ("Final events list cmd: " +Events)
	print ("Final ticks list cmd: " +Ticks)
#	print "caput " +SYSTEM +DEVICE +COMMIT +" 1"
#	os.system("/opt/epics/bases/base-3.15.4/bin/centos7-x86_64/"+Ticks)
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/"+Ticks)
	time.sleep(1)
	#os.system("/opt/epics/bases/base-3.15.4/bin/centos7-x86_64/"+Events)	
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/"+Events)
#	print(output)
	time.sleep(1)
#	os.system("/opt/epics/bases/base-3.15.4/bin/centos7-x86_64/caput " +SYSTEM +DEVICE +COMMIT +" 1")
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/caput MDTST{evr:1-SoftSeq:0}Commit-Cmd" +" 1")
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/caput MDTST{evr:1-ts:1}CptEvt-SP" +" " +str(EvtNo[0]))
	os.system("/home/michaeldavidsaver/work/epics-base/bin/linux-x86_64/caput MDTST{evr:1-ts:1}FlshEvt-SP" +" " +str(FlshNo[0]))
	time.sleep(1)	

#	os.system("/opt/epics/bases/base-3.15.4/bin/centos7-x86_64/caput LabS-Embla{evr:1-DlyGen:0}Delay-SP "+Delays[0])
#	os.system("/opt/epics/bases/base-3.15.4/bin/centos7-x86_64/caput LabS-Embla{evr:1-DlyGen:1}Delay-SP "+Delays[1])
#	os.system("/opt/epics/bases/base-3.15.4/bin/centos7-x86_64/caput LabS-Embla{evr:1-DlyGen:2}Delay-SP "+Delays[2])

	CalcDiff()

if __name__ == "__main__":
	main()
