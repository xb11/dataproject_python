#! /usr/bin/env python
#coding=utf-8
#this program is trying to import SCHDEV database and calculate the on-time
#performance of user-specified date,time interval,stop(constant route) and 
#paint the histogram of one sample 

import mysql.connector
import numpy
import math
import matplotlib.pyplot as plt
from mysql.connector import errorcode

#Try to test if the connection is done
user_id = "root"
password = "0820"
database = "dataproject"
port = "3306"
try:
  cnx = mysql.connector.connect(user='root',password='0820',database='dataproject',port='3306')
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
endmonth = 11
starttime = 7
endtime = 9
stopA = 2
stopB = 3
route = 1

#on-timeperformance calculate and painting in histogram
#DEFINE data-import function  
def calculate_ontimeperformance(startmonth,endmonth,starttime,endtime,stopB,route):
    sql = "select `daymoyr`,`TRIPA`,`SCHDEV`  from `dataproject`.`transit` \
     where ROUTE = %d AND STOPA = %d AND %d<=HR AND HR<%d AND DOW = 1 AND \
    '2012-%d-01'<=daymoyr AND daymoyr<='2013-%d-31' \
     AND SCHDEV <= 50 order by daymoyr ASC;"\
    %(route,stopB,starttime,endtime,startmonth,endmonth)
    cursor.execute(sql)
    results = cursor.fetchall()
    A = []
    for row in results:
        A.append(row[2])
    return A

#get the data calculated from the database and put them into histogram
ontimeperformance = calculate_ontimeperformance(startmonth,endmonth,starttime,endtime,stopB,route)
#ontimeperformance =[0.73, 1.42, 3.43, 9.12, 0.52, 1.53, 3.45, 2.18, 1.77, 1.83, \
#-0.03, 1.4, 2.15, 1.97, 13.35, 2.08, 1.47, 7.52, 6.47, 1.95, 1.42, 1.9, 7.93, 0.43, \
#2.03, 5.4, 1.92, 3.17, 2.98, 0.38, 2.32, 1.82, 0.58, 1.98, 1.55, 1.8, 6.45, 2.03, \
#1.88, 10.88, 2.12, -0.62, 1.83, 4.8, 2.83, 5.88, 6.4, 3.48, 11.98, 1.93, 3.35, 2.87, \
#4.97, 3.3, 0.38, 4.7, 0.75, 4.78, 3.82, 0.03, 2.9, 2.98, 2.02, 3.57, 3.27, 1.4, 0.7, 4.47, 4.52, 0.38, 0.57, 1.78]

#define a funtion to calculate a interval upper_bound whose intergration of (lower_bound,upper_bound]
# is the largest among all the upper_bound whose intergration of (lower_bound,upper_bound)
# is no more than percentage_specified
def maximum_nomorethan_dichotomy(count, interval,lower_bound_specified,percentage_specified):
    lower_bound_ofinterval = numpy.min(interval)
    upper_bound_ofinterval = numpy.max(interval)
    totalnumber = numpy.sum(count)
    upper_bound_calculated = upper_bound_ofinterval
    if numpy.sum(count[lower_bound_specified-lower_bound_ofinterval:upper_bound_calculated-lower_bound_ofinterval])*1.0/totalnumber <= percentage_specified :
        return upper_bound_ofinterval
    else:
        lower = lower_bound_specified
        upper = upper_bound_ofinterval
        while upper - lower > 1:
            upper_bound_calculated = (lower + 1 + upper + 1)/2
#            print lower,upper_bound_calculated,upper
            if numpy.sum(count[lower_bound_specified-lower_bound_ofinterval:upper_bound_calculated-lower_bound_ofinterval])*1.0/totalnumber > percentage_specified:
                upper = upper_bound_calculated-1
            else:
                lower = upper_bound_calculated-1
        upper_bound_calculated = upper
        return upper_bound_calculated

#define a function to obtain all the interval whose lower bound is arithmetic sequence and their corresponding upper
#bound make them individually the largest among all interval whose lower bound is the same as them and the intergration
#of (lower_bound,upper_bound) is no more than percentage_specified
def maximum_nomorethan_getboundarray(count,interval,percentage_specified,first_lower_bound,first_upper_bound):
    bound = [[] for i in range(2)]
    bound[0].append(first_lower_bound)
    bound[1].append(first_upper_bound)
    lower_bound_ofinterval = numpy.min(interval)
    upper_bound_ofinterval = numpy.max(interval)
    totalnumber = numpy.sum(count)
    lower = first_lower_bound+1
    upper = first_upper_bound
    intervaltotal = numpy.sum(count[lower-lower_bound_ofinterval:upper-lower_bound_ofinterval])
    while numpy.sum(count[lower-lower_bound_ofinterval:upper_bound_ofinterval-lower_bound_ofinterval])*1.0/totalnumber > percentage_specified:
        while intervaltotal*1.0/totalnumber <= percentage_specified:
            upper = upper +1
            intervaltotal = intervaltotal + count[upper-lower_bound_ofinterval-1]
        intervaltotal = intervaltotal - count[upper-lower_bound_ofinterval-1]
        upper = upper -1
        bound[0].append(lower)
        bound[1].append(upper)
        intervaltotal = intervaltotal - count[lower-lower_bound_ofinterval]
        lower = lower+1
    for i in range(lower,upper_bound_ofinterval):
        bound[0].append(i)
        bound[1].append(upper_bound_ofinterval)
    return bound

#after getting the boundarray by the function(maximum_nomorethan_getboundarray) choose the most
#suitable one according to the following criterion：the range whose length in positive axle is
#longer than which in negative and negative part is existed and the intergration 
#of bound is the closest to the percentage_specified of the total area
def maximum_nomorethan_screenboundarray(bound,percentage_specified,count,interval):
    bound_select = []
    bound_select.append(bound[0][0])
    bound_select.append(bound[1][0])
    lower_bound_ofinterval = numpy.min(interval)
    if len(bound) == 1:
        return bound_select
    for i in range(1,len(bound)):
        if bound[0][i] >0:
            break
        if bound[1][i] + bound[0][i]>=0:
            if numpy.sum(count[bound[0][i]-lower_bound_ofinterval:bound[1][i]-lower_bound_ofinterval])\
                >= numpy.sum(count[bound_select[0]-lower_bound_ofinterval:bound_select[1]-lower_bound_ofinterval]):
                    bound_select[0] = bound[0][i]
                    bound_select[1] = bound[1][i]
    return bound_select

#define a funtion to calculate a interval upper_bound whose intergration of (lower_bound,upper_bound]
# is the smallest among all the upper_bound whose intergration of (lower_bound,upper_bound)
# is no less than percentage_specified
def minimum_nolessthan_dichotomy(count, interval,lower_bound_specified,percentage_specified):
    lower_bound_ofinterval = numpy.min(interval)
    upper_bound_ofinterval = numpy.max(interval)
    totalnumber = numpy.sum(count)
    upper_bound_calculated = upper_bound_ofinterval
    if numpy.sum(count[lower_bound_specified-lower_bound_ofinterval:upper_bound_calculated-lower_bound_ofinterval])*1.0/totalnumber <= percentage_specified :
        return upper_bound_ofinterval+1  #upper+1 exceed the range of interval,it means the uppper_bound_calculated  meeting the requirement is not existed
    else:
        lower = lower_bound_specified
        upper = upper_bound_ofinterval
        while upper - lower > 1:
            upper_bound_calculated = (lower + upper)/2
#            print lower,upper_bound_calculated,upper
            if numpy.sum(count[lower_bound_specified-lower_bound_ofinterval:upper_bound_calculated-lower_bound_ofinterval])*1.0/totalnumber < percentage_specified:
                lower = upper_bound_calculated
            else:
                upper = upper_bound_calculated
        upper_bound_calculated = upper
        return upper_bound_calculated

#define a function to obtain all the interval whose lower bound is arithmetic sequence and their corresponding upper
#bound make them individually the smallest among all interval whose lower bound is the same as them and the intergration
#of (lower_bound,upper_bound) is no less than percentage_specified
def minimum_nolessthan_getboundarray(count,interval,percentage_specified,first_lower_bound,first_upper_bound):
    bound = [[] for i in range(2)]
    bound[0].append(first_lower_bound)
    bound[1].append(first_upper_bound)
    lower_bound_ofinterval = numpy.min(interval)
    upper_bound_ofinterval = numpy.max(interval)
    totalnumber = numpy.sum(count)
    lower = first_lower_bound+1
    upper = first_upper_bound
    intervaltotal = numpy.sum(count[lower-lower_bound_ofinterval:upper-lower_bound_ofinterval])
    while numpy.sum(count[lower-lower_bound_ofinterval:upper_bound_ofinterval-lower_bound_ofinterval])*1.0/totalnumber >= percentage_specified:
#        if intervaltotal*1.0/totalnumber >= percentage_specified:
#            bound[0].append(lower)
#            bound[1].append(upper)
#            intervaltotal = intervaltotal - count[lower-lower_bound_ofinterval]
#            lower = lower + 1 
        while intervaltotal*1.0/totalnumber < percentage_specified:
            upper = upper +1
            intervaltotal = intervaltotal + count[upper-lower_bound_ofinterval-1]
        bound[0].append(lower)
        bound[1].append(upper)
        intervaltotal = intervaltotal - count[lower-lower_bound_ofinterval]
        lower = lower + 1 
    return bound

#after getting the boundarray by the function(minimum_nolessthan_getboundarray) choose the most
#suitable one according to the following criterion：the range whose length in positive axle is
#longer than which in negative and negative part is existed and the intergration 
#of bound is the closest to the percentage_specified of the total area
def minimum_nolessthan_screenboundarray(bound,percentage_specified,count,interval):
    bound_select = []
    bound_select.append(bound[0][0])
    bound_select.append(bound[1][0])
    lower_bound_ofinterval = numpy.min(interval)
    if len(bound) == 1:
        return bound_select
    for i in range(1,len(bound)):
        if bound[0][i] >0:
            break
        if bound[1][i] + bound[0][i]>=0:
            if numpy.sum(count[bound[0][i]-lower_bound_ofinterval:bound[1][i]-lower_bound_ofinterval])\
                <= numpy.sum(count[bound_select[0]-lower_bound_ofinterval:bound_select[1]-lower_bound_ofinterval]):
                    bound_select[0] = bound[0][i]
                    bound_select[1] = bound[1][i]
    return bound_select


#calculate the lowerbound and the upperbound of the figure which will be showed                        
upper_bound = int(math.ceil(numpy.max(ontimeperformance)))
lower_bound = int(math.floor(numpy.min(ontimeperformance)))
#obtain the x-axis coordinate range
x = range(lower_bound,upper_bound + 1)
#print lower_bound,upper_bound,x

#bins:x-axis coordinate range  n:y-axis coordinate value
n, bins, patches = plt.hist(ontimeperformance,bins = x, normed=0, facecolor='green', alpha=0.5)

print n,bins,patches
threshold_lower = 0
threshold_upper = 5
percentage_specified = 0.8
percentage = numpy.sum(n[threshold_lower-bins[0]:threshold_upper-bins[0]])*1.0/numpy.sum(n)


upper_bound_specified = minimum_nolessthan_dichotomy(n,bins,-1,percentage_specified)
bound = [[] for i in range(2)]
bound = minimum_nolessthan_getboundarray(n,bins,percentage_specified,-1,upper_bound_specified)
print bound[0]
print bound[1]
#bound_select is the most suitable range according to the user-specified criterion
bound_select = minimum_nolessthan_screenboundarray(bound,percentage_specified,n,bins)
print bound_select

#print upper_bound_specified
#upper_bound_specified = maximum_nomorethan_dichotomy(n,bins,-1,percentage_specified)
#bound = [[] for i in range(2)]
#bound = maximum_nomorethan_getboundarray(n,bins,percentage_specified,-1,upper_bound_specified)
#print bound[0]
#print bound[1]
#bound_select  =  maximum_nomorethan_screenboundarray(bound,percentage_specified,n,bins)
#print bound_select

#if the user-specified interval is between the lower_bound and the upper_bound ,it will be showed in the histogram
if threshold_lower >= lower_bound:
    plt.axvline(x = threshold_lower)
if threshold_upper <= upper_bound:
    plt.axvline(x = threshold_upper)

plt.text(threshold_lower,numpy.max(n),'%f'%percentage,horizontalalignment='center')
plt.xlabel('on-time performance')
plt.ylabel('count')
plt.show()
