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
#sql = """INSERT INTO USERS(UserName,
#   Email, UserPassword)
#   VALUES ('ay7d2', 'ay7d@ay7aga1.com', '123')"""
sql ="INSERT INTO USERS (UserName,Email, UserPassword) VALUES ( %s , %s ,%s )"
try:
   # Execute the SQL command
   cursor.execute(sql,("hhh3","uuu","bla",))
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()
sql = "SELECT * FROM USERS "
cursor.execute(sql)
result = cursor.fetchall()
print(result)
if len(result)==0:
    print("NOOO")
# disconnect from server
db.close()