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
try:
<<<<<<< HEAD
  cnx = mysql.connector.connect(user='root',password='1234',database='dataproject',port='3308')
=======
  cnx = mysql.connector.connect(user='root',password='0820',database='dataproject')
>>>>>>> ecf08a23559bc5a84885705e1531cc8cc57a50e9
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
<<<<<<< HEAD
cnx = mysql.connector.connect(user='root',password='1234',database='dataproject',port='3308')
=======
cnx = mysql.connector.connect(user='root',password='0820',database='dataproject')
>>>>>>> ecf08a23559bc5a84885705e1531cc8cc57a50e9
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
        

<<<<<<< HEAD
#ontimeperformance calculate and painting in histogram
def calculate_ontimeperformance(startmonth,endmonth,starttime,endtime,stopB,route):
    sql = "select `daymoyr`,`TRIPA`,`SCHDEV`  from `dataproject`.`transit` \
     where ROUTE = %d AND STOPA = %d AND %d<=HR AND HR<%d AND DOW = 1 AND \
    '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31' \
     AND SCHDEV <= 50 order by daymoyr ASC;"\
    %(route,stopB,starttime,endtime,startmonth,endmonth)
=======

<<<<<<< HEAD
<<<<<<< HEAD
def calculate_crowding(startmonth,endmonth,starttime,endtime):
    sql = "SELECT `LOAD_NUM`,`capacity` FROM `dataproject`.`Transit` \
    WHERE %d<=HR AND HR<=%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'" \
    % (starttime,endtime,startmonth,endmonth)
=======
def calculate_crowding(startmonth,endmonth,starttime,endtime,stopA,stopB,route):
    sql = "SELECT `LOAD_NUM`,`capacity`,`STOPA` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<=%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'\
     AND ROUTE = %d AND %d < STOPA AND STOPA <= %d"\
    % (starttime,endtime,startmonth,endmonth,route,stopA,stopB)
>>>>>>> origin/master
>>>>>>> origin/master
    cursor.execute(sql)
    results = cursor.fetchall()
    A = []
    for row in results:
        A.append(row[2])
    return A

ontimeperformance = calculate_ontimeperformance(9,10,7,9,3,1)
upper_bound = int(math.ceil(numpy.max(ontimeperformance)))
lower_bound = int(math.floor(numpy.min(ontimeperformance)))
x = range(lower_bound,upper_bound + 1)

n, bins, patches = plt.hist(ontimeperformance,bins = x, normed=0, facecolor='green', alpha=0.5)
# print n
# print bins

threshold_lower = -1
threshold_upper = 5
percentage = numpy.sum(n[threshold_lower-bins[0]:threshold_upper-bins[0]-1])*1.0/numpy.sum(n)

plt.axvline(x = threshold_lower)
plt.axvline(x = threshold_upper)

plt.text(threshold_lower,numpy.max(n),'%f'%percentage,horizontalalignment='center')
plt.show()

#WAITINGTIME CALCULATE AND PAINTING IN HISTOGRAM
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
#percentage = numpy.sum(waitingtime[0:threshold-1])*1.0/numpy.sum(waitingtime)
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

# CROWDING CALCULATE AND PAINT IN BAR PLOTS
#def calculate_crowding(startmonth,endmonth,starttime,endtime,stopA,stopB,route):
#    sql = "SELECT `LOAD_NUM`,`capacity`,`STOPA` FROM `dataproject`.`transit` \
#    WHERE %d<=HR AND HR<=%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'\
#     AND ROUTE = %d AND %d < STOPA AND STOPA <= %d"\
#    % (starttime,endtime,startmonth,endmonth,route,stopA,stopB)
#    cursor.execute(sql)
#    results = cursor.fetchall()
#    number = stopB - stopA
#    crowding = [[] for i in range(number)]
#    for row in results:
#        crowding[row[2]-stopA-1].append(row[0]/30.0/row[1])
#    return crowding
#
#crowd = calculate_crowding(10,10,7,9,stopA,stopB,1)
#
#StopMeans   = []
#
#for i in range(stopA + 1, stopB+1):
#    StopMeans.append(numpy.mean(crowd[i-stopA-1]))
#    print "from stop %d to %d, the crowding is %f "%(i-1,i,StopMeans[i-stopA -1])
#
##StopMeans = [0.174056,0.153506,0.164026]
#N = stopB - stopA
#max = numpy.max(StopMeans)
##print max
##print numpy.arange(0,max*1.33,max/6.0)
##ticks = ['stop3','stop4','stop5']
#ticks = []
#for i in range(stopA + 1, stopB+1):
#    ticks.append('stop%d'%i)
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



#sql = """select * FROM `dataproject`.`transit` limit 200"""
#cursor.execute(sql)
##print cursor.fetchone()
#results = cursor.fetchall()
#print results[0]

cnx.close()

=======
>>>>>>> ecf08a23559bc5a84885705e1531cc8cc57a50e9
