#-*- coding: utf-8 -*-
#! python

# Installed Libs
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from control import *

# Local Libs
from physicochemical_properties import *
from streams import *
from valves import *
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

ts = 0.5		#sampling time [s]
tf = 20.0		#simulation time [min]
tf = 60.0*tf
t = np.arange(0.0, tf, ts)
tt = t/60.0

# Parameters
Np = 36.0
Nst = 4.0
Dosp = 2.0
Lp = 6.57
Ip = 1.2
Ep = 0.09
Gf = 0.8
Op = 100.0

# Juice Properties 
Mjin = 103.0
Mjin = Mjin/3.6 #kg/s
Tjin = 77.0
Bjin = 0.15
Zjin = 0.87
Ij= 0.08
Pjin=400000.0
pjin = liquor_prpty.density(Tjin,Bjin,Zjin)
Fjin = (Mjin)/pjin;
pHj=7.0

# Vapor Properties
Pvin = 134000.0

# Initial juice temperature (out)
x0 = 78.0

# Model parmeters
u = (Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op, Fjin, Tjin, Bjin, Zjin, Pvin)

print('\n')
print("=================================================================================")
print("                           Heater Model, Shell & Tubes                           ")
print("=================================================================================")
print("Heater Design Properties")
print("Np[]: 6.0")
print("Nst[]: 2.0")
print("Dosp[in]: 2.0")
print("Lp[m]: 6.57")
print("Ip[mm]: 1.2" )
print("Ep[mm]: 0.090")
print("Gf[]: 0.8")
print("Op[h]: 100.0")

print("\nJuice Properties")
print("Fjin[m3/s]:" + str(Fjin)) #100 t/h
print("Tjin[oC]: 77.0")
print("Bjin[kg/kg]: 0.15")
print("Zjin[kg/kg]: 0.87")

print("\nSaturated Vapor Properties")
print("Pvin[Pa]: 134000")
print("Tvin[oC]: " + str(vapor_prpty.temperature(Pvin)))


# ============================================================================================
#                                       Simulation
# ============================================================================================

sp_tmp = 81.159  ##Con Ap=10
sp_tmp = 82.27   ##Con Ap=30
# sp_tmp = 82.6
Ap0 = 0.7
Ap = Ap0*100
# ctrl1 = pid(ts, -178.17,  0.0, 0.0)
ctrl1 = pid(ts,147.0,0.0, 0.0)

ht_model=heater_shell_tube(Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op,x0)
Valve=valve_vapor(8.0*0.0254,Ap0)
# Run Model
sol = odeint(ht_model.model_temperature, x0, t, args=u)
Mvin=0.9828
Mvout=0.9828

Mvin=Mvin/3.6 #kg/s
Mvout=Mvout/3.6 #kg/s

stream_in=vapor(Mvin,Pvin,None)
stream_out=vapor(0,stream_in.Pv-400.0,None)

Ap_arr=[]
Tmp_arr=[]
Pout_arr=[]

fluid_in=juice(Mjin,Pjin,Tjin, Bjin,Zjin,Ij,pHj)
fluid_out=juice(Mjin,Pjin,x0, Bjin,Zjin,Ij,pHj)




vapor_in=vapor(Mvin,Pvin-400.0,None)
vapor_out=vapor(vapor_in.Mv,Pvin,None)

for k in range(t.size):
	
	ht_model.in_out(fluid_in, fluid_out, vapor_in, vapor_out)
	fluid_in, fluid_out, vapor_in, vapor_out = ht_model.solve([tt[-2],tt[-1]])

	tmp=fluid_out.Tj
	Tmp_arr.append(tmp)

	x0 = tmp

	Ap_arr.append(Ap)

	Ap = ctrl1.solve(sp_tmp, tmp)
	
	# print ("Tmp: "+str(tmp))
	# print "---!!--"
	# if k==0:
	
	if Ap>100.0:
		Ap=100
	elif Ap<10.0:
		Ap=10.0
	# print ("Ap: "+str(round(Ap,1)))


	# stream_in.Mv=vapor_in.Mv

	# stream_in.update_()

	Valve.in_out(stream_in, vapor_in,Ap/100.0)
	strm_in, strm_out = Valve.solve(np.array([0.0, ts]),"Diametro",None,None)
	
	stream_in.Mv=vapor_in.Mv
	
	stream_in = strm_in
	vapor_in = strm_out

	stream_in.update_()
	vapor_in.update_()

	Pvin=vapor_in.Pv
	# print(Pvin)
	
	Pout_arr.append(Pvin)

print("Tjout: "+str(Tmp_arr[-1]))
print("Ap: "+str(Ap_arr[-1]))

# ============================================================================================
#                                       Plotting
# ============================================================================================
plt.plot(t, sol, 'b', label='Temperature')
plt.legend(loc='best')
plt.ylabel('Temperature [^oC]')
plt.xlabel('Time [s]')
plt.grid()
plt.show()


f, axarr = plt.subplots(3, sharex=True)
axarr[0].plot(tt, Ap_arr, 'b', label='Ap')
axarr[0].legend(loc='best')
axarr[0].grid()
axarr[0].set_title('Heater')
axarr[1].plot(tt, Pout_arr, 'r', label='Pout')
axarr[1].legend(loc='best')
axarr[1].grid()
axarr[2].plot(tt, Tmp_arr, 'r', label='Temp')
axarr[2].legend(loc='best')
axarr[2].grid()

plt.show()