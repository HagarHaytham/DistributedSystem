# -*- coding: utf-8 -*-
"""
Created on Sat May  4 01:21:31 2019

@author: hagar
"""
import zmq
import pymysql as PyMySQL
import threading
from multiprocessing import Process, Lock
import sys

def ServerPub(dbLock,db,cursor,socketServer,socketPub):
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
        socketServer.send_string(messageToSend)


def Sub(dbLock,db,cursor,socketSub,serverPort):
    print('Subscriber thread began')
    while True:
        messagedata = socketSub.recv()
        print('Subscriber on .. inserting in db query at port of server', serverPort)
        try:
            dbLock.acquire()
            # Execute the SQL command
            cursor.execute(messagedata)
            # Commit your changes in the database
            db.commit()
            dbLock.release()
        
        except:
            print("Already inserted (may be) ..")
            

def Shard(dbLock,serverPort,PubPort,IP1,IP2,NProcesses,firstPortSecondShard,firstPortThirdShard):
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
    
    ### server connection with client
    contextServer = zmq.Context()
    socketServer = contextServer.socket(zmq.REP)
    socketServer.bind("tcp://*:%s" % serverPort)
    
    ### publisher connection with my subsribers
    contextPub = zmq.Context()
    socketPub = contextPub.socket(zmq.PUB)
    #for i in range(len(mysub)):
    socketPub.bind("tcp://*:%s" % PubPort)
    
    ### subsriber connection with my subscribers(in this case they are the publishers)
    contextSub = zmq.Context()
    socketSub = contextSub.socket(zmq.SUB)
    for i in range (NProcesses): 
        topicfilter = "INSERT"
        ### 3 subscribes for each machines as each machine has 3 processes running (3 publishers)
        socketSub.connect ("tcp://%s:%s" % (IP1, FirstMachineSub[i]))
        socketSub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
        
        socketSub.connect ("tcp://%s:%s" % (IP2, SecondMachineSub[i]))
        socketSub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

    server_pub = threading.Thread(target=ServerPub, args=(dbLock,db,cursor,socketServer,socketPub))
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
IP1='localhost'
IP2='localhost'

if __name__ == '__main__':
    dbLock = Lock()
    p=[]
    for i in range (3):
        ser=portServer+i
        pub=portPub+i
#        sec = firstPortSecondShard+i
#        thir = firstPortThirdShard+i
        p.append(Process(target=Shard,args=(dbLock,ser,pub,IP1,IP2,3,SecondShard,ThirdShard)))
        p[i].start()

        
        