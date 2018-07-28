#!/usr/bin/env python
# -*- coding: utf-8 -*-


################################
# import modules
################################
import socket
import time
import gzip
import os
import sys
from scapy.all import *

################################
# Variable settings
################################
start = time.time()
target_server = ""
target_port = 514
start_path = ""
i = 1

# gzip / plain
filemode = "plain"

# scoket / scapy
mode = "socket"

# scapy mode setting
source_server = ""
source_port = 12345

# socket mode setting
# tcp / udp
proto = "tcp"
flag = False

################################
# Define action
################################
def action(file_path):
    global i, flag
    
    # socket mode
    if mode == "socket":
	if proto == "udp":
    		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    	if proto == "tcp":
    		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # open and read file 
    if filemode == "gzip":
    	f = gzip.open(file_path,"rb")
    elif filemode == "plain":
	f = open(file_path,"r")

    payload = f.readline()

    # send data
    while payload:
	if mode == "socket":
		if proto == "udp":
			client.sendto(payload,(target_server,target_port))
		if proto == "tcp" and flag:
                        client.send(payload)
                elif proto == "tcp" and flag == False:
        		client.connect((target_server,target_port))
        		client.send(payload)
                        flag = True
	
	if mode == "scapy":
		packet = IP(src=source_server, dst=target_server)/UDP(sport=source_port, dport=target_port)/payload
                send(packet)
        
	payload = f.readline()
	i = i + 1


    # file close
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

################################
# Main
################################
recursive(start_path)
stop = time.time()
print "処理時間：" + str(format(stop-start,'.3f')) + "秒"
print "処理行数：" + str(i)
