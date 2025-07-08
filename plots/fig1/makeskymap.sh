#!/bin/bash


base="coinc-1365948658.8011718-xzwiyh_HLV.fits"
filenames=($(ls ${base}/*.fits))


CMD="ligo-skymap-plot --output ${base}.png --contour 50 90 --annotate --colorbar ${filenames[@]} --zoom-radius 4deg"
echo $CMD
eval $CMD