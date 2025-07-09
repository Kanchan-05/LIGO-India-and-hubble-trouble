#!/bin/bash

waveform='IMRPhenomXAS'
f_min=20

# detectors used H1,I1,K1,L1,V1
coincfile='coinc-1365948658.8011718-xzwiyh.xml'


# HL (disable V1, K1, I1)
bayestar-localize-coincs \
    -o coinc-1365948658.8011718-xzwiyh_HL.fits \
    -d V1 K1 I1 \
    --f-low ${f_min} \
    ${coincfile} ${coincfile} \
    --waveform ${waveform} \
    --seed 21343

# L only (disable H1, V1, K1, I1)
bayestar-localize-coincs \
    -o coinc-1365948658.8011718-xzwiyh_L.fits \
    -d H1 V1 K1 I1 \
    --f-low ${f_min} \
    ${coincfile} ${coincfile} \
    --waveform ${waveform} \
    --seed 21343

# HLV (disable K1, I1)
bayestar-localize-coincs \
    -o coinc-1365948658.8011718-xzwiyh_HLV.fits \
    -d K1 I1 \
    --f-low ${f_min} \
    ${coincfile} ${coincfile} \
    --waveform ${waveform} \
    --seed 21343

# HLVK (disable I1)
bayestar-localize-coincs \
    -o coinc-1365948658.8011718-xzwiyh_HLVK.fits \
    -d I1 \
    --f-low ${f_min} \
    ${coincfile} ${coincfile} \
    --waveform ${waveform} \
    --seed 21343

# HLI (disable V1, K1)
bayestar-localize-coincs \
    -o coinc-1365948658.8011718-xzwiyh_HLI.fits \
    -d V1 K1 \
    --f-low ${f_min} \
    ${coincfile} ${coincfile} \
    --waveform ${waveform} \
    --seed 21343

# HLVI (disable K1)
bayestar-localize-coincs \
    -o coinc-1365948658.8011718-xzwiyh_HLVI.fits \
    -d K1 \
    --f-low ${f_min} \
    ${coincfile} ${coincfile} \
    --waveform ${waveform} \
    --seed 21343

bayestar-localize-coincs \
    -o coinc-1365948658.8011718-xzwiyh_HLVIK.fits \
    --f-low ${f_min} \
    ${coincfile} ${coincfile} \
    --waveform ${waveform} \
    --seed 21343
 