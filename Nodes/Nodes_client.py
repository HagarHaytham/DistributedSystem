# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 22:17:55 2019

@author: Dalia
"""
import zmq
import time
import sys
import socket
import threading


#def run():
 #   if(thread.getName()):
        

def alive():
    i=0
    while i<5:
        topicfilter = socket.gethostbyname(socket.gethostname())
        topicfilter+= "@" + port1
        messagedata = "ALIVE"
        socket1.send_string("%s %s" % (messagedata, topicfilter))
        time.sleep(1)
        print(topicfilter)
        i+=1


def upload():
    name = socket2.recv_string()
    f = open(name,'wb')
    time.sleep(1)
    l = socket2.recv()
    print ("Receiving...")
    time.sleep(1)
    f.write(l)
    f.close()
    #time.sleep(10)
    #print ("Done Receiving")
    socket2.send_string('Done Sending')
    time.sleep(1)
    print(socket2.recv_string())
    time.sleep(1)
    
    socket1.send_string("success uploading")
    socket1.send_string(name)
    print("upload")


if __name__ == "__main__": 
    
    port = "777"
    if len(sys.argv) > 1:
        port =  sys.argv[1]
        int(port)
    context = zmq.Context()
    socket2 = context.socket(zmq.REP)
    socket2.bind("tcp://*:%s" % port)
    
    print ("connecting to client...")
    
    ################################################
    #publisher
    
    port1 = "5555"
    socket1 = context.socket(zmq.PUB)
    socket1.bind("tcp://*:%s" % port1)
    print ("connecting to Nodes...")
    #topicfilter = socket.gethostbyname(socket.gethostname())
    #topicfilter+= "@" + port


    # creating thread 
    t1 = threading.Thread(target=upload) 
    t2 = threading.Thread(target=alive) 
  
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start() 
    #alive()
    # wait until thread 1 is completely executed 
    t2.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
  
    # both threads completely executed 
    print("Done!")

#port = "777"
#if len(sys.argv) > 1:
#    port =  sys.argv[1]
#    int(port)
#context = zmq.Context()
#socket2 = context.socket(zmq.REP)
#socket2.bind("tcp://*:%s" % port)
#
#print ("connecting to client...")
#name = socket2.recv_string()
#f = open(name,'wb')
#
#################################################
##publisher
#
#port1 = 9999
#socket1 = context.socket(zmq.PUB)
#socket1.bind("tcp://*:%s" % port1)
#print ("connecting to Nodes...")
##topicfilter = socket.gethostbyname(socket.gethostname())
##topicfilter+= "@" + port
#
#t1 = thread()
#t2 = thread()
#t1.setName('1')
#t1.start()
#

#while True:
    
#    messagedata = "ALIVE"
#    socket1.send_string("%s %s" % (messagedata, topicfilter))
#    time.sleep(1)

##################################################
    #upload()
    #alive()
    

    
#    l = socket2.recv()
#    print ("Receiving...")
#    time.sleep(1)
#    f.write(l)
#    f.close()
#    #time.sleep(10)
#    #print ("Done Receiving")
#    socket2.send_string('Done Sending')
#    time.sleep(1)
#    print(socket2.recv_string())
#    time.sleep(1)
#    
#    socket1.send_string("success uploading")
#    socket1.send_string(name)
    #socket2.close()                # Close the connection
