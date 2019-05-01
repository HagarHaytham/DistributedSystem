# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 06:28:32 2019

@author: hagar
"""

#import PyMySQL
import pymysql as PyMySQL


# Open database connection
db = PyMySQL.connect("localhost","testuser","123456","Usersdb" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO USERS(UserName,
   Email, UserPassword)
   VALUES ('ay7d', 'ay7d@ay7aga.com', '123')"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()