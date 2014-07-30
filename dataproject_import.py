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

def load_database(cursor):
  
    try:
      SetGlobal ="SHOW GLOBAL VARIABLES LIKE 'local_infile'\
      SET GLOBAL local_infile = 'ON'\
      SHOW GLOBAL VARIABLES LIKE 'local_infile'"
      sql = '''LOAD DATA INFILE 'E:/Document/2012-2014CMU/Semesters/2014 Summer/Data Project/Transit/OriginalData2012-2013/2012 1209-1211/WEEKDAYRIDECHECK_GROUP1_NOVEMBER2012.csv' INTO TABLE Transit
FIELDS TERMINATED BY ','
ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
IGNORE 3 LINES
(DOW, dir, ROUTE, TRIPA, BLOCKA, VEHNOA, @var1, STOPA, QSTOPA, ANAME, HR, MIN, SEC, DHR, DMIN, DSEC, ON_NUM, OFF_NUM, LOAD_NUM, DLMILES, DLMIN, DLPMLS, DWTIME, DELTA, SCHTIM, SCHDEV, SRTIME, ARTIME)
set daymoyr = STR_TO_DATE(SUBSTRING(@var1,1,10) '%e.%c.%Y')'''
      #cursor.execute(SetGlobal)
      #print"local infile set to ON"
      cursor.execute(sql)
      cnx.commit()
      print"data successfully loaded!"
    except mysql.connector.Error as err:
      print("Failed loading database: {}".format(err))
      exit(1)

#print cnx.database  == 'dataproject'

try:
    cnx.database == 'dataproject'
    print "dataproject Used"
    load_database(cursor)
    print"dataproject loaded with new data"
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Failed loading database: {}".format(err))
      exit(1)

