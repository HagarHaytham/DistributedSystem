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

dataNodes = []
for i in range(9):
    dataNodes.append([sys.argv[i+2], str(int(sys.argv[i+2])+50), str(int(sys.argv[i+2])+100), 'A', 'A'])

print(dataNodes)


def initConnDB(context):
    socketDB = context.socket(zmq.REP)
    socketDB.bind("tcp://*:%s" %sys.argv[1])
    return socketDB


def initClient(context,newPort):
    clientSocket = context.socket(zmq.REP)
    clientSocket.bind("tcp://*:%s" %newPort)
    return clientSocket

# def initSockets(port):
#     defSocket = context.socket(zmq.REP)
#     defSocket.bind ("tcp://*:%s" % port)
#     return defSocket


#connect to default port of server from db, connect to this port w send username
def handleClient(context,newPort, username):
    print("enter handle")
    socketClient = initClient(context,newPort)
    
    while 1:
        
        choice = socketClient.recv_string()

        if(choice == '1'):
            upld(context,socketClient, username)
        
        elif(choice == '2'):
            show(context,socketClient, username)
            
        elif(choice == '3'):
            dwnld()
        
        return


def upld(context,socketClient, username):
    #pick machine random and choose random port alive
    #random pickNode
    print ("Finding available ports... ")

    loc = 0
    for i in range(len(dataNodes)):
        if dataNodes[i][3] == 'A':
            if dataNodes[i][4] == 'A':
                loc = i
                dataNodes[i][4] = 'B'
                break

    
    #send port to client
    socketClient.send_string(dataNodes[loc][1])
    #time.sleep(1)
    print ("Reply is sent... ")
    success(context,dataNodes[loc][0], socketClient,username)

def success(context, dataNodePort,socketClient, username):
    
    dataNodeSocket = context.socket(zmq.REP)
    dataNodeSocket.bind ("tcp://*:%s" % dataNodePort)
    
    succ, filename = (dataNodeSocket.recv_string()).split()
    print(succ)
    dummy = socketClient.recv_string()
    socketClient.send_string("success")
    #if(succ == 'Success'):
        #TODO call lookup table to add file
        #updateLookup(dataNodePort, filename, username)
    return

def show(context,socketClient, username):
    return

def dwnld(socketClient, username):
    return


    #print(socketNode1.recv_string())
    ##################################
    #load()

    #send success to client
    # portx = "1088"
    # #context = zmq.Context()
    # socketClient = context.socket(zmq.REQ)
    # socketClient.connect ("tcp://localhost:%s" % portx)    
    # #send success to client
    # socketClient.send_string("Uploaded Successfully")



#############################################################
#def Nodes(context):
#    #connecting to Nodes
#    port1 = sys.argv[6]
#    socketNode = context.socket(zmq.SUB)
#    print("conecting to nodes...")
#    socketNode.connect ("tcp://localhost:%s" % port1)
#    while 1:
#     #connecting to Nodes
#        socketNode.setsockopt_string(zmq.SUBSCRIBE, "ALIVE")
#        string = socketNode.recv_string()
#        #print("recieved ",string )
#        time.sleep(1)
#        topic, IP = string.split()
#        print (topic, IP)

#############################################################
def main(): 

    context = zmq.Context()
    socketDB = initConnDB(context)

#    NodeThread = threading.Thread(target=Nodes,args=(context)) 
#    NodeThread.start()

    clientThreads = []

    #mainThread = threading.Thread(target = getClient(socketDB))

    while True:
        
        newPort, clientUsername = (socketDB.recv_string()).split()
        print(newPort, clientUsername)
        socketDB.send_string("recived port Successfully")

        clientThreads.append(threading.Thread(target = handleClient,args=(context,newPort, clientUsername)))
        clientThreads[-1].start()

    return

main()
     # creating thread 
    # defThread = threading.Thread(target=recvUserName,args=(defSocket,choiceSocket,uplSocket,showSocket,dwnldSocket))
    # defThread.start()
    
    #port = "5556"
    
    
#    socket = context.socket(zmq.REP)
#    socket.bind("tcp://*:%s" % port)
#    print("connecting to client...")
    
    ##############################################################
    
    ##############################################################
    #connect client userID
#    socketID = context.socket(zmq.REP)
#    varport = "2001"
#    socketID.bind("tcp://*:%s" % varport)
    ##############################################################
   
   
    # starting threads 
    
#############################################################
# def client():
#     #  Wait for next request from client
    
#      #send choice to node
# #    choicePort = "1066"
# #    choiceNode = context.socket(zmq.REP)
# #    choiceNode.bind("tcp://*:%s" % choicePort)
#     ##################################
     
# #    UserID = socketID.recv_string()
# #    print(UserID)
#     #socketID.send_string("recieved userId = %s" %UserID)
#     ##################################
#     while(1):
        
#         message = ""
#         message = socket.recv_string()
#         print ("Received request: ", message)
#         time.sleep(1)
#         msg = str(message)
       
#         if(msg == "1"):
# #            #pick machine random and choose random port alive
# #            #random pickNode
# #            print ("Finding available ports... ")
# #            n= []
# #            for i in range(len(LookUpTable)):
# #                if LookUpTable[i][1] == 'Y':
# #                    n.append(i)
# #            
# #            k=random.choice(n)
# #            
# #            res = ""
# #            j=0
# #            while (res=="" and j in range(len(Nports[k]))):
# #                if Nports[k][j][1] == 'Y':
# #                    res = Nports[k][j][0]
# #                j+=1
# #            #set busy
# #            #Nports[k][j-1][2]= 'B'
# #            
# #            #send port to client
# #            socket.send_string(res)
# #            #time.sleep(1)
# #            print ("Reply is sent... ")
# #            
# #            ##########################
# #            #send choice to node
# #            print(choiceNode.recv_string())
# #            choiceNode.send_string(msg)
# #            #########################
# #            #recived and send success  
# #            success()
# #        
#         elif(msg == "2"):
            
#             ##########################
#             #send choice to node
#             print(choiceNode.recv_string())
#             choiceNode.send_string(msg)
#             #########################
#             #################################################
#             #get files for user
#             UserId = 100
#             arr = ""
#             for i in range(len(LookUpTable)):
#                 if(LookUpTable[i][0][UserId]):
#                     userFiles = LookUpTable[i][0][UserId] 
#                     for j in range(len(userFiles)):
#                         arr += userFiles[j]
#                         arr += '\n'
               
#             print(arr)
#             socket.send_string(arr)
        
#             #send success to client
#             #portx = "1088"
#             #context = zmq.Context()
#             #socketClient = context.socket(zmq.REQ)
#             #socketClient.connect ("tcp://localhost:%s" % portx)    
#             #socketClient.send_string("show done Successfully")
        
# #############################################################


    