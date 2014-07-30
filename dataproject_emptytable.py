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
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dataproject))
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

sql = "DROP TABLE IF EXISTS `Transit`"
cursor.execute(sql)
print "Transit Table Deleted!"
sql2 = "CREATE TABLE Transit(DOW int(2) NOT NULL,\
dir int(2) NOT NULL,\
ROUTE int(2) NOT NULL,\
TRIPA int(4) NOT NULL,\
BLOCKA int(6) NOT NULL,\
VEHNOA int(4) NOT NULL,\
daymoyr date NOT NULL,\
STOPA int(4) NOT NULL,\
QSTOPA char(10) NOT NULL,\
ANAME varchar(30) NOT NULL,\
HR int(2) NOT NULL,\
MIN int(2) NOT NULL,\
SEC int(2) NOT NULL, \
DHR int(2) NOT NULL,\
DMIN int(2) NOT NULL,\
DSEC int(2) NOT NULL,\
ON_NUM int(2) NOT NULL,\
OFF_NUM int(2) NOT NULL,\
LOAD_NUM int(2) NOT NULL,\
DLMILES float(5,2) NOT NULL,\
DLMIN float(5,2) NOT NULL,\
DLPMLS float(5,3) NOT NULL,\
DWTIME float(5,2) NOT NULL,\
DELTA int(10) NOT NULL,\
SCHTIM int(10) NOT NULL,\
SCHDEV float(5,2) NOT NULL,\
SRTIME float(5,2) NOT NULL,\
ARTIME float(5,2) NOT NULL)"

cursor.execute(sql2)
print "Transit Table Created!"

