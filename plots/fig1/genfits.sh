#!/bin/bash

waveform='IMRPhenomXAS'
f_min=20

coincfile='coinc-1365948658.8011718-xzwiyh.xml'

bayestar-localize-coincs  -o coinc-1365948658.8011718-xzwiyh_only_L.fits -d H1 V1 I1  --f-low ${f_min} ${coincfile} ${coincfile} --waveform ${waveform} --seed 21343 
bayestar-localize-coincs  -o coinc-1365948658.8011718-xzwiyh_HL.fits -d V1 I1  --f-low ${f_min} ${coincfile} ${coincfile} --waveform ${waveform} --seed 21343
bayestar-localize-coincs  -o coinc-1365948658.8011718-xzwiyh_HLV.fits -d I1 --f-low ${f_min} ${coincfile} ${coincfile} --waveform ${waveform} --seed 21343
bayestar-localize-coincs  -o coinc-1365948658.8011718-xzwiyh_HLVI.fits --f-low ${f_min} ${coincfile} ${coincfile} --waveform ${waveform} --seed 21343

