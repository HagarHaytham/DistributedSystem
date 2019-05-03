# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 15:22:33 2019

@author: hagar
"""
import zmq
import sys
import pymysql as PyMySQL

# Open database connection
db = PyMySQL.connect("localhost","testuser","123456","Usersdb" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

#### be a server when a client wants a task done 
#### if sign up make sure the username is new and not on the db
#### if login check for the paswword


port=int(sys.argv[1])
portPub = int(sys.argv[2])
firstPortSecondShard = int (sys.argv[3])
firstPortThirdShard = int (sys.argv[4])
mysub=[]
for i in range (3):
    mysub.append(firstPortSecondShard+i)
    mysub.append(firstPortThirdShard+i)

### server connection with client
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

### publisher connection with my subsribers
contextPub = zmq.Context()
socketPub = contextPub.socket(zmq.PUB)
#for i in range(len(mysub)):
socketPub.bind("tcp://*:%s" % portPub)

### subsriber connection with my subscribers(in this case they are the publishers)
contextSub = zmq.Context()
socketSub = contextSub.socket(zmq.SUB)
for i in range (len(mysub)): 
    socketSub.connect ("tcp://localhost:%s" % mysub[i])
    topicfilter = "Insert"
    socketSub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

while True:
    message = socket.recv()
    print ("Received request: ", message)    
    msg = str(message,'utf-8')
    query = msg.split()
    print(query)
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
               topic = "Insert"
               messagedata = "INSERT INTO USERS (UserName,UserPassword,Email) VALUES ( "+query[1]+" , "+query[2]+" , " +query[3] + " )"
               socket.send_string("%d %d" % (topic, messagedata))
            except:
               # Rollback in case there is any error
               db.rollback()
            messageToSend = "Signed in Sucessfully"
    else: #log in
        print("Log in")
        sql = "SELECT * FROM USERS where Username= %s and UserPassword = %s"
        cursor.execute(sql,(query[1],query[2],))
        result = cursor.fetchall()
        if len(result) ==0:
            messageToSend = "Username or password is incorrect, Please try again"
        else:
            messageToSend="Logged in Sucessfully"
        
    socket.send_string(messageToSend)



### subscribe to other machines to get new updates
    string = socketSub.recv()
    topic, messagedata = string.split()
    print (messagedata) ## sql query to be executed
    try:
           # Execute the SQL command
           cursor.execute(sql,(query[1],query[2],query[3],))
           # Commit your changes in the database
           db.commit()
    except:
           # Rollback in case there is any error
           db.rollback()


# disconnect from server
#db.close()