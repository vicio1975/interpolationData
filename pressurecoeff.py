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

def eq_fit(n, x, y, nv, N):
    #equation string
    s = ""
    results = {}
    coeff = np.polyfit(x, y, N)
    Y = np.poly1d(coeff)
    correlation = np.corrcoef(x, y)[0,1]
     # r
    results['correlation'] = correlation
     # r-squared
    results['determination'] = correlation**2

    #string creation for Fluent
    #x[k]**n * p[0] + ... + x[k] * p[n-1] + p[n] = y[k]

    for i in range(0, N+1):
        s = " +VelocityMagnitude^" + str(N-i) + " * " + '{:.6f}'.format(coeff[i]) + " [m^" + str(-(N-i+1)) + " s^" + str((N-i)) + " ] " + s
        
    print("\nR, R^2 = ", results)
    
    axs.plot(x,Y(x),"ob")
    axs.plot(x,y,"--r")
    plt.xlabel("V, m/s")
    plt.ylabel("Pressure Coeff Loss, 1/m")

    return s

def porous_set():
    """
This function is to set the porous media
"""
    #Porous escription
    print("\n\nPlease add three points coorditanes for Porous media orientation...")
    print("...Point P1")
    P1 = [float(input("x1 (mm) = ")), float(input("y1 (mm)  = ")), float(input("z1 (mm) = ") ) ]
    print("...Point P2")
    P2 = [float(input("x2 (mm)  = ")), float(input("y2 (mm) = ")), float(input("z2 (mm) = ") ) ]
    print("...Point P3")
    P3 = [float(input("x3 (mm)  = ")), float(input("y3 (mm)  = ")), float(input("z3 (mm) = ") ) ]

    print("\nPlease define the Porous media volumes...")
    fluid_vol = float(input("Fluid Volume (mm³) = "))
    solid_vol = float(input("Solid Volume (mm³) = "))


    v2_1 = [P2[0]-P1[0], P2[1]-P1[1] , P2[2]-P1[2]]
    v3_1 = [P3[0]-P1[0], P3[1]-P1[1] , P3[2]-P1[2]]
    mag2_1 = (v2_1[0]**2 + v2_1[1]**2 +v2_1[2]**2)**0.5
    mag3_1 = (v3_1[0]**2 + v3_1[1]**2 +v3_1[2]**2)**0.5    

    dir1 = [v2_1[0]/mag2_1, v2_1[1]/mag2_1, v2_1[2]/mag2_1]
    dir2 = [v3_1[0]/mag3_1, v3_1[1]/mag3_1, v3_1[2]/mag3_1]
    
    tot_vol =     fluid_vol + solid_vol
    porosity = fluid_vol/tot_vol 

    print("\ndirection 1 = ", dir1, "\ndirection 2 = ", dir2, "\nporosity = ", porosity)

    return dir1, dir2, porosity

def journal(named_function, porous_details, res):
    """
This is to write a journal file

"""
    d1 = porous_details[0]
    d2 = porous_details[1]
    porosity = porous_details[2]
    
    file_jou = "dp.jou"
    fid2 = open(file_jou,"w+")
    j1 = "/define/named-expressions add dp_loss_coeff definition"
    j2 = " desc dp_loss_coeff q "
    journal1 = "\n;;;Create named expression 'dp_loss_coeff' = pressure loss coeff equation = (dp/0.5*rho*v2*L)\n"
    journal1 =  journal1 + j1 + ' " '+ named_function + ' " ' + j2
    fid2.write(journal1)
    
    journal2 = "\n;;;Set porous media params on the porous zone named 'porous'\n"
    journal2 = journal2  +  "/define/boundary-conditions/set/fluid porous* ()\nporous y\ndirection-1-x n {} direction-1-y n {} direction-1-z n {}\ndirection-2-x n {} direction-2-y n {} direction-2-z n {}"
    journal2 .format(d1[0], d1[1], d1[2], d2[0], d2[1], d2[2])
    
    journal2 = journal2  + "\nporous-r-1 n 1.0 porous-r-2 n 1.0 porous-r-3 n 1.0"
    journal2 = journal2 + "\nporous-c-1 n " + '"dp_loss_coeff "'+ " porous-c-2 n {} porous-c-3 n {}".format(res, res)
    journal2 = journal2 + "\nalt-inertial-form y\nporosity n {}".format(porosity)+"\nsources n\nq"
    
    fid2.write(journal2)
    fid2.close()
    print("\n\n The journal file for the porous setting is written in the same folder of the input file")
    input("anykeys to shut the app!")

if __name__ == '__main__':
    n = "Loss Coefficient"
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
    res = DP[0]*100
    fig, axs = plt.subplots(figsize=(10,5))

    #function call
    pol = 2
    s1  = eq_fit(n, Vel[0:3], DP[0:3], 0, pol)
    s2  = eq_fit(n, Vel[2:6], DP[2:6], 0, pol)
    s3  = eq_fit(n, Vel[5:-1], DP[5:-1], 0, pol)
    s4  = eq_fit(n, Vel[-2:], DP[-2:], 0, 1)
    
    s_1 = "IF(VelocityMagnitude < " + str(Vel[0])  + " [m s^-1] , " + str(DP[0]*10) + " [m^-1] , "
    s_2 = " IF(AND(VelocityMagnitude >= " + str(Vel[0])  + " [m s^-1] , VelocityMagnitude < " + str(Vel[3])  + " [m s^-1]) , " + s1
    s_3 = ", IF(AND(VelocityMagnitude >= " + str(Vel[3])  + " [m s^-1] , VelocityMagnitude < " + str(Vel[6])  + " [m s^-1]) , " + s2
    s_4 = ", IF(AND(VelocityMagnitude >= " + str(Vel[6])  + " [m s^-1] , VelocityMagnitude < " + str(Vel[-2]) + " [m s^-1]) , " + s3
    s_5 = " , " +s4 + ")))"
    named_function = s_1 + s_2 + s_3 + s_4 + s_5

    print("\nThe equation for ",n," =\n", named_function)

    journal(named_function, porous_set(), res)
        
    plt.show()
