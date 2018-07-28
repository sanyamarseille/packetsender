#!/usr/bin/env python
# -*- coding: utf-8 -*-

##### Import module #####
import socket
import time
import gzip
import os
import sys
from scapy.all import *
#########################


##### Variable settings #####

#### share setting ####
start = time.time()
target_server = ""
target_port = 
start_path = ""
i = 0
### gzip or plain
filemode = "plain"

### scoket or scapy
mode = "scapy"

## scapy mode setting
source_server = ""
source_port = 

## socket mode setting
# tcp or udp
proto = "tcp"
flag = False
#############################



##### Define action #####
def action(file_path):
    global i

    #### socket mode
    if mode == "socket":
    	### protocol select
	if proto == "udp":
    		## UDP
    		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	if proto == "tcp":
		## TCP
    		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #### open and read file 
    if filemode == "gzip":
    	f = gzip.open(file_path,"rb")
    elif filemode == "plain":
	f = open(file_path,"r")
    payload = f.readline()

    #### send log
    while payload:
	#### socket mode
	if mode == "socket":
		## UDP
		if proto == "udp":
			client.sendto(payload,(target_server,target_port))
		## TCP 
                # connected
		if proto == "tcp" and flag:
                        client.send(payload)
                elif proto == "tcp" and flag == False:
        		client.connect((target_server,target_port))
        		client.send(payload)
                        Flag = True
	
	#### scapy mode
	if mode == "scapy":
		packet = IP(src=source_server, dst=target_server)/UDP(sport=source_port, dport=target_port)/payload
                send(packet)
        #### read next line
        sys.stdout.flush()
        i = i + 1
        payload = f.readline()

    ######################

    #### file close
    f.close()

    if mode == "socket" and proto == "tcp":
        client.close()

def recursive(path):
    ## sub_directory check
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            ## check nest
            recursive(path + "/" + file)
    else:
        action(path)

## program start
recursive(start_path)

stop = time.time()

print "処理時間：" + str(format(stop-start,'.3f')) + "秒"
print "処理行数：" + str(i)
