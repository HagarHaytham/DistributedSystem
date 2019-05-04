# -*- coding: utf-8 -*-
"""
Created on Sat May  4 00:15:14 2019

@author: hagar
"""

from multiprocessing import Process, Lock
import sys
import time
def f(l, i):
    print('I am at the beginig of ',i)
    l.acquire()
    try:
        print('hello world', i)
        time.sleep(2)
    finally:
        l.release()
#x = sys.argv[1]
if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()