# -*- coding: utf-8 -*-
"""

@author: sammav
"""

import matplotlib.pyplot as plt
import numpy as np


#Functions
def clearScreen():
 import os
 os.system("clear")
 os.system("reset -f")
 clearScreen()

def eq_fit(n,x,y,nv,N):
    s = "" #equation string
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
    

    RMS_error = (np.square(np.subtract(y,Y(x))).mean())**.5

    
    #string creation for Fluent
    #x[k]**n * p[0] + ... + x[k] * p[n-1] + p[n] = y[k]


    #first part
    s0 = "IF(VelocityMagnitude < " + str(x[0]) + " [m/s] , " + str(y[0]) + " [1/m] , "

    #second part   
    for i in range(0,N+1):
        s = " +VelocityMagnitude^" + str(N-i) + " * " + '{:.1f}'.format(coeff[i]) + " [m^" + str(-(N-i+1)) + "s^" + str((N-i)) + " ] " + s

    #third part    
    s_full = s0 + " IF(VelocityMagnitude > " + str(x[-1])  + " [m/s] , " + str(y[-1]) + " [1/m] , " + s + ") )"

    print("\nThe equation for ",n," =\n", s_full )
    print("\nRoot mean square Error = ", RMS_error)
    
    fig.subplots_adjust(hspace = 0.5)
    
    return RMS_error


if __name__ == '__main__':
    
    #data acquisition
    file = "dp.txt" #name of the file to be opened 
    fid = open(file,"r+")
    velocity = []
    dp = []

    #Data from file
    for line in fid:
        line = line.split("\t") #remove the commas
        velocity.append(float(line[0])) 
        dp.append(float(line[1]))
    fid.close()


    #Data
    Vel = np.asarray(velocity)
    DP  = np.asarray(dp)
    #fig, axs = plt.subplots(2,figsize=(10,10))
    fig, axs = plt.subplots(figsize=(10,5))


    #function call
    pol = 4
    RMS_error = 1
    while RMS_error > 0.05:
        RMS_error = eq_fit("Loss Coefficient", Vel, DP, 0, pol)
        pol += 1
    print(pol)
    
    plt.show()
