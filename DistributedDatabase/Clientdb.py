# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:29:14 2019

@author: hagar
"""

## Client Process ## Cordinator ####
import getpass  # for password to be invisible
import zmq
import sys
#import tim
#port=[]
#for i in range(1,len(sys.argv)):
#    port.append(int(sys.argv[i]))
port1=int(sys.argv[1])
port2=int(sys.argv[2])
port3=int(sys.argv[3])

context1 = zmq.Context()
print ("Connecting to server(s) of machine 1...")
socket1 = context1.socket(zmq.REQ)
socket1.connect ("tcp://localhost:%s" % port1)

context2 = zmq.Context()
print ("Connecting to server(s) of machine 2...")
socket2 = context2.socket(zmq.REQ)
socket2.connect ("tcp://localhost:%s" % port2)

context3 = zmq.Context()
print ("Connecting to server(s) of machine 3...")
socket3 = context3.socket(zmq.REQ)
socket3.connect ("tcp://localhost:%s" % port3)

while True:
    request =input("Enter your request ")
    print ("Sending request ", request)
    msg="request no is "+str(request)
    if (int(request)==1):
        socket1.send_string(msg)
        message = socket1.recv()
    elif (int(request)==2):
        socket2.send_string(msg)
        message = socket2.recv()
    else:
        socket3.send_string(msg)
        message = socket3.recv()
        
    print ("Received reply of request ", request, "recieved ", message)


####Letters for each machine(shard)
Listm1 =['j','s','b','w','f','g','q','u']
Listm2 =['m','c','l','e','t','p','i','n']
Listm3 =['r','d','a','k','h','o','v','x','y','z']

####### take the command from user
mode = input("To Sign Up type 1 and to log in choose 2\n")
while(mode != "1" and mode != "2"):
    mode = input("To Sign Up type 1 and to log in choose 2\n")

##### ADD CHECKS ON INPUT!!!!
username = input('Enter Username(Username MUST begin with letter):')
while not(username[0].isalpha()):
    username = input('Enter Username(Username MUST begin with letter):')
Password = getpass.getpass('Enter Password:') 
if (mode =="1"):  # sign up
    ## new user so check if user name exists
     Email = input('Enter Email:')
     
#else: # log in
     
     
####### (pick server to assign this task for)
     
     
     
###### get response from that server
     
     
##### if authenticated let it talk to the master tracker