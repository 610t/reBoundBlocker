#!/bin/sh
export DISPLAY=:0
MY_PATH=`dirname $0`
echo ${MY_PATH}
while true
do
  ${MY_PATH}/../i2c/sensors_sgp30_bme280_bh1750.py
done | \
osd_cat --align left \
  --pos bottom \
  --lines 6 \
  -c white \
  --font -*-*-*-*-*--34-*-*-*-*-*-*-* \
  -s 5

  #-delay 1 \
