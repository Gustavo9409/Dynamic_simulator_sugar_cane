#-*- coding: utf-8 -*-
#! python

# Installed Libs
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

from pint import UnitRegistry

# import matplotlib
# font = {'family' : 'normal',
#         'weight' : 'bold',
#         'size'   : 12}

# matplotlib.rc('font', **font)

# Local Libs
from physicochemical_properties import *
from streams import *
from valves import *
# from evaporators import *
# from control import *

liquor_prpty=liquor_properties()
vapor_prpty=vapor_properties()

ureg = UnitRegistry()


# ============================================================================================
#                                       Model Initialization
# ============================================================================================
# Time definition
ts = 1.0		#sampling time
tf = 50.0		#simulation time
t = np.arange(0.0, tf, ts)

# Parameters
Dv = 8.0*0.0254
Ap = 0.7
delay = 3.0

# Initial
Ap0 = 0.4

# Juice Properties 
Mjin = 100.0 #t/h
Mjout= Mjin*0.9 #t/h
Mjin = Mjin/3.6 #kg/s
Tjin = 115.0
Bjin = 0.15
Zjin = 0.85
Ijin = 0.0
pHjin = 7.0
pjin = liquor_prpty.density(Tjin,Bjin,Zjin)
Tjout = Tjin
Bjout = Bjin
Zjout = Zjin
Ijout = Ijin
pHjout = pHjin
pjout = liquor_prpty.density(Tjout,Bjout,Zjout)

Fjin = (Mjin)/pjin; 

# Pressure conditions
Pin = 20000.0
# Pout = 10000.0
Pout=Pin-400.0

Mjout = Mjout/3.6 #kg/s

Fjout = (Mjout)/pjout; 

# Streams
juice_in = juice(Mjin, Pin, Tjout, Bjout, Zjout, Ijout, pHjout)
juice_out = juice(Mjout, Pout, Tjout, Bjout, Zjout, Ijout, pHjout)

Mvin=1 #t/h
Mvout=Mvin#*0.9 #t/h

Mvin=Mvin/3.6 #kg/s
Mvout=Mvout/3.6 #kg/s


Pvin=134200.0
Pvout=Pvin-400.0
pvin=vapor_prpty.density(Pvin)
pvout=vapor_prpty.density(Pvout)

Fvin=Mvin/pvin;
Fvout=Mvout/pvin;

vapor_in=vapor(Mvin, Pvin, None)
vapor_out=vapor(Mvout, Pvout,None)
# ============================================================================================
#                                      Test Valve Units
# ============================================================================================

# SI Units
Fjout_u = Fjout*(ureg.meter**3)/(ureg.seconds)
Pin_u = Pin*ureg.pascal
Pout_u = Pout*ureg.pascal

Pvin_u = Pvin*ureg.pascal
Pvout_u = Pvout*ureg.pascal

# Imperial Units
Fjout_u_imp = Fjout_u.to(ureg.gallon/ureg.minute)
Pin_u_imp = Pin_u.to(ureg.psi)
Pout_u_imp = Pout_u.to(ureg.psi)

Pvin_u_imp = Pvin_u.to(ureg.psi)
Pvout_u_imp = Pvout_u.to(ureg.psi)


# Valve
CV_u = 250*ureg.gallon/(ureg.minute*ureg.psi**0.5)
Rf_u = CV_u.to(ureg.meter**3/ureg.second/ureg.pascal**0.5)

# Flow formula
pw = 1000.0 
G = pjout/pw
G2= pvout/pw
Fout_v = Rf_u*((Pin_u - Pout_u)/G)**0.5


Fout_v_imp = CV_u*((Pin_u_imp - Pout_u_imp)/G)**0.5

F_vapor=1*(ureg.feet**3/ureg.hour)

Tjout = 333.15
Tjout_imp = 599.67
Tjout_k= Tjout

print(Tjout_imp)
Q_imp = 1360.0*CV_u*(((Pin_u_imp-Pout_u_imp)/G*(Tjout_imp))**0.5)*((Pin_u_imp.magnitude+Pout_u_imp.magnitude)/2.0)**0.5
Q = (1/61.8903927797)*1360.0*Rf_u*(((Pin_u-Pout_u)/G*Tjout_k)**0.5)*((Pin_u.magnitude+Pout_u.magnitude)/2.0)**0.5

Q_imp2=59.64*CV_u*Pvin_u_imp.magnitude*(((Pvin_u_imp-Pvout_u_imp)/Pvin_u_imp.magnitude)**0.5)*((520/(G2*Tjout_imp))**0.5)
Q2=(1/111.402707003)*59.64*Rf_u*Pvin_u.magnitude*(((Pvin_u-Pvout_u)/Pvin_u.magnitude)**0.5)*((520/(G2*Tjout_k))**0.5)
print Q_imp
print Q
print Q_imp.to(ureg.meter**3/ureg.seconds)
print Q_imp2
print Q2
print Rf_u.magnitude
# print Q2.magnitude/Q_imp2.to(ureg.meter**3/ureg.seconds).magnitude
print Q_imp2.to(ureg.meter**3/ureg.seconds)

Pout_sol=Pvin_u.magnitude-(0.0067098509773907*G2*((Q2.magnitude)**2)*Tjout_k)/(Pvin_u.magnitude*(Rf_u.magnitude**2))
print Pout_sol


# H=(1360.0)
# Px=((-2.0*G*Tjout*(Q.magnitude**2.0))/((H**2.0)*(Rf_u.magnitude**2.0)) + Pin**2.0)
# print(Pout)
# print G
# print(Px)

# Psol_imp=Pin-((Pin**2)-(G*Tjout)*((Q.magnitude/(963*Rf_u.magnitude))**2))**0.5
# print Psol_imp
# Psol=59.64*Rf_u.magnitude*Pin*()**0.5

# print(F_vapor.to((ureg.meter**3)/(ureg.seconds)))

# valve1 = valve_liquid(Dv, Ap, delay)
# Fout_v = valve1.flow_calc(Pin.magnitude, Pout.magnitude, pjout, Rf)

# Fout_v_imp = valve1.flow_calc(Pin_imp.magnitude, Pout_imp.magnitude, pjout, CV)

# print('\n')
# print("=================================================================================")
# print("                                  Valve Data                                     ")
# print("=================================================================================")
# print("Valve Design Properties")
# print("Diameter [m]: " + str(Dv))
# print("Delay [s]: " + str(delay))
# print("Aperture []: " + str(Ap))
# print("CV : " + str(CV_u))
# print("Pressure in [kPa]: " + str(Pin/1000.0))
# print("Pressure out [kPa]: " + str(Pout/1000.0))
# print("Flow: " + str(Fout_v))
# print("Flow: " + str(Fout_v.to(ureg.gallon/ureg.minute)))
# print("Flow: " + str(Fout_v_imp))


# # # ============================================================================================
# # #                                   Valve Delay Model
# # # ============================================================================================
# # Inputs
# u = (Ap, delay)


# # Run Model
# x0 = Ap0
# sol = odeint(valve.model, x0, t, args=u)
# ApAp = sol[:,0]

# # ============================================================================================
# #                                          Plotting
# # ============================================================================================
# plt.plot(t, 100*ApAp, 'b', label='Ap')
# plt.legend(loc='best')
# plt.title('Valve Delay Aperture')
# plt.ylabel('Ap [%]')
# plt.xlabel('Time [s]')
# plt.grid()
# plt.show()


# valve1 = valve_liquid(5.0*0.0254, 0.5)
# Rf = valve1.coefficient()
# print Rf



# ============================================================================================
#                                       Model
# ============================================================================================
print('\n')
print("=================================================================================")
print("                                  Valve Data                                     ")
print("=================================================================================")
print("Valve liquid Design Properties")
print("Diameter [m]: " + str(Dv))
print("Delay [s]: " + str(delay))
print("Aperture []: " + str(Ap))
print("Pressure in [kPa]: " + str(Pin/1000.0))
print("Pressure out [kPa]: " + str(Pout/1000.0))
print("Flow in [t/h]: " + str(Mjin*3.6))
print("Flow out [t/h]: " + str(Mjout*3.6))
print("Flow in [m3/s]: " + str(Fjin))
print("Flow out [m3/s]: " + str(Fjout))

print("\nValve vapor Design Properties")
print("Diameter [m]: " + str(Dv))
print("Delay [s]: " + str(delay))
print("Aperture []: " + str(Ap))
print("Pressure in [kPa]: " + str(Pvin/1000.0))
print("Pressure out [kPa]: " + str(Pvout/1000.0))
print("Flow in [t/h]: " + str(Mvin*3.6))
print("Flow out [t/h]: " + str(Mvout*3.6))
print("Flow in [m3/s]: " + str(Fvin))
print("Flow out [m3/s]: " + str(Fvout))


# # ============================================================================================
# #                                       Simulation
# # ============================================================================================

# Time definition
ts = 0.5		#sampling time [s]
tf = 2			#simulation time [min]
tf = 60*tf
t = np.arange(0, tf, ts)
tt = t/60

# Data
Ap0 = 0.7
Ap = 0.3
FjFj = np.zeros(t.shape)
FjoFjo = np.zeros(t.shape)
PoPo = np.zeros(t.shape)
PiPi = np.zeros(t.shape)

plot_FjFj = []
plot_FjoFjo = []
plot_PoPo = []
plot_PiPi = []
plot_tt=[]
cnt=0
# Valve Instance 
valve1 = valve_liquid(Dv, Ap0)

for k in range(t.size):
	valve1.in_out(juice_in, juice_out, Ap)
	# print([t[k],t[k+1]])
	# jin, jout = valve1.solve([t[k],t[k+1]])
	jin, jout = valve1.solve(np.array([0.0, ts]),"Diametro",None,None)
	# jin, jout = valve1.solve(np.array([0.0, ts]),"Coeficientes de flujo",47.0,2000.0)

	FjFj[k] = jin.Fj
	FjoFjo[k] = jout.Fj
	PiPi[k] = jin.Pj
	PoPo[k] = jout.Pj
	
	juice_in = jin
	juice_out = jout

	print ("Mjin: "+str(jin.Mj/juice_in.pj)+" m3/s y en ton/h: "+str(jin.Mj*3.6))
	print ("Mjout: "+str(juice_out.Mj/juice_out.pj)+" m3/s y en ton/h: "+str(jout.Mj*3.6))

	print("Pjin: "+str(jin.Pj))
	print("Pjout: "+str(jout.Pj))

	# if k%2 != 0:

	# 	plot_tt.append(k)
	# 	plot_FjFj.append(jin.Fj)
	# 	plot_FjoFjo.append(jout.Fj)
	# 	plot_PoPo.append(jin.Pj)
	# 	plot_PiPi.append(jout.Pj)	
		# print("t= "+str(k))


FvFv = np.zeros(t.shape)
FvoFvo = np.zeros(t.shape)
PvoPvo = np.zeros(t.shape)
PviPvi = np.zeros(t.shape)

valve2 = valve_vapor(Dv, Ap0)

for k in range(t.size):
	valve2.in_out(vapor_in, vapor_out, Ap)
	# print([t[k],t[k+1]])
	# jin, jout = valve1.solve([t[k],t[k+1]])
	vin, vout = valve2.solve(np.array([0.0, ts]),"Diametro",None,None)
	
	FvFv[k] = vin.Fv
	FvoFvo[k] = vout.Fv
	PviPvi[k] = vin.Pv
	PvoPvo[k] = vout.Pv
	
	vapor_in = vin
	vapor_out = vout

	print ("Mvin: "+str(vin.Fv)+" m3/s y en ton/h: "+str(vin.Mv*3.6))
	print ("Mvout: "+str(vapor_out.Fv)+" m3/s y en ton/h: "+str(vout.Mv*3.6))

	# print("Pvin: "+str(vin.Pv))
	print("Pvout: "+str(vout.Pv))

# ============================================================================================
#                                       Plotting
# ============================================================================================

f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(tt, FjFj, 'b', label='Flow')
axarr[0].plot(tt, FjoFjo, 'r', label='Flow out')
axarr[0].legend(loc='best')
axarr[0].set_ylabel('Flow [m3/s]')
axarr[0].grid()
axarr[0].set_title('Valve liquid all data')
axarr[1].plot(tt, PiPi, 'b', label='Pressure in')
axarr[1].plot(tt, PoPo, 'r', label='Pressure out')
axarr[1].legend(loc='best')
axarr[1].grid()
axarr[1].set_ylabel('Pressure [kPa]')
axarr[1].set_xlabel('Tiempo [min]')
plt.show()

f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(tt, FvFv, 'b', label='Flow')
axarr[0].plot(tt, FvoFvo, 'r', label='Flow out')
axarr[0].legend(loc='best')
axarr[0].set_ylabel('Flow [m3/s]')
axarr[0].grid()
axarr[0].set_title('Valve vapor all data')
axarr[1].plot(tt, PviPvi, 'b', label='Pressure in')
axarr[1].plot(tt, PvoPvo, 'r', label='Pressure out')
axarr[1].legend(loc='best')
axarr[1].grid()
axarr[1].set_ylabel('Pressure [kPa]')
axarr[1].set_xlabel('Tiempo [min]')
plt.show()


# f, axarr = plt.subplots(2, sharex=True)
# axarr[0].plot(plot_tt, plot_FjFj, 'b', label='Flow')
# axarr[0].plot(plot_tt, plot_FjoFjo, 'r', label='Flow out')
# axarr[0].legend(loc='best')
# axarr[0].set_ylabel('Flow [m3/s]')
# axarr[0].grid()
# axarr[0].set_title('Valve odd data')
# axarr[1].plot(plot_tt, plot_PiPi, 'b', label='Pressure in')
# axarr[1].plot(plot_tt, plot_PoPo, 'r', label='Pressure out')
# axarr[1].legend(loc='best')
# axarr[1].grid()
# axarr[1].set_ylabel('Pressure [kPa]')
# axarr[1].set_xlabel('Tiempo [min]')
# plt.show()



