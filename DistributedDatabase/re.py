# -*- coding: utf-8 -*-
"""
Created on Sun May  5 15:02:14 2019

@author: hagar
"""

import re

str = "xx 3001"
x = re.search("Signed in Sucessfully", str)
if x!=None:
    print("The first white-space character is located in position:", x.start())