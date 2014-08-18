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
host = ""
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
def calculate_crowding_maximum(startyear,startmonth,endyear,endmonth,starttime,endtime,stopA,QstopA,stopB,QstopB,route):
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
def calculate_crowding_mileaverage(startyear,startmonth,endyear,endmonth,starttime,endtime,stopA,QstopA,stopB,QstopB,route):
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
    Dcrowd = row[0]*1.0/row[1]*row[5]
    DLMILES = row[5]
    results = cursor.fetchall()
    count = 0
    j = 0
    for row in results:
        if row[3] == daymoyr:
            if row[4] == TRIPA:
                count = count+1
                Dcrowd = row[0]*1.0/row[1]*row[5]+Dcrowd 
                DLMILES = DLMILES + row[5]                   
            else:
                if count == stopB - stopA:
                    crowding[j].append(Dcrowd/DLMILES)
                if row[6] == QstopA:
                    TRIPA = row[4]
                    Dcrowd = row[0]*1.0/row[1]*row[5]
                    DLMILES = row[5]
                count = 0
        else:
            if count == stopB - stopA:
                crowding[j].append(Dcrowd/DLMILES)
            if row[6] == QstopA:
                j = j+1
                daymoyr = row[3]
                TRIPA = row[4]
                Dcrowd = row[0]*1.0/row[1]*row[5]
                DLMILES = row[5]                
            count = 0
#    if j+1 < number:
#        for i in range(j+1,number):
#            del crowding[i]
    print j+1
    return crowding


#crowd_1 = calculate_crowding_maximum(startyear,startmonth,endyear,endmonth,starttime,endtime,stopA,QstopA,stopB,QstopB,route)
#crowd_2 = calculate_crowding_mileaverage(startyear,startmonth,endyear,endmonth,starttime,endtime,stopA,QstopA,stopB,QstopB,route)
#print crowd_1
#print crowd_2
crowd_1 = [[0.5833333333333334, 0.4594594594594595, 0.5, 1.054054054054054, 0.03333333333333333, 0.4, 0.016666666666666666, 0.02702702702702703, 0.32432432432432434], [0.0, 0.95, 0.4, 0.6486486486486487, 1.3243243243243243, 0.05, 0.03333333333333333, 0.0, 0.2702702702702703, 0.6216216216216216], [0.0, 0.21666666666666667, 0.65, 0.18333333333333332, 0.6756756756756757, 0.0, 0.016666666666666666, 0.24324324324324326], [0.016666666666666666, 0.6166666666666667, 0.08108108108108109, 0.016666666666666666, 0.4864864864864865, 0.03333333333333333, 0.03333333333333333, 0.05, 0.918918918918919], [0.2, 0.425, 0.45, 0.05, 0.02702702702702703, 0.2, 0.02702702702702703, 0.26666666666666666], [0.016666666666666666, 0.38333333333333336, 1.2162162162162162, 0.2833333333333333, 0.5833333333333334, 1.5945945945945945, 0.24324324324324326, 0.18333333333333332, 0.4864864864864865], [0.0, 0.8833333333333333, 0.25, 1.027027027027027, 0.1891891891891892, 0.36666666666666664, 0.03333333333333333, 0.3333333333333333, 0.225], [0.03333333333333333, 0.21666666666666667, 0.6833333333333333, 0.03333333333333333, 0.3333333333333333, 0.7166666666666667, 0.016666666666666666, 0.25], [0.016666666666666666, 0.3333333333333333, 0.8, 0.4166666666666667, 0.5, 0.10810810810810811, 0.1, 0.55, 0.6486486486486487, 0.38333333333333336, 0.02702702702702703, 0.4594594594594595], [0.0, 0.18333333333333332, 0.4666666666666667, 0.2, 0.6166666666666667, 0.2702702702702703, 0.5333333333333333, 0.0, 0.05405405405405406, 0.25, 0.325], [0.0, 0.36666666666666664, 0.7333333333333333, 1.9189189189189189, 1.0, 0.1], [0.0, 0.18333333333333332, 0.9, 1.135135135135135, 0.0, 1.3513513513513513, 0.6333333333333333, 0.0, 0.35135135135135137, 0.625], [0.0, 0.7333333333333333, 0.36666666666666664, 0.35135135135135137, 0.2972972972972973, 0.0, 0.35, 0.21621621621621623, 0.625], [0.0, 0.3, 0.35, 0.5135135135135135, 0.016666666666666666, 0.6216216216216216], [0.0, 0.3, 0.48333333333333334, 0.43333333333333335, 0.0, 0.016666666666666666, 0.05, 0.0, 0.26666666666666666], [0.0, 0.31666666666666665, 0.45, 0.23333333333333334, 0.05405405405405406, 0.425, 0.6166666666666667, 0.1, 0.925, 0.025, 0.0], [0.25, 0.45, 0.4, 0.2702702702702703, 0.06666666666666667, 0.16666666666666666, 0.0], [0.26666666666666666, 0.05], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
crowd_2 = [[0.5610544217687076, 0.4594594594594595, 0.5, 1.0080802451936473, 0.026934523809523814, 0.3862654320987654, 0.0016819571865443425, 0.011466011466011467, 0.3243243243243244], [0.0, 0.9264525993883792, 0.39812925170068025, 0.6373414230557087, 1.265254945667317, 0.05, 0.018877551020408164, 0.0, 0.2588464753413207, 0.5907335907335908], [0.0, 0.21666666666666665, 0.644954128440367, 0.17854938271604937, 0.6398080323313968, 0.0, 0.008075601374570446, 0.24324324324324326], [0.005154639175257732, 0.611111111111111, 0.02238602238602239, 0.016666666666666666, 0.475020475020475, 0.03149847094801223, 0.014646464646464647, 0.05, 0.8908908908908909], [0.2, 0.39311224489795915, 0.45000000000000007, 0.02346938775510204, 0.02421171171171171, 0.2, 0.02702702702702703, 0.26666666666666666], [0.0147766323024055, 0.3833333333333333, 1.1967121760936195, 0.2639455782312925, 0.5766323024054983, 1.550468836183122, 0.19691119691119693, 0.18333333333333332, 0.4507810562856434], [0.0, 0.8737003058103976, 0.2403780068728522, 1.0156032320980775, 0.1891891891891892, 0.3554982817869416, 0.015757575757575755, 0.3333333333333333, 0.22500000000000003], [0.03333333333333333, 0.21666666666666667, 0.6796969696969697, 0.02638888888888889, 0.32176870748299324, 0.7129251700680272, 0.016666666666666666, 0.23470790378006876], [0.016666666666666666, 0.3280612244897959, 0.793577981651376, 0.4166666666666667, 0.5, 0.0885885885885886, 0.08090277777777778, 0.5419003115264797, 0.6486486486486488, 0.3753822629969419, 0.011423794928949568, 0.4518817883303865], [0.0, 0.18333333333333332, 0.4437694704049844, 0.2, 0.61343537414966, 0.2702702702702703, 0.5281786941580756, 0.0, 0.013923013923013924, 0.24217687074829933, 0.32500000000000007], [0.0, 0.35635738831615116, 0.7138047138047139, 1.8776412776412774, 0.9969350794093061, 0.08776758409785933], [0.0, 0.17628865979381442, 0.882828282828283, 1.1276276276276276, 0.0, 1.2764127764127764, 0.6204545454545454, 0.0, 0.32306137913614547, 0.6249999999999999], [0.0, 0.7262626262626263, 0.35945017182130584, 0.35135135135135137, 0.2972972972972973, 0.0, 0.32306397306397305, 0.1401504597380886, 0.6067129629629628], [0.0, 0.292354740061162, 0.33639455782312927, 0.502089718584564, 0.004672897196261682, 0.5987740317637225], [0.0, 0.29999999999999993, 0.47628865979381446, 0.4333333333333334, 0.0, 0.016666666666666666, 0.030709876543209877, 0.0, 0.26666666666666666], [0.0, 0.3166666666666667, 0.4398625429553265, 0.23161512027491404, 0.022932022932022934, 0.4143939393939394, 0.6110091743119266, 0.1, 0.8851010101010102, 0.025, 0.0], [0.25, 0.45, 0.3857638888888889, 0.2702702702702703, 0.047474747474747475, 0.16666666666666666, 0.0], [0.2575163398692811, 0.028458049886621317], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
crowd_1_perday = []
crowd_1_pertrip = []
crowd_2_perday = []
crowd_2_pertrip = []

for i in range(len(crowd_1)):
    if len(crowd_1[i]) >0:
        crowd_1_perday.append(numpy.mean(crowd_1[i]))

for i in range(len(crowd_1)):
    if len(crowd_1[i]) >0:
        crowd_1_pertrip.extend(crowd_1[i])

for i in range(len(crowd_2)):
    if len(crowd_2[i]) >0:
        crowd_2_perday.append(numpy.mean(crowd_2[i]))

for i in range(len(crowd_2)):
    if len(crowd_2[i]) >0:
        crowd_2_pertrip.extend(crowd_2[i])

fig = plt.figure()
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

upper_bound1_perday = math.ceil(numpy.max(crowd_1_perday)*10)
lower_bound1_perday = math.floor(numpy.min(crowd_1_perday)*10)
x1 = numpy.arange(lower_bound1_perday/10,(upper_bound1_perday+0.5)/10,0.05)

upper_bound1_pertrip = math.ceil(numpy.max(crowd_1_pertrip)*10)
lower_bound1_pertrip = math.floor(numpy.min(crowd_1_pertrip)*10)
x2 = numpy.arange(lower_bound1_pertrip/10,(upper_bound1_pertrip+0.5)/10,0.05)

upper_bound2_perday = math.ceil(numpy.max(crowd_2_perday)*10)
lower_bound2_perday = math.floor(numpy.min(crowd_2_perday)*10)
x3 = numpy.arange(lower_bound2_perday/10,(upper_bound2_perday+0.5)/10,0.05)

upper_bound2_pertrip = math.ceil(numpy.max(crowd_2_pertrip)*10)
lower_bound2_pertrip = math.floor(numpy.min(crowd_2_pertrip)*10)
x4 = numpy.arange(lower_bound2_pertrip/10,(upper_bound2_pertrip+0.5)/10,0.05)

n1, bins1, patches1 = ax1.hist(crowd_1_perday,bins = x1, normed=0, facecolor='green', alpha=0.5)
n2, bins2, patches2 = ax2.hist(crowd_1_pertrip,bins = x2, normed=0, facecolor='blue', alpha=0.5)
n3, bins3, patches3 = ax3.hist(crowd_2_perday,bins = x3, normed=0, facecolor='green', alpha=0.5)
n4, bins4, patches4 = ax4.hist(crowd_2_pertrip,bins = x4, normed=0, facecolor='blue', alpha=0.5)

threshold_lower = 0.2
threshold_upper = 0.4
#print n
percentage = numpy.sum(n1[int((threshold_lower-bins1[0])*20):int((threshold_upper-bins1[0])*20)])*1.0/numpy.sum(n1)

ax1.axvline(x = threshold_lower)
ax1.axvline(x = threshold_upper)
ax1.text(threshold_lower,threshold_upper,'%f'%percentage,horizontalalignment='center')

#set the label of each plot
ax1.set_xlabel('crowding_maximum_perday')
ax1.set_ylabel('count')
ax2.set_xlabel('crowding_maximum_pertrip')
ax2.set_ylabel('count')
ax3.set_xlabel('crowding_milesaverage_perday')
ax3.set_ylabel('count')
ax4.set_xlabel('crowding_milesaverage_pertrip')
ax4.set_ylabel('count')

plt.show()

cnx.close()

