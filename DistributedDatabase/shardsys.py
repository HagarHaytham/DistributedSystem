# -*- coding: utf-8 -*-
"""
Created on Sat May  4 01:21:31 2019

@author: hagar
"""
import zmq
import pymysql as PyMySQL
import threading
from multiprocessing import Process, Lock, Value
import sys

def SendMasterNewPort(socketClient,PortClientAssigned,portClientLock,username):
    portClientLock.acquire()
    PortClientAssigned +=1
    portassigned =PortClientAssigned
    portClientLock.release()
    
    msgToSend = portassigned+" "+username ## send to master the client username and the port to talk to
    socketClient.send_message(msgToSend)
    socketClient.recv(flags=zmq.NOBLOCK)
    return portassigned
 

def ServerPub(dbLock,db,cursor,socketServer,socketPub,socketClient,PortClientAssigned,portClientLock):
    # this function is responsible for executing client command
    # and if sign up (new insetion) publish to other shards immediatly
    print('ServerPub thread began')
    while True:
        message = socketServer.recv()
        print ("Received request: ", message)    
        msg = str(message,'utf-8')
        query = msg.split()
        print(query)
        dbLock.acquire()
        print("Lock aquired server")
        if (query[0] =='1'): # Sign Up
            sqlcheck = "SELECT * FROM USERS where Username= %s"
            cursor.execute(sqlcheck,(query[1],))
            result = cursor.fetchall()
            print(result)
            if len(result)>0:
                messageToSend = "Can't sign Up with this Username , please choose another One"
            else:            
                sql ="INSERT INTO USERS (UserName,UserPassword,Email) VALUES ( %s , %s ,%s )"
                try:
                   # Execute the SQL command
                    cursor.execute(sql,(query[1],query[2],query[3],))
                    # Commit your changes in the database
                    db.commit()
                    ### then publish that if it is an insertion
                    #topic = "Insert"
                    messagedata = "INSERT INTO USERS (UserName,UserPassword,Email) VALUES ( '"+query[1]+"' , '"+query[2]+"' , '" +query[3] + "' )"
                    socketPub.send_string("%s" % (messagedata))
                    messageToSend = "Signed in Sucessfully"
                except:
                   messageToSend = "Couldn't connect .. try again later"
                   
        else: #log in
            print("Log in")
            try:
                sql = "SELECT * FROM USERS where Username= %s and UserPassword = %s"
                cursor.execute(sql,(query[1],query[2],))
                result = cursor.fetchall()
                if len(result) ==0:
                    messageToSend = "Username or password is incorrect, Please try again"
                else:
                    messageToSend="Logged in Sucessfully"
            except:
                messageToSend = "Couldn't connect .. try again later"
        dbLock.release()
        print("Lock released server")
        
        
        if messageToSend =="Logged in Sucessfully" or messageToSend== "Signed in Sucessfully":
            # add port assigned to client to the message sent to client
            messageToSend += SendMasterNewPort(socketClient,PortClientAssigned,portClientLock,query[0]) ## username
            
        socketServer.send_string(messageToSend)
        print("Message sent")

def Sub(dbLock,db,cursor,socketSub,serverPort):
    print('Subscriber thread began')
    while True:
        messagedata = socketSub.recv()
        print('Subscriber on .. inserting in db query at port of server', serverPort)
        try:
            dbLock.acquire()
            print("Lock aquired subscriber")
            # Execute the SQL command
            cursor.execute(messagedata)
            # Commit your changes in the database
            db.commit()
            dbLock.release()
            print("Lock released subscriber")
        
        except:
            dbLock.release()
            print("Lock released subscriber")
            print("Already inserted (may be) ..")
            

def Shard(dbLock,serverPort,PubPort,IP1,IP2,NProcesses,firstPortSecondShard,firstPortThirdShard,IPMaster,portMaster,PortClientAssigned,portClientLock):
# Open database connection
    print('A shard process has began')
    db = PyMySQL.connect("localhost","testuser","123456","Usersdb" )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    FirstMachineSub=[]
    SecondMachineSub=[]
    for i in range (NProcesses):
        FirstMachineSub.append(firstPortSecondShard+i)
        SecondMachineSub.append(firstPortThirdShard+i)
    
    ###my  server connection with client
    contextServer = zmq.Context()
    socketServer = contextServer.socket(zmq.REP)
    socketServer.bind("tcp://*:%s" % serverPort)
    
    ###my publisher connection with my subsribers
    contextPub = zmq.Context()
    socketPub = contextPub.socket(zmq.PUB)
    #for i in range(len(mysub)):
    socketPub.bind("tcp://*:%s" % PubPort)
    
    ###my subsriber connection with my subscribers(in this case they are the publishers)
    contextSub = zmq.Context()
    socketSub = contextSub.socket(zmq.SUB)
    for i in range (NProcesses): 
        topicfilter = "INSERT"
        ### 3 subscribes for each machines as each machine has 3 processes running (3 publishers)
        socketSub.connect ("tcp://%s:%s" % (IP1, FirstMachineSub[i]))
        socketSub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
        
        socketSub.connect ("tcp://%s:%s" % (IP2, SecondMachineSub[i]))
        socketSub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

    ## my client connection with the Master to send port assigned to the new client
    contextClient = zmq.Context()
    socketClient = contextClient.socket(zmq.REQ)
    socketClient.connect("tcp://%s:%s" % (IPMaster,portMaster))
    
    server_pub = threading.Thread(target=ServerPub, args=(dbLock,db,cursor,socketServer,socketPub,socketClient,PortClientAssigned,portClientLock))
    sub = threading.Thread(target=Sub, args=(dbLock,db,cursor,socketSub,serverPort))
    
    server_pub.start()
    sub.start()
    
    server_pub.join()
    sub.join()
    
portServer=int(sys.argv[1])
portPub = int(sys.argv[2])
### ports should be the same , instead i should takes IPs of the other 2 machines
SecondShard = int (sys.argv[3])
ThirdShard = int (sys.argv[4])
#IP1='10.5.50.33'
IPShard2='localhost'
IPShard3='localhost'

IPMaster='localhost'
portMaster=int (sys.argv[5])

if __name__ == '__main__':
    dbLock = Lock()
    p=[]
    PortClientAssigned = Value('h',portMaster+1) # if master connection is 3000 , begin to assign ports to client from 3001
    portClientLock = Lock()
    for i in range (3):
        ser=portServer+i
        pub=portPub+i
#        sec = firstPortSecondShard+i
#        thir = firstPortThirdShard+i
        p.append(Process(target=Shard,args=(dbLock,ser,pub,IPShard2,IPShard3,3,SecondShard,ThirdShard,IPMaster,portMaster,PortClientAssigned,portClientLock)))
        p[i].start()

        
        