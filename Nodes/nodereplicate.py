# -*- coding: utf-8 -*-
"""
Created on Sat May  4 00:28:29 2019

@author: Mary
"""
import zmq
import sys
#import time

def replicate(sport,nport):
    #port = "1100"
    if len(sys.argv) > 1:
        sport =  int(sys.argv[1])
        nport = int(sys.argv[2])
        context = zmq.Context()
        rSocket = context.socket(zmq.REP)
        rSocket.bind("tcp://*:%s" % sport)
        #int(port)
    while(1):

        rOrS=rSocket.recv_string()
        dIP1 = ""
        dst1 = ""
        dIP2 = ""
        dst2 = ""
        file = ""
        rSocket.send_string("node: your request recieved")
        if(rOrS == "s"):
            dIP1 = rSocket.recv_string()
            rSocket.send_string("node: IP1 recieved")
            dst1 = rSocket.recv_string()
            rSocket.send_string("node: dst1 recieved")
            
            dIP2 = rSocket.recv_string()
            rSocket.send_string("node: IP2 recieved")
            dst2 = rSocket.recv_string()
            rSocket.send_string("node: dst2 recieved")
    
            file = rSocket.recv_string()
            rSocket.send_string("node: file recieved")
            
            print(rSocket.recv_string())
            print("Hey I am sending" , file)
            #time.sleep(5)
            openedFile = open(file,'rb')
            readFile = openedFile.read()
            if(dst1 != ""):
                dstSocket1 = context.socket(zmq.REQ)
                dstSocket1.connect("tcp://%s:%s" % (dIP1,dst1))
        
                print("sending first copy..." )
                dstSocket1.send(readFile)
                dstSocket1.close()
            if(dst2 != ""):
                dstSocket2 = context.socket(zmq.REQ)
                dstSocket2.connect("tcp://%s:%s" % (dIP2,dst2)) 
                
                print("sending second copy..." )
                dstSocket2.send(readFile)
                dstSocket2.close()
            openedFile.close()
            rSocket.send_string("node: Done replicating")
            #rSocket.close()
        elif(rOrS == "r"):
            context = zmq.Context()
            nSocket = context.socket(zmq.REP)
            nSocket.bind("tcp://*:%s" % nport)
            print("replicating...")
            file = rSocket.recv_string()
            rSocket.send_string("rep node: file name recieved")
    
            recFile = nSocket.recv()
            print("Done replication")
            openedFile = open(file,'wb')
            openedFile.write(recFile)
            openedFile.close()
            nSocket.close()
            #rSocket.close()
            
        
#replicate(7000,6000)

    
    
    
    
    
    
    
    

