#!/bin/sh
export DISPLAY=:0
MY_PATH=`dirname $0`
while true
do
  sudo ${MY_PATH}/../BLE/Get_from_M5Walker.py
  sleep 10
done | \
osd_cat --align right \
  --pos bottom \
  --lines 1 \
  -c white \
  --font -*-*-*-*-*--34-*-*-*-*-*-*-* \
  -d 30 \
  -s 5

