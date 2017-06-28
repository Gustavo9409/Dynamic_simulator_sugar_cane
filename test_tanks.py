 #-*- coding: utf-8 -*-
from scipy import *
from scipy.integrate import odeint
from physicochemical_properties import liquor_properties
from tanks import *
from time import sleep, clock

import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import threading


Dp=2.0
V=62.83
A=12.6
Tj=50.0
Bj=0.15
Zj=0.87
Ltk=0.2

hmax=V/A

x0 = [Ltk]
u = ()

print("=================================================================================")
print("                                Tank Model                                  ")
print("=================================================================================")
print("Tank Design Properties")
print("Dp[in]: " + str(Dp))
print("V[m3]: " + str(V))
print("A[m]: " + str(A))
print("hmax[m]: " + str(hmax))

print("\nInitial Conditions")
print("Ltk [%]: " + str(Ltk*100.0))

print("\nFluid Properties")
print("Tjin[oC]: " + str(Tj))
print("Bjin[kg/kg]: " + str(Bj))
print("Zjin[kg/kg]: " + str(Zj))



# ============================================================================================
#                                       Simulation
# ============================================================================================

# Time definition
ts = 0.5 #sampling time in seconds
tend = 100 #simulation time in minutes
#tend = tend*60 #simulation time in seconds
tt =  arange(0, tend, ts)

# Time vector definition, tt used for external time vector
t = np.linspace(0,tend,len(tt))
timestep = t[1]-t[0]

# ============================================================================================
#                                       Plotting
# ============================================================================================


fig = plt.figure()
fig.suptitle('Simulation conditions of tank')
# ##------------------------Pout condition to Fout>Fin----------------------------##

Fin=4.0
Pout=-65600
u = (Dp,A,hmax,Fin,Pout,Tj,Bj,Zj)   

ax2 = fig.add_subplot(221)
#Solve model
yout =  odeint(tank.model_level,x0,t,u)
Ltk=yout[:,0]
ax2.set_title('Fout>Fin --- Fin=4Kg/s | Fout=4.6Kg/s')
ax2.set_xlabel('Time (min)')
ax2.set_ylabel('Ltk (%)')
ax2.plot(t,Ltk*100.0)

##------------------------Pout condition to Fin>Fout----------------------------##

Fin=10.0
Pout=-105000.0
u = (Dp,A,hmax,Fin,Pout,Tj,Bj,Zj)    

ax2 = fig.add_subplot(222)
#Solve model
yout =  odeint(tank.model_level,x0,t,u)
Ltk=yout[:,0]
ax2.set_title('Fin>Fout --- Fin=10Kg/s | Fout=7.0Kg/s')
ax2.set_xlabel('Time (min)')
ax2.set_ylabel('Ltk (%)')
ax2.plot(t,Ltk*100.0)

##-------------------------Pout condition to Fin=Fout----------------------------##

Fin=2.0
Pout=-22738.4
u = (Dp,A,hmax,Fin,Pout,Tj,Bj,Zj)  

ax2 = fig.add_subplot(223)
#Solve model
yout = odeint(tank.model_level,x0,t,u) # integrate
Ltk=yout[:,0]
ax2.set_title('Fin=Fout --- Fin=2Kg/s | Fout=1.999Kg/s')
ax2.set_xlabel('Time (min)')
ax2.set_ylabel('Ltk (%)')
ax2.plot(t,Ltk*100.0)

mng = plt.get_current_fig_manager()
mng.window.state('zoomed')

plt.tight_layout()
plt.show()






