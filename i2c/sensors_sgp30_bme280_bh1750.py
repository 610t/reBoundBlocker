#!/usr/bin/env python3
import os
import smbus
import time
import subprocess
from subprocess import PIPE

addr=0x58

i2c=smbus.SMBus(1)
i2c.write_byte_data(addr, 0x36, 0x82)
time.sleep(0.01)
i2c.write_byte_data(addr, 0x20, 0x2f)
time.sleep(0.01)
i2c.write_byte_data(addr, 0x20, 0x03)
time.sleep(0.01)
#time.sleep(15)

path=os.path.dirname(__file__)

while True:
  ## BH1750
  proc_bh1750=subprocess.run(path+"/bh1750.py",shell=True,stdout=PIPE,text=True)
  ## BME280
  proc_bme280=subprocess.run(path+"/bme280.py",shell=True,stdout=PIPE,text=True)
  ## SGP30
  i2c.write_byte_data(addr, 0x20, 0x08)
  time.sleep(0.01)
  data=i2c.read_i2c_block_data(addr,0x00,6)
  time.sleep(0.01)
  #print("Raw:",data)

  # DISPLAY result
  print(proc_bh1750.stdout.strip())
  print(proc_bme280.stdout.strip())
  print("eCO2:",data[0]<<8|data[1], flush=True)
  print("TVOC:",data[3]<<8|data[4], flush=True)
  # time.sleep(1)
