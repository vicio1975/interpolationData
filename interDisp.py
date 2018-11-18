# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 11:53:08 2018

@author: bmusammartanoV
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def clearScreen():
 import os
 os.system("clear")
 os.system("reset -f")
clearScreen()

#data acquisition
file = "int.csv" #name of the file to be opened 
fid = open(file,"r+")
disp = []
lh = []
rh = []
disp_n = []
next(fid) #skip the header file
for line in fid:
    line = line.split(",") #remove the commas
    disp.append(float(line[0])) #displacements
    lh.append(float(line[1]))   #left hand steering angle
    rh.append(float(line[2]))   #right hand steering angle
    disp_n.append(float(line[3])) #new displacements   
fid.close()

#Data
Disp = np.asarray(disp) #displacements
disp_n = np.asarray(disp_n) #new displacements
Lh = np.asarray(lh)     #left hand steering angle
Rh = np.asarray(rh)     #right hand steering angle
Disp_n = np.asarray([i for i in disp_n if (i < 999) and (i < max(Disp) and i> min(Disp)) ])

#Interpolation functions
fl = interp1d(Disp, Lh, kind='cubic') # interpolation of disp. - left hand steering angle
fr = interp1d(Disp, Rh, kind='cubic') # interpolation of disp. - right hand steering angle

#New steering angles
LhN = fl(Disp_n) #new l. hand steering angles
RhN = fr(Disp_n) #new R. hand steering angles
#############

####plot
fig1 = plt.figure("figure 1")
ax1 = fig1.add_axes()
plt.plot(Disp,Lh,"o")
plt.plot(Disp,Rh,"o")

plt.plot(Disp_n,LhN,"o")
plt.plot(Disp_n,RhN,"o")

#plt.xlabel('X')
#plt.ylabel('Y')
#plt.interpolation('Histogram of IQ')

