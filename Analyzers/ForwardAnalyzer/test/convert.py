# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: test -s RAW2DIGI --no_exec --conditions auto:run2_data -n 10 --data --repacked
import FWCore.ParameterSet.Config as cms

process = cms.Process('CONVERT')

# import of standard configurations
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Input source
process.load("IORawData.HcalTBInputService.HcalTBSource_cfi")

process.source.fileNames = cms.untracked.vstring(
#            'file:/afs/cern.ch/user/q/qwang/public/ForZDC2016/USC_284671.root'
    'file:USC_284671.root'
    )

process.source.streams = cms.untracked.vstring(
                'HCAL_Trigger',
                'HCAL_SlowData',
                'HCAL_DCC690',
                'HCAL_DCC691',
                'HCAL_DCC692',
                'HCAL_DCC693',
)

process.options = cms.untracked.PSet(

)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('USC_284671_RAW.root'),
    outputCommands = cms.untracked.vstring( ('keep *') ),
    splitLevel = cms.untracked.int32(0)
)

process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.RECOSIMoutput_step)


