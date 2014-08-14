#! /usr/bin/env python
#coding=utf-8
import mysql.connector
import numpy
import math
import pylab
import matplotlib.pyplot as plt
from mysql.connector import errorcode
#Try to test if the connection is done

user_id = "root"
password = "1234"
database = "dataproject"
port = "3308"
host = "192.168.2.107"
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
        


startyear = 2012
startmonth =9
endyear = 2013
endmonth = 10
starttime = 6
endtime = 12
stopA = 9
QstopA = "  E19790"#"  S48270"
stopB = 15
QstopB = "  E19310"#"  E41250"
route = 614


#CROWDING CALCULATE AND PAINT IN HISTOGRAM
#define a function to calculate crowding based on the database user-specified,
#first we calculate a value named Dcorwd:LOAD/CAPACITY of a section between the adjacent stop  
#then based on the exact TRIP of one day,we select the maximum of the Dcrowd between the stopA and
#stopB which are specified by user
def calculate_crowding(startyear,startmonth,endyear,endmonth,starttime,endtime,stopA,QstopA,stopB,QstopB,route):
    sql = "SELECT `LOAD_NUM`,`CAPACITY`,`STOPA`,`daymoyr`,`TRIPA`,`DLMILES`,`QSTOPA` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<%d AND '%d-%d-01'<=daymoyr AND daymoyr<='%d-%d-31'\
    AND ROUTE = %d AND %d <= STOPA AND STOPA <= %d order by daymoyr,TRIPA,STOPA ASC"\
    % (starttime,endtime,startyear,startmonth,endyear,endmonth,route,stopA,stopB)
    cursor.execute(sql)
   
    number = (endmonth-startmonth+1+12*(endyear-startyear))*31 
    crowding = [[] for i in range(number)]
    row = cursor.fetchone()
    while row[6] != QstopA:
        row = cursor.fetchone()
    daymoyr = row[3]
    TRIPA = row[4]
    Dcrowd = row[0]*1.0/row[1]
    results = cursor.fetchall()
    count = 0
    j = 0
    for row in results:
        if row[3] == daymoyr:
            if row[4] == TRIPA:
                count = count+1
                if row[0]*1.0/row[1] > Dcrowd:
                    Dcrowd = row[0]*1.0/row[1]                    
            else:
                if count == stopB - stopA:
                    crowding[j].append(Dcrowd)
                if row[6] == QstopA:
                    TRIPA = row[4]
                    Dcrowd = row[0]*1.0/row[1]
                count = 0
        else:
            if count == stopB - stopA:
                crowding[j].append(Dcrowd)
            #print j
            if row[6] == QstopA:
                j = j+1
                daymoyr = row[3]
                TRIPA = row[4]
                Dcrowd = row[0]*1.0/row[1]
            count = 0    
#    if j+1 < number:
#        for i in range(j+1,number):
#            del crowding[i]                        
    print j+1
    return crowding

#define a function to calculate crowding based on the database user-specified,
#first we calculate a value named Dcorwd:LOAD/CAPACITY of a section between the adjacent stop 
#then based on the exact TRIP of one day,we calculate the weighted average of the 
#Dcrowd(weight is the delta miles between the adjacent stop) between the stopA and
#stopB which are specified by user
def calculate_crowding2(startmonth,endmonth,starttime,endtime,stopA,stopB,route):
    sql = "SELECT `LOAD_NUM`,`CAPACITY`,`STOPA`,`daymoyr`,`TRIPA`,`DLMILES` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'\
    AND ROUTE = %d AND %d < STOPA AND STOPA <= %d AND DLMILES != 0 order by daymoyr,TRIPA ASC"\
    % (starttime,endtime,startmonth,endmonth,route,stopA,stopB)
    cursor.execute(sql)
   
    number = (endmonth-startmonth)*31 +31
    crowding = [[] for i in range(number)]
    row = cursor.fetchone()
    daymoyr = row[3]
    TRIPA = row[4]
    Dcrowd = row[0]*1.0/row[1]*row[5]
    DLMILES = row[5]
    results = cursor.fetchall()
    j = 0
    for row in results:
        if row[3] == daymoyr:
            if row[4] == TRIPA:
                Dcrowd = row[0]*1.0/row[1]*row[5]+Dcrowd 
                DLMILES = DLMILES + row[5]                   
            else:
                crowding[j].append(Dcrowd/DLMILES)
                TRIPA = row[4]
                Dcrowd = row[0]*1.0/row[1]*row[5]
                DLMILES = row[5]
        else:
            crowding[j].append(Dcrowd/DLMILES)
            #print j
            j = j+1
            daymoyr = row[3]
            TRIPA = row[4]
            Dcrowd = row[0]*1.0/row[1]*row[5]
            DLMILES = row[5]
#    if j+1 < number:
#        for i in range(j+1,number):
#            del crowding[i]                        
    return crowding


crowd_1 = calculate_crowding(startyear,startmonth,endyear,endmonth,starttime,endtime,stopA,QstopA,stopB,QstopB,route)

crowd_2 = []

for i in range(len(crowd_1)):
    if len(crowd_1[i]) >0:
        crowd_2.append(numpy.mean(crowd_1[i]))

#for i in range(len(crowd_1)):
#    if len(crowd_1[i]) >0:
#        crowd_2.extend(crowd_1[i])

print crowd_2 
upper_bound = math.ceil(numpy.max(crowd_2)*10)
lower_bound = math.floor(numpy.min(crowd_2)*10)
x = numpy.arange(lower_bound/10,(upper_bound+0.5)/10,0.05)

n, bins, patches = plt.hist(crowd_2,bins = x, normed=0, facecolor='green', alpha=0.5)
threshold_lower = 0.2
threshold_upper = 0.4
print n
percentage = numpy.sum(n[int((threshold_lower-bins[0])*20):int((threshold_upper-bins[0])*20)])*1.0/numpy.sum(n)

plt.axvline(x = threshold_lower)
plt.axvline(x = threshold_upper)
plt.text(threshold_lower,numpy.max(n),'%f'%percentage,horizontalalignment='center')
plt.xlabel('crowding')
plt.ylabel('count')

plt.show()

cnx.close()

