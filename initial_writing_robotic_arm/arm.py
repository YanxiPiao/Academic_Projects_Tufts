#!/usr/bin/env python
"""For this project, we are building a raspberry pi driven initial writing robotic arm
using two MG996R servos and a micro servo."""
from math import pi, cos, sin
import csv
import math
import matplotlib.pyplot as plt
import numpy as np


font=10 # [milimiter]
current_x=-100 # record the current pen position x
current_y=120 # record the current pen position y

list =[] # for coordinate lists
x_list=[] # import x axis data
y_list=[] # import y axis data
theta_list=[] # import angle data
pi = math.pi

# import data from csv file
def get_data(input):
    global x_list
    global y_list
    global theta_list
    with open('alphabets.csv') as f:
        reader=csv.DictReader(f)
        for row in reader:
            if row['char']==input:
                for k in range(0,len(row['x']),2):
                    x_list.append(int(row['x'][k]))
                    y_list.append(int(row['y'][k]))
                for k in range(0,len(row['theta']),2):
                    theta_list.append(int(row['theta'][k]))
    print('x_list is {0}, y_list is{1}, and theta_list is{2}.'.format(x_list, y_list, theta_list))

# returns list of coordinates
def path_straight(x,y):
    global list
    global current_x
    global current_y
    list=[]
    for i in range(0, len(x), 2):
        a = x[i] * font
        b = y[i] * font
        print(a,'',b)
        dist = math.sqrt(math.pow((x[i] - x[i + 1]), 2) + math.pow((y[i] - y[i + 1]), 2))
        intervals_x = (x[i + 1] - x[i]) / (dist * font)
        intervals_y = (y[i + 1] - y[i]) / (dist * font)
        for k in range(int(dist * font)):
            a += intervals_x * font
            b += intervals_y * font
            list.append((current_x-a, current_y-b))
        print(list)
        list = []
        print('next line')
        # pen up and move to first coor in list
        # pen down
        # draw using IK from list
        # pen up

def path_curve(theta):
    global list
    global current_x
    global current_y
    list=[]
    for i in range(0, len(theta),5):
        if theta_list[i+3]>=4:
            degrees_travel = (abs(theta_list[i + 3] - 8) + abs(theta_list[i + 4] - 0)) * pi / 4 * 180 / pi
        elif theta_list[i + 3]-theta_list[i + 4]==0:
            degrees_travel=360
        else:
            degrees_travel=abs(theta_list[i+3] - theta_list[i+4])
        number_of_travel=int(degrees_travel/font)
        increment=font*pi/180 # increase by font degrees each time
        radius=theta[i]*font

        center_x=current_x-theta[i+1]*font
        center_y=current_y-theta[i+2]*font

        print('radius',radius,'center',center_x,center_y)
        a =theta[i+3]*pi/4
        print(number_of_travel)
        for k in range(number_of_travel):
            list.append(curve(center_x, center_y, radius, a))
            a += increment
        print(list)
        list=[]
        print('next line')
        # pen up and move to first coor in list
        # pen down
        # draw using IK from list
        # pen up

# move to the next character
def next_character():
    global current_x
    global current_y
    current_x+=font*5
    # move pen to (current_x,current_y)

# calculate circumference of a circle
def curve(x, y, r, theta):
    return x + cos(theta) * r, y + sin(theta) * r


input='c'
for char in input:
    get_data(char) # import x_list, y_list, and theta_list
    path_straight(x_list,y_list)
    path_curve(theta_list)
    next_character()
    x_list=[]
    y_list=[]
    theta_list=[]


newx=-134.14213562373095,-131.47152872702094,-128.452365234814, -125.17638090205043,-121.74311485495318,-118.25688514504687,-114.82361909794962,-111.54763476518605,-108.5284712729791,-105.85786437626908,-103.61695911422018,-101.87384425926702,-100.68148347421865, -100.0761060381651,-100.07610603816508,-100.68148347421862,-101.87384425926697,-103.61695911422012,-105.85786437626899,-108.528471272979,-111.54763476518593,-114.8236190979495,-118.25688514504674,-121.74311485495306,-125.17638090205034,-128.4523652348139,-131.47152872702085
newy=65.85786437626905, 63.616959114220165, 61.873844259267, 60.68148347421864, 60.07610603816509, 60.076106038165086, 60.68148347421862, 61.87384425926699, 63.616959114220144, 65.85786437626902, 68.52847127297905, 71.54763476518596, 74.82361909794953, 78.25688514504678, 81.7431148549531, 85.17638090205035, 88.45236523481393, 91.47152872702087, 94.1421356237309, 96.38304088577979, 98.12615574073297, 99.31851652578135, 99.9238939618349, 99.92389396183492, 99.31851652578139, 98.12615574073304, 96.38304088577989
plt.scatter(newx,newy)
plt.show()