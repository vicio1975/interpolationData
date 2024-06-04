# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 11:53:08 2018

@author: bmusammartanoV
"""

import matplotlib.pyplot as plt
import numpy as np


#Functions
def clearScreen():
 import os
 os.system("clear")
 os.system("reset -f")
 clearScreen()

def eq_fit(n,x,y,nv):
    s = "" #equation string
    N = 6
    coeff = np.polyfit(x, y, N)
    Y = np.poly1d(coeff)

##    axs[nv].plot(x,Y(x),"ob")
##    axs[nv].plot(x,y,"--r")
##    axs[nv].set_title(n)
    axs.set_title(n)
    axs.plot(x,Y(x),"ob")
    axs.plot(x,y,"--r")
    axs.set_title(n)
    plt.xlabel("Velocity, m/s")
    plt.ylabel("Loss Coeff, 1/m")
    
    RMS_error = np.sqrt(np.mean(np.square(np.subtract(y,Y(x)))))

    #x[k]**n * p[0] + ... + x[k] * p[n-1] + p[n] = y[k]
    
    s0 = "IF(VelocityMagnitude < " + str(x[0]) + " [m/s] , " + str(y[0]) + " [1/m] ,"
    for i in range(0,N+1):
        s="+VelocityMagnitude^"+str(N-i)+ "*" + str(coeff[i])+" [m^"+str(-(N-i+1))+"s^"+str((N-i))+"]"+s

    s_full = s0 + s + " , " + "IF(VelocityMagnitude > " + str(x[-1])  + " [m/s] , " + str(y[-1]) + " [1/m]  ))"
 
    print("\nThe equation for ",n," =\n", s_full )
    print("\nRoot mean square Error = ", RMS_error)
    fig.subplots_adjust(hspace=0.5) 
    return s, RMS_error


#data acquisition
file = "dp.txt" #name of the file to be opened 
fid = open(file,"r+")
velocity = []
dp = []

#Data from file
next(fid) #skip the header file
for line in fid:
    line = line.split("\t") #remove the commas
    velocity.append(float(line[0])) 
    dp.append(float(line[1]))
fid.close()

#Data
Vel = np.asarray(velocity)
DP  = np.asarray(dp)
#fig, axs = plt.subplots(2,figsize=(10,10))
fig, axs = plt.subplots()

if __name__ == '__main__':
    eq_fit("Loss Coefficient",Vel, DP,0)
    
    plt.show()
