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
from multiprocessing import Process

file = ""

def connectClients(context, uplPort, dnlwdPort):
    
    #connect client
    uplSocket = context.socket(zmq.REP)
    uplSocket.bind ("tcp://*:%s" % uplPort)
    
    dnlwdSocket = context.socket(zmq.REP)
    dnlwdSocket.bind ("tcp://*:%s" % dnlwdPort)
        
    return uplSocket,dnlwdSocket
    

def initConn(context, successPort):
    #connect server
    successSocket = context.socket(zmq.REQ)
    successSocket.connect ("tcp://localhost:%s" % successPort)
    
    return successSocket
    
##########################################################

def alive(context,aliveP):
    
    serverSocket = context.socket(zmq.PUB)
    serverSocket.bind("tcp://*:%s" % aliveP)
    print ("connecting to Server...")
    while (1):
       
        topicfilter = socket.gethostbyname(socket.gethostname())
        topicfilter+= "@" + port1
        messagedata = "ALIVE"
        serverSocket.send_string("%s %s" % (messagedata, topicfilter))
        time.sleep(1)
        print(topicfilter)
        
##########################################################

def upload(uplS,succ):
    #connect to client 
    print ("connecting to client...")
    #recv file name
    file= uplS.recv_string()
    print("recieved file name ",file)
    uplS.send_string('Thank you for connecting') 
    #recv video
    l = uplS.recv()
    uplS.send_string('dummy')
    #time.sleep(1)
    f = open(file,'wb')
    f.write(l)
    f.close()
    print ("Done Receiving")
    
    msg="Success " + file
    succ.send_string(msg)
    print(msg)

    return


def dwnld(dwnldS):

    while True:
        message = dwnldS.recv_string()
        print ("Received request: ", message)
        time.sleep (1)
        dwnldS.send_string("World from ..." )
    return

########################################################## 
def main(masterIP, aliveP, upldP, successP, dwnldP, replServerP):

    print('run data node', aliveP)  

    context = zmq.Context()
    success = initConn(context, successP)  
    
    uplS,dwnldS = connectClients(context, upldP, dwnldP)
    
    t1 = threading.Thread(target=upload,args=(uplS,success)) 
    t2 = threading.Thread(target=alive, args = (aliveP))
    dwnldThread = threading.Thread(target=dwnld,args=(dwnldS))
    
    t1.start()
    # t2.start()

    return

# if __name__=='__main__':
#     p=[]
#     for i in range(3):
#         p.append(Process(target=main,args=(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])))
#         p[i].start()
        

