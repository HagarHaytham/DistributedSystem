# -*- coding: utf-8 -*-
"""
Created on Fri May  3 16:51:35 2019

@author: Mary
"""


import zmq
import socket
import time
#updated when a file is uploaded
files = ["name.mp4","name2.mp4","name3.mp4","name4.mp4","name5.mp4","name6.mp4"]

file02 =[]
file02.append("name.mp4")
file02.append("name6.mp4")

file03 =[]
file03.append("name2.mp4")

file11 =[]
file11.append("name3.mp4")

file12 =[]
file12.append("name.mp4")

file13 =[]
file13.append("name4.mp4")
file13.append("name2.mp4")


file21 =[]
file21.append("name5.mp4")

file22 =[]
file22.append("name6.mp4")
file22.append("name.mp4")



user0 ={}
user0[2]=file02
user0[3]=file03

user1 ={}
user1[1]=file11
user1[2]=file12
user1[3]=file13

user2 ={}
user2[1]=file21
user2[2]=file22

alive='Y'
Nalive='N'
node0 = [user0,alive]
node1 = [user1,alive]
node2 = [user2,alive]

LookUpTable={}

LookUpTable[0]=node0
LookUpTable[1]=node1
LookUpTable[2]=node2
print(LookUpTable)
Nports = [[["1500",'Y','A'],["2000",'N','A'],["3000",'Y','A']],[["4000",'Y','A'],["5000",'Y','A'],["6000",'Y','A']],[["7000",'Y','A'],["9100",'Y','A'],["9000",'Y','A']]]
rPorts = [[["6000",'A'],["6100",'A'],["6200",'A']],[["7000",'A'],["7100",'A'],["7200",'A']],[["8000",'A'],["8100",'A'],["8200",'A']]]

#ports that will recieve copies
dstport1 = ""
dstport2 = ""

#port that will send copies
srcport = ""

# detecting if a file has less than 3 replicates
for i in range(len(files)):
    fCount = 0
    nodes = []
    fUser = 0
    for node in LookUpTable:
        for user in LookUpTable[node][0]:
            for q in range(len(LookUpTable[node][0][user])):
                if(LookUpTable[node][0][user][q] == files[i]):
                    fCount += 1
                    nodes.append(node)
                    fUser = user
    print("nodes that have "+files[i] +": "+str(nodes))
    
    # getting nodes to be copied to 
    
    if(fCount < 3):
        # the following variables used to update availablity
        srcNode = 0
        srcPort = 0
        dstNode1 = 0
        dstPort1 = 0
        dstNode2 = 0
        dstPort2 = 0
        for node in LookUpTable:
            if (node not in nodes ):
                j = 0
                while (dstport1=="" and j in range(len(Nports[node]))):
                    if(Nports[node][j][1] == 'Y' and rPorts[node][j][1] == 'A' ):
                        dstport1 = rPorts[node][j][0]
                        rPorts[node][j][1] == 'B'
                        #updating in lookup table
                        if (fUser not in LookUpTable[node][0] ):
                            LookUpTable[node][0][fUser] = {files[i]}
                        else:
                            LookUpTable[node][0][fUser].append(files[i])
                            
                        dstNode1 = node
                        dstPort1 = j
                        nodes.append(node)
                        
                    j += 1
                
                
                j = 0
            if(fCount < 2):
                if(node not in nodes):  
                    while (dstport2=="" and j in range(len(Nports[node]))):
                        if(Nports[node ][j][1] == 'Y' and rPorts[node ][j][1] == 'A' ):
                            dstport2 = rPorts[node ][j][0]
                            rPorts[node ][j][1] == 'B'
                            #updating in lookup table
                            if (fUser not in LookUpTable[node][0] ):
                                LookUpTable[node][0][fUser] = {files[i]}
                            else:
                                LookUpTable[node][0][fUser].append(files[i])       
                            
                            dstNode2 = node
                            dstPort2 = j                        
                            
                            break
                        j += 1
                        
                
            
        # getting the node that will send copy
        
        for k in range(len(nodes)):    
            j=0
            while (srcport=="" and j in range(len(Nports[nodes[k]]))):
                if (Nports[nodes[k]][j][1] == 'Y' and rPorts[nodes[k]][j][1] == 'A'):
                    srcport = rPorts[k][j][0]
                    rPorts[nodes[k]][j][1] == 'B'
                    
                    srcNode = nodes[k]
                    srcPort = j
                    break
                j+=1
                
                
        # notifying sender 
        context = zmq.Context()
        senderSocket = context.socket(zmq.REQ)
        senderSocket.connect ("tcp://localhost:%s" % srcport)
        
        print("Notifying Sender...")
        senderSocket.send_string("s")
        #time.sleep(5)
        print(senderSocket.recv_string())
        #senderSocket.connect ("tcp://localhost:%s" % srcPort)
        senderSocket.send_string(dstport1)
        print(senderSocket.recv_string())

        
        senderSocket.send_string(dstport2)
        print(senderSocket.recv_string())

        senderSocket.send_string(files[i])
        print(senderSocket.recv_string())

        if(dstport1 != ""):
            print("Notifying reciever1...")
            recSocket1 = context.socket(zmq.REQ)
            recSocket1.connect ("tcp://localhost:%s" % dstport1)
            recSocket1.send_string("r")
            print(recSocket1.recv_string())
    
            recSocket1.send_string(files[i])
        else:
            print ("can't repicate, there is no alive nodes")
            continue
            
        if(dstport2 != ""):
            print("Notifying reciever2...")
            recSocket2 = context.socket(zmq.REQ)
            recSocket2.connect ("tcp://localhost:%s" % dstport2)
            recSocket2.send_string("r")   
            print(recSocket2.recv_string())
    
            recSocket2.send_string(files[i])
            
        senderSocket.send_string("master: Done Notifying... ")
        
        senderSocket.recv_string()
        
        rPorts[srcNode][srcPort][1] = 'A'
        rPorts[dstNode1][dstPort1][1] = 'A'
        rPorts[dstNode2][dstPort2][1] = 'A'
        break
            
            
print(LookUpTable)
print(rPorts)            
            
    




























