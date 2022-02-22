#!/usr/bin/env python3
import smbus
import time

addr=0x45

i2c=smbus.SMBus(1)

## Data read loop
# while True:
i2c.write_byte_data(addr, 0x2c, 0x06)
time.sleep(0.5)
data=i2c.read_i2c_block_data(addr,0x00,6)
# print("Raw:",data)
print("Temp:",(((data[0]<<8|data[1])*175)/65535)-45)
print("Hum :",(((data[3]<<8|data[4])*100)/65535))
time.sleep(0.5)
