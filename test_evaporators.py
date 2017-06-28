#-*- coding: utf-8 -*-
#! python

# Installed Libs
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Local Libs
from physicochemical_properties import *
from evaporators import *
from control import *

liquor_prpty=liquor_properties()
vapor_prpty=vapor_properties()


# ============================================================================================
#                                       Model Initialization
# ============================================================================================
# Time definition
ts = 1.0		#sampling time
tf = 100.0		#simulation time
t = np.arange(0.0, tf, ts)

# Parameters
A = 800.0
h = 2.0
Ne = 1.0
Op = 0.0
Ls = 0.0
At = 10.0 # Transversal Area of juice

# Juice Properties 
Mjin = 100.0 #t/h
Mjin = Mjin/3.6 #kg/s
Tjin = 115.0
Bjin = 0.15
Zjin = 0.85
pjin = liquor_prpty.density(Tjin,Bjin,Zjin)
Fjin = (Mjin)/pjin; 

# Vapor Properties
Pvin = 253037.6 # 36.7 psia -> 22 psig
Tvin = vapor_prpty.temperature(Pvin)

Pvv = 184090 # 26.7 psia -> 12 psig

# Initial juice temperature (out)
Bjout0 = 0.185
Lje0 = 0.36
Tje = 118.07
Tjout = Tje

# Juice out
Mjout = 0.8*Mjin*Bjin/Bjout0
pjout = liquor_prpty.density(Tjout,Bjout0,Zjin)
Fjout = (Mjout)/pjout; 

# Model parmeters
u = (A, h, At, Ls, Ne, Op, Fjin, Tjin, Bjin, Zjin, Tvin, Fjout, Tjout, Pvv)

# ============================================================================================
#                                      Test HTC Function
# ============================================================================================
Bx_out = 0.22 # Temporal variable for HTC
#evap = evaporator_roberts(A, h, Ls, Ne, Op)
htc = evaporator_roberts.htc_calc(Op, Ne, Bx_out, Tje, Lje0)

print('\n')
print("=================================================================================")
print("                                  HTC, Roberts                                   ")
print("=================================================================================")
print("Evaporator Design Properties")
print("A[m2]: " + str(A))
print("h[m]: " + str(h))
print("Ne[]: " + str(Ne))
print("Op[d]: " + str(Op))
print("Ls[%]: " + str(Ls))
print("Bjout [%]: " + str(Bx_out*100.0))
print("Tje [%]: " + str(Tje))
print("Lje [%]: " + str(Lje0*100.0))
print("HTC [W/m2.K]: " + str(htc))

# # ============================================================================================
# #                                       HTC Calc
# # ============================================================================================
# L = np.arange(0.2, 1.0, 0.01)
# htc = evaporator_roberts.htc_calc(Op, Ne, Bx_out, Tje, L)

# # ============================================================================================
# #                                       Plotting
# # ============================================================================================
# plt.plot(L, htc, 'b', label='HTC')
# plt.legend(loc='best')
# plt.title('Heat Transfer Coefficient')
# plt.ylabel('HTC [W/m2.K]')
# plt.xlabel('Level [%]')
# plt.grid()
# plt.show()


# ============================================================================================
#                                      Evaporator Model
# ============================================================================================
print('\n')
print("=================================================================================")
print("                            Evaporator Model, Roberts                            ")
print("=================================================================================")
print("Evaporator Design Properties")
print("A[m2]: " + str(A))
print("h[m]: " + str(h))
print("Ne[]: " + str(Ne))
print("Op[d]: " + str(Op))
print("Ls[%]: " + str(Ls))


print("\nJuice Properties")
print("Mjin[kg/s]: " + str(Mjin)) #100 t/h
print("Tjin[oC]: " + str(Tjin))
print("Bjin[kg/kg]: " + str(Bjin))
print("Zjin[kg/kg]: " + str(Zjin))


print("\nVapor in Properties")
print("Pvin[Pa]: " + str(Pvin))
print("Tvin[oC]: " + str(Tvin))

print("\nVapor out Properties")
print("Pvv[Pa]: " + str(Pvv))
print("Tvv[oC]: " + str(vapor_prpty.temperature(Pvv)))

print("\nInitial Conditions")
print("Bjout [%]: " + str(Bjout0*100.0))
print("Tje [%]: " + str(Tje))
print("Lje [%]: " + str(Lje0*100.0))

# ============================================================================================
#                                       Simulation
# ============================================================================================

# Time definition
ts = 10		#sampling time [s]
tf = 60		#simulation time [min]
tf = 60*tf
t = np.arange(0, tf, ts)
tt = t/60

# Run Model
x0 = Bjout0, Lje0
sol = odeint(evaporator_roberts.model, x0, t, args=u)
Bx = sol[:,0]
Lv = sol[:,1]

# ============================================================================================
#                                       Plotting
# ============================================================================================

f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(tt, Bx, 'b', label='Brix')
axarr[0].legend(loc='best')
#axarr[0].ylabel('Brix [%]')
axarr[0].grid()
axarr[0].set_title('Evaporator')
axarr[1].plot(tt, Lv, 'r', label='Level')
axarr[1].legend(loc='best')
axarr[1].grid()
#axarr[1].ylabel('Level [%]')
#axarr[1].xlabel('Time [s]')
plt.show()


# ============================================================================================
#                                 Evaporator Level Control
# ============================================================================================
print('\n')
print("=================================================================================")
print("                            Evaporator Level Control                             ")
print("=================================================================================")
print("Evaporator Design Properties")
print("A[m2]: " + str(A))
print("h[m]: " + str(h))
print("Ne[]: " + str(Ne))
print("Op[d]: " + str(Op))
print("Ls[%]: " + str(Ls))


print("\nJuice Properties")
print("Mjin[kg/s]: " + str(Mjin)) #100 t/h
print("Tjin[oC]: " + str(Tjin))
print("Bjin[kg/kg]: " + str(Bjin))
print("Zjin[kg/kg]: " + str(Zjin))


print("\nVapor in Properties")
print("Pvin[Pa]: " + str(Pvin))
print("Tvin[oC]: " + str(Tvin))

print("\nVapor out Properties")
print("Pvv[Pa]: " + str(Pvv))
print("Tvv[oC]: " + str(vapor_prpty.temperature(Pvv)))

print("\nInitial Conditions")
print("Bjout [%]: " + str(Bjout0*100.0))
print("Tje [%]: " + str(Tje))
print("Lje [%]: " + str(Lje0*100.0))

# ============================================================================================
#                                       Simulation
# ============================================================================================

# Time definition
ts = 1.0		#sampling time [s]
tf = 60.0		#simulation time [min]
tf = 60.0*tf
t = np.arange(0.0, tf, ts)
tt = t/60.0

# Control
sp_lvl = 0.4
ctrl = pid(ts, -2.5, 0.3, 0.0)

# Run Model
x0 = Bjout0, Lje0

BxBx = np.zeros(t.shape)
LvLv = np.zeros(t.shape)

for k in range(t.size):
	sol = odeint(evaporator_roberts.model, x0, np.array([0.0, ts]), args=u)
	Bx = sol[1,0]
	Lv = sol[1,1]

	x0 = Bx, Lv
	BxBx[k] = Bx
	LvLv[k] = Lv

	Fjout = ctrl.solve(sp_lvl, Lv)
	u = (A, h, At, Ls, Ne, Op, Fjin, Tjin, Bjin, Zjin, Tvin, Fjout, Tjout, Pvv)


	

# ============================================================================================
#                                       Plotting
# ============================================================================================

f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(tt, BxBx, 'b', label='Brix')
axarr[0].legend(loc='best')
#axarr[0].ylabel('Brix [%]')
axarr[0].grid()
axarr[0].set_title('Evaporator')
axarr[1].plot(tt, LvLv, 'r', label='Level')
axarr[1].legend(loc='best')
axarr[1].grid()
#axarr[1].ylabel('Level [%]')
#axarr[1].xlabel('Time [s]')
plt.show()