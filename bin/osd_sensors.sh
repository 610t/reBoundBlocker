#!/bin/sh
export DISPLAY=:0
MY_PATH=$(dirname $0)
while true; do
  ${MY_PATH}/../i2c/all_sensors.py
done |
  osd_cat --align left \
    --pos bottom \
    --lines 6 \
    -c white \
    --font -*-*-*-*-*--34-*-*-*-*-*-*-* \
    -s 5
ß