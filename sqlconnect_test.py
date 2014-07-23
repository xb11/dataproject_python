#! /usr/bin/env python
#coding=utf-8
import mysql.connector
import numpy
from mysql.connector import errorcode
#Try to test if the connection is done

#user_id = "root"
#password = "1234"
try:
  cnx = mysql.connector.connect(user='root',password='1234',database='dataproject')
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
cnx = mysql.connector.connect(user='root',password='1234',database='dataproject')
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
        
startmonth = 10
endmonth = 10
starttime = 7
endtime = \
9

def calculate_crowding(startmonth,endmonth,starttime,endtime):
    sql = "SELECT `LOAD_NUM`,`capacity` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<=%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'" \
    % (starttime,endtime,startmonth,endmonth)
    cursor.execute(sql)
    results = cursor.fetchall()
    crowding = []
    for row in results:
        crowding.append(row[0]/30.0/row[1])
    return crowding

crowd = calculate_crowding(10,10,7,9)
#print numpy.mean(crowd)
print crowd[0:5]


#sql = """select * FROM `dataproject`.`transit` limit 200"""
#cursor.execute(sql)
##print cursor.fetchone()
#results = cursor.fetchall()
#print results[0]

cnx.close()

