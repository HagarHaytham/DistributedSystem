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
    #i=0
    while 1:
     #connecting to Nodes
        socket1.setsockopt_string(zmq.SUBSCRIBE, "ALIVE")
        string = socket1.recv_string()
        #print("recieved ",string )
        time.sleep(1)
        topic, IP = string.split()
        print (topic, IP)
        #i+=1
   
    


    
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
        
        
def success():        
    
     #recived success from node 
    print(socket1.recv_string())
    time.sleep(1)
    fileName= socket1.recv_string()
    print ("Recieved file name is ",fileName)
    
    LookUpTable[k][0][100].append(fileName)
    print(LookUpTable[k][0][100])
    
    #send success to client
    socket.send_string("success uploading")
    
   


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
    socket1 = context.socket(zmq.SUB)
        
    print("conecting to nodes...")
    socket1.connect ("tcp://localhost:%s" % port1)
    
    
    # creating thread 
    t1 = threading.Thread(target=Nodes) 
    t2 = threading.Thread(target=client) 
    t3 = threading.Thread(target=success)
    
    #while True:
        # starting thread 1 
    t2.start() 
    # starting thread 2 
    t1.start() 
    
    
    
    
    #Nodes()
    # wait until thread 1 is completely executed 
    #t2.join()
    t3.start()
        #t1.join()
    #success()
     # both threads completely executed 
    print("Done!")

#if len(sys.argv) > 2:
 #   socket1.connect ("tcp://localhost:%s" % port1)

#socket1.setsockopt_string(zmq.SUBSCRIBE, "ALIVE")
    
##############################################################    


    
     #################################################
#    #connecting to Nodes
#    string = socket1.recv()
#    topic, IP = string.split()
#    #total_value += int(messagedata)
#    print (topic, IP)
    
    #################################################
    
#    #  Wait for next request from client
#    message = socket.recv_string()
#    print ("Received request: ", message)
#    time.sleep(1)
#    print ("Finding available ports... ")
#    
#    msg = str(message)
#    
#    if(msg == "1"):
#        n= []
#        
#        for i in range(len(LookUpTable)):
#            if LookUpTable[i][1] == 'Y':
#                n.append(i)
#        
#        #pick machine random and choose first port alive
#        res = ""
#        j=0
#        k=random.choice(n)
#        while (res=="" and j in range(len(Nports[k]))):
#            if Nports[k][j][1] == 'Y':
#                res = Nports[k][j][0]
#            
#            j+=1
#        #set busy
#        Nports[k][j-1][2]= 'B'
#        
#        socket.send_string(res)
#        time.sleep(1)
#        print ("Reply is sent... ")
#   

#########################################################
#        #recived success from node 
#        success= socket1.recv_string()
#        fileName= socket1.recv_string()
#        print ("Recieved file name is ",fileName)
#        
#        LookUpTable[k][0][100].append(fileName)
#        print(LookUpTable[k][0][100])
#    
#        #send success to client
#        socket.send_string("success uploading")
#        
    
    
       



