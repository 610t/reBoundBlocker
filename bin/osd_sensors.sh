#!/bin/sh
export DISPLAY=:0
while true
do
  /home/pi/reBoundBlocker/i2c/sensors_sgp30_bme280_bh1750.py
done | \
osd_cat --align left \
  --pos bottom \
  --lines 6 \
  -c white \
  --font -*-*-*-*-*--34-*-*-*-*-*-*-* \
  -s 5

  #-delay 1 \
