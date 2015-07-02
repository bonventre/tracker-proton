## Data Format

The proton data is saved in a simple root format. Each file has two TTrees: "T", which has all the straw hit information, and "Run", which has the meta information about the run.

Run generate_library.sh to create the ROOT dictionary for the custom classes used.

### Event Data

"T" has one branch, "events". The events are created by looping over all the straw hits. After the first hit, a 250ns window after it is opened and additional hits in any straw within this window are added to the event. 

The hit data format is documented in Hit.h

### Run Data

The "Run" tree branches are:

- totalTime: the wall clock length of the run
- threshHV: vector of the preamp thresholds in DAC counts for the HV side preamps. Higher DAC counts = lower threshold
- threshCal: vector of the preamp thresholds in DAC counts for the cal side preamps. Higher DAC counts = lower threshold
- gainHV: vector of the preamp gains in DAC counts for the HV side preamps. Higher DAC counts = higher stage 3 gain
- gainCal: vector of the preamp gains in DAC counts for the cal side preamps. Higher DAC counts = higher stage 3 gain
- calDAC: vector of the calibration DAC amplitude setting in DAC counts. Higher DAC counts = larger calibration pulse
- runMode: readout configuration
- adcMode: 0=normal, 1+ = ADC patterns
- tdcMode: 0=normal, 1  = trigger on internal pulser
- samples: number of ADC samples to save per hit, including presamples
- lookback: number of ADC presamples, samples before the hit triggered
- triggers: readout configuration
- chanMask: bit mask of channels that had readout enabled
- message: metainformation about the run
- filename:
- runnumber:

## Example Script

The file example.py shows how to analyze the data, including calculating livetime and plotting coincidences
