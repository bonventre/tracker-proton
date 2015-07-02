#ifndef __HIT_T__
#define __HIT_T__

#include <Rtypes.h>
#include <vector>

class Hit : public TObject {
  public:
    Hit(){};
    ~Hit(){};

    Int_t channel;          // straw number
    ULong64_t timeGlobal;   // 36 bit clock counter, lsb is 15.625ps*2^28 = 4.2ms
    ULong64_t timeHV;       // 28 bit clock counter, lsb is 15.625ps. Latched when HV side TDC triggers
    ULong64_t timeCal;      // 28 bit clock counter, lsb is 15.625ps. Latched when cal side TDC triggers
    Double_t deltaT;        // time difference between timeHV and timeCal
    Float_t pedestal;       // average ADC value of presamples in ADC counts
    Float_t peak;           // maximum ADC value after presamples in ADC counts (not pedestal subtracted)
    Float_t minimum;        // minimum ADC value after presamples in ADC counts (not pedestal subtracted)
    Short_t samples[16];    // ADC value in counts of each of the 16 samples, each 20ns apart. The first 3-4 are presamples
    Bool_t trigHV;          // True if the HV side TDC triggered for this hit
    Bool_t trigCal;         // True if the cal side TDC triggered for this hit

    ClassDef(Hit, 1);
};


class Event : public TObject {
  public:
    Event(){};
    ~Event(){};

    int nHits;             // number of hits within this 250ns window
                           // the window starts at the timeCal of the first hit
    bool fifosfull;        // True if fifo was full after this event, so it should be thrown out
                           // when looking for straw to straw coincidences
    std::vector<Hit> hits; // vector of hits in this event, in time order

    ClassDef(Event, 1);
};

#endif
