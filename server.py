# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 13:29:00 2019

@author: Dalia
"""
import zmq
import time
import sys
import random


#LookUpTable

file ={}
file["name"]="c://name.txt"

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

Nports = [[["1100",'Y'],["2000",'N'],["3000",'N']],[["4000",'N'],["5000",'Y'],["600",'Y']],[["700",'Y'],["800",'Y'],["900",'Y']]]

#print(LookUpTable)



###################################################


port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

message = ""

while True:
    #  Wait for next request from client
    message = socket.recv_string()
    print ("Received request: ", message)
    
    print ("Finding available ports... ")
    
    msg = str(message)
    if msg.find("Upload") != -1:
        n= []
        
        for i in range(len(LookUpTable)):
            if LookUpTable[i][1] == 'Y':
                n.append(i)
        #print(n)
        
        #respond with a list of ports
        '''ports=[]
        for i in range(len(n)):
            for j in range(len(Nports)): #3
                if Nports[n[i]][j][1] == 'Y':
                    ports.append(Nports[n[i]][j][0])
                    
        res =""
        for i in ports:
            res += i
            res += " "
        '''
        #pick machine random and choose first port alive
        res = ""
        j=0
        k=random.choice(n)
        while (res=="" and j in range(len(Nports[k]))):
            if Nports[k][j][1] == 'Y':
                res = Nports[k][j][0]
            
            j+=1
            
        socket.send_string(res)
        print ("Sending Reply... ")
   











