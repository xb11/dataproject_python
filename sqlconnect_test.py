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
        

##ontimeperformance calculate and painting in histogram
#def calculate_ontimeperformance(startmonth,endmonth,starttime,endtime,stopB,route):
#    sql = "select `daymoyr`,`TRIPA`,`SCHDEV`  from `dataproject`.`transit` \
#     where ROUTE = %d AND STOPA = %d AND %d<=HR AND HR<%d AND DOW = 1 AND \
#    '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31' \
#     AND SCHDEV <= 50 order by daymoyr ASC;"\
#    %(route,stopB,starttime,endtime,startmonth,endmonth)
#    cursor.execute(sql)
#    results = cursor.fetchall()
#    A = []
#    for row in results:
#        A.append(row[2])
#    return A
#
#ontimeperformance = calculate_ontimeperformance(9,10,7,9,3,1)
#upper_bound = int(math.ceil(numpy.max(ontimeperformance)))
#lower_bound = int(math.floor(numpy.min(ontimeperformance)))
#x = range(lower_bound,upper_bound + 1)
#
#n, bins, patches = plt.hist(ontimeperformance,bins = x, normed=0, facecolor='green', alpha=0.5)
#
#threshold_lower = -1
#threshold_upper = 5
#percentage = numpy.sum(n[threshold_lower-bins[0]:threshold_upper-bins[0]])*1.0/numpy.sum(n)
#
#plt.axvline(x = threshold_lower)
#plt.axvline(x = threshold_upper)
#
#plt.text(threshold_lower,numpy.max(n),'%f'%percentage,horizontalalignment='center')
#plt.xlabel('on-time performance')
#plt.ylabel('count')
#plt.show()
#
##WAITINGTIME CALCULATE AND PAINTING IN HISTOGRAM
#def calculate_waitingtime(startmonth,endmonth,starttime,endtime,stopB,route):
#    sql = "select `daymoyr`,`TRIPA`,`DHR`,`DMIN`,`DSEC`,`ON_NUM`  from \
#    `dataproject`.`transit` where ROUTE = %d AND STOPA = %d  \
#    AND %d<=HR AND HR<%d AND DOW = 1 AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31' \
#     order by daymoyr,DHR,DMIN,DSEC ASC;"\
#    %(route,stopB,starttime,endtime,startmonth,endmonth)
#    cursor.execute(sql)
#    row = cursor.fetchone()
#    date = row[0]
#    Dtime = row[2]*60 + row[3] + row[4]/60.0
#    waiting_time = []
#    results = cursor.fetchall()
#    for row in results:
#        if row[0] == date:
#            Dtime2 = row[2]*60 + row[3] + row[4]/60.0
#            waiting_time.append((Dtime2 - Dtime)/2.0)
#            Dtime = Dtime2
#        else:
#            date = row[0]
#            Dtime = row[2]*60 + row[3] + row[4]/60.0
#                
#        
#    return waiting_time
#    
#A = calculate_waitingtime(9,10,7,9,20,614)
#number = int(math.ceil(numpy.max(A)))
#waitingtime = [0 for i in range(0,number)]
#for i in A:
#    waitingtime[int(math.floor(i)):int(math.floor(i)) + 1] = [waitingtime[int(math.floor(i))] + 1]
#
##print waitingtime
#
#x = range(0,number + 1)
#threshold = 15
#percentage = numpy.sum(waitingtime[0:threshold])*1.0/numpy.sum(waitingtime)
## the histogram of the data
#n, bins, patches = plt.hist(A,bins = x, normed=0, facecolor='green', alpha=0.5)
##print bins
##print n
##print patches
##pylab.hist(A,bins = x)
##pylab.show()
#l = plt.axvline(x=threshold)
#plt.text(threshold,0,'%f'%percentage,horizontalalignment='center')
#plt.xlabel('waiting time')
#plt.ylabel('count')
#plt.show()

startmonth = 9
endmonth = 10
starttime = 7
endtime = 9
stopA = 3
stopB = 7
route = 614


#CROWDING CALCULATE AND PAINT IN HISTOGRAM
#define a function to calculate crowding based on the database user-specified,
#first we calculate a value named Dcorwd:LOAD/CAPACITY of a section between the adjacent stop  
#then based on the exact TRIP of one day,we select the maximum of the Dcrowd between the stopA and
#stopB which are specified by user
def calculate_crowding(startmonth,endmonth,starttime,endtime,stopA,stopB,route):
    sql = "SELECT `LOAD_NUM`,`CAPACITY`,`STOPA`,`daymoyr`,`TRIPA`,`DLMILES` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'\
    AND ROUTE = %d AND %d < STOPA AND STOPA <= %d order by daymoyr,TRIPA ASC"\
    % (starttime,endtime,startmonth,endmonth,route,stopA,stopB)
    cursor.execute(sql)
   
    number = (endmonth-startmonth)*31 +31
    crowding = [[] for i in range(number)]
    row = cursor.fetchone()
    daymoyr = row[3]
    TRIPA = row[4]
    Dcrowd = row[0]*1.0/row[1]
    results = cursor.fetchall()
    j = 0
    for row in results:
        if row[3] == daymoyr:
            if row[4] == TRIPA:
                if row[0]*1.0/row[1] > Dcrowd:
                    Dcrowd = row[0]*1.0/row[1]                    
            else:
                crowding[j].append(Dcrowd)
                TRIPA = row[4]
                Dcrowd = row[0]*1.0/row[1]
        else:
            crowding[j].append(Dcrowd)
            #print j
            j = j+1
            daymoyr = row[3]
            TRIPA = row[4]
            Dcrowd = row[0]*1.0/row[1]
#    if j+1 < number:
#        for i in range(j+1,number):
#            del crowding[i]                        
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


crowd_1 = calculate_crowding(startmonth,endmonth,starttime,endtime,stopA,stopB,route)
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
threshold_lower = 0.1
threshold_upper = 0.3
print n
percentage = numpy.sum(n[int((threshold_lower-bins[0])*20):int((threshold_upper-bins[0])*20)])*1.0/numpy.sum(n)

plt.axvline(x = threshold_lower)
plt.axvline(x = threshold_upper)
plt.text(threshold_lower,numpy.max(n),'%f'%percentage,horizontalalignment='center')
plt.xlabel('crowding')
plt.ylabel('count')

plt.show()

##StopMeans = [0.174056,0.153506,0.164026]
#N = stopB - stopA
#max = numpy.max(StopMeans)
##print max
##print numpy.arange(0,max*1.33,max/6.0)
##ticks = ['stop3','stop4','stop5']
#ticks = []
#for i in range(stopA + 1, stopB+1):
#   ticks.append('stop%d'%i)
#
#ind = numpy.arange(N)    # the x locations for the groups
#width = 0.35       # the width of the bars: can also be len(x) sequence
#
#p1 = plt.bar(ind, StopMeans,   width, color='r')
#
#
#plt.ylabel('crowding')
#plt.title('crowding between stop')
#plt.xticks(ind+width/2., ticks )
#plt.yticks(numpy.arange(0,max*1.33,max/6.0))
##plt.legend( (p1[0]), ('Crowding'),loc = 2)
#
#plt.show()
#
#
#sql = """select * FROM `dataproject`.`transit` limit 200"""
#cursor.execute(sql)
#results = cursor.fetchall()
#print results[0]

cnx.close()

