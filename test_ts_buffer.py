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

Freqs = []
FreqEvt = []
EvtNo = []
FlshNo = []
TotalFreqs = 0
EvgPrescaleSP 	= pvaccess.Channel("Utgard:MDS:TS-EVG-01:Mxc1-Prescaler-SP", pvaccess.ProviderType.CA)
EvgEvtCode 	= pvaccess.Channel("Utgard:MDS:TS-EVG-01:TrigEvt0-EvtCode-SP", pvaccess.ProviderType.CA)
EvrOutTrig 	= pvaccess.Channel("MDTST{evr:1-DlyGen:3}Evt:Trig0-SP", pvaccess.ProviderType.CA)
EvrInEvt 	= pvaccess.Channel("MDTST{evr:1-In:0}Code:Ext-SP", pvaccess.ProviderType.CA)
EvrCptEvtSP 	= pvaccess.Channel("MDTST{evr:1-ts:1}CptEvt-SP", pvaccess.ProviderType.CA)
EvrFlshEvtSP 	= pvaccess.Channel("MDTST{evr:1-ts:1}FlshEvt-SP", pvaccess.ProviderType.CA)
EvrTSI		= pvaccess.Channel("MDTST{evr:1-ts:1}TS-I", pvaccess.ProviderType.CA)

def pvget(channel):
	return channel.get()["value"]

#pdb.set_trace()
class IOC:
	def __init__(self):
		# the PVs of the IOC
		self.pv_names = ["Utgard:MDS:TS-EVG-01:Mxc1-Prescaler-SP", "Utgard:MDS:TS-EVG-01:TrigEvt0-EvtCode-SP", "MDTST{evr:1-DlyGen:3}Evt:Trig0-SP", "MDTST{evr:1-In:0}Code:Ext-SP", "MDTST{evr:1-ts:1}CptEvt-SP", "MDTST{evr:1-ts:1}CptEvt-SP", "MDTST{evr:1-ts:1}TS-I"]
	# wait for the IOC to come online
	#        c = pvaccess.Channel(self.pv_names[0])
	#        c.setTimeout(30);
	#        c.get()
	# create the channels
		self.EvgPrescaleSP, self.EvgEvtCode, self.EvrOutEvtTrig, self.EvrInEvt, self.EvrCptEvtSP, self.EvrFlshEvtSP, self.EvrTSI = [pvaccess.Channel(n, pvaccess.ProviderType.CA) for n in self.pv_names]

@pytest.fixture(scope="function")
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

#def test_get(ioc):
#	x = pvget(ioc.EvgPrescaleSP)
#	assert(x == 1000)

#def test_put(ioc):
#	x = 10000
#	ioc.EvgPrescaleSP.put(x)
#	assert(ioc.EvgPrescaleSP ==x)

	
def test_timestamp_diff(ioc,params):
	TSDiffList = []
	MaxDiff = MinDiff = -1
#	ioc.EvgPrescaleSP
	TSList = pvget(ioc.EvrTSI)
	for i in range(len(TSList)):
		if i > 0:
			TSDiffList.append(TSList[i]-TSList[i-1])
	MaxDiff = max(TSDiffList)
	MinDiff = min(TSDiffList)
	print ("Mindiff: ", MinDiff)
	print ("Maxdiff: ", MaxDiff)
	print ("SP freq: ", params.Freq, "Act freq :", len(TSList)*14, "No of TS: ", len(TSList))
	# within 2 ticks
	assert(MaxDiff-MinDiff < 1000000000/88052500*2)
	#assert(testPar[0] - len(TSList)*14 < 200)
	#minmax(MaxDiff,MinDiff)
	

#def test_minmax(MaxDiff, MinDiff):	
#	assert(MaxDiff-MinDiff < 23)

def TestChngCptEvt():
	return
	
def main():
#	os.system("caput Utgard:MDS:TS-EVG-01:Mxc1-Prescaler-SP " +str(88052500/Freqs[0]))
#	os.system("caput Utgard:MDS:TS-EVG-01:TrigEvt0-EvtCode-SP " +str(FreqEvt[0]))
#	os.system("caput MDTST{evr:1-DlyGen:3}Evt:Trig0-SP " +str(FreqEvt[0]))
#	caput('Utgard:MDS:TS-EVG-01:Mxc1-Prescaler-SP', 88052500/Freqs[0])
#	time.sleep(1) 
#	os.system("caput MDTST{evr:1-SoftSeq:0}Commit-Cmd" +" 1")
#	os.system("caput MDTST{evr:1-In:0}Code:Ext-SP " +str(EvtNo[0]))
#	os.system("caput MDTST{evr:1-ts:1}CptEvt-SP " +str(EvtNo[0]))
#	os.system("caput MDTST{evr:1-ts:1}FlshEvt-SP " +str(FlshNo[0]))
#	time.sleep(1)	
#	EvgEvtCode 	= pvaccess.Channel(""	, pvaccess.ProviderType.CA)
	with open("freq.cfg","r") as FreqFile:
		for x in FreqFile:
			if x[0] != "#" and int(x[0]) > 0:
				Freqs.append(int(x.split(",")[0]))
				FreqEvt.append(int(x.split(",")[1]))
				EvtNo.append(int(x.split(",")[2]))
				FlshNo.append(int(x.split(",")[3]))
	TestChngCptEvt()	
	EvgPrescaleSP.putInt(int(round(88052500/Freqs[0])))	
	EvgEvtCode.putInt(int(FreqEvt[0]))
	EvrOutTrig.putInt(int(FreqEvt[0]))
	EvrInEvt.putInt(int(EvtNo[0]))
	EvrCptEvtSP.putInt(int(EvtNo[0]))
	EvrFlshEvtSP.putInt(int(FlshNo[0]))
#	myCA = pvaccess.Channel("MDTST{evr:1-ts:1}FlshEvt-SP", pvaccess.ProviderType.CA)
#	print(myCA.get().getInt())
#	print (caget('MDTST{evr:1-ts:1}CptEvt-SP'))

	time.sleep(1)
	calcDiff()

if __name__ == "__main__":
	main()
