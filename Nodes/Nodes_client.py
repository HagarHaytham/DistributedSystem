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

def alive(serverSocket):

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
#    port = sys.argv[2]
#    clientSocket = context.socket(zmq.REP)
#    clientSocket.bind("tcp://*:%s" % port)
    #####################################
    
    print ("connecting to client...")
    file= uplS.recv_string()
    print("recieved file name ",file)
    uplS.send_string('Thank you for connecting') 
    
    l = uplS.recv()
    uplS.send_string('dummy')
    #time.sleep(1)
    f = open(file,'wb')
    f.write(l)
    f.close()
    print ("Done Receiving")
    
    msg="Success " + file
    succ.send_string(msg)
    #serverSocket1.send_string(file)
    #time.sleep(1)
    print(msg)

    return

def dwn(uplS):
    return

def replicate(context, port):
    
    while True:
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
                dstSocket1.close()
                
            if(dst2 != ""):
                dstSocket2 = context.socket(zmq.REQ)
                dstSocket2.connect("tcp://localhost:%s" % dst2) 
                
                print("sending second copy..." )
                dstSocket2.send(readFile)
                dstSocket2.close()
                
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

        rSocket.close()

    return

########################################################## 
def main(aliveP, upldP, successP, dwnldP, replServerP)

    
    context = zmq.Context()
    success = initConn(context, successP)    
    
    
    uplS,dwnldS = connectClients(context, upldP, dwnldP)
    # repPort = sys.argv[4]
    
    t1 = threading.Thread(target=upload,args=(uplS,success)) 
    t2 = threading.Thread(target=alive, args = (aliveP))
    t3 = threading.Thread(target=dwn,args=(dwnldS))
    replicationThread = threading.Thread(target = replicate, args = (context, replServerP))
    replicationThread.start()
    #connecting to server
#    port1 = "5555"
    
    serverSocket = context.socket(zmq.PUB)
#    serverSocket.bind("tcp://*:%s" % port1)
#    print ("connecting to Server...")

    t1.start()
    #t2.start()


if __name__=='__main__':
    p=[]
    for i in range(3):
        p.append(Process(target=main,args=(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])))
        p[i].start()
        

