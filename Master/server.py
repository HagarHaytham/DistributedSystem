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
from multiprocessing import Process

def initConnDB(context, dbPort):
    socketDB = context.socket(zmq.REP)
    socketDB.bind("tcp://*:%s" %dbPort)
    return socketDB

###############################################################################
def initClient(context,newPort):
    clientSocket = context.socket(zmq.REP)
    clientSocket.bind("tcp://*:%s" %newPort)
    return clientSocket

###############################################################################
#connect to default port of server from db, connect to this port w send username
def handleClient(context, Nports, newPort, username):
    print("enter handle")
    socketClient = initClient(context,newPort)
    
    while 1:
        
        choice = socketClient.recv_string()

        if(choice == '1'):
            upld(context, Nports, socketClient, username)
        
        elif(choice == '2'):
            show(context,LookUpTable,socketClient, username)
            
        elif(choice == '3'):
            dwnld(Nports, socketClient, username)
        
        return

def upld(context, Nports, socketClient, username):
    #pick machine random and choose random port alive
    #random pickNode
    print ("Finding available ports... ")

    loc = 0
    for i in range(len(LookUpTable)):
        if Nports[i][6] == 'A':
            if Nports[i][7] == 'A':
                loc = i
                Nports[i][7] = 'B'
                print(Nports[loc][1])
                break
                
    socketClient.send_string(Nports[loc][1])
    
    #time.sleep(1)
    print ("Reply is sent... ")
    success(context,Nports, loc, socketClient,username)

###############################################################################

def success(context, Nports, loc, socketClient, username):
    
    dataNodeSocket = context.socket(zmq.REP)
    dataNodeSocket.bind ("tcp://*:%s" % Nports[loc][2])
    
    succ, filename = (dataNodeSocket.recv_string()).split()
    print(succ)
    dummy = socketClient.recv_string()

    socketClient.send_string("success")
    Nports[loc][7] = 'A'
    
    #if(succ == 'Success'):
        #TODO call lookup table to add file
        #updateUserLookup(LookUpTable, filename, username,loc)
    return

###############################################################################
def updateUserLookup(LookUpTable, filename, username,loc):
    
    if(username in LookUpTable[loc][0]): #if user already exists
        temp = LookUpTable[i][0][username]
    else: #if new user
        temp = []
        
    temp.append(filename)
    LookUpTable[i][0][username] = temp
    return 
    
###############################################################################
def Nodes(context,Nports,LookUpTable): #sending alive to server
    #connecting to Nodes
    socketNode = context.socket(zmq.SUB)
    print("conecting to nodes...")
    socketNode.connect ("tcp://localhost:%s" % port1)
    while 1:
     #connecting to Nodes
        socketNode.setsockopt_string(zmq.SUBSCRIBE, "ALIVE")
        #NEED timeout
        string = socketNode.recv_string()
        #
        #print("recieved ",string )
        time.sleep(1)
        topic, IP = string.split()
        print (topic, IP)
    
###############################################################################
def updateAliveLookup(LookUpTable, live, username,loc):
    return
    
###############################################################################
def show(context,LookUpTable,socketClient, username):
    arr = ""
    for i in range(len(LookUpTable)):
        if(username in LookUpTable[i][0]):
            userFiles = LookUpTable[i][0][username] 
            for j in range(len(userFiles)):
                arr += userFiles[j]
                arr += '\n'
       
    print(arr)
    if(arr == ""):
        arr = "You don't have any files, choose upload to add files"
        
    socketClient.send_string(arr)
        
    return

###############################################################################
def runReplicate(context, rPorts, files,LookUpTable):
    while True:
        replicate(context, rPorts, files,LookUpTable)
        time.sleep(100000)
    return

###############################################################################
def dwnld(socketClient, username, filename):

    while True:
        message = socketClient.recv_string()
        print ("Received request: ", message)
        time.sleep (1)
        state = "Found"     #retrieve from lookup table
        fileSize = "3000"   #retrieve from lookup table

        #retrieve list of ips and ports from lookup table
        ips, ports = getDwnldList(fileName)
        
        socketClient.send_string(state + " " + fileSize + " "+ ips + " " + ports)

def getDwnldList(fileName):
    return "localhost localhost ", "6666 8888"

# def runReplicate(context, rPorts, files):
#     while True:
#         replicate(context, rPorts, files)
#         time.sleep(100000)
#     return
                

###############################################################################
def main(LookUpTable, Nports, dbPort): 

    clientThreads = []
    context = zmq.Context()
    socketDB = initConnDB(context, dbPort)
    NodeThread = []

    # for i in range(3):
    #     NodeThread.append(threading.Thread(target=Nodes,args=(context,Nports[:][:][0:1],LookUpTable))) #alivePort
    #     NodeThread[i].start()

    # replicationThread = threading.Thread(target = runReplicate, args = (context, replicationPorts, allFiles, LookUpTable))

    while True:
        newPort, clientUsername = (socketDB.recv_string()).split()
        print(newPort, clientUsername)
        socketDB.send_string("recived port Successfully")

        clientThreads.append(threading.Thread(target = handleClient,args=(context, LookUpTable, newPort, clientUsername)))
        clientThreads[-1].start()

    return

    

	# for i in range(len(Nports)):

	#use example of lookup table
	# temp = temp = Nports[0]
	# if(dbPort == "3000"):
	# 	temp[0][0] = "blaaaah"
		
	# elif(dbPort == "3001"):
	# 	temp[0][1] = 'a'
		
	# else:
	# 	temp[0][2] = 'qrrrr'
		
	# Nports[0] = temp

	# print('/n/n')
	# print(Nports[0], Nports[1], Nports[2])
	# print('/n/n')


    


