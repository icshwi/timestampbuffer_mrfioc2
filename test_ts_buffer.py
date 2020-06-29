import numpy as np
import sys
from collections import OrderedDict
import os
import time
import pdb
import pvaccess
from epics import caget, caput, cainfo, camonitor
import pytest
import struct


def pvget(channel):
	return channel.get()["value"]

class IOC:
	def __init__(self):
		#Define all channels with CA
		self.EvgPrescaleSP1 = pvaccess.Channel("Utgard:MDS:TS-EVG-01:Mxc2-Prescaler-SP", pvaccess.ProviderType.CA)
		self.EvgPrescaleSP2 = pvaccess.Channel("Utgard:MDS:TS-EVG-01:Mxc3-Prescaler-SP", pvaccess.ProviderType.CA)
		self.EvgPrescaleSP3 = pvaccess.Channel("Utgard:MDS:TS-EVG-01:Mxc4-Prescaler-SP", pvaccess.ProviderType.CA)
		self.EvgPrescaleSP4 = pvaccess.Channel("Utgard:MDS:TS-EVG-01:Mxc5-Prescaler-SP", pvaccess.ProviderType.CA)
		self.EvgEvtCode1 = pvaccess.Channel("Utgard:MDS:TS-EVG-01:TrigEvt2-EvtCode-SP", pvaccess.ProviderType.CA)
		self.EvgEvtCode2 = pvaccess.Channel("Utgard:MDS:TS-EVG-01:TrigEvt3-EvtCode-SP", pvaccess.ProviderType.CA)
		self.EvgEvtCode3 = pvaccess.Channel("Utgard:MDS:TS-EVG-01:TrigEvt4-EvtCode-SP", pvaccess.ProviderType.CA)
		self.EvgEvtCode4 = pvaccess.Channel("Utgard:MDS:TS-EVG-01:TrigEvt5-EvtCode-SP", pvaccess.ProviderType.CA)
		self.EvrOutEvtTrig = pvaccess.Channel("MDTST{evr:1-DlyGen:3}Evt:Trig0-SP", pvaccess.ProviderType.CA)
		self.EvrInEvt = pvaccess.Channel("MDTST{evr:1-In:0}Code:Ext-SP", pvaccess.ProviderType.CA)
		self.EvrCptEvtSP1 = pvaccess.Channel("MDTST{evr:1-tsflu:1}CptEvt-SP", pvaccess.ProviderType.CA)
		self.EvrCptEvtSP2 = pvaccess.Channel("MDTST{evr:1-tsflu:2}CptEvt-SP", pvaccess.ProviderType.CA)
		self.EvrCptEvtSP3 = pvaccess.Channel("MDTST{evr:1-tsflu:3}CptEvt-SP", pvaccess.ProviderType.CA)
		self.EvrCptEvtSP4 = pvaccess.Channel("MDTST{evr:1-tsflu:4}CptEvt-SP", pvaccess.ProviderType.CA)
		self.EvrFlshEvtSP1 = pvaccess.Channel("MDTST{evr:1-tsflu:1}FlshEvt-SP", pvaccess.ProviderType.CA)
		self.EvrFlshEvtSP2 = pvaccess.Channel("MDTST{evr:1-tsflu:2}FlshEvt-SP", pvaccess.ProviderType.CA)
		self.EvrFlshEvtSP3 = pvaccess.Channel("MDTST{evr:1-tsflu:3}FlshEvt-SP", pvaccess.ProviderType.CA)
		self.EvrFlshEvtSP4 = pvaccess.Channel("MDTST{evr:1-tsflu:4}FlshEvt-SP", pvaccess.ProviderType.CA)
		self.EvrTSI1 = pvaccess.Channel("MDTST{evr:1-tsflu:1}TS-I", pvaccess.ProviderType.CA)
		self.EvrTSI2 = pvaccess.Channel("MDTST{evr:1-tsflu:2}TS-I", pvaccess.ProviderType.CA)
		self.EvrTSI3 = pvaccess.Channel("MDTST{evr:1-tsflu:3}TS-I", pvaccess.ProviderType.CA)
		self.EvrTSI4 = pvaccess.Channel("MDTST{evr:1-tsflu:4}TS-I", pvaccess.ProviderType.CA)
		self.EvrCptEvtFirSP1 = pvaccess.Channel("MDTST{evr:1-tsfir:1}CptEvt-SP", pvaccess.ProviderType.CA)
		self.EvrFlshEvtFirSP1 = pvaccess.Channel("MDTST{evr:1-tsfir:1}FlshEvt-SP", pvaccess.ProviderType.CA)
		self.EvrCptEvtFirSP2 = pvaccess.Channel("MDTST{evr:1-tsfir:2}CptEvt-SP", pvaccess.ProviderType.CA)
		self.EvrFlshEvtFirSP2 = pvaccess.Channel("MDTST{evr:1-tsfir:2}FlshEvt-SP", pvaccess.ProviderType.CA)
		self.EvrTSIFir1 = pvaccess.Channel("MDTST{evr:1-tsfir:1}TS-I", pvaccess.ProviderType.CA)
		self.EvrTSIFir2 = pvaccess.Channel("MDTST{evr:1-tsfir:2}TS-I", pvaccess.ProviderType.CA)
		self.EvrManFlshFir2 = pvaccess.Channel("MDTST{evr:1-tsfir:2}Flsh-SP", pvaccess.ProviderType.CA)
		self.EvrDropI1 = pvaccess.Channel("MDTST{evr:1-tsflu:1}Drop-I", pvaccess.ProviderType.CA)
		self.EvrDropI2 = pvaccess.Channel("MDTST{evr:1-tsflu:2}Drop-I", pvaccess.ProviderType.CA)
		self.EvgSeq2Unit = pvaccess.Channel("Utgard:MDS:TS-EVG-01:SoftSeq2-TsResolution-Sel", pvaccess.ProviderType.CA)
		self.EvgSeq2Evts = pvaccess.Channel("Utgard:MDS:TS-EVG-01:SoftSeq2-EvtCode-SP", pvaccess.ProviderType.CA)
		self.EvgSeq2TS = pvaccess.Channel("Utgard:MDS:TS-EVG-01:SoftSeq2-Timestamp-SP", pvaccess.ProviderType.CA)
		self.EvgSeq2Commit = pvaccess.Channel("Utgard:MDS:TS-EVG-01:SoftSeq2-Commit-Cmd", pvaccess.ProviderType.CA)


@pytest.fixture(scope="session")
def ioc():
	return IOC()

class ParamStruct:
	def __init__(self):
		self.Freq = Freq
		self.FreqEvt = FreqEvt
		self.EvtNo = EvtNo
		self.FlshNo = FlshNo

#Used if a separate parameter file is needed
@pytest.fixture(scope="function")
def params():
	array = []
	with open("freq.cfg","r") as FreqFile:
		for x in FreqFile:
			if x[0] != "#" and int(x[0]) > 0:
				ParamStruct.Freq = int(x.split(",")[0])
				ParamStruct.FreqEvt = int(x.split(",")[1])
				ParamStruct.EvtNo = int(x.split(",")[2])
				ParamStruct.FlshNo = int(x.split(",")[3])
					
	return ParamStruct
#Resets the parameters for every test
def setup_env(ioc):
	EVGFreq = 28
	FreqEvt = 92
	CptEvt = 92
	FlshEvt = 14
	ioc.EvgPrescaleSP1.put(round(88052500/EVGFreq))
	ioc.EvgPrescaleSP2.put(round(88052500/EVGFreq))
	ioc.EvgPrescaleSP3.put(round(88052500/EVGFreq))
	ioc.EvgPrescaleSP4.put(round(88052500/EVGFreq))
	ioc.EvgEvtCode1.put(FreqEvt)
	ioc.EvgEvtCode2.put(FreqEvt+1)
	ioc.EvgEvtCode3.put(FreqEvt+2)
	ioc.EvgEvtCode4.put(FreqEvt+3)
	ioc.EvrOutEvtTrig.put(FreqEvt)
	ioc.EvrInEvt.put(FreqEvt-1)
	ioc.EvrCptEvtSP1.put(CptEvt)
	ioc.EvrCptEvtSP2.put(CptEvt+1)
	ioc.EvrCptEvtSP3.put(CptEvt+2)
	ioc.EvrCptEvtSP4.put(CptEvt+3)
	ioc.EvrFlshEvtSP1.put(FlshEvt)
	ioc.EvrFlshEvtSP2.put(FlshEvt)
	ioc.EvrFlshEvtSP3.put(FlshEvt)
	ioc.EvrFlshEvtSP4.put(FlshEvt)
	ioc.EvrCptEvtFirSP1.put(CptEvt)
	ioc.EvrFlshEvtFirSP1.put(FlshEvt)
	time.sleep(0.2)

#Asserts the difference between SP capture event and ReadBack capture event if larger than 255
def tooHighCptEvt(ioc):
	tooHighEvtNo = 300
	setup_env(ioc)
	origCptEvt = pvget(ioc.EvrCptEvtSP1)
	ioc.EvrCptEvtSP1.put(tooHighEvtNo)
	time.sleep(0.2)
	newCptEvt = pvget(ioc.EvrCptEvtSP1)
	assert(origCptEvt == newCptEvt)

#Assert the difference between SP flush event and ReadBack flush event number if larger than 255
def tooHighFlshEvt(ioc):
	tooHighEvtNo = 300
	setup_env(ioc)
	origCptEvt = pvget(ioc.EvrFlshEvtSP1)
	ioc.EvrFlshEvtSP1.put(tooHighEvtNo)
	time.sleep(0.2)
	newCptEvt = pvget(ioc.EvrFlshEvtSP1)
	assert(origCptEvt == newCptEvt)

#Assert changing capture event on the fly
def test_changeCptEvt(ioc):
	setup_env(ioc)
	origCptEvt = pvget(ioc.EvrCptEvtSP1)
	time.sleep(0.5)
	origCptEvt = pvget(ioc.EvrCptEvtSP1)
	ioc.EvrCptEvtSP1.put(104)
	time.sleep(0.5)
	assert(origCptEvt != pvget(ioc.EvrCptEvtSP1))

#Assert changing flush event on the fly
def test_changeFlshEvtAndLowFreqFlsh(ioc):
	newFlshEvt = 125
	setup_env(ioc)
	ioc.EvrFlshEvtSP1.put(14)
	time.sleep(0.4)
	noTS14 = len(pvget(ioc.EvrTSI1))
	ioc.EvrFlshEvtSP1.put(newFlshEvt)
	time.sleep(2.2)
	noTS125 = len(pvget(ioc.EvrTSI1))
	assert(noTS14*14==noTS125)

#Assert the period stability in ticks when using a physical input to generate events
def test_period_diff_1ch(ioc):
	# this test assumes that there is one physical output connected to an input
	setup_env(ioc)
	TSDiffList = []
	MaxPeriod = MinPeriod = -1
	TSList = pvget(ioc.EvrTSI1)
	for i in range(len(TSList)):
		if i > 0:
			TSDiffList.append(TSList[i]-TSList[i-1])
	MaxPeriod = max(TSDiffList)
	MinPeriod = min(TSDiffList)
	#print ("SP freq: ", params.Freq, "Act freq :", len(TSList)*14, "No of TS: ", len(TSList))
	# within 2 ticks
	assert(MaxPeriod-MinPeriod < 1000000000/88052500*2)

#Assert the frequency high limit for 1 channel
def test_highBWLimit_1ch(ioc):
	bwHzLimit = 14*1024
	setup_env(ioc)
	ioc.EvgPrescaleSP1.put(round(88052500/bwHzLimit))
	timestampsPerFlush = round(bwHzLimit/14)
	time.sleep(0.2)
	TSDiffList = []
	TSList = pvget(ioc.EvrTSI1)
	# less than 2 timestamps difference
	assert(timestampsPerFlush-len(TSList)<2)

#Assert the frequency low limit for 4 channels
def test_highBWLimit_4ch(ioc):
	bwHzLimit = 14336
	setup_env(ioc)
	ioc.EvgPrescaleSP1.put(round(88052500/bwHzLimit))
	ioc.EvgPrescaleSP2.put(round(88052500/bwHzLimit))
	ioc.EvgPrescaleSP3.put(round(88052500/bwHzLimit))
	ioc.EvgPrescaleSP4.put(round(88052500/bwHzLimit))
	timestampsPerFlush = round(bwHzLimit/14)
	time.sleep(0.2)
	TSDiffList1 = []
	TSDiffList2 = []
	TSDiffList3 = []
	TSDiffList4 = []
	TSList1 = pvget(ioc.EvrTSI1)
	TSList2 = pvget(ioc.EvrTSI2)
	TSList3 = pvget(ioc.EvrTSI3)
	TSList4 = pvget(ioc.EvrTSI4)
	#print ("TS per flush: ", timestampsPerFlush, "No of TS: ", len(TSList1), len(TSList2), len(TSList3), len(TSList4))
	# less than 2 timestamps difference
	assert(timestampsPerFlush-len(TSList1) < 2 and timestampsPerFlush-len(TSList2) < 2 and timestampsPerFlush-len(TSList3) < 2 and timestampsPerFlush-len(TSList4) < 2)

#Assert the high limit for flushing
def test_highBWLimitflush(ioc):
	bwHzLimit = 896 #Hz
	setup_env(ioc)
	ioc.EvgPrescaleSP1.put(round(88052500/(bwHzLimit*14)))
	ioc.EvgPrescaleSP2.put(round(88052500/bwHzLimit))
	ioc.EvrFlshEvtSP1.put(93)
	timestampsPerFlush = round(bwHzLimit/14)
	time.sleep(0.2)
	TSDiffList = []
	TSList = pvget(ioc.EvrTSI1)
#	print ("TS per flush: 14, No of TS: ", len(TSList))
	# less than 2 timestamps difference
	assert(14-len(TSList)<2)

#Assert using first event as timestamp reference
def test_relFirst(ioc):
	cptFreq = 56
	setup_env(ioc)
	ioc.EvgPrescaleSP1.put(round(88052500/cptFreq))
	time.sleep(0.2)
	TSDiffList = []
	MaxPeriod = MinPeriod = -1
	TSList = pvget(ioc.EvrTSIFir1)
	for i in range(len(TSList)):
		if i > 0:
			TSDiffList.append(TSList[i]-TSList[i-1])
	MaxPeriod = max(TSDiffList)
	MinPeriod = min(TSDiffList)
	assert(TSList[0] == 0 and MaxPeriod-MinPeriod < 1000000000/88052500*2)

#Assert catching buffer overflow, 10s response time by design
def test_bufferOflw(ioc):
	#assuming 10000 elements in buffer, cpt event at > 10kHz and flsh event at 1Hz
	freqOverflow = 1024*14
	setup_env(ioc)	
	dropEvtStart1 = pvget(ioc.EvrDropI1)
	dropEvtStart2 = pvget(ioc.EvrDropI2)
	ioc.EvrFlshEvtSP1.put(125)
	ioc.EvgPrescaleSP1.put(round(88052500/freqOverflow))
	time.sleep(0.2)
	ioc.EvrFlshEvtSP2.put(125)
	ioc.EvgPrescaleSP2.put(round(88052500/freqOverflow))
	time.sleep(11)
	dropEvtEnd1 = pvget(ioc.EvrDropI1)
	dropEvtEnd2 = pvget(ioc.EvrDropI2)
#	print(dropEvtStart1, dropEvtEnd1, dropEvtStart2, dropEvtEnd2)
	assert(dropEvtStart1 < dropEvtEnd1 and dropEvtStart2 < dropEvtEnd2)

#Assert manual flush. Evt 14 happens 14 times per second, during 2s sleep, 28 events should be timestamped
def test_manualFlsh(ioc):
	setup_env(ioc)
	ioc.EvrFlshEvtFirSP2.put(199)
	ioc.EvrCptEvtFirSP2.put(14)
	time.sleep(0.2)
	ioc.EvrManFlshFir2.put(1)
	time.sleep(2.0)
	ioc.EvrManFlshFir2.put(1)
	NoEvtsEnd = len(pvget(ioc.EvrTSIFir2))
	#print(NoEvtsEnd, len(pvget(ioc.EvrTSIFir2)), pvget(ioc.EvrTSIFir2))
	assert(NoEvtsEnd == 28)

#Assert that even if consecutive ticks are timestamped, and a flush is put in the middle, the buffer can handle it
def test_performanceStress(ioc):
	ioc.EvgSeq2Unit.put("Ticks")
	ioc.EvgSeq2Evts.put([10, 98, 98, 98, 98, 99, 98, 98, 98, 98])
	ioc.EvgSeq2TS.put([10, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009])
	ioc.EvrCptEvtFirSP1.put(98)
	ioc.EvrFlshEvtFirSP1.put(99)
	ioc.EvrCptEvtSP4.put(98)
	ioc.EvrFlshEvtSP4.put(99)
	time.sleep(0.2)
	ioc.EvgSeq2Commit.put(1)
	time.sleep(0.2)
	FirstTS = pvget(ioc.EvrTSIFir1)
	FlushTS = pvget(ioc.EvrTSI4)
	#First TS should be one tick earlier than flush TS. Flush event happens one tick earlier
	#Reverse array, add 11ns (1 tick) and make timestamp positive
	FlushTSRev = [(x+11)*-1 for x in FlushTS[::-1]]
	
#	print("TS: ", FirstTS, FlushTS, FlushTSRev, np.subtract(FlushTSRev,FirstTS))
	#If difference is larger than 2ns, not ok
	assert(max(np.subtract(FlushTSRev,FirstTS)) <= 2)

#Reset the HW
def test_reset(ioc):
	setup_env(ioc)
	assert(pvget(ioc.EvrFlshEvtSP1) == 14)
