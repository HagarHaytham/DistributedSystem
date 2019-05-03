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


def alive():
#    i=0
    while (1):
        topicfilter = socket.gethostbyname(socket.gethostname())
        topicfilter+= "@" + port1
        messagedata = "ALIVE"
        serverSocket.send_string("%s %s" % (messagedata, topicfilter))
        time.sleep(1)
        print(topicfilter)
#        i+=1

def upload():
    print ("Receiving...")
    l = clientSocket.recv()
    f.write(l)
    f.close()
    #time.sleep(10)
    print ("Done Receiving")
    clientSocket.send_string('Thank you for connecting') 
    file= clientSocket.recv_string()
    print("recieved file name ",file)

    
def success():
#    while 1:
    msg="Uploaded Successfully"
    serverSocket1.send_string(msg)
    
    time.sleep(1)
    print(msg)

    
if __name__ == "__main__":
    
    
    port = "2000"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)
    context = zmq.Context()
    clientSocket = context.socket(zmq.REP)
    clientSocket.bind("tcp://*:%s" % port)
    
    print ("connecting to client...")
    
    
    #####################################
    
    port1 = "5555"
    serverSocket = context.socket(zmq.PUB)
    serverSocket.bind("tcp://*:%s" % port1)
    print ("connecting to Server...")
    
    ####################################
    
    #to send success to server
    portz= "1077"
    serverSocket1 = context.socket(zmq.REQ)
    serverSocket1.connect("tcp://localhost:%s" % portz)
    
    ####################################
    
    f = open('file.mp4','wb')
    
    #while True:
    t1 = threading.Thread(target=upload) 
    t2 = threading.Thread(target=alive)
    t3 = threading.Thread(target=success)
    
    t1.start()
    t2.start()
    
    t1.join()
    
    t3.start()
    
    
   
