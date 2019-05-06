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
def handleClient(context, LookUpTable, Nports, newPort, username, files):
    print("enter handle")
    socketClient = initClient(context,newPort)
    
    while 1:
        print('waiting client')        
        choice = socketClient.recv_string()
        socketClient.send_string('dummy')

        if(choice == '1'):
            upld(context, LookUpTable, Nports, socketClient, username, files)
 
        elif(choice == '2'):
            show(context,LookUpTable,socketClient, username)
            
        elif(choice == '3'):
            dwnld(LookUpTable, Nports, socketClient, username)
        
    return

def upld(context, LookUpTable, Nports, socketClient, username, files):
    #pick machine random and choose random port alive
    #random pickNode
    print ("Finding available ports... ")

    loc = 0
    for i in range(len(Nports)):
        if Nports[i%3][i][7] == 'A':
            if Nports[i%3][i][8] == 'A':
                loc = i
                state = 'B'
                Nports[i%3][i][8] = state
                print(Nports[i%3][i][8])
                print(Nports[i%3][loc][2])
                break
                
    socketClient.recv_string()
    socketClient.send_string(Nports[loc%3][loc][2])
    
    #time.sleep(1)
    print ("Reply is sent... ")
    success(context, LookUpTable, Nports, loc, socketClient,username, files)
    return

###############################################################################

def success(context, LookUpTable, Nports, loc, socketClient, username, files):
    
    dataNodeSocket = context.socket(zmq.REP)
    dataNodeSocket.bind ("tcp://*:%s" % Nports[loc%3][loc][3])
    
    succ, filename = (dataNodeSocket.recv_string()).split()
    dataNodeSocket.send_string("dummy")

    print(succ, filename)
    dummy = socketClient.recv_string()

    socketClient.send_string("success")
    state = 'A'
    Nports[loc%3][loc][8] = state
    print("Nports", Nports[loc%3][loc][8])
    
    if(succ == 'Success'):
        #TODO call lookup table to add file
        print('send successfully')
        updateUserLookup(LookUpTable, filename, username,loc,files)
    return

###############################################################################
def updateUserLookup(LookUpTable, filename, username,i,files):
    temp = dict()
    if(username not in LookUpTable[str(i)][0]): #if user already exists
        temp= {str(i) :[{'':[]}, '']}
        
    else: #if new user
        temp = LookUpTable[str(i)]
    
    newFile = [username,filename]
    files.append(newFile) #dumy array for replicate

    temp[0][username].append(filename)
    
    print(temp,i)
    LookUpTable[str(i)] = temp
    print(LookUpTable)
    return 
    
###############################################################################
def Nodes(context, aliveP, Nports, NportsIp, LookUpTable): #sending alive to server
    #connecting to Nodes
    socketNode = context.socket(zmq.SUB)
    print("conecting to nodes...")
    #socketNode.RCVTIMEO = 500
    socketNode.connect ("tcp://localhost:%s" % aliveP)
    
    while 1:
     #connecting to Nodes
        for i in range(len(NportsIp)):
            print("enter nodes")
            socketNode.setsockopt_string(zmq.SUBSCRIBE, str(NportsIp[i][0]) + ':' + str(NportsIp[i][1]))
            string= "N"
            string = socketNode.recv_string()
            print(string)
            Nports[i][7] = string
            LookUpTable[i][1] = string
            print()
    time.sleep(1)

###############################################################################
def show(context,LookUpTable,socketClient, username):
    arr = ""
    for i in range(len(LookUpTable)):
        if(username not in LookUpTable[str(i)][0]):
            pass
        else:
            userFiles = LookUpTable[str(i)][0][username] 
            for j in range(len(userFiles)):
                arr += userFiles[j]
                arr += '\n'
       
    print(arr)
    if(arr == ""):
        arr = "You don't have any files, choose upload to add files"
        
    socketClient.recv_string()
    socketClient.send_string(arr)
    
    return

###############################################################################
def dwnld(LookUpTable, Nports, socketClient, username):

    #TODO add receive file name
    
    fileName = None
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
def main(LookUpTable, Nports, files, dbPort): 

    clientThreads = []
    context = zmq.Context()
    socketDB = initConnDB(context, dbPort)
    #NodeThread = []

    #for i in range(3):
    # NodeThread= threading.Thread(target=Nodes,args=(context, Nports[0][0][1], Nports, Nports[:][:][0:1],LookUpTable)) #alivePort
    # NodeThread.start()

    # replicationThread = threading.Thread(target = runReplicate, args = (context, replicationPorts, allFiles, LookUpTable))

    while True:
        newPort, clientUsername = (socketDB.recv_string()).split()
        print(newPort, clientUsername)
        socketDB.send_string("recived port Successfully")

        clientThreads.append(threading.Thread(target = handleClient,args=(context, LookUpTable, Nports, newPort, clientUsername, files)))
        clientThreads[-1].start()

    return

# for i in range(len(Nports)):

    #use example of lookup table
    # temp = temp = Nports[0]
    # if(dbPort == "3000"):
    #   temp[0][0] = "blaaaah"
        
    # elif(dbPort == "3001"):
    #   temp[0][1] = 'a'
        
    # else:
    #   temp[0][2] = 'qrrrr'
        
    # Nports[0] = temp

    # print('/n/n')
    # print(Nports[0], Nports[1], Nports[2])
    # print('/n/n')

