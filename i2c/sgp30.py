#!/usr/bin/env python3
import smbus
import time

addr=0x58

i2c=smbus.SMBus(1)
i2c.write_byte_data(addr, 0x36, 0x82)
time.sleep(0.01)
i2c.write_byte_data(addr, 0x20, 0x2f)
time.sleep(0.01)
i2c.write_byte_data(addr, 0x20, 0x03)
time.sleep(0.01)
time.sleep(15)

## Data read loop
# while True:
i2c.write_byte_data(addr, 0x20, 0x08)
time.sleep(0.01)
data=i2c.read_i2c_block_data(addr,0x00,6)
# print("Raw:",data)
print("eCO2:",data[0]<<8|data[1])
print("TVOC:",data[3]<<8|data[4])
