 #-*- coding: utf-8 -*-
# Installed Libs
import numpy as np
import math
import sys
import threading

from time import sleep, clock
# Local Libs
from global_data import *

#global values
global texc
global a
global ts
global yout
global yb

yb=0.0
yout=0
a=0.0
texc=0.0
ts=0.5


## Thread for run time simulation
def Thread_time():
	global a
	global b
	global texc
	global tt
	global yt
	global yout
	global Time_exec_thread
	global u
	global db
	global cnt_id

	tt= [0.0,0.0]
	yt=[0.0,0.0]
	db.clear_table("Time_exec")
	db.clear_table("outputs_heater")
	db.clear_table("outputs_evaporator")
	db.clear_table("outputs_valve")
	end_tt=[0.0,Ts_2]
	id_time=0
	time=""
	cnt_id=0

	while True:
		b = clock()
		
		if b - a > Ts_2:

			
			if time=="stop":
				Db_data.time="stop"
				texc=0.0
				break	

			Db_data.ts=Ts_2
			texc=texc+Ts_2
			tt.append(texc)


			output_time=tt[len(tt)-1]

			w="TS,TIME"
			h=[Ts_2,output_time]
			
			x=db.read_data("TIME_EXEC","id,TIME",None,None)
			
			if len(x)>0:
				id_time=str(list(x[-1])[0])
				time=str(list(x[-1])[1])
			
				if time=="stop":
					Db_data.time="stop"
					texc=0.0
					break		
				
			if time!="stop":
				db.insert_data("TIME_EXEC",w,h)
				cnt_id=cnt_id+1
				Db_data.time_id=str(cnt_id)
				Db_data.time=str(output_time)
			print("TIME: "+str(output_time))
	
			a = b
		

'''
# ============================================================================================
#                                      Simulation Initialization
# ============================================================================================
'''
class Simulation:

	def __init__(self,name,Ts,Data_Base):
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
		global db

		db=Data_Base


		self.name=name
		self.time_samp=Ts
		Ts_2=Ts


		Time_exec_thread =threading.Thread(target = Thread_time)
		#Time_exec.setDaemon(True)
		Time_exec_thread.start()



