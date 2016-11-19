import FWCore.ParameterSet.Config as cms

process = cms.Process("Forward")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.load("IORawData.HcalTBInputService.HcalTBSource_cfi")

process.TFileService = cms.Service("TFileService",
                                   fileName = cms.string("ZDCDigi.root")
                                   )
#process.TFileService = cms.Service("TFileService",fileName=cms.string("ZDCRawToDiigi_QWM.root")) 

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/express/PARun2016B/ExpressPhysicsPA/FEVT/Express-v1/000/285/090/00000/FEC8A603-5EA7-E611-BFD6-FA163EDA9B74.root')
#    fileNames = cms.untracked.vstring('file:test_RAW2DIGI.root')
#    fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/w/wmcbraye/private/ZDC_Master/ZDC_2016_pPb_RawToDigi/CMSSW_8_0_23/src/QWM/test_RAW2DIGI.root')
    )

process.analyzer = cms.EDAnalyzer('ForwardAnalyzer'
                                , nZdcTs = cms.untracked.int32(10)
                                , calZDCDigi = cms.untracked.bool(False)
                                , castor = cms.InputTag("castorDigis")
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.globaltag = '80X_dataRun2_Express_v15'

process.p = cms.Path(process.analyzer)

