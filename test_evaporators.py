#-*- coding: utf-8 -*-
#! python

# Installed Libs
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import matplotlib
# font = {'family' : 'normal',
#         'weight' : 'bold',
#         'size'   : 12}

# matplotlib.rc('font', **font)

# Local Libs
from physicochemical_properties import *
from streams import *
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
A = 900.0
h = 2.0
Np = 1500.0
Di = 0.0508 #1.5 inch
V = 20.0
Dd = 0.4
hc = 0.5
Ne = 1.0
Op = 0.0
Ls = 0.0
#At = 10.0 # Transversal Area of juice

# Juice Properties 
Mjin = 100.0 #t/h
Mjin = Mjin/3.6 #kg/s
Pjin = 517100.0
Tjin = 115.0
Bjin = 0.15
Zjin = 0.85
Ijin = 0.0
pHjin = 7.0
pjin = liquor_prpty.density(Tjin,Bjin,Zjin)
Fjin = (Mjin)/pjin; 

juice_in = juice(Mjin, Pjin, Tjin, Bjin, Zjin, Ijin, pHjin)

# Initial juice temperature (out)
Bjout0 = 0.19
Lje0 = 0.35
Tje = 118.07
Tjout = Tje

# Juice out
Mjout = 0.95*Mjin*Bjin/Bjout0
pjout = liquor_prpty.density(Tjout,Bjout0,Zjin)
Fjout = (Mjout)/pjout
pHjout = pHjin - 0.4

juice_out = juice(Mjout, Pjin, Tjout, Bjout0, Zjin, Ijin, pHjout)

# Vapor in Properties
Mvin = 1.05*(Mjin - Mjout)
Pvin = 253037.6 # 36.7 psia -> 22 psig
Tvin = vapor_prpty.temperature(Pvin)

vapor_in = vapor(Mvin, Pvin, None)

# Vapor out Properties
Mvv = Mjin - Mjout
Pvv = 184090 # 26.7 psia -> 12 psig

vapor_out = vapor(Mvv, Pvv, None)
vapor_use = vapor_out
Mw=Mjin
Pw=Pjin
Tw=Tjin
pHw=pHjin
vapor_cond = water(Mw, Pw, Tw, pHw)

Mvc = Mvv

# # ============================================================================================
# #                                      Test HTC Function
# # ============================================================================================
# Bx_out = 0.22 # Temporal variable for HTC
# #evap = evaporator_roberts(A, h, Ls, Ne, Op)
# htc = evaporator_roberts.htc_calc(Op, Ne, Lje0, Tje, Bx_out)

# print('\n')
# print("=================================================================================")
# print("                                  HTC, Roberts                                   ")
# print("=================================================================================")
# print("Evaporator Design Properties")
# print("A[m2]: " + str(A))
# print("h[m]: " + str(h))
# print("Ne[]: " + str(Ne))
# print("Op[d]: " + str(Op))
# print("Ls[%]: " + str(Ls))
# print("Bjout [%]: " + str(Bx_out*100.0))
# print("Tje [%]: " + str(Tje))
# print("Lje [%]: " + str(Lje0*100.0))
# print("HTC [W/m2.K]: " + str(htc))

# # ============================================================================================
# #                                       HTC Calc
# # ============================================================================================
# L = np.arange(0.0, 1.0, 0.01)
# htc = evaporator_roberts.htc_calc(Op, Ne, L, Tje, Bx_out)

# # ============================================================================================
# #                                       Plotting
# # ============================================================================================
# plt.plot(100*L, htc, 'b', label='HTC')
# plt.legend(loc='best')
# plt.title('Heat Transfer Coefficient')
# plt.ylabel('HTC [W/m2.K]')
# plt.xlabel('Level [%]')
# plt.grid()
# plt.show()


# # ============================================================================================
# #                                      Evaporator Model
# # ============================================================================================
# print('\n')
# print("=================================================================================")
# print("                      Evaporator Simple Model, Roberts                           ")
# print("=================================================================================")
# print("Evaporator Design Properties")
# print("A[m2]: " + str(A))
# print("h[m]: " + str(h))
# print("Ne[]: " + str(Ne))
# print("Op[d]: " + str(Op))
# print("Ls[%]: " + str(Ls))


# print("\nJuice Properties")
# print("Mjin[kg/s]: " + str(Mjin)) #100 t/h
# print("Tjin[oC]: " + str(Tjin))
# print("Bjin[kg/kg]: " + str(Bjin))
# print("Zjin[kg/kg]: " + str(Zjin))


# print("\nVapor in Properties")
# print("Pvin[Pa]: " + str(Pvin))
# print("Tvin[oC]: " + str(Tvin))

# print("\nVapor out Properties")
# print("Pvv[Pa]: " + str(Pvv))
# print("Tvv[oC]: " + str(vapor_prpty.temperature(Pvv)))

# print("\nInitial Conditions")
# print("Bjout [%]: " + str(Bjout0*100.0))
# print("Tje [%]: " + str(Tje))
# print("Lje [%]: " + str(Lje0*100.0))

# # ============================================================================================
# #                                       Simulation
# # ============================================================================================

# # Time definition
# ts = 0.5		#sampling time [s]
# tf = 30		#simulation time [min]
# tf = 60*tf
# t = np.arange(0, tf, ts)
# tt = t/60

# # A = 1000.0
# # At = 3.15
# # Bjout0 = 0.185
# # Lje0 = 0.30
# # Mjout = 0.8*Mjin*Bjin/Bjout0

# evaporator1 = evaporator_roberts(A, h, Np, Di, V, Dd, hc, Ne, Op, Ls, Lje0)
# At = evaporator1.At
# print("At: " + str(At))

# # Model parmeters
# u = (A, h, At, Ls, Ne, Op, Fjin, Tjin, Bjin, Zjin, Tvin, Fjout, Tjout, Pvv)

# # Run Model
# x0 = Bjout0, Lje0

# BxBx = np.zeros(t.shape)
# LvLv = np.zeros(t.shape)

# # Run Model
# x0 = Bjout0, Lje0
# sol = odeint(evaporator_roberts.model, x0, t, args=u)
# BxBx = sol[:,0]
# LvLv = sol[:,1]


# # for k in range(t.size):
# # 	sol1 = odeint(evaporator_roberts.model, x0, np.array([0.0, ts]), args=u)
# # 	Bx = sol1[1,0]
# # 	Lv = sol1[1,1]

# # 	x0 = Bx, Lv
# # 	BxBx[k] = Bx
# # 	LvLv[k] = Lv


# # ============================================================================================
# #                                       Plotting
# # ============================================================================================

# f, axarr = plt.subplots(2, sharex=True)
# axarr[0].plot(tt, 100*BxBx, 'b', label='Brix')
# axarr[0].legend(loc='best')
# axarr[0].set_ylabel('Brix [%]')
# axarr[0].grid()
# axarr[0].set_title('Evaporador')
# axarr[1].plot(tt, 100*LvLv, 'r', label='Level')
# axarr[1].legend(loc='best')
# axarr[1].grid()
# axarr[1].set_ylabel('Nivel [%]')
# axarr[1].set_xlabel('Tiempo [min]')
# plt.show()



# # ============================================================================================
# #                                 Evaporator Level Control
# # ============================================================================================
# print('\n')
# print("=================================================================================")
# print("                            Evaporator Level Control                             ")
# print("=================================================================================")
# print("Evaporator Design Properties")
# print("A[m2]: " + str(A))
# print("h[m]: " + str(h))
# print("Ne[]: " + str(Ne))
# print("Op[d]: " + str(Op))
# print("Ls[%]: " + str(Ls))


# print("\nJuice Properties")
# print("Mjin[kg/s]: " + str(Mjin)) #100 t/h
# print("Tjin[oC]: " + str(Tjin))
# print("Bjin[kg/kg]: " + str(Bjin))
# print("Zjin[kg/kg]: " + str(Zjin))


# print("\nVapor in Properties")
# print("Pvin[Pa]: " + str(Pvin))
# print("Tvin[oC]: " + str(Tvin))

# print("\nVapor out Properties")
# print("Pvv[Pa]: " + str(Pvv))
# print("Tvv[oC]: " + str(vapor_prpty.temperature(Pvv)))

# print("\nInitial Conditions")
# print("Bjout [%]: " + str(Bjout0*100.0))
# print("Tje [%]: " + str(Tje))
# print("Lje [%]: " + str(Lje0*100.0))

# # ============================================================================================
# #                                       Simulation
# # ============================================================================================

# # Time definition
# ts = 1.0		#sampling time [s]
# tf = 60.0		#simulation time [min]
# tf = 60.0*tf
# t = np.arange(0.0, tf, ts)
# tt = t/60.0

# evaporator1 = evaporator_roberts(A, h, Np, Di, V, Dd, hc, Ne, Op, Ls, Lje0)
# At = evaporator1.At

# # Model parmeters
# u = (A, h, At, Ls, Ne, Op, Fjin, Tjin, Bjin, Zjin, Tvin, Fjout, Tjout, Pvv)

# # Control
# # Level
# sp_lvl = 0.35
# ctrl1 = pid(ts, -2.5, -0.9, 0.0)
# # ctrl1 = pid(ts, 2.0, 2.2, 0.0)

# # Brix
# sp_bx = 0.21
# # ctrl2 = pid(ts, -1.0, -1.8, 0.0)
# # ctrl2 = pid(ts, -2.0, -0.4, 0.0)

# # Run Model
# x0 = Bjout0, Lje0

# BxBx = np.zeros(t.shape)
# LvLv = np.zeros(t.shape)

# for k in range(t.size):
# 	sol = odeint(evaporator_roberts.model, x0, np.array([0.0, ts]), args=u)
# 	Bx = sol[1,0]
# 	Lv = sol[1,1]

# 	x0 = Bx, Lv
# 	BxBx[k] = Bx
# 	LvLv[k] = Lv

# 	Fjout = ctrl1.solve(sp_lvl, Lv)
# 	#Fjin = ctrl1.solve(sp_lvl, Lv)
# 	#Fjout = ctrl2.solve(sp_bx, Bx)

# 	u = (A, h, At, Ls, Ne, Op, Fjin, Tjin, Bjin, Zjin, Tvin, Fjout, Tjout, Pvv)

	
# # ============================================================================================
# #                                       Plotting
# # ============================================================================================

# f, axarr = plt.subplots(2, sharex=True)
# axarr[0].plot(tt, BxBx*100, 'b', label='Brix')
# axarr[0].legend(loc='best')
# axarr[0].set_ylabel('Brix [%]')
# # axarr[0].set_ylim((15.0,35.0))
# axarr[0].set_xlabel('Time [min]')
# axarr[0].grid()
# axarr[0].set_title('Evaporator')
# axarr[1].plot(tt, LvLv*100, 'r', label='Level')
# axarr[1].legend(loc='best')
# axarr[1].set_ylabel('Level [%]')
# # axarr[1].set_ylim((20.0,50.0))
# axarr[1].set_xlabel('Time [min]')
# axarr[1].grid()
# plt.show()



# ============================================================================================
#                                      Evaporator Model
# ============================================================================================
print('\n')
print("=================================================================================")
print("                      Evaporator Complex Model, Roberts                          ")
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

# # Run Model
# x0 = Bjout0, Lje0
# sol = odeint(evaporator_roberts.model, x0, t, args=u)
# Bx = sol[:,0]
# Lv = sol[:,1]

evaporator1 = evaporator_roberts(A, h, Np, Di, V, Dd, hc, Ne, Op, Ls, Lje0)
At = evaporator1.At

evaporator1.in_out(juice_in, vapor_in, juice_out, vapor_out, vapor_use, vapor_cond)


# Model parmeters
u = (A, h, At, Ls, Ne, Op, Fjin, Tjin, Bjin, Zjin, Tvin, Fjout, Tjout, Pvv)

u_ve = (Mvv, Mvc)

# Run Model
x0 = Bjout0, Lje0

deltaP0 = 62052.81563851526
mve0 = evaporator1.mve_init(Pvv-deltaP0, V, At, h, Lje0)
print("mve [kg]: " + str(mve0))

BxBx = np.zeros(t.shape)
LvLv = np.zeros(t.shape)
PvPv = np.zeros(t.shape)
mveve = np.zeros(t.shape)

BxBx2 = np.zeros(t.shape)
LvLv2 = np.zeros(t.shape)

u_ve = (Mvv, Mvc)

for k in range(t.size):
	print("\nIter: " + str(k))
	sol1 = odeint(evaporator_roberts.model, x0, np.array([0.0, ts]), args=u)
	Bx = sol1[1,0]
	Lv = sol1[1,1]

	x0 = Bx, Lv
	BxBx[k] = Bx
	LvLv[k] = Lv

	evaporator1.update(A, h, Np, Di, V, Dd, hc, Ne, Op, Ls, Lv)

	Mvin = evaporator1.mass_vapor_in()

	print("Bx: " + str(Bx) + "\tLv: " + str(Lv))

	sol2 = odeint(evaporator_roberts.model_ve, mve0, np.array([0.0, ts]), args=u_ve)
	mve = sol2[1,0]

	mve0 = mve
	mveve[k] = mve

	Mvv = evaporator1.mass_vapor_out()
	Pvv = evaporator1.Pvv(mve)
	Tjout = evaporator1.Tje(Pvv)
	Mvc = Mvv

	print("mve: " + str(mve) + "\tPvv: " + str(Pvv) + "\tTje: " + str(Tjout))

	u = (A, h, At, Ls, Ne, Op, Fjin, Tjin, Bjin, Zjin, Tvin, Fjout, Tjout, Pvv)

	u_ve = (Mvv, Mvc)

	juice_in.update(Mjin, Pjin, Tjin, Bjin, Zjin, Ijin, pHjin)
	juice_out.update(Mjout, Pjin, Tjout, Bx, Zjin, Ijin, pHjout)
	vapor_in.update(Mvin, Pvin, None)
	vapor_out.update(Mvv, Pvv, None)

	PvPv[k] = Pvv

	evaporator1.in_out(juice_in, vapor_in, juice_out, vapor_out, vapor_use, vapor_cond)


# for k in range(t.size):
# 	print("\nIter: " + str(k))

# 	evaporator1.in_out(juice_in, vapor_in, juice_out, vapor_out, vapor_use, vapor_cond)
# 	juice_in, juice_out, vapor_in, vapor_out = evaporator1.solve(np.array([0.0, ts]))

# 	BxBx[k] = juice_out.Bj
# 	LvLv[k] = evaporator1.Lje
# 	PvPv[k] = vapor_out.Pv

# 	vapor_use = vapor_out
	
# 	print("Bx: " + str(juice_out.Bj) + "\tLv: " + str(evaporator1.Lje))
# 	print("mve: " + str(evaporator1.mve0) + "\tPvv: " + str(vapor_out.Pv) + "\tTje: " + str(juice_out.Tj))




# ============================================================================================
#                                       Plotting
# ============================================================================================

f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot(tt, BxBx, 'b', label='Brix')
axarr[0].legend(loc='best')
#axarr[0].ylabel('Brix [%]')
axarr[0].grid()
axarr[0].set_title('Evaporator')
axarr[1].plot(tt, LvLv, 'r', label='Level')
axarr[1].legend(loc='best')
axarr[1].grid()
axarr[2].plot(tt, PvPv, 'g', label='Press')
axarr[2].legend(loc='best')
axarr[2].grid()
#axarr[1].ylabel('Level [%]')
#axarr[1].xlabel('Time [s]')

plt.show()



# Nv = 35.0*np.ones((50))
# tnv = np.arange(0, Nv.size)
# plt.plot(tnv, Nv, 'r', label='Nivel')
# plt.title('Evaporador')
# plt.xlabel('Tiempo [min]')
# plt.ylabel('Nivel [%]')
# plt.ylim((20.0,50.0))
# plt.legend(loc='best')
# plt.grid()
# plt.show()