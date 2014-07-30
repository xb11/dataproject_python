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
        
startmonth = 10
endmonth = 10
starttime = 7
endtime = 9
stopA = 2
stopB = 5
route = 1



#ontimeperformance calculate and painting in histogram
def calculate_ontimeperformance(startmonth,endmonth,starttime,endtime,stopB,route):
    sql = "select `daymoyr`,`TRIPA`,`SCHDEV`  from `dataproject`.`transit` \
     where ROUTE = %d AND STOPA = %d AND %d<=HR AND HR<%d AND DOW = 1 AND \
    '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31' \
     AND SCHDEV <= 50 order by daymoyr ASC;"\
    %(route,stopB,starttime,endtime,startmonth,endmonth)



def calculate_crowding(startmonth,endmonth,starttime,endtime,stopA,stopB,route):
    sql = "SELECT `LOAD_NUM`,`capacity`,`STOPA` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<=%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'\
     AND ROUTE = %d AND %d < STOPA AND STOPA <= %d"\
    % (starttime,endtime,startmonth,endmonth,route,stopA,stopB)

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

#ontimeperformance calculate and painting in histogram
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
#plt.show()


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

# CROWDING CALCULATE AND PAINT IN BAR PLOTS
def calculate_crowding(startmonth,endmonth,starttime,endtime,stopA,stopB,route):
    sql = "SELECT `LOAD_NUM`,`capacity`,`STOPA`,`daymoyr`,`TRIPA`,`DLPMLS` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'\
    AND ROUTE = %d AND %d < STOPA AND STOPA <= %d order by daymoyr,TRIPA ASC"\
    % (starttime,endtime,startmonth,endmonth,route,stopA,stopB)
    cursor.execute(sql)
   
    number = (endmonth-startmonth)*31 +31
    crowding = [[] for i in range(number)]
    row = cursor.fetchone()
    daymoyr = row[3]
    TRIPA = row[4]
    Dcrowd = row[0]/30.0/row[1]
    results = cursor.fetchall()
    j = 0
    for row in results:
        if row[3] == daymoyr:
            if row[4] == TRIPA:
                if row[0]/30.0/row[1] > Dcrowd:
                    Dcrowd = row[0]/30.0/row[1]                    
            else:
                crowding[j].append(Dcrowd)
                TRIPA = row[4]
                Dcrowd = row[0]/30.0/row[1]
        else:
            crowding[j].append(Dcrowd)
            #print j
            j = j+1
            daymoyr = row[3]
            TRIPA = row[4]
            Dcrowd = row[0]/30.0/row[1]
#    if j+1 < number:
#        for i in range(j+1,number):
#            del crowding[i]                        
    return crowding

def calculate_crowding2(startmonth,endmonth,starttime,endtime,stopA,stopB,route):
    sql = "SELECT `LOAD_NUM`,`capacity`,`STOPA`,`daymoyr`,`TRIPA`,`DLPMLS` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'\
    AND ROUTE = %d AND %d < STOPA AND STOPA <= %d AND DLPMLS != 0 order by daymoyr,TRIPA ASC"\
    % (starttime,endtime,startmonth,endmonth,route,stopA,stopB)
    cursor.execute(sql)
   
    number = (endmonth-startmonth)*31 +31
    crowding = [[] for i in range(number)]
    row = cursor.fetchone()
    daymoyr = row[3]
    TRIPA = row[4]
    Dcrowd = row[0]/30.0/row[1]*row[5]
    DLPMLS = row[5]
    results = cursor.fetchall()
    j = 0
    for row in results:
        if row[3] == daymoyr:
            if row[4] == TRIPA:
                Dcrowd = row[0]/30.0/row[1]*row[5]+Dcrowd 
                DLPMLS = DLPMLS + row[5]                   
            else:
                crowding[j].append(Dcrowd/DLPMLS)
                TRIPA = row[4]
                Dcrowd = row[0]/30.0/row[1]*row[5]
                DLPMLS = row[5]
        else:
            crowding[j].append(Dcrowd/DLPMLS)
            #print j
            j = j+1
            daymoyr = row[3]
            TRIPA = row[4]
            Dcrowd = row[0]/30.0/row[1]*row[5]
            DLPMLS = row[5]
#    if j+1 < number:
#        for i in range(j+1,number):
#            del crowding[i]                        
    return crowding


crowd_1 = calculate_crowding2(9,10,7,9,stopA,stopB,1)
crowd_2 = []

for i in range(len(crowd_1)):
    if len(crowd_1[i]) >0:
        crowd_2.append(numpy.mean(crowd_1[i]))

#for i in range(len(crowd_1)):
#    if len(crowd_1[i]) >0:
#        crowd_2.extend(crowd_1[i])

#crowd_2 = [0.10833333333333334, 0.23333333333333331, 0.73333333333333328, 0.14999999999999999, 0.35416666666666669, 0.29166666666666669, 0.11666666666666665, 0.33333333333333337, 0.080000000000000002, 0.16666666666666666, 0.10000000000000001, 0.22666666666666671, 0.22666666666666666, 0.1111111111111111, 0.21666666666666665, 0.29444444444444445, 0.42222222222222222, 0.055555555555555559, 0.095833333333333326, 0.35833333333333334, 0.12083333333333332, 0.15555555555555553, 0.32222222222222219, 0.11666666666666665, 0.33666666666666667, 0.17999999999999999, 0.21333333333333332, 0.44166666666666665, 0.39999999999999997, 0.35999999999999999, 0.15277777777777779, 0.072222222222222229, 0.25, 0.14999999999999999, 0.087499999999999994, 0.27777777777777773, 0.16666666666666666, 0.033333333333333333]
upper_bound = math.ceil(numpy.max(crowd_2)*10)
lower_bound = math.floor(numpy.min(crowd_2)*10)
x = numpy.arange(lower_bound/10,(upper_bound+1)/10,0.1)

n, bins, patches = plt.hist(crowd_2,bins = x, normed=0, facecolor='green', alpha=0.5)
threshold_lower = 0.1
threshold_upper = 0.6
print n
percentage = numpy.sum(n[int((threshold_lower-bins[0])*10):int((threshold_upper-bins[0])*10)])*1.0/numpy.sum(n)

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


#sql = """select * FROM `dataproject`.`transit` limit 200"""
#cursor.execute(sql)
#results = cursor.fetchall()
#print results[0]

cnx.close()

