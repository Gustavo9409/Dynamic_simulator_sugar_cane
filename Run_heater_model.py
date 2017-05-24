 #-*- coding: utf-8 -*-
from scipy import *
from scipy.integrate import odeint
from scipy.integrate import ode
from physicochemical_properties import liquor_properties
from heaters import *
from time import sleep, clock

import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import threading

global texc

global a
global ts

global yout
global yb
global time_1
global outout_1
yb=0.0
yout=0
a=0.0
texc=0.0
ts=0.5

time_1=0.0
outout_1=0.0



def Thread_time(output_time,output_model_value):
	global a
	global b
	global texc
	global tt
	global yt
	global yout
	global Time_exec_thread
	global u
	band=1
	tt= [0.0,0.0]
	yt=[0.0,0.0]
	outfile=open('time_exec.txt', 'w') ##Para cuando no sea pausa sino detenimiento
	outfile.close()
	plt.ion()
	yb_l=yb
	yt=[0.0,Tjout]
	end_tt=[0.0,Ts_2]
	inf2=[0.0,0.0,0.0]
	fl=0

	while True:
		b = clock()
		#print Ts_2
		if b - a > Ts_2:
			texc=texc+Ts_2
			tt.append(texc)
			end_tt=[tt[-2],tt[-1]]

			yout = odeint(heater_shell_tube.model_temperature,yb_l,end_tt,u)
			yb_l=[yout[1,0]]
			# print yout
			#print end_tt
			yt.append(yout[1,0])

			output_time=tt[len(tt)-1]
			output_model_value=yt[len(tt)-1]
			
			infile = open('time_exec.txt', 'r')
			data=infile.readlines()
			
			if len(data)>0:
				time_exec=data[-1].strip()
				infile.close()
				info=time_exec.split("\t")

				print ("HILO:"+str(time_exec))
				if time_exec=="stop":
					texc=0.0
					break					
				
			outfile = open('time_exec.txt', 'a')
			outfile.write(str(output_time)+"\t"+str(output_model_value)+"\n")
			outfile.close()

			#print("t="+str(output_time)+" ,Tjout="+str(output_model_value))	
			a = b
		
		input_heat = open('Blocks_data.txt', 'r+')
		data=input_heat.readlines()
		vapor_data=[]
		juice_data=[]
		lst = list(u)
		for i in data:
			info=(i.strip()).split("\t")
			if len(info)>1:
				flag=info[0]
				if flag[:2]=="Fv":
					for k in range(1,len(info)):
						vapor_data.append(float(info[k]))
					lst[12]=vapor_data[0]
					#print lst[9]		
				elif flag[:2]=="Fj":
					for k in range(1,len(info)):
						juice_data.append(float(info[k]))
					lst[8]=(juice_data[0]/3.6)/juice_data[8]
					lst[9]=juice_data[1]
					lst[10]=juice_data[2]
					lst[11]=juice_data[3]
					# lst[6:9]=juice_data[1:4]
					#print lst[5]
		input_heat.close()
		u=tuple(lst)

		# (Np, Nst, Lp, dp, Dosp, Fjin, Bjin, Zjin, Tjin, Pvin, Ep, B, Hrop)
		# u = (Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op, Fjin, Tjin, Bjin, Zjin, Pvin)

'''
# ============================================================================================
#                                       Model Initialization
# ============================================================================================
'''
class Simulation_heat:
	def __init__(self,name,param,Ts):
		global Tjout
		global yb
		global u
		global Ts_2

		global a
		global b
		global texc
		global tt
		global yt
		global yout
		global Time_exec_thread
		global u

		liquor=liquor_properties()
		self.name=name
		self.time_samp=Ts
		Ts_2=Ts
		#self.salida=yt[len(tt)-1]
		#self.tiempo=tt[len(tt)-1]
		Np=float(param[0])
		Nst=float(param[1])
		Dosp=float(param[2])
		Lp=float(param[3])
		Ip=float(param[4])
		Ep=float(param[5])
		Gf=float(param[6])
		Op=float(param[7])
		Tjout=float(param[8])
		Mjin=float(param[9])
		Tjin=float(param[10])
		Bjin=float(param[11])
		Zjin=float(param[12])
		Pvin=float(param[13])

		# Np=6.0         #-
		# Nst=2          #-
		# Lp=6.57        #m
		# dp=1.2         #mm
		# Dosp=2.0       #"
		# Mjin=103       #ton/h
		# Bjin=0.15      #kg/kg
		# Zjin=0.87      #kg/kg
		# Tjin=77     	#C  
		# Pvin=4.738     #psig =134Kpa for Tvin=108C
		# Ep=0.090       #mm
		# B= 0.8         #-
		# Hrop=100       #hr

		#Initial condition
		# Tjout=78.0    #C°

		#Density
		pjin = liquor.density(Tjin,Bjin,Zjin)

		#Pressure in Pa (psig to Pa abs)
		#Pvin=(Pvin+14.7)*6894.76;

		#Volumetric flow in m3/s
		Fjin=(Mjin/3.6)/pjin;

		initial_x = [Tjout]
		yb = initial_x
		u = ()
		u = (Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op, Fjin, Tjin, Bjin, Zjin, Pvin)
		#print ("tupla_1 ")+str(u)

		'''
		# ============================================================================================
		#                                      Simulation
		# ============================================================================================
		'''
		#TIME
		# ts = 0.5 #sampling time in seconds
		# tend = 60 #simulation time in minutes
		# #tend = tend*60 #simulation time in seconds
		# tt =  arange(0, tend, ts)

		# #Time vector definition, tt used for external time vector
		# t = np.linspace(0,tend,len(tt))
		# timestep = t[1]-t[0]

		# plot results
		# yout = odeint(ht_model,yb,t,u) # integrate
		# Tjout=yout[:,0]
		# plt.figure(1)
		# plt.plot(t,Tjout)
		# plt.xlabel('Time (min)')
		# plt.ylabel('Tjout (C)')
		# plt.show()
		

		Time_exec_thread =threading.Thread(target = Thread_time, args=(time_1,outout_1))
		#Time_exec.setDaemon(True)
		Time_exec_thread.start()

# Simulation("_")


