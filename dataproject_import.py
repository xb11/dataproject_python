#! /usr/bin/env python
#coding=utf-8
import mysql.connector
import numpy
import matplotlib.pyplot as plt
from mysql.connector import errorcode
import glob
import os
#Try to test if the connection is done

user_id = "root"
password = "0820"
database = "dataproject"
port = "3306"

try:
  cnx = mysql.connector.connect(user=user_id,password=password,database=database,port=port)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENOR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exists")
  else:
    print(err)
else:
  cnx.close()
  
#Prepare for loading Database
cnx = mysql.connector.connect(user=user_id,password=password,database=database,port=port)
cursor = cnx.cursor()


      #SetGlobal ="SHOW GLOBAL VARIABLES LIKE 'local_infile'\
      #SET GLOBAL local_infile = 'ON'\
      #SHOW GLOBAL VARIABLES LIKE 'local_infile'"
path = "E:/Document/2012-2014CMU/Semesters/2014_Summer/Data_Project/Transit/OriginalData2012-2013/2012 1209-1211/1209_complete_zipped/SEPTEMBER2012_ALLGROUPS/*.csv"
file_path="E:/Document/2012-2014CMU/Semesters/2014_Summer/Data_Project/Transit/OriginalData2012-2013/2012 1209-1211/1209_complete_zipped/SEPTEMBER2012_ALLGROUPS/"
def load_database(cursor):
    try:
      sql = '''LOAD DATA INFILE '{}'
INTO TABLE Transit
FIELDS TERMINATED BY ',' ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(DOW, dir, ROUTE, TRIPA, BLOCKA, VEHNOA, @var1, STOPA, QSTOPA, ANAME, HR, MIN, SEC, DHR, DMIN, DSEC, ON_NUM, OFF_NUM, LOAD_NUM, DLMILES, DLMIN, DLPMLS, DWTIME, @var3, @var2, SCHDEV, SRTIME, ARTIME)
set daymoyr = STR_TO_DATE(left(@var1,11), '%e-%b-%Y'),
DELTA = right(@var2, 3),SCHTIM = right(@var3, 3)'''
      l = os.listdir(file_path)
      #for fname in glob.glob(path):
      for fname in l:
        if fname.endswith('.csv'):
          print(fname)
          cursor.execute(sql.format(file_path+fname))
          cnx.commit()
          print"Loading file:"+fname
    except mysql.connector.Error as err:
        print("Failed loading database: {}".format(err))
        exit(1)
 
try:
    cnx.database == 'dataproject'
    print "dataproject Used"
    load_database(cursor)
    print "All data successfully loaded!"
except mysql.connector.Error as err:
    print("Failed loading database: {}".format(err))
    exit(1)

    

