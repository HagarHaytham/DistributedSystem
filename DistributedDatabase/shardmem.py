# -*- coding: utf-8 -*-
"""
Created on Sun May  5 13:42:50 2019

@author: hagar
"""

from multiprocessing import Process, Value, Array,Lock
import sys

def f(n, portLock,i):
    print("Value before lock of",i," is ",n.value)
    portLock.acquire()
    n.value +=1
    portLock.release()
    print("Value after lockof",i," is ",n.value)
if __name__ == '__main__':
    PortMaster = 3000
    num = Value('h',PortMaster)
    portLock = Lock()
    p=[]
    for i in range (3):
        p.append(Process(target=f, args=(num, portLock,i)))
        p[i].start()
        p[i].join()

    print(num.value)
    