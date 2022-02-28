#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Based on https://github.com/AmbientDataInc/EnvSensorBleGw/blob/master/src/gw_RPi/env2ambientBS.py .

from bluepy.btle import Peripheral, DefaultDelegate, Scanner, BTLEException, UUID
import bluepy.btle
import sys
import struct
from datetime import datetime
import argparse
import time

total_step=0
last_step=0
last_seq=0

devs = {
    'M5Walker': {'companyID': 'ffff'}
}
target = 'M5Walker'

Debugging = False
def DBG(*args):
    if Debugging:
        msg = " ".join([str(a) for a in args])
        print(msg)
        sys.stdout.flush()

Verbose = True
def MSG(*args):
    if Verbose:
        msg = " ".join([str(a) for a in args])
        print(msg)
        sys.stdout.flush()

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.lastseq = None
        self.lasttime = datetime.fromtimestamp(0)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev or isNewData:
            for (adtype, desc, value) in dev.getScanData():
                DBG(adtype, desc, value)
                if target in ('M5Walker'):
                    if desc == 'Manufacturer' and value[0:4] == devs[target]['companyID']:
                        delta = datetime.now() - self.lasttime
                        if value[4:6] != self.lastseq and delta.total_seconds() > 11: # アドバタイズする10秒の間に測定が実行されseqが加算されたものは捨てる
                            global last_seq, total_step, last_step
                            seq = int(value[4:6], 16)
                            if seq < last_seq:
                                total_step += last_step
                            last_seq = seq
                            DBG("Seq:", self.lastseq)
                            self.lasttime = datetime.now()
                            DBG("Time:", self.lasttime)
                            DBG("Value:",value[6:10],bytes.fromhex(value[6:10]))
                            step = struct.unpack('<h', bytes.fromhex(value[6:10]))[0]
                            print("Step:", step, "+", total_step)
                            sys.stdout.flush()
                            last_step = step

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',action='store_true', help='debug msg on')

    args = parser.parse_args(sys.argv[1:])

    global Debugging
    Debugging = args.d
    bluepy.btle.Debugging = args.d

    global target
    print(target)

    scanner = Scanner().withDelegate(ScanDelegate())
    while True:
        try:
            scanner.scan(5.0) # スキャンする。デバイスを見つけた後の処理はScanDelegateに任せる
        except BTLEException:
            MSG('BTLE Exception while scannning.')

if __name__ == "__main__":
    main()
