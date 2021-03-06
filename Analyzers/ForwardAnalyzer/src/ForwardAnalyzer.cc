// ForwardAnalyzer.cc 
//
// Convert ZDC Raw to Digi
// Author: Will McBrayer, University of Kansas


#define versionTag "v1"
// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"

#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"

// include root files
#include "TFile.h"
#include "TTree.h"
#include "TString.h"


class ForwardAnalyzer : public edm::EDAnalyzer {
    public:
        explicit ForwardAnalyzer(const edm::ParameterSet&);
        ~ForwardAnalyzer();

        static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

    private:
        virtual void beginJob();
        virtual void analyze(const edm::Event&, const edm::EventSetup&);
        virtual void endJob();

        long runBegin, lumibegin, lumiend, evtNo;
        int run, event, lumi;
        std::string startTime;
        std::string *BranchNames;
        int DigiDataADC[180];
        float DigiDatafC[180];
        int BeamData[6];
        int Runno;
        edm::Service<TFileService> mFileServer;

        TTree* ZDCDigiTree;
        TTree* BeamTree;
    
        edm::Service<TFileService> fs;

        edm::EDGetTokenT<ZDCDigiCollection> token;
};


// constructor
ForwardAnalyzer::ForwardAnalyzer(const edm::ParameterSet& iConfig) {
  //usesResource("TFileService");
    token = consumes<ZDCDigiCollection>(iConfig.getParameter<edm::InputTag>("castor"));

    runBegin = -1;
    evtNo = 0;
    lumibegin = 0;
    lumiend = 0;
    startTime = "NotAvaliable";
}


// destructor
ForwardAnalyzer::~ForwardAnalyzer() {
}


// analyzer
void ForwardAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) 
{
    using namespace edm;
    using namespace std;

    // get ZDC digis
    edm::Handle<ZDCDigiCollection> zdcdigis;
    try{ iEvent.getByToken(token,zdcdigis); }
    catch(...) { edm::LogWarning(" ZDC ") << " Cannot get ZDC Digis " << std::endl; }

    ++evtNo;
    time_t a = (iEvent.time().value()) >> 32; // store event info                    
    event = iEvent.id().event();
    run = iEvent.luminosityBlock();
    edm::ESHandle<HcalTopology> htopo;
    iSetup.get<IdealGeometryRecord>().get(htopo);

    if (runBegin < 0) {  // parameters for the first event
        startTime = ctime(&a);
        lumibegin = lumiend = lumi;
        runBegin = iEvent.id().run();
        Runno = iEvent.id().run();
    }
    if (lumi < lumibegin) lumibegin = lumi;
    if (lumi > lumiend)   lumiend = lumi;
    
    BeamData[0] = iEvent.bunchCrossing();
    BeamData[1] = lumi;
    BeamData[2] = run;
    BeamData[3] = event;

    BeamTree->Fill();

    const ZDCDigiCollection * zdc_digi = zdcdigis.failedToGet()? 0 : &*zdcdigis;
    if (zdc_digi) {
        for (int i = 0; i<180; i++) {DigiDatafC[i] = 0; DigiDataADC[i] = 0;}
	for (ZDCDigiCollection::const_iterator j = zdc_digi->begin(); j!=zdc_digi->end(); j++) {
  	    const ZDCDataFrame digi = (const ZDCDataFrame)(*j);
	    int iSide    = digi.id().zside();
	    int iSection = digi.id().section();
	    int iChannel = digi.id().channel();
	    int chid     = (iSection-1)*5 + (iSide+1)/2*9 + (iChannel-1);
//	    cout << "iSide: " << iSide << "  Section: " << iSection << "  Channel: " << iChannel << "  chid: " << chid << endl;

      	    CaloSamples caldigi;
	    int fTS = digi.size();

     	    for (int i = 0; i < fTS; i++) {
		DigiDatafC[i+chid*10] = digi[i].nominal_fC();
       		DigiDataADC[i+chid*10] = digi[i].adc();
//     		cout << "i: " << i << "  chid*10: " << chid*10 << "  DigiDatafC: " << DigiDatafC[i+chid*10] << "  DigiDataADC: " << DigiDataADC[i+chid*10] << endl;
	    }
	}

      	ZDCDigiTree->Fill();
 
    }
}

void ForwardAnalyzer::beginJob() 
{

    mFileServer->file().SetCompressionLevel(9);
    mFileServer->file().cd();

    std::string bnames[] = {"negEM1","negEM2","negEM3","negEM4","negEM5",
			    "negHD1","negHD2","negHD3","negHD4",
			    "posEM1","posEM2","posEM3","posEM4","posEM5",
			    "posHD1","posHD2","posHD3","posHD4"};
    BranchNames = bnames;
    ZDCDigiTree = new TTree("ZDCDigiTree","ZDC Digi Tree 2");
    BeamTree = new TTree("BeamTree","Beam Tree");

    for (int i = 0; i<18; i++) {
        ZDCDigiTree->Branch((bnames[i]+"fC").c_str(),&DigiDatafC[i*10],(bnames[i]+"cFtsz[10]/F").c_str());
	ZDCDigiTree->Branch((bnames[i]+"ADC").c_str(),&DigiDataADC[i*10],(bnames[i]+"ADCtsz[10]/I").c_str());
    }

    BeamTree->Branch("BunchXing",&BeamData[0],"BunchXing/I");
    BeamTree->Branch("LumiBlock",&BeamData[1],"LumiBlock/I");
    BeamTree->Branch("Run",&BeamData[2],"Run/I");
    BeamTree->Branch("Event",&BeamData[3],"Event/I");

}

void ForwardAnalyzer::endJob() { 
}

void ForwardAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    descriptions.addDefault(desc);
}

// define this as a plug-in
DEFINE_FWK_MODULE(ForwardAnalyzer);
