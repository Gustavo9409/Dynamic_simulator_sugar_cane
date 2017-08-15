#-*- coding: utf-8 -*-
#! python

# Installed Libs
import math
import numpy as np
from scipy.integrate import odeint


class valve:
	'''
	Parameters:
	Dv [m], Valve diameter
	Ap [], Aperture Value [0 to 1]
	'''

	def __init__(self, Dv, Ap, delay = 3.0):
		# Create valve properties
		self.Dv = Dv
		self.Ap = Ap
		self.delay = delay


	def update(self, Dv, Ap, delay = 3.0):
		# Update valve properties
		self.Dv = Dv
		self.Ap = Ap
		self.delay = delay

	def in_out(self, stream_in, stream_out, Ap):
		self.stream_in = stream_in
		self.stream_out = stream_out
		self.Ap0 = self.Ap
		self.Ap = Ap

	def solve(self, time):
		pass

	# def aperture(self, Ap, delay = 3.0):
	# 	Tao = delay/5
	# 	self.Ap = Ap*(1-math.exp(-t/Tao))
	
	@staticmethod # static method to be used in scipy.integrate.odeint
	def model(x, t, Ap, delay):
		Tao = delay/5
		V = x

		dV_dt = (Ap - V)/Tao
		
		return dV_dt

	def lineal(self, cvmax, Ap):
		self.Rf = (7.598054212083366e-07)*cvmax*Ap
		return self.Rf

	def equal_percentage(self, cvmin, cvmax, Ap):
		# Flow coefficient in [m3*sqrt(Pa)/s]
		qmin = cvmin
		qmax = cvmax
		self.Cv = qmin*(qmax/qmin)**Ap
		print ("Cv: "+str(self.Cv)+" con Ap: "+str(self.Ap)+" y Dv: "+str(self.Dv))
		self.Rf = self.Cv*7.598054212083366e-07 #Units conversion gpm/sqrt(psi)
		return self.Rf

	def coefficient(self):
		pass

	def flow(self):
		pass

	def flow_calc(self, Pin, Pout, pout, Rf):
		pass

	def pressure(self):
		pass

	def pressure_calc(self, Pin, Fout, pout, Rf):
		pass

class valve_vapor(valve):
	'''
	Equations form Dia-Flo Diaphragm Valves
	'''
	def solve(self, time, _type,Cvmin,Cvmax):
		stream_in = self.stream_in
		stream_out = self.stream_out

		# Delay response model
		x0 = self.Ap0
		u = (self.Ap, self.delay)

		sol = odeint(valve.model, x0, time, args=u)
		self.Ap = sol[-1,0]
		self.Ap0 = self.Ap

		# Valve model, pressure
		if _type=="Diametro":
			self.coefficient()
		elif _type=="Coeficientes de flujo":
			self.equal_percentage(Cvmin,Cvmax,self.Ap)
		
		stream_out.Pv=self.pressure()
		
		stream_out.update_()

		stream_in.Mv = stream_out.Mv
		stream_in.update_()
		
		
		return stream_in, stream_out


	# def coefficient(self):
	# 	# Assumend typical for steam valves, lineal
	# 	# Based on Fisher TBX steam conditioning valves.
	# 	Cvmax = 21267.14875*self.Dv**2 + 6869.27004*self.Dv - 884.31123
	# 	self.Cv = Cvmax*self.Ap
	# 	print ("Vapor!! Cv: "+str(self.Cv)+" con Ap: "+str(self.Ap)+" y Dv: "+str(self.Dv))
	# 	self.Rf = self.Cv*7.598054212083366e-07 #Units conversion gpm/sqrt(psi)
	# 	return self.Rf

	# def flow(self):
	# 	Pin = self.stream_in.Pv
	# 	Pout = self.stream_out.Pv
	# 	pout = self.stream_out.pv
	# 	Tout=self.stream_out.Tv

	# 	pw = 1000.0
	# 	G = pout/pw

	# 	Touta = Tout + 237.15

	# 	Fout = (1360.0/61.8903927797)*self.Rf*math.sqrt((Pin - Pout)/(G*Touta))*math.sqrt((Pin + Pout)/2.0)
	# 	return Fout

	# def pressure(self):
	# 	Pin = self.stream_in.Pv
	# 	Fout = self.stream_out.Fv
	# 	pout = self.stream_out.pv
	# 	Tout=self.stream_out.Tv

	# 	Tout_abs=Tout+237.15

	# 	pw = 1000.0
	# 	G = pout/pw

	# 	# Pout = - Pin - Pin_abs + math.sqrt(Pin_abs**2 - G*Tout*(Fout/963*self.Rf)**2)
	# 	Pout_abs = math.sqrt(Pin**2 - (G*Tout_abs)*((Fout*7.86579072e-06)/963*self.Rf)**2)
	# 	Pout=Pout_abs-89325.99
	# 	print("Vapor Pout: "+str(Pout))
	# 	#TODO: Check because Pin is already abs
	# 	return Pout

	##Temporaly liquid equations

	def coefficient(self):
		# Assumend typical for butterfly valves, isoporcentual
		# Based on Bray 40 valves. Class 300
		self.Cv = 393.408270437072*self.Ap*self.Dv + 42323.6170171287*(self.Ap**2)*(self.Dv**2) + 14.0060365876889*self.Ap**3
		# print ("Cv: "+str(self.Cv)+" con Ap: "+str(self.Ap)+" y Dv: "+str(self.Dv))
		self.Rf = self.Cv*7.598054212083366e-07 #Units conversion gpm/sqrt(psi)
		# print self.Rf
		return self.Rf

	def flow(self):
		Pin = self.stream_in.Pv
		Pout = self.stream_out.Pv
		pout = self.stream_out.pv
		pw = 1000.0
		G = pout/pw
		Fout = self.Rf*math.sqrt((Pin - Pout)/G)
		return Fout

	def pressure(self):
		Pin = self.stream_in.Pv
		Fout = self.stream_out.Fv
		pout = self.stream_out.pv
		pw = 1000.0
		G = pout/pw
		# print(str(Pin)+" "+str(Fout)+" "+str(pout)+" "+str(G)+ " "+str(self.Rf))
		# Pout = Pin - (G*((Fout/(self.Rf*55.0))**2.0))
		Pout = Pin - (G*((Fout/(self.Rf*0.703))**2.0))
		if Pout<100000.0:
			Pout=100000.0
		return Pout


class valve_liquid(valve):
	'''
	Standard liquid equations. Emerson Technical Report of Valve Sizing Calculations
	'''
	def solve(self, time, _type,Cvmin,Cvmax):
		stream_in = self.stream_in
		stream_out = self.stream_out

		# Delay response model
		x0 = self.Ap0
		u = (self.Ap, self.delay)

		sol = odeint(valve.model, x0, time, args=u)
		self.Ap = sol[-1,0]
		self.Ap0 = self.Ap

		# Valve model, pressure
		if _type=="Diametro":
			self.coefficient()
		elif _type=="Coeficientes de flujo":
			self.equal_percentage(Cvmin,Cvmax,self.Ap)
		
		# stream_out.update(self.flow()*stream_out.pj, self.pressure(), stream_out.Tj, stream_out.Bj, stream_out.Zj, stream_out.Ij, stream_out.pHj)
		stream_out.Pj=self.pressure()
		# stream_out.Mj=(self.flow())*stream_out.pj
		# stream_out.update_()
		
		stream_out.update_()


		# stream_out.Pj = self.pressure()
		# stream_out.update_()
		
		stream_in.Mj = stream_out.Mj
		stream_in.update_()
		
		
		return stream_in, stream_out

	def coefficient(self):
		# Assumend typical for butterfly valves, isoporcentual
		# Based on Bray 40 valves. Class 300
		self.Cv = 393.408270437072*self.Ap*self.Dv + 42323.6170171287*(self.Ap**2)*(self.Dv**2) + 14.0060365876889*self.Ap**3
		# print ("Cv: "+str(self.Cv)+" con Ap: "+str(self.Ap)+" y Dv: "+str(self.Dv))
		self.Rf = self.Cv*7.598054212083366e-07 #Units conversion gpm/sqrt(psi)
		return self.Rf

	def flow_calc(self, Pin, Pout, pout, Rf):
		pw = 1000.0
		G = pout/pw
		Fout = Rf*math.sqrt((Pin - Pout)/G)
		return Fout

	def flow(self):
		Pin = self.stream_in.Pj
		Pout = self.stream_out.Pj
		pout = self.stream_out.pj
		pw = 1000.0
		G = pout/pw
		Fout = self.Rf*math.sqrt((Pin - Pout)/G)
		return Fout

	def pressure_calc(self, Pin, Fout, pout, Rf):
		pw = 1000.0
		G = pout/pw
		Pout = Pin - G*(Fout/Rf)**2
		return Pout

	def pressure(self):
		Pin = self.stream_in.Pj
		Fout = self.stream_out.Fj
		pout = self.stream_out.pj
		pw = 1000.0
		G = pout/pw
		# print(str(Pin)+" "+str(Fout)+" "+str(pout)+" "+str(G)+ " "+str(self.Rf))
	
		Pout = Pin - (G*((Fout/self.Rf)**2))

		return Pout


		