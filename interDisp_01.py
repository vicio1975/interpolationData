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
    N = 14
    coeff = np.polyfit(x, y, N)
    Y = np.poly1d(coeff)

    axs[nv].plot(x,Y(x),"ob")
    axs[nv].plot(x,y,"--r")
    axs[nv].set_title(n)
    RMS_error = np.sqrt(np.mean(np.square(np.subtract(y,Y(x)))))

    #x[k]**n * p[0] + ... + x[k] * p[n-1] + p[n] = y[k]
    

    for i in range(0,N+1):
        s="+X^"+str(N-i)+ "*" + str(coeff[i])+s
    print("\nThe equation for ",n," =\n",s)
    print("\nRoot mean square Error = ", RMS_error)
    fig.subplots_adjust(hspace=0.5) 
    return s, RMS_error


#data acquisition
file = "foam.dat" #name of the file to be opened 
fid = open(file,"r+")
time = []
density = []
viscosity = []

#Data from file
next(fid) #skip the header file
for line in fid:
    line = line.split("\t") #remove the commas
    time.append(float(line[0])) #time
    density.append(float(line[1]))   #density
    viscosity.append(float(line[2])) #viscosity
fid.close()

#Data
Time = np.asarray(time)
Density = np.asarray(density)
Viscosity = np.asarray(viscosity)
fig, axs = plt.subplots(2,figsize=(10,10))

if __name__ == '__main__':
    eq_fit("Density",Time, Density,0)
    eq_fit("Viscosity",Time, Viscosity,1)
    
    plt.show()
    
# ######## way 1
# #Interpolation functions
# f1 = interp1d(Time, Density, kind='cubic')

# Y = interpolate.CubicSpline(Time, Density, bc_type='natural')
# X1 = np.min(Time)
# Y1 = Y(X1)

#https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html