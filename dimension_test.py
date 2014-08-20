#! /usr/bin/env python
#coding=utf-8
A = [[2,3,4],[5,6,7]]
# calculate the dimension of list A
x = A
dimension = 0
while type(x) != type(1):
    x = x[0]
    dimension = dimension + 1
print dimension

out = open('1.txt',"r")
for row in out.readlines():
    print row
    print type(row)
    
#out.write(([' '+(map(str, i)) for i in A]))

#a = numpy.array(A)
#print a
#print a.shape
