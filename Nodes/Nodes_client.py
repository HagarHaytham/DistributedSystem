# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:17:55 2019

@author: Dalia
"""
import zmq
import time
import sys


port = "777"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

print ("connecting to client...")

f = open('file.mp4','wb')

#while True:
    
l = socket.recv()
print ("Receiving...")
time.sleep(1)
f.write(l)
f.close()
#time.sleep(10)
#print ("Done Receiving")
socket.send_string('Done Sending')
time.sleep(1)
print(socket.recv_string())
time.sleep(1)
socket.close()                # Close the connection
