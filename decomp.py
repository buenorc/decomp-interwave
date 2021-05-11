# -*- coding: utf-8 -*-
"""
Created on Sun Mar 21 18:15:49 2021

Decomposition module to read data from Interwave Analyzer and horizontal 
velocity measurements, and find the velocity profile at each time step
associated to the first 5 vertical internal seiche mode. 

@author: Rafael de Carvalho Bueno
"""

import numpy as np 

def resolution(dt_model, dt):
    
    if dt_model < dt:
        dt_model = dt 

    else:
        if ((dt_model)%(dt)!=0):
            dt_model = int(dt *round(float(dt_model)/(dt))) + dt
                         
    return int(dt_model/dt)

def wp_function(umea, h, hmod, dz, N):

    Nu  = len(umea)

    wp1 = np.zeros((N),float)
    wp  = np.zeros((N),float)

    
    # Calculate the horizontal velocities using the refined grid
    u = np.zeros((N),float)
    
    i = 0
    z = hmod[0]

    for j in range(Nu-1):            # vary for all measured data points 

        while z < h[j]:              # calculate the velocity in a refined grid
            u[i] = umea[j]          # vel from cm/s to m/s

            i = i + 1
            z = z + dz  
                   
    while z <= h[-1]:
        u[i] = umea[-2]
        i = i + 1
        z = z + dz
  
    for i in range(1,N):
        wp1[i] = u[i] + wp1[i-1]
    
    for i in range(N):
        wp[i] = wp1[i] - wp1[-1]*i/(N-1)    
        
    return wp

#  Input data:
#
#  umea: horizontal water velocity in the direction of the wave propagation (m/s)*
#  h   : meters above bed - refined grid (IWA output) 
#  hmea: meters above bed - original grid (IWA output)       
#  t   : time vector (IWA output)
#
#
#  Input variables:
#
#  N   : number of cells in the vertical direction (according to the model coupled with IWA)
#  dt  : temporal resolution of velocity data
#  dt_model : temporal resolution specified in the IWA (for the decomposition model)
#
#  Output results:
#  
#  Uvel_mode: velocity associated to each baroclininc mode [mode,t,z] in m/s 
#  Uvel: velocity associated to all baroclininc modes [t,z] in m/s 
#
#  *   umea does not need to be in the same tempral resolution than the IWA outputs
#

ut = []
cp = []

# 
umea = np.loadtxt('input-velocity/velocity-y.csv')   
umea = np.flip(np.insert(umea, 0, -9999, axis=1),axis=1)

h    = np.loadtxt('outputs-interwave/mab_decomp.txt',skiprows=1)
t    = np.loadtxt('outputs-interwave/time_decomp.txt',skiprows=1)
hmea = np.loadtxt('outputs-interwave/mab_decomp_oiginal.txt')

N         = 100   # number of cells in vertical dir (fixed) 
dt        = 1     # minutes (temporal resolution of the measured data)
dt_model  = 30    # minutes (same dt used to run the decomposition model in the interwave analyzer)

dz        = h[0] - h[1]

Nt = len(t)
Cp = np.zeros((5,Nt),float)

skipt = resolution(dt_model, dt)

imod  = 0
itm   = 0

wp    = []

hsurf = h[0] - h

umea_it = []
for it in range(len(umea[:,0])):
    
    if imod == 0 or imod == 1: 

        hsurf_ori = h[0] - hmea[:,itm]
        umea_it.append(umea[it])
        wp.append(wp_function(umea[it,:],hsurf_ori,hsurf,dz,N))   
        
        imod  = skipt 
        itm = itm + 1
        
    else:
        imod  = imod - 1

umea_it   = np.array(umea_it)
Uvel      = np.zeros((len(wp),N-1),float)
Uvel_mode = np.zeros((5,len(wp),N-1),float)
             
for m in range(5):
    ut.append(np.loadtxt('outputs-interwave/uarbit_decomp_mode'+str(m+1)+'.txt'))
    cp.append(np.loadtxt('outputs-interwave/cpzinho_mode'+str(m+1)+'.txt'))
    
    for it in range(Nt):
    
        Cp = sum(wp[it][:]*cp[m][:,it])
        Uvel_mode[m,it,:] = Cp*ut[m][:,it]
    
for it in range(Nt):
    Uvel[it,:] = np.sum(Uvel_mode[:,it,:],axis=0)



