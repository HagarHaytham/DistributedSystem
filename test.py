# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:40:35 2019

@author: Dalia
"""

import zmq
import sys
import time


context = zmq.Context()
message="700"
print ("Received port ", message)


socket1 = context.socket(zmq.REQ)
socket1.connect ("tcp://localhost:%s" % message)

print ("connecting to process...Enter your file") 
file=input()

f = open(file,'rb')
print ('Sending...')
l = f.read()
#while (l):
 #   print ('Sending...')
socket1.send(l)
#time.sleep(10)
#    l = f.read(1024)
#socket1.send(l)
f.close()
print ("Done Sending")
#socket1.shutdown(socket1.SHUT_WR)
print (socket1.recv())
socket1.close()






'''ports=[]
        for i in range(len(n)):
            for j in range(len(Nports)): #3
                if Nports[n[i]][j][1] == 'Y':
                    ports.append(Nports[n[i]][j][0])
                    
        res =""
        for i in ports:
            res += i
            res += " "
        '''