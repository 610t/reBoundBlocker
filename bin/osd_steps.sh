#!/bin/sh
export DISPLAY=:0
MY_PATH=`dirname $0`
echo ${MY_PATH}
while true
do
  ${MY_PATH}/../BLE/Get_from_M5Walker.py
done | \
osd_cat --align right \
  --pos bottom \
  --lines 1 \
  -c white \
  --font -*-*-*-*-*--34-*-*-*-*-*-*-* \
  -d 30 \
  -s 5

