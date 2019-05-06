# -*- coding: utf-8 -*-
"""
Created on Fri May  3 16:51:35 2019

@author: Mary
"""


import zmq
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
#print(LookUpTable)
#Nports = [[["1500",'Y','A'],["2000",'N','A'],["3000",'Y','A']],[["4000",'Y','A'],["5000",'Y','A'],["6000",'Y','A']],[["7000",'Y','A'],["9100",'Y','A'],["9000",'Y','A']]]
rPorts = [["localhost","6000",'A'],["localhost","6100",'A'],["localhost","6200",'A']]
sPorts = [["localhost","7000",'A'],["localhost","7100",'A'],["localhost","7200",'A']]
#ports that will recieve copies


#port that will send copies


# detecting if a file has less than 3 replicates

def main(LookUpTable,files,rPorts):
    while(1):
        for i in range(len(files)):
            srcIP = ""
            srcport = ""
            serPort1 = ""
            serPort2 = ""
            dstIP1 = ""
            dstport1 = ""
            dstIP2 = ""
            dstport2 = ""
            fCount = 0
            nodes = []
            nodesToHave = []
            fUser = 0
            for node in LookUpTable:
                for user in LookUpTable[node][0]:
                    for q in range(len(LookUpTable[node][0][user])):
                        if(LookUpTable[node][0][user][q] == files[i]):
                            fCount += 1
                            nodes.append(node)
                            nodesToHave.append(node)
                            fUser = user
            print("nodes that have "+files[i] +": "+str(nodes))
            
            
            # getting nodes to be copied to 
            
            if(fCount < 3):
                # the following variables used to update availablity
                srcNode = 0
                dstNode1 = 0
                dstNode2 = 0
                for node in LookUpTable:
                    if (node not in nodesToHave ):
                        
                        while (dstport1 == "" ):
                            if(LookUpTable[node][1] == 'Y' and rPorts[node][2] == 'A' ):
                                dstIP1 = rPorts[node][0]
                                dstport1 = rPorts[node][1]
                                rPorts[node][2] == 'B'
                                serPort1 = sPorts[node][1]
                                #updating in lookup table
                                if (fUser not in LookUpTable[node][0] ):
                                    LookUpTable[node][0][fUser] = [files[i]]
                                else:
                                    LookUpTable[node][0][fUser].append(files[i])
                                    
                                dstNode1 = node
                                nodesToHave.append(node)

                    if(fCount < 2):
                        if(node not in nodesToHave):  
                            while (dstport2=="" ):
                                if(LookUpTable[node ][1] == 'Y' and rPorts[node ][2] == 'A' ):
                                    dstIP2 = rPorts[node][0]
                                    dstport2 = rPorts[node][1]
                                    rPorts[node][2] == 'B'
                                    serPort2 = sPorts[node][1]

                                    #updating in lookup table
                                    if (fUser not in LookUpTable[node][0] ):
                                        LookUpTable[node][0][fUser] = [files[i]]
                                    else:
                                        LookUpTable[node][0][fUser].append(files[i])       
                                    
                                    dstNode2 = node
                                                           
                                    
                                    break
                                

                # getting the node that will send copy
                
                for k in range(len(nodes)):    
                    
                    while (srcport == "" ):
                        if (LookUpTable[nodes[k]][1] == 'Y' and rPorts[nodes[k]][2] == 'A'):
                            srcIP = rPorts[nodes[k]][0]
                            srcport = sPorts[nodes[k]][1]
                            rPorts[nodes[k]][2] == 'B'
                            
                            srcNode = nodes[k]
                           
                            break
                        
                        
                   
                # notifying sender 
                context = zmq.Context()
                senderSocket = context.socket(zmq.REQ)
                senderSocket.connect ("tcp://%s:%s" % (srcIP,srcport))
                
                print("Notifying Sender...")
                senderSocket.send_string("s")
                print(senderSocket.recv_string())
                
                senderSocket.send_string(dstIP1)
                print(senderSocket.recv_string())
                senderSocket.send_string(dstport1)
                print(senderSocket.recv_string())
        
                senderSocket.send_string(dstIP2)
                print(senderSocket.recv_string())
                senderSocket.send_string(dstport2)
                print(senderSocket.recv_string())
        
                senderSocket.send_string(files[i])
                print(senderSocket.recv_string())
        
                if(dstport1 != ""):
                    print("Notifying reciever1...")
                    recSocket1 = context.socket(zmq.REQ)
                    recSocket1.connect ("tcp://%s:%s" % (dstIP1,serPort1))
                    recSocket1.send_string("r")
                    print(recSocket1.recv_string())
            
                    recSocket1.send_string(files[i])
                    recSocket1.close()
                else:
                    print ("can't repicate, there is no alive nodes")
                    continue
                    
                if(dstport2 != ""):
                    print("Notifying reciever2...")
                    recSocket2 = context.socket(zmq.REQ)
                    recSocket2.connect ("tcp://%s:%s" % (dstIP2,serPort2))
                    recSocket2.send_string("r")   
                    print(recSocket2.recv_string())
            
                    recSocket2.send_string(files[i])
                    recSocket2.close()
                    
                senderSocket.send_string("master: Done Notifying... ")
                
                print(senderSocket.recv_string())
                senderSocket.close()
                rPorts[srcNode][2] = 'A'
                rPorts[dstNode1][2] = 'A'
                rPorts[dstNode2][2] = 'A'
                
        time.sleep(10)    
main(LookUpTable,files,rPorts)    
#print(LookUpTable)
#print(rPorts)            
            
    




























