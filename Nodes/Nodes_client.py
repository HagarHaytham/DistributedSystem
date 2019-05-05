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


def connectClients(context,uplPort,dnlwdPort):
    
    #connect client
    # uplPort = sys.argv[2]
    uplSocket = context.socket(zmq.REP)
    uplSocket.bind ("tcp://*:%s" % uplPort)
    
    
    # dnlwdPort = sys.argv[3]
    dnlwdSocket = context.socket(zmq.REP)
    dnlwdSocket.bind ("tcp://*:%s" % dnlwdPort)
        
    return uplSocket,dnlwdSocket
    

def initConn(context,port1,ip1):
     #connect server
    # serverPort = sys.argv[1]
    serverSocket = context.socket(zmq.REQ)
    serverSocket.connect ("tcp://%s:%s" % (ip1,port1)
    
    return serverSocket
    
        #recv choice of client from server
        #serverChoice.send_string("Node ready for request...")
#        choice = serverChoice.recv_string()
#        
#        if(choice == '1'):
#            upload()
#        elif(choice == '2'):
#            print("show")
#        elif(choice == '3'):
#            print("download")
    
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
    
    while True:
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
        
        #    
        #####################################
        #    portz= "1077"
        #    serverSocket1 = context.socket(zmq.REQ)
        #    serverSocket1.connect("tcp://localhost:%s" % portz)
        
        msg="Success " + file
        succ.send_string(msg)
        #serverSocket1.send_string(file)
        #time.sleep(1)
        print(msg)
    
    return

def dwn(uplS):
    return
########################################################## 
def main(port1,port2,port3,ip1):

    
    context = zmq.Context()
    success = initConn(context,port1,ip1)    
    
    uplS,dwnldS = connectClients(context,port2,port3)
    
    t1 = threading.Thread(target=upload,args=(uplS,success)) 
    t2 = threading.Thread(target=alive, args = (success))
    t3 = threading.Thread(target=dwn,args=(dwnldS))
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
        

