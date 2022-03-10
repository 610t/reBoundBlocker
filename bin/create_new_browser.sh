#!/bin/sh
WINDOW_IDS=`wmctrl -l|grep -i chromium|awk '{print $1}'`
# echo ${WINDOW_IDS}

## Create new browser
chromium-browser --new-window $1

## Delete other windows
for i in ${WINDOW_IDS}
do
  wmctrl -i -c $i
done

## Force play movie
sleep 10
xte 'mousemove 500 500'
xte 'mouseclick 1'
