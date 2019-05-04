# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:17:55 2019

@author: Dalia
"""
import zmq
import time
import sys
import socket
import threading

file = ""


def connectClient():
    
    while 1:
        #connect server
        portChoice = "1066"
        serverChoice = context.socket(zmq.REQ)
        serverChoice.connect ("tcp://localhost:%s" % portChoice)
        #recv choice of client from server
        serverChoice.send_string("Node ready for request...")
        choice = serverChoice.recv_string()
        
        if(choice == '1'):
            upload()
        elif(choice == '2'):
            print("show")
        elif(choice == '3'):
            print("download")
    
##########################################################

def alive():

    while (1):
       
        topicfilter = socket.gethostbyname(socket.gethostname())
        topicfilter+= "@" + port1
        messagedata = "ALIVE"
        serverSocket.send_string("%s %s" % (messagedata, topicfilter))
        time.sleep(1)
        print(topicfilter)
        
##########################################################

def upload():
    #connect to client
    port = "2000"
    clientSocket = context.socket(zmq.REP)
    clientSocket.bind("tcp://*:%s" % port)
    #####################################
    print ("connecting to client...")
    l = clientSocket.recv()
    #time.sleep(1)
    f = open('file.mp4','wb')
    f.write(l)
    f.close()
    print ("Done Receiving")
    clientSocket.send_string('Thank you for connecting') 
    file= clientSocket.recv_string()
    print("recieved file name ",file)
    #####################################
    portz= "1077"
    serverSocket1 = context.socket(zmq.REQ)
    serverSocket1.connect("tcp://localhost:%s" % portz)
    
    msg="Uploaded Successfully"
    serverSocket1.send_string(msg)
    #serverSocket1.send_string(file)
    #time.sleep(1)
    print(msg)

########################################################## 
if __name__ == "__main__":
    
    t1 = threading.Thread(target=connectClient) 
    t2 = threading.Thread(target=alive)
    
    #connecting to server
    port1 = "5555"
    context = zmq.Context()
    serverSocket = context.socket(zmq.PUB)
    serverSocket.bind("tcp://*:%s" % port1)
    print ("connecting to Server...")

    t1.start()
    t2.start()
