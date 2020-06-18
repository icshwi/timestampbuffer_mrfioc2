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

#pdb.set_trace()
class IOC:
    def __init__(self):
        # the PVs of the IOC
        self.pv_names = ["Utgard:MDS:TS-EVG-01:Mxc1-Prescaler-SP", "Utgard:MDS:TS-EVG-01:TrigEvt0-EvtCode-SP", "MDTST{evr:1-DlyGen:3}Evt:Trig0-SP", "MDTST{evr:1-In:0}Code:Ext-SP", "MDTST{evr:1-ts:1}CptEvt-SP", "MDTST{evr:1-ts:1}CptEvt-SP", "MDTST{evr:1-ts:1}TS-I"]

        # wait for the IOC to come online
        c = pvaccess.Channel(self.pv_names[0])
        c.setTimeout(30);
        c.get()

        # creaete the channels
        self.EvgPresSP, self.EvgEvtCode, self.EvrOutEvtTrig, self.EvrInEvt, self.EvrCptEvtSP, self.EvrFlshEvtSP, self.EvrTSI = [pvaccess.Channel(n, pvaccess.ProviderType.CA) for n in self.pv_names]

@pytest.fixture(scope="function")
def ioc(function_scoped_container_getter):
    return IOC()

def test_put(ioc):
    x = [1,2,3]
    ioc..put(x)
    assert_pv_array_equal(ioc.addresses, x)

def TestCaput():
	return
	
def CalcDiff():
	# calc diff
	global TSString, TSSplitString, TSList, TSDiffList, MaxDiff, MinDiff
	TSSplitString = []
	TSDiffList = []
	TSList = []
	MaxDiff = MinDiff = -1
	TSList = EvrTSI.get()["value"]
	for i in range(len(TSList)):
#		print(TSList[i])
		if i > 0:
			TSDiffList.append(TSList[i]-TSList[i-1])
	MaxDiff = max(TSDiffList)
	MinDiff = min(TSDiffList)
	print ("Mindiff: ", MinDiff)
	print ("Maxdiff: ", MaxDiff)
	print ("SP freq: ", Freqs[0], "Act freq :", len(TSList)*14, "No of TS: ", len(TSList))
	
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
	CalcDiff()

if __name__ == "__main__":
	main()
