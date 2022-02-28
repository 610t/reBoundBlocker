#!/bin/sh
export DISPLAY=:0
while true
do
  sudo /home/pi/reBoundBlocker/BLE/Get_from_M5Walker.py
done | \
osd_cat --align right \
  --pos bottom \
  --lines 1 \
  -c white \
  --font -*-*-*-*-*--34-*-*-*-*-*-*-* \
  -d 30 \
  -s 5

