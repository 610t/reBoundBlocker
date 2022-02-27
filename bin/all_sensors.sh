#!/bin/sh
echo "* BME280"
~/reBoundBlocker/i2c/bme280.py
echo "* SHT3x"
~/reBoundBlocker/i2c/sht3x.py
echo "* BH1750"
~/reBoundBlocker/i2c/bh1750.py
echo "* SGP30"
~/reBoundBlocker/i2c/sgp30.py
