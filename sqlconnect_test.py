#! /usr/bin/env python
#coding=utf-8
import mysql.connector
import numpy
import matplotlib.pyplot as plt
from mysql.connector import errorcode
#Try to test if the connection is done

user_id = "root"
password = "0820" 
try:
  cnx = mysql.connector.connect(user='root',password='0820',database='dataproject')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENOR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exists")
  else:
    print(err)
else:
  cnx.close()
  
#Create Database
cnx = mysql.connector.connect(user='root',password='0820',database='dataproject')
cursor = cnx.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "SHOW GLOBAL VARIABLES LIKE 'local_infile'")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

#print cnx.database  == 'dataproject'

try:
    cnx.database == 'dataproject'
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = dataproject
    else:
        print(err)
        exit(1)
        


