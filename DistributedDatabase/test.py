# -*- coding: utf-8 -*-
"""
Created on Thu May  2 17:51:40 2019

@author: hagar
"""

#sql ="INSERT INTO USERS (UserName,UserPassword,Email) VALUES ( %s , %s ,%s )"
#query=['0','1','2','3']

import threading
from queue import Queue
import time

# lock on shared variables
# when a thread is trying to access a locked variable
# it acts as a queue ?
#print('hi')
print_lock = threading.Lock()
#print('hi2')
def exampleJob(worker):
    time.sleep(0.5)
#    print('are we here')
    with print_lock:
        print(threading.current_thread().name,worker)
        
def threader():
    while True:
        worker = q.get()
        exampleJob(worker)
        q.task_done()
q = Queue()

for x in range (10):
    t = threading.Thread(target=threader)
    t.daemon = True  # by default it is false
    # true means it dies when the main dies
    t.start()
start = time.time()
for worker in range (20):
    q.put(worker)
    print(q.qsize())
q.join() # wait for the thread to terminate
print ('Entire job took : ' ,time.time()-start)
    
import zmq

print("Current libzmq version is %s" % zmq.zmq_version())
print("Current  pyzmq version is %s" % zmq.__version__)
    