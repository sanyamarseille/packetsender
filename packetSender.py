#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import sys
import yaml
import traceback
import time
import logging
# https://docs.python.org/ja/3/library/logging.html#levels
logging.getLogger('scapy').setLevel(logging.ERROR)

# https://scapy.readthedocs.io/en/latest/extending.html
from scapy.all import *

def Error(e, TracebackData):
    print(TracebackData)
    print(e)
    sys.exit(1)

# Get setting
def LoadSettings():
    try:
        with open('setting.yaml', 'r') as yml:
            config = yaml.safe_load(yml)

    except Exception as e:
        Error(e, traceback.format_exc())

    print('Load settings...\tOK')
    return config

# Get log file path
def LoadLogs(config):
    DirPath = config['Logs']['DirPath']
    try:
        # directory check
        if os.path.isdir(DirPath):
            if DirPath[:-1] == "/":
                tail = "*"
            else:
                tail = "/*"
            Files = glob(DirPath + tail)
        else:
            Files = []
            Files.append(DirPath)
        
        print('Load logs...\t\tOK')
        return Files

    except Exception as e:
        Error(e, traceback.format_exc())

def SendPacket(config, LogFile, LogLineCounter):

    print('Send logs...')
    try:
        s = conf.L3socket()
        packet = IP(
            src = config['Source']['IPAddress'],
            dst = config['Destination']['IPAddress'])\
            /UDP(
            sport = config['Source']['Port'],
            dport = config['Destination']['Port'])
        with open(LogFile, 'r') as f:
            for payload in f:
                s.send(packet/payload)
                LogLineCounter += 1

    except Exception as e:
        Error(e, traceback.format_exc())

    print('\t\t\tOK\t', LogFile)
    return LogLineCounter

## main

if __name__ == "__main__":

    LogLineCounter = 0

    StartTime = time.time()

    # Load setting.yaml
    Config = LoadSettings()

    # List up at log files
    LogFiles = LoadLogs(Config)

    # Send logs
    for i in range(len(LogFiles)):
        LogLineCounter = SendPacket(Config, LogFiles[i], LogLineCounter)

    EndTime = time.time()

    print('Send log line:\t\t' + str(LogLineCounter))
    print('Duration Time:\t\t' + str(format(EndTime - StartTime,'.3f')) + 's')
    
    sys.exit(0)

else:
    print('Usage: python3 packetSender.py')
