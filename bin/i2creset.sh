#!/bin/sh
sudo rmmod i2c_dev
sudo rmmod i2c_bcm2708
sleep 5
sudo modprobe i2c_bcm2708
sudo modprobe i2c_dev
