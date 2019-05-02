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
portsbegin=[5000,5005,5010] # shard 1 begins from port 5000 , shard 2 begins from 5005 and shard 3 from 5010
port=[]
context =[]
socket=[] 
    
for i in range (3): # 3 shards
    port.append([])
    for j in range (3): # 3 processes for each shard
        port[i].append( portsbegin[i]+j)


for i in range (3): # 3 shards
    context.append(zmq.Context())
    print ("Connecting to server(s) of machine %s...",i)
    socket.append(context[i].socket(zmq.REQ))
    for j in range (3): # 3 processes for each shard
        socket[i].connect ("tcp://localhost:%s" % port[i][j])
        
####Letters for each machine(shard)
Listm1 =['j','s','b','w','f','g','q','u']
Listm2 =['m','c','l','e','t','p','i','n']
Listm3 =['r','d','a','k','h','o','v','x','y','z']
Error = True
while Error == True:
    ####### take the command from user
    mode = input("To Sign Up type 1 and to log in choose 2\n")
    while(mode != "1" and mode != "2"):
        mode = input("To Sign Up type 1 and to log in choose 2\n")
    
    ##### ADD CHECKS ON INPUT!!!!
    username = input('Enter Username(Username MUST begin with letter):')
    while not(username[0].isalpha()):
        username = input('Enter Username(Username MUST begin with letter):')
    Password = getpass.getpass('Enter Password:') 
    
    ####### Construct the message
    msg=mode+" " +username+" "+ Password+" "
    if (mode =="1"):  # sign up
        ## new user so check if user name exists
         Email = input('Enter Email:')
         msg +=Email
         
    #else: # log in
         
        
    ####### (pick server to assign this task for)
         
    if username[0] in Listm1 :
        shard=0
    elif username[0] in Listm2 :
        shard=1
    else:
        shard=2
    
    
    #while True:
        
    print ("Sending request ")
    socket[shard].send_string(msg)
    message = socket[shard].recv()
        
    print ("Received reply of request ,recieved ", message)
    RecievedMsg = str(message,'utf-8')
    if (RecievedMsg == "Signed in Sucessfully"):
        Error = False
     
###### get response from that server
     
     
##### if authenticated let it talk to the master tracker