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


#{0: [{100: ['name.mp4'], 200: ['name.mp4'], 300: ['name.mp4']}, 'Y'],
# 1: [{100: ['name.mp4'], 200: ['name.mp4'], 300: ['name.mp4']}, 'Y'], 
# 2: [{100: ['name.mp4'], 200: ['name.mp4'], 300: ['name.mp4']}, 'Y']}

#array nodes and processes
Nports = [[["1100",'Y','A'],["2000",'N','A'],["3000",'N','A']],[["4000",'N','A'],["5000",'Y'],["600",'Y','A']],[["700",'Y','A'],["800",'Y','A'],["900",'Y','A']]]

##def pickNode():
#n= []
#for i in range(len(LookUpTable)):
#    if LookUpTable[i][1] == 'Y':
#        n.append(i)
#
#k=random.choice(n)
    
#print(LookUpTable)

#############################################################
def Nodes():
    while 1:
     #connecting to Nodes
        socketNode.setsockopt_string(zmq.SUBSCRIBE, "ALIVE")
        string = socketNode.recv_string()
        #print("recieved ",string )
        time.sleep(1)
        topic, IP = string.split()
        print (topic, IP)

#############################################################
def client():
    #  Wait for next request from client
    
     #send choice to node
    choicePort = "1066"
    choiceNode = context.socket(zmq.REP)
    choiceNode.bind("tcp://*:%s" % choicePort)
    ##################################
    while(1):
        
        message = ""
        message = socket.recv_string()
        print ("Received request: ", message)
        time.sleep(1)
        msg = str(message)
       
        if(msg == "1"):
            #pick machine random and choose random port alive
            #random pickNode
            print ("Finding available ports... ")
            n= []
            for i in range(len(LookUpTable)):
                if LookUpTable[i][1] == 'Y':
                    n.append(i)
            
            k=random.choice(n)
            
            res = ""
            j=0
            while (res=="" and j in range(len(Nports[k]))):
                if Nports[k][j][1] == 'Y':
                    res = Nports[k][j][0]
                j+=1
            #set busy
            #Nports[k][j-1][2]= 'B'
            
            #send port to client
            socket.send_string(res)
            #time.sleep(1)
            print ("Reply is sent... ")
            
            ##########################
            #send choice to node
            print(choiceNode.recv_string())
            choiceNode.send_string(msg)
            #########################
            #recived and send success  
            success()
        
        elif(msg == "2"):
            
            ##########################
            #send choice to node
            print(choiceNode.recv_string())
            choiceNode.send_string(msg)
            #########################
            #################################################
            #get files for user
            UserId = 100
            arr = ""
            for i in range(len(LookUpTable)):
                if(LookUpTable[i][0][UserId]):
                    userFiles = LookUpTable[i][0][UserId] 
                    for j in range(len(userFiles)):
                        arr += userFiles[j]
                        arr += '\n'
               
            print(arr)
            socket.send_string(arr)
        
            #send success to client
            #portx = "1088"
            #context = zmq.Context()
            #socketClient = context.socket(zmq.REQ)
            #socketClient.connect ("tcp://localhost:%s" % portx)    
            #socketClient.send_string("show done Successfully")
        
#############################################################
def success():
    
     #recived success from node 
     portz = "1077"
     socketNode1 = context.socket(zmq.REP)
     socketNode1.bind ("tcp://*:%s" % portz)
     succ= socketNode1.recv_string()
     print(succ)
     ##################################
     #send success to client
     portx = "1088"
     #context = zmq.Context()
     socketClient = context.socket(zmq.REQ)
     socketClient.connect ("tcp://localhost:%s" % portx)    
     #send success to client
     socketClient.send_string("Uploaded Successfully")
     

#############################################################
if __name__ == "__main__": 
    #connecting to clients
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

    # creating thread 
    t1 = threading.Thread(target=Nodes) 
    t2 = threading.Thread(target=client) 
   
    # starting threads 
    t2.start() 
    t1.start() 
    