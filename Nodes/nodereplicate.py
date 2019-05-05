# -*- coding: utf-8 -*-
"""
Created on Sat May  4 00:28:29 2019

@author: Mary
"""
import zmq
import socket
import sys
import time

def replicate():
    port = "1100"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)
    context = zmq.Context()
    rSocket = context.socket(zmq.REP)
    rSocket.bind("tcp://*:%s" % port)
    rOrS=rSocket.recv_string()
    dst1 = ""
    dst2 = ""
    file = ""
    rSocket.send_string("node: your request recieved")
    if(rOrS == "s"):
        dst1 = rSocket.recv_string()
        #time.sleep(5)
        rSocket.send_string("node: dst1 recieved")

        dst2 = rSocket.recv_string()
        rSocket.send_string("node: dst2 recieved")

        file = rSocket.recv_string()
        rSocket.send_string("node: file recieved")
        
        print(rSocket.recv_string())
        
        time.sleep(5)
        openedFile = open(file,'rb')
        readFile = openedFile.read()
        if(dst1 != ""):
            dstSocket1 = context.socket(zmq.REQ)
            dstSocket1.connect("tcp://localhost:%s" % dst1)
    
            print("sending first copy..." )
            dstSocket1.send(readFile)
            
        if(dst2 != ""):
            dstSocket2 = context.socket(zmq.REQ)
            dstSocket2.connect("tcp://localhost:%s" % dst2) 
            
            print("sending second copy..." )
            dstSocket2.send(readFile)
            
        openedFile.close()
        rSocket.send_string("node: Done replicating")
        
    elif(rOrS == "r"):
        print("replicating...")
        file = rSocket.recv_string()
        rSocket.send_string("rep node: file name recieved")

        recFile = rSocket.recv()
        
        openedFile = open(file,'wb')
        openedFile.write(recFile)
        openedFile.close()
        
        
replicate()

    
    
    
    
    
    
    
    

