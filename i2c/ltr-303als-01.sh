#!/bin/sh
echo -n "Light:"
cat /sys/bus/iio/devices/iio\:device0/in_illuminance_input
