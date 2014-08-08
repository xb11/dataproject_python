#! /usr/bin/env python
#coding=utf-8
#this program is trying to import the park and ride database and calculate the park-and-ride
#occupancies of each public park and paint the histogram of one sample park

import numpy
import math
import pylab
import matplotlib.pyplot as plt
import xlrd

#input database by xlrd
book = xlrd.open_workbook("Park and Ride Database.xlsx")
#print "The number of worksheets is", book.nsheets
#print "Worksheet name(s):", book.sheet_names()
sh = book.sheet_by_index(0)

#print sh.name, sh.nrows, sh.ncols
#print "Cell D30 is", sh.cell_value(rowx=29, colx=3)
#for rx in range(sh.nrows):
#    print sh.row(rx)
PAR_occupancy = []
capacity = []
public_name = []
for i in range(1,sh.nrows):
    capacity.append(sh.cell(i,1).value)
#print capacity
#we choose the public park--ALPINE VILLAGE as a example
#if there is no value in one cell of excel, we will get output as empty string 
for i in range(2,sh.ncols):
    if sh.cell(1,i).value == '':
        continue
    PAR_occupancy.append(sh.cell(1,i).value/capacity[0])


#get the data calculated from the database and put them into histogram
#PAR_occupancy=[1.073469388,1,1.044897959,1.073469388,1.126530612,0.983673469,1.151020408,1.085714286,1.085714286,1.044897959,1.126530612,1.089795918,1.073469388,1.093877551,1.044897959,1.048979592,1.036734694,1.028571429,1.081632653,1.089795918,1.12244898,1.106122449,1.093877551]
upper_bound = math.ceil(numpy.max(PAR_occupancy)*100)
lower_bound = math.floor(numpy.min(PAR_occupancy)*100)
x = numpy.arange(lower_bound/100,(upper_bound+1)/100,0.01)

n, bins, patches = plt.hist(PAR_occupancy,bins = x, normed=0, facecolor='green', alpha=0.5)
threshold_lower = 1.00
threshold_upper = 1.05
print n
percentage = numpy.sum(n[int((threshold_lower-bins[0])*100):int((threshold_upper-bins[0])*100)])*1.0/numpy.sum(n)
#if the user-specified interval is between the lower_bound and the upper_bound ,it will be showed in the histogram
if threshold_lower >= lower_bound/100:
    plt.axvline(x = threshold_lower)
    
if threshold_upper <= (upper_bound+1)/100:
    plt.axvline(x = threshold_upper)

plt.text(threshold_lower,numpy.max(n),'%f'%percentage,horizontalalignment='center')
plt.xlabel('park and ride occupancy of %s'%(sh.cell(1,0).value))
plt.ylabel('count')
plt.show()

cnx.close()
