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

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)
insertion = False
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
               insertion = True
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
    ### then publish that if it is an insertion
#    if insertion == True:
        
    socket.send_string(messageToSend)


# disconnect from server
db.close()




### then publish that if it is an insertion


### subscribe to other machines to get new updates

