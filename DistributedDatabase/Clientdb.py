# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 14:29:14 2019

@author: hagar
"""

## Client Process ## Cordinator ####
import getpass  # for password to be invisible
import zmq
import re



def UserAuthenticate(IPS,portsbegin):
        ##### ----------- initial db Configuration --------------------#####
    
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
            socket[i].connect ("tcp://%s:%s" %(IPS[i], port[i][j]))
            socket[i].RCVTIMEO =500
            socket[i].setsockopt(zmq.LINGER, 500)  # set zmq.LINGER to 0.5 seconds to let the client process terminate if there is no servers up
            
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
        print ("Any input cannot contain spaces")
        space=[]
        while True:
            username = input('Enter Username(Username MUST begin with letter):')
            space=username.split()
            if  len(space)==1 and (username[0].isalpha()):
                break
        while True:
            Password = getpass.getpass('Enter Password:')
            space=Password.split()
            if len(space)==1:
                break
            
        ####### Construct the message
        msg=mode+" " +username+" "+ Password+" "
        if (mode =="1"):  # sign up
             while True:
                 Email = input('Enter Email:')
                 space=Email.split()
                 if len(space)==1:
                     break
             msg +=Email
            
        ####### (pick server to assign this task for)
        shardbusy=[0,0,0]
        if username[0] in Listm1 :
            shard=0
        elif username[0] in Listm2 :
            shard=1
        else:
            shard=2
        shardbusy[shard] =1
        
        connectingDb=True
        while connectingDb==True:
            
            print ("Sending request ")
            message = b'this server is busy .. please wait connecting to another server'
            try:  
                ###### get response from that server
                socket[shard].send_string(msg)  ## bocking or not ?
                message = socket[shard].recv()#(flags=zmq.NOBLOCK)
            except:
                pass
                
            print ("Received reply of request: ", message)
            
            RecievedMsg = str(message,'utf-8')
            if RecievedMsg =="this server is busy .. please wait connecting to another server":
                ## connect to another shard if any
                i=0
                found = False
                while (i<3 and found==False):
                    if (shardbusy[i]==0):
                        shardbusy[i]=1
                        shard=i
                        found=True
                        break
                    i+=1
                if found == False:
                    print("Sorry, all servers are busy.. try again later")
                    return False,username
            else:
                connectingDb=False
            x = re.search("Signed in Sucessfully",RecievedMsg) 
            y = re.search("Logged in Sucessfully",RecievedMsg)
            if (x !=None or y != None):
                msgPort= RecievedMsg.split()
                Error = False
                print(msgPort)
                return True,int(msgPort[3])

#IPS = ['localhost','localhost','localhost'] # 3 shards IPs
## for testing on one machine , can begin from the same port in diffrent machines
#portsbegin=[5000,5005,5010] # shard 1 begins from port 5000 , shard 2 begins from 5005 and shard 3 from 5010     
#isAuthenticated ,port=UserAuthenticate(IPS,portsbegin)  
#print(isAuthenticated)
#print(port)
###### if authenticated let it talk to the master tracker
#        