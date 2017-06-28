#-*- coding: utf-8 -*-
#! python

# Installed Libs
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Local Libs
from physicochemical_properties import *
from heaters import *

liquor_prpty=liquor_properties()
vapor_prpty=vapor_properties()
htc_s=htc_shell_tube()


# ============================================================================================
#                                       Model Initialization
# ============================================================================================

# Time definition
ts = 1		#sampling time
tf = 100		#simulation time
t = np.arange(0, tf, ts)

# Parameters
Np = 12.0
Nst = 2.0
Dosp = 1.5
Lp = 5.0
Ip = 1.2
Ep = 0.09
Gf = 0.8
Op = 0.0

# Juice Properties 
Mjin = 100
Tjin = 50.0
Bjin = 0.15
Zjin = 0.87
pjin = liquor_prpty.density(Tjin,Bjin,Zjin)
Fjin = (Mjin/3.6)/pjin;

# Vapor Properties
Pvin = 169019

# Initial juice temperature (out)
x0 = 55.0

# Model parmeters
u = (Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op, Fjin, Tjin, Bjin, Zjin, Pvin)

print('\n')
print("=================================================================================")
print("                           Heater Model, Shell & Tubes                           ")
print("=================================================================================")
print("Heater Design Properties")
print("Np[]: 12.0")
print("Nst[]: 2.0")
print("Dosp[in]: 1.5")
print("Lp[m]: 5.0")
print("Ip[mm]: 1.2" )
print("Ep[mm]: 0.090")
print("Gf[]: 0.8")
print("Op[h]: 0.0")

print("\nJuice Properties")
print("Fjin[kg/s]:" + str(Fjin)) #100 t/h
print("Tjin[oC]: 50.0")
print("Bjin[kg/kg]: 0.15")
print("Zjin[kg/kg]: 0.87")

print("\nSaturated Vapor Properties")
print("Pvin[Pa]: 169019")
print("Tvin[oC]: " + str(vapor_prpty.temperature(Pvin)))


# ============================================================================================
#                                       Simulation
# ============================================================================================

# Run Model
sol = odeint(heater_shell_tube.model_temperature, x0, t, args=u)



# ============================================================================================
#                                       Plotting
# ============================================================================================
plt.plot(t, sol, 'b', label='Temperature')
plt.legend(loc='best')
plt.ylabel('Temperature [^oC]')
plt.xlabel('Time [s]')
plt.grid()
plt.show()