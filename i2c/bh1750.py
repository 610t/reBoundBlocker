#!/usr/bin/env python3
import smbus
import time

addr=0x23

i2c=smbus.SMBus(1)

## Data read loop
# while True:
i2c.write_byte(addr, 0x10)
time.sleep(0.5)
data=i2c.read_i2c_block_data(addr,0x00,2)
# print("Raw:",data)
print("lx:",(data[0]<<8|data[1])/1.2)
