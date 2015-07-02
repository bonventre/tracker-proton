import ROOT
ROOT.gSystem.Load("Dict.so")
from ROOT import Event, Hit

import sys
f = ROOT.TFile(sys.argv[1])
t = f.Get("T")
run = f.Get("Run")
run.GetEntry(0)

total_deadtime = 0

# first calculate actual livetime.
# deadtime is time from first hit in event with
# fifosfull = True to first hit in next event
dead = False
deadstarttime = 0
lasthittime = 0
for i in range(t.GetEntries()):
  t.GetEntry(i)

  if dead:
    # get hit time in seconds since start of run
    hittime = (t.events.hits[0].timeGlobal*2**28 + t.events.hits[0].timeCal)*15.625*10**-12 
    total_deadtime += hittime-deadstarttime
    dead = False

  if t.events.fifosfull:
    dead = True
    # get hit time in seconds since start of run
    deadstarttime = (t.events.hits[0].timeGlobal*2**28 + t.events.hits[0].timeCal)*15.625*10**-12

# livetime is total run time minus deadtime
total_livetime = run.totalTime - total_deadtime
print total_livetime

# now we will find all the ''good'' hits and look for coincidences
# between hits in straws 1 and 2
h1 = ROOT.TH1F("h1","Straw 1 / straw 2 coincidence",100,-100,100)
h1.GetXaxis().SetTitle("Straw 1 time - straw 2 time (ns)")
for i in range(t.GetEntries()):
  t.GetEntry(i)
  if t.events.fifosfull:
    continue
  straw1 = -1
  straw2 = -1
  for j in range(t.events.nHits):
    hit = t.events.hits[j]
    # cut if only one side of straw fired
    if not hit.trigHV or not hit.trigCal:
      continue
    # cut if delta t too large
    if hit.deltaT < -40 or hit.deltaT > 40:
      continue
    # cut if pulse too small
    if hit.peak - hit.pedestal < 50:
      continue
    # probably a good hit here
    if hit.channel == 1:
      straw1 = j
    if hit.channel == 2:
      straw2 = j
  # check if we found good hits in both straws in this event
  if straw1 != -1 and straw2 != -1:
    # get the difference in the hit times (in ns)
    straw1time = (t.events.hits[straw1].timeGlobal*2**28 + t.events.hits[straw1].timeCal)*15.625*10**-3
    straw2time = (t.events.hits[straw2].timeGlobal*2**28 + t.events.hits[straw2].timeCal)*15.625*10**-3
    h1.Fill(straw1time-straw2time)

h1.Draw()
raw_input()
