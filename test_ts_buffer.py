import numpy as np
import sys
from collections import OrderedDict
import os
import time
import pdb
import subprocess as sp
#from pvaccess import Channel
import pvaccess
from epics import caget, caput, cainfo, camonitor
import pytest
import struct

#Freqs = []
#FreqEvt = []
#EvtNo = []
#FlshNo = []
#TotalFreqs = 0
#EvgPrescaleSP 	= pvaccess.Channel("Utgard:MDS:TS-EVG-01:Mxc1-Prescaler-SP", pvaccess.ProviderType.CA)
#EvgEvtCode 	= pvaccess.Channel("Utgard:MDS:TS-EVG-01:TrigEvt0-EvtCode-SP", pvaccess.ProviderType.CA)
#EvrOutTrig 	= pvaccess.Channel("MDTST{evr:1-DlyGen:3}Evt:Trig0-SP", pvaccess.ProviderType.CA)
#EvrInEvt 	= pvaccess.Channel("MDTST{evr:1-In:0}Code:Ext-SP", pvaccess.ProviderType.CA)
#EvrCptEvtSP 	= pvaccess.Channel("MDTST{evr:1-ts:1}CptEvt-SP", pvaccess.ProviderType.CA)
#EvrFlshEvtSP 	= pvaccess.Channel("MDTST{evr:1-ts:1}FlshEvt-SP", pvaccess.ProviderType.CA)
#EvrTSI		= pvaccess.Channel("MDTST{evr:1-ts:1}TS-I", pvaccess.ProviderType.CA)

def pvget(channel):
	return channel.get()["value"]

#pdb.set_trace()
class IOC:
	def __init__(self):
		# the PVs of the IOC
		self.pv_names = ["Utgard:MDS:TS-EVG-01:Mxc1-Prescaler-SP", "Utgard:MDS:TS-EVG-01:TrigEvt0-EvtCode-SP", "MDTST{evr:1-DlyGen:3}Evt:Trig0-SP", "MDTST{evr:1-In:0}Code:Ext-SP", "MDTST{evr:1-ts:1}CptEvt-SP", "MDTST{evr:1-ts:1}FlshEvt-SP", "MDTST{evr:1-ts:1}TS-I"]
	# wait for the IOC to come online
	#        c = pvaccess.Channel(self.pv_names[0])
	#        c.setTimeout(30);
	#        c.get()
	# create the channels
		self.EvgPrescaleSP, self.EvgEvtCode, self.EvrOutEvtTrig, self.EvrInEvt, self.EvrCptEvtSP, self.EvrFlshEvtSP, self.EvrTSI = [pvaccess.Channel(n, pvaccess.ProviderType.CA) for n in self.pv_names]

#use session or module scope; the channel is not closed between tests and will therefore cause an error if scope is function
@pytest.fixture(scope="session")
def ioc():
	return IOC()

class ParamStruct:
	def __init__(self):
		self.Freq = Freq
		self.FreqEvt = FreqEvt
		self.EvtNo = EvtNo
		self.FlshNo = FlshNo

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

def setup_env(ioc,params):
	ioc.EvgPrescaleSP.put(round(88052500/params.Freq))
	ioc.EvgEvtCode.put(params.FreqEvt)
	ioc.EvrOutEvtTrig.put(params.FreqEvt)
	ioc.EvrInEvt.put(params.EvtNo)
	ioc.EvrCptEvtSP.put(params.EvtNo)
	ioc.EvrFlshEvtSP.put(params.FlshNo)
	time.sleep(0.2)

def test_period_diff(ioc,params):
	setup_env(ioc,params)
	TSDiffList = []
	MaxPeriod = MinPeriod = -1
	TSList = pvget(ioc.EvrTSI)
	for i in range(len(TSList)):
		if i > 0:
			TSDiffList.append(TSList[i]-TSList[i-1])
	MaxPeriod = max(TSDiffList)
	MinPeriod = min(TSDiffList)
	#print ("Mindiff: ", MinPeriod)
	#print ("Maxdiff: ", MaxPeriod)
	print ("SP freq: ", params.Freq, "Act freq :", len(TSList)*14, "No of TS: ", len(TSList))
	# within 2 ticks
	assert(MaxPeriod-MinPeriod < 1000000000/88052500*2)
	#assert(testPar[0] - len(TSList)*14 < 200)
	#minmax(MaxPeriod,MinPeriod)	

def tooHighCptEvt(ioc):
	tooHighEvtNo = 300
	setup_env(ioc,params)
	origCptEvt = pvget(ioc.EvrCptEvtSP)
	ioc.EvrCptEvtSP.put(tooHighEvtNo)
	time.sleep(0.2)
	newCptEvt = pvget(ioc.EvrCptEvtSP)
	assert(origCptEvt == newCptEvt)

def tooHighFlshEvt(ioc):
	tooHighEvtNo = 300
	setup_env(ioc,params)
	origCptEvt = pvget(ioc.EvrFlshEvtSP)
	ioc.EvrFlshEvtSP.put(tooHighEvtNo)
	time.sleep(0.2)
	newCptEvt = pvget(ioc.EvrFlshEvtSP)
	assert(origCptEvt == newCptEvt)

def test_changeCptEvt(ioc,params):
	setup_env(ioc,params)
#	EvrCptEvtSP = pvaccess.Channel("MDTST{evr:1-ts:1}CptEvt-SP", pvaccess.ProviderType.CA)
#	origCptEvt = ioc.EvrCptEvtSP.get()["value"]
	origCptEvt = pvget(ioc.EvrCptEvtSP)
	ioc.EvrCptEvtSP.put(params.EvtNo)
	time.sleep(0.5)
	origCptEvt = pvget(ioc.EvrCptEvtSP)
	ioc.EvrCptEvtSP.put(94)
	time.sleep(0.5)
	assert(origCptEvt != pvget(ioc.EvrCptEvtSP))

def test_changeFlshEvt(ioc,params):
	newFlshEvt = 125
	setup_env(ioc,params)
	ioc.EvrFlshEvtSP.put(14)
	time.sleep(0.2)
	noTS14 = len(pvget(ioc.EvrTSI))
	ioc.EvrFlshEvtSP.put(newFlshEvt)
	time.sleep(2.2)
	noTS125 = len(pvget(ioc.EvrTSI))
	assert(noTS14*14==noTS125)

def test_highBWLimit(ioc,params):
	bwHzLimit = 20000
	setup_env(ioc,params)
	ioc.EvgPrescaleSP.put(round(88052500/bwHzLimit))
	timestampsPerFlush = round(bwHzLimit/14)
	time.sleep(0.2)
	TSDiffList = []
	TSList = pvget(ioc.EvrTSI)
	#print ("Mindiff: ", MinPeriod)
	#print ("Maxdiff: ", MaxPeriod)
	print ("TS per flush: ", timestampsPerFlush, "No of TS: ", len(TSList))
	# less than 2 timestamps difference
	assert(timestampsPerFlush-len(TSList)<2)

