#!./mrfioc2/bin/linux-x86_64-debug/mrf

#< envPaths

cd("mrfioc2")

## Register all support components
dbLoadDatabase("dbd/mrf.dbd")
mrf_registerRecordDeviceDriver(pdbbase)

epicsEnvSet("EPICS_CA_MAX_ARRAY_BYTES","1000000")

mrmEvrSetupPCI("EVR","1:0.0")

#dbLoadRecords("db/evr-pcie-300dc.db","SYS=MDTST, D=evr:1, EVR=EVR, FEVT=88.051948")
dbLoadRecords("db/evr-pcie-300dc.db","SYS=MDTST, D=evr:1, EVR=EVR, FEVT=88.0525")

dbLoadRecords("db/mrmevrtsbuf.db","SYS=MDTST, D=evr:1-ts:1, EVR=EVR, CODE=98, TRIG=10, FLUSH=TimesRelPrevFlush")

#dbLoadRecords("db/iocAdminRTEMS.db", "IOC=mrftest")

# Auto save/restore
#save_restoreDebug(2)
#dbLoadRecords("db/save_restoreStatus.db", "P=mrftest:")
#save_restoreSet_status_prefix("mrftest:")

#set_savefile_path("${mnt}/as","/save")
#set_requestfile_path("${mnt}/as","/req")

#set_pass0_restoreFile("mrf_settings.sav")
#set_pass0_restoreFile("mrf_values.sav")
#set_pass1_restoreFile("mrf_values.sav")
#set_pass1_restoreFile("mrf_waveforms.sav")

var evrMrmTimeNSOverflowThreshold 10000

iocInit()
#makeAutosaveFileFromDbInfo("as/req/mrf_settings.req", "autosaveFields_pass0")
#makeAutosaveFileFromDbInfo("as/req/mrf_values.req", "autosaveFields")
#makeAutosaveFileFromDbInfo("as/req/mrf_waveforms.req", "autosaveFields_pass1")

#create_monitor_set("mrf_settings.req", 5 , "")
#create_monitor_set("mrf_values.req", 5 , "")
#create_monitor_set("mrf_waveforms.req", 30 , "")
