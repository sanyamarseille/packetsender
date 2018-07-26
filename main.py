#!/usr/bin/env python
# -*- coding: utf-8 -*-

##### Import module #####
import socket
import time
import gzip
import os


##### Variable settings #####
start = time.time()
target_server = ""
target_port = 514
start_path = ""


##### Define action #####
def action(file_path):
    ##### Make socket #####
    ## UDP
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ## TCP
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    ## open and read file 
    f = gzip.open(file_path,"rb")
    line = f.readline()

    ## send log
    while line:
        client.sendto(line,(target_server,target_port))
        ## TCP
        # client.connect((target_server,target_port))
        # client.send(line)
        # client.recv(4096)
        ## read next line
        line = f.readline()
    f.close()

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