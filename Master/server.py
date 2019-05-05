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

# file =[]
# file.append("name.mp4")

# user ={}
# user[100]=file
# user[200]=file
# user[300]=file

# alive='Y'
# Nalive='N'
# node = [user,alive]
# node1 = [user,alive]
# node2 = [user,alive]
# LookUpTable={}

# LookUpTable[0]=node
# LookUpTable[1]=node1
# LookUpTable[2]=node2


#{0: [{100: ['name.mp4'], 200: ['name.mp4'], 300: ['name.mp4']}, 'Y'],
# 1: [{100: ['name.mp4'], 200: ['name.mp4'], 300: ['name.mp4']}, 'Y'], 
# 2: [{100: ['name.mp4'], 200: ['name.mp4'], 300: ['name.mp4']}, 'Y']}

#array nodes and processes
#Nports = [[["1100",'Y','A'],["2000",'N','A'],["3000",'N','A']],[["4000",'N','A'],["5000",'Y'],["600",'Y','A']],[["700",'Y','A'],["800",'Y','A'],["900",'Y','A']]]

#print(LookUpTable)

# dataNodes = []
# for i in range(9):
#     dataNodes.append([sys.argv[i+2], str(int(sys.argv[i+2])+50), str(int(sys.argv[i+2])+100), 'A', 'A'])
# 
# print(dataNodes)


def initConnDB(context, dbPort):
    socketDB = context.socket(zmq.REP)
    socketDB.bind("tcp://*:%s" %dbPort)
    return socketDB


def initClient(context,newPort):
    clientSocket = context.socket(zmq.REP)
    clientSocket.bind("tcp://*:%s" %newPort)
    return clientSocket


#connect to default port of server from db, connect to this port w send username
def handleClient(context, LookUpTable, newPort, username):
    print("enter handle")
    socketClient = initClient(context,newPort)
    
    while 1:
        
        choice = socketClient.recv_string()

        if(choice == '1'):
            upld(context, LookUpTable, socketClient, username)
        
        elif(choice == '2'):
            show(context,socketClient, username)
            
        elif(choice == '3'):
            dwnld(context, LookUpTable, socketClient, username)
        
        return


def upld(context, LookUpTable, socketClient, username):
    #pick machine random and choose random port alive
    #random pickNode
    print ("Finding available ports... ")

    loc = 0
    for i in range(len(LookUpTable)):
        if LookUpTable[i][3] == 'A':
            if LookUpTable[i][4] == 'A':
                loc = i
                LookUpTable[i][4] = 'B'
                print(LookUpTable[loc][1])
                break
    
    #send port to client
    socketClient.send_string(LookUpTable[loc][1])
    #time.sleep(1)
    print ("Reply is sent... ")
    success(context,LookUpTable, loc, socketClient,username)


def success(context, LookUpTable, loc, socketClient, username):
    
    dataNodeSocket = context.socket(zmq.REP)
    dataNodeSocket.bind ("tcp://*:%s" % LookUpTable[loc][0])
    
    succ, filename = (dataNodeSocket.recv_string()).split()
    print(succ)
    dummy = socketClient.recv_string()
    socketClient.send_string("success")
    LookUpTable[loc][4] = 'A'
    #if(succ == 'Success'):
        #TODO call lookup table to add file
        #updateLookup(LookUpTable, filename, username)
    return


def show(context,socketClient, username):
    return


def dwnld(socketClient, username):
    return


def runReplicate(context, rPorts, files):
    while True:
        replicate(context, rPorts, files)
        time.sleep(100000)
    return


def replicate(context, rPorts, files):

    #read from input
    rPorts = [[["6000",'A'],["6100",'A'],["6200",'A']],[["7000",'A'],["7100",'A'],["7200",'A']],[["8000",'A'],["8100",'A'],["8200",'A']]]
    files = ["name.mp4","name2.mp4","name3.mp4","name4.mp4","name5.mp4","name6.mp4"]

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
            #context = zmq.Context()
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
                recSocket1.close()

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
                recSocket2.close()
                
            senderSocket.send_string("master: Done Notifying... ")
            
            senderSocket.recv_string()
            
            rPorts[srcNode][srcPort][1] = 'A'
            rPorts[dstNode1][dstPort1][1] = 'A'
            rPorts[dstNode2][dstPort2][1] = 'A'

            senderSocket.close()
                
                
    print(LookUpTable)
    print(rPorts)            
                

#############################################################
def main(LookUpTable, Nports, dbPort): 

	# print(LookUpTable, Nports)
	context = zmq.Context()
	socketDB = initConnDB(context, dbPort)

	# for i in range(len(Nports)):

	#use example
	temp = temp = Nports[0]
	if(dbPort == "3000"):
		temp[0][0] = "blaaaah"
		
	elif(dbPort == "3001"):
		temp[0][1] = 'a'
		
	else:
		temp[0][2] = 'qrrrr'
		
	Nports[0] = temp

	print('/n/n')
	print(Nports[0], Nports[1], Nports[2])
	print('/n/n')

#    NodeThread = threading.Thread(target=Nodes,args=(context)) 
#    NodeThread.start()
	
	clientThreads = []
	replicationPorts = []
	allFiles = []

    # replicationThread = threading.Thread(target = runReplicate, args = (context, replicationPorts, allFiles))

	while True:
        
		newPort, clientUsername = (socketDB.recv_string()).split()
		print(newPort, clientUsername)
		socketDB.send_string("recived port Successfully")

		clientThreads.append(threading.Thread(target = handleClient,args=(context, LookUpTable, newPort, clientUsername)))
		clientThreads[-1].start()

	return



