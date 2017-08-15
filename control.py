#-*- coding: utf-8 -*-
#! python

# Installed Libs
import math
import numpy as np



class pid:
	'''
	Parameters:
	sp, Setpoint
	pv, Process Variable
	mv, Manipulated Variable
	'''

	def __init__(self, ts, kp, ki, kd):
		# Create pid properties
		self.ts = ts
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.error0 = 0.0
		
	def update(self, ts, kp, ki, kd):
		self.ts = ts
		self.kp = kp
		self.ki = ki
		self.kd = kd
		self.error0 = 0.0

	def solve(self, sp, pv):
		self.sp = sp
		self.pv = pv
		self.error = self.sp - self.pv

		p = self.kp*self.error
		i = self.ki*0.5*(self.error + self.error0)*self.ts
		d = self.kd*(self.error - self.error0)/self.ts

		self.mv = p + i + d
		self.error0 = self.error # saving error for next loop
		return self.mv

	def solve_normalized(self, sp, pv, min_mv, max_mv):
		self.sp = sp
		self.pv = pv
		self.offset= max_mv - min_mv
		self.error = (self.sp - self.pv) + self.offset/2.0
		
		p = self.kp*self.error
		i = self.ki*0.5*(self.error + self.error0)*self.ts
		d = self.kd*(self.error - self.error0)/self.ts

		self.mv = p + i + d
		self.error0 = self.error # saving error for next loop
		return self.mv

		