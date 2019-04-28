# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:29:00 2019

@author: Dalia
"""
import zmq
import time
import sys
import random
import threading

#LookUpTable

file =[]
file.append("name.mp4")

user ={}
user[100]=file
user[200]=file
user[300]=file

alive='Y'
Nalive='N'
node = [user,alive]
node1 = [user,alive]
node2 = [user,alive]
LookUpTable={}

LookUpTable[0]=node
LookUpTable[1]=node1
LookUpTable[2]=node2


#array nodes and processes
Nports = [[["1100",'Y','A'],["2000",'N','A'],["3000",'N','A']],[["4000",'N','A'],["5000",'Y'],["600",'Y','A']],[["700",'Y','A'],["800",'Y','A'],["900",'Y','A']]]

#def pickNode():
n= []
for i in range(len(LookUpTable)):
    if LookUpTable[i][1] == 'Y':
        n.append(i)

k=random.choice(n)
    
#print(LookUpTable)

def Nodes():
#    i=0
    while 1:
     #connecting to Nodes
        socketNode.setsockopt_string(zmq.SUBSCRIBE, "ALIVE")
        string = socketNode.recv_string()
        #print("recieved ",string )
        time.sleep(1)
        topic, IP = string.split()
        print (topic, IP)
#        i+=1
   
    


    
def client():
    #  Wait for next request from client
    while(1):
        message = ""
        message = socket.recv_string()
        print ("Received request: ", message)
        time.sleep(1)
        print ("Finding available ports... ")
        
        msg = str(message)
        
        if(msg == "1"):
 
            #pick machine random and choose first port alive
            res = ""
            j=0
 
            while (res=="" and j in range(len(Nports[k]))):
                if Nports[k][j][1] == 'Y':
                    res = Nports[k][j][0]
                j+=1
            #set busy
            #Nports[k][j-1][2]= 'B'
            
            socket.send_string(res)
            time.sleep(1)
            print ("Reply is sent... ")
        
        
def successNode():        
     #recived success from node 
     print(socketNode1.recv_string())
     time.sleep(1)
#     socket.send_string("Uploaded Successfully")
   
def successClient():
#    while 1:
    #send success to client
    socketClient.send_string("Uploaded Successfully")


###################################################
#connecting to clients
if __name__ == "__main__": 
    
    port = "5556"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)
    
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    print("connecting to client...")
    
    ##############################################################
    #connecting to Nodes
    port1 = "5555"
    socketNode = context.socket(zmq.SUB)
        
    print("conecting to nodes...")
    socketNode.connect ("tcp://localhost:%s" % port1)
    
    
    ##############################################################
    #to recieve success from nodes
    portz = "1077"

    socketNode1 = context.socket(zmq.REP)
    socketNode1.bind ("tcp://*:%s" % portz)
    
    ##############################################################
    
    #to send success to clients
    portx = "1088"

    socketClient = context.socket(zmq.REP)
    socketClient.bind ("tcp://*:%s" % portx)
    
    ##############################################################
    # creating thread 
    t1 = threading.Thread(target=Nodes) 
    t2 = threading.Thread(target=client) 
    t3 = threading.Thread(target=successNode)
    t4 = threading.Thread(target=successClient)
    #while True:
        # starting thread 1 
    t2.start() 
    # starting thread 2 
    t1.start() 
    
    t3.start()
    
    t3.join()
    t4.start()