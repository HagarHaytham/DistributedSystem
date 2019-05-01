# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 15:22:33 2019

@author: hagar
"""
import zmq
import sys
#### be a server when a client wants a task done 
#### if sign up make sure the username is new and not on the db
#### if login check for the paswword


port=int(sys.argv[1])

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)
while True:
    message = socket.recv()
    print ("Received request: ", message)    
    msg = str(message,'utf-8')#+ str(port)
    socket.send_string(msg)
### then publish that if it is an insertion


### subscribe to other machines to get new updates

