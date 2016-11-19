# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: test -s RAW2DIGI --no_exec --conditions auto:run2_data -n 10 --data --repacked
import FWCore.ParameterSet.Config as cms

process = cms.Process('RAW2DIGI')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.RawToDigi_Data_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
#            'file:/afs/cern.ch/user/q/qwang/public/ForZDC2016/run284755_ls0460_streamDQM_mrg.root'
        'file:USC_284671_RAW.root'
#                            fileNames = cms.untracked.vstring('file:/afs/cern.ch/work/w/wmcbraye/private/ZDC_Master/ZDC_2016_pPb_RawToDigi/CMSSW_8_0_23/src/QWM/test_RAW2DIGI.root'
                                   )
)
#process.load("IORawData.HcalTBInputService.HcalTBSource_cfi")

#process.source = cms.Source("PoolSource",
#    fileNames = cms.untracked.vstring(
##            'file:/afs/cern.ch/user/q/qwang/public/ForZDC2016/run284755_ls0460_streamDQM_mrg.root'
#            'file:/afs/cern.ch/user/q/qwang/public/ForZDC2016/USC_284671.root'
#    )
#)
#process.source.streams = cms.untracked.vstring(
#                'HCAL_Trigger',
#                'HCAL_SlowData',
#                'HCAL_DCC690',
#                'HCAL_DCC691',
#                'HCAL_DCC692',
#                'HCAL_DCC693',
#)

#process.options = cms.untracked.PSet(
#
#)

# Output definition

process.RECOSIMoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string(''),
        filterName = cms.untracked.string('')
    ),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    fileName = cms.untracked.string('test_RAW2DIGI.root'),
    outputCommands = process.RECOSIMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition

# Other statements
#from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
###from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
###process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')

#process.castorDigis.InputLabel = cms.InputTag("rawDataCollector")

# Path and EndPath definitions
#process.raw2digi_step = cms.Path(process.RawToDigi)
###process.raw2digi_step = cms.Path(process.castorDigis)
###process.endjob_step = cms.EndPath(process.endOfProcess)
###process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)

# Schedule definition
###process.schedule = cms.Schedule(process.raw2digi_step,process.endjob_step,process.RECOSIMoutput_step)


