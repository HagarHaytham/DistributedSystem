# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 15:22:33 2019

@author: hagar
"""
import zmq
import sys
import pymysql as PyMySQL
import threading

# Open database connection
db = PyMySQL.connect("localhost","testuser","123456","Usersdb" )

# prepare a cursor object using cursor() method
cursor = db.cursor()


#------------------ initial configuration -----------------------#
port=int(sys.argv[1])
portPub = int(sys.argv[2])
### ports should be the same , instead i should takes IPs of the other 2 machines
IP1='localhost'
IP2='localhost'
firstPortSecondShard = int (sys.argv[3])
firstPortThirdShard = int (sys.argv[4])
FirstMachineSub=[]
SecondMachineSub=[]
for i in range (3):
    FirstMachineSub.append(firstPortSecondShard+i)
    SecondMachineSub.append(firstPortThirdShard+i)

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
for i in range (3): 
    topicfilter = "INSERT"
    ### 3 subscribes for each machines as each machine has 3 processes running (3 publishers)
    socketSub.connect ("tcp://%s:%s" % (IP1, FirstMachineSub[i]))
    socketSub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    
    socketSub.connect ("tcp://%s:%s" % (IP2, SecondMachineSub[i]))
    socketSub.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

dbLock = threading.Lock()

def ServerPub():
    # this function is responsible for executing client command
    # and if sign up (new insetion) publish to other shards immediatly
    while True:
        message = socket.recv()
        print ("Received request: ", message)    
        msg = str(message,'utf-8')
        query = msg.split()
        print(query)
        with dbLock:
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
            
        socket.send_string(messageToSend)


def Sub():
    while True:
        messagedata = socketSub.recv()
        print('Subscriber on .. inserting in db query',messagedata)
        try:
            with dbLock:
                # Execute the SQL command
                cursor.execute(messagedata)
                # Commit your changes in the database
                db.commit()
        
        except:
            print("Already inserted (may be) ..")
            

server_pub = threading.Thread(target=ServerPub)
sub = threading.Thread(target=Sub)

server_pub.start()
sub.start()

server_pub.join()
sub.join()

# disconnect from server
#db.close()