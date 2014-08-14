#! /usr/bin/env python
#coding=utf-8
#this program is trying to import actual departure time database and calculate 
#actual waiting time of user-specified date,time interval,stop(constant route) and 
#paint the histogram of one sample 

import mysql.connector
import numpy
import math
import matplotlib.pyplot as plt
from mysql.connector import errorcode

#Try to test if the connection is done
user_id = "root"
password = ""
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
  
#Create Database
cnx = mysql.connector.connect(user=user_id,password=password,database=database,port=port)
cursor = cnx.cursor()
#if there is no database set-up
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dataproject))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

#print cnx.database  == 'dataproject'
#test if we can access the database--dataproject
try:
    cnx.database == 'dataproject'
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = dataproject
    else:
        print(err)
        exit(1)
#user-specified data        
startmonth = 9
endmonth = 10
starttime = 7
endtime = 9
stopA = 19
stopB = 20
route = 614

#WAITINGTIME CALCULATE AND PAINTING IN HISTOGRAM
#define data-import and pre-processing function 
def calculate_waitingtime(startmonth,endmonth,starttime,endtime,stopB,route):
    sql = "select `daymoyr`,`TRIPA`,`DHR`,`DMIN`,`DSEC`,`ON_NUM`  from \
    `dataproject`.`transit` where ROUTE = %d AND STOPA = %d  and QSTOPA = '  E19840' \
    AND %d<=HR AND HR<%d AND DOW = 1 AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31' \
     order by daymoyr,DHR,DMIN,DSEC ASC;"\
    %(route,stopB,starttime,endtime,startmonth,endmonth)
    cursor.execute(sql)
    row = cursor.fetchone()
    date = row[0]
    Dtime = row[2]*60 + row[3] + row[4]/60.0
    waiting_time = []
    results = cursor.fetchall()
    for row in results:
        if row[0] == date:
            Dtime2 = row[2]*60 + row[3] + row[4]/60.0
            waiting_time.append((Dtime2 - Dtime)/2.0)
            Dtime = Dtime2
        else:
            date = row[0]
            Dtime = row[2]*60 + row[3] + row[4]/60.0
                
        
    return waiting_time
    
A = calculate_waitingtime(startmonth,endmonth,starttime,endtime,stopB,route)
upper_bound = int(math.ceil(numpy.max(A)))
waitingtime = [0 for i in range(0,upper_bound)]
for i in A:
    waitingtime[int(math.floor(i)):int(math.floor(i)) + 1] = [waitingtime[int(math.floor(i))] + 1]

#print waitingtime

x = range(0,upper_bound + 1)
threshold = 15
percentage = numpy.sum(waitingtime[0:threshold])*1.0/numpy.sum(waitingtime)
# the histogram of the data
n, bins, patches = plt.hist(A,bins = x, normed=0, facecolor='green', alpha=0.5)
#if the user-specified threshold is between the lower_bound and the upper_bound ,it will be showed in the histogram
if threshold < upper_bound:
    l = plt.axvline(x=threshold)

plt.text(threshold,0,'%f'%percentage,horizontalalignment='center')
plt.xlabel('waiting time')
plt.ylabel('count')
plt.show()

cnx.close()