#! /usr/bin/env python
#coding=utf-8
import mysql.connector
import numpy
import matplotlib.pyplot as plt
from mysql.connector import errorcode
#Try to test if the connection is done

user_id = "root"
password = "1234"
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
        
startmonth = 10
endmonth = 10
starttime = 7
endtime = 9
stopA = 2
stopB = 5
route = 1



def calculate_crowding(startmonth,endmonth,starttime,endtime,stopA,stopB,route):
    sql = "SELECT `LOAD_NUM`,`capacity`,`STOPA` FROM `dataproject`.`transit` \
    WHERE %d<=HR AND HR<=%d AND '2013-%d-01'<=daymoyr AND daymoyr<='2013-%d-31'\
     AND ROUTE = %d AND %d < STOPA AND STOPA <= %d"\
    % (starttime,endtime,startmonth,endmonth,route,stopA,stopB)

    cursor.execute(sql)
    results = cursor.fetchall()
    number = stopB - stopA
    crowding = [[] for i in range(number)]
    for row in results:
        crowding[row[2]-stopA-1].append(row[0]/30.0/row[1])
    return crowding

crowd = calculate_crowding(10,10,7,9,stopA,stopB,1)

StopMeans   = []

for i in range(stopA + 1, stopB+1):
    StopMeans.append(numpy.mean(crowd[i-stopA-1]))
    print "from stop %d to %d, the crowding is %f "%(i-1,i,StopMeans[i-stopA -1])

#StopMeans = [0.174056,0.153506,0.164026]
N = stopB - stopA
max = numpy.max(StopMeans)
#print max
#print numpy.arange(0,max*1.33,max/6.0)
#ticks = ['stop3','stop4','stop5']
ticks = []
for i in range(stopA + 1, stopB+1):
    ticks.append('stop%d'%i)

ind = numpy.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars: can also be len(x) sequence

p1 = plt.bar(ind, StopMeans,   width, color='r')


plt.ylabel('crowding')
plt.title('crowding between stop')
plt.xticks(ind+width/2., ticks )
plt.yticks(numpy.arange(0,max*1.33,max/6.0))
#plt.legend( (p1[0]), ('Crowding'),loc = 2)

plt.show()



#sql = """select * FROM `dataproject`.`transit` limit 200"""
#cursor.execute(sql)
##print cursor.fetchone()
#results = cursor.fetchall()
#print results[0]

cnx.close()

