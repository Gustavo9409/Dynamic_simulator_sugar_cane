 #-*- coding: utf-8 -*-
from scipy import *
from scipy.integrate import odeint
from physicochemical_properties import liquor_properties
from tank import *
from time import sleep, clock

import numpy as np
import math
import sys
import matplotlib.pyplot as plt
import threading

global texc

global a
global ts
global liquor

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

liquor=liquor_properties()


def Thread_time(output_time,output_model_value):

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
	yb_l=yb
	yt=[0.0,Ltk]
	end_tt=[0.0,Ts_2]
	inf2=[0.0,0.0,0.0]

	while True:
		b = clock()
		#print Ts_2
		if b - a > Ts_2:
			texc=texc+Ts_2
			tt.append(texc)

			end_tt=[tt[-2],tt[-1]]

			yout = odeint(tank.model_level,yb_l,end_tt,u)
			yb_l=[yout[1,0]]
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

			a = b


'''
# ============================================================================================
#                                       Model Initialization
# ============================================================================================
'''
class Simulation_tank:
	def __init__(self,name,param,Ts):
		
		global Ltk
		global yb
		global u
		global Ts_2

		global Time_exec_thread
		global u

		self.name=name
		self.time_samp=Ts
		Ts_2=Ts

		Dp=float(param[0])
		Lp=float(param[1])
		V=float(param[2])
		A=float(param[3])
		Pin=float(param[4])
		Pout=float(param[5])
		Tj=float(param[6])
		Bj=float(param[7])
		Zj=float(param[8])
		Ltk=float(param[9])

		hmax=V/A

		initial_x = [Ltk]
		yb = initial_x
		u = ()
		u = (Dp,Lp,A,hmax,Pin,Pout,Tj,Bj,Zj)
		#print ("tupla_1 ")+str(u)

		'''
		# ============================================================================================
		#                                      Simulation
		# ============================================================================================
		'''

		#TIME
		ts = 0.5 #sampling time in seconds
		tend = 100 #simulation time in minutes
		#tend = tend*60 #simulation time in seconds
		tt =  arange(0, tend, ts)

		#Time vector definition, tt used for external time vector
		t = np.linspace(0,tend,len(tt))
		timestep = t[1]-t[0]

		#plot results
		yout = odeint(tank.model_level,yb,t,u) # integrate
		Ltk=yout[:,0]
		plt.figure(1)
		plt.plot(t,Ltk)
		plt.xlabel('Time (min)')
		plt.ylabel('Ltk (m/m)')
		plt.show()

		# Time_exec_thread =threading.Thread(target = Thread_time, args=(time_1,outout_1))
		# #Time_exec.setDaemon(True)
		# Time_exec_thread.start()
param=[2,62.83,12.6,101410,119000,50,0.015,0.87,0.2]
Simulation_tank("_",param,0.5)


