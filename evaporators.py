#-*- coding: utf-8 -*-
#! python

# Installed Libs
import math
import numpy as np

from scipy.integrate import odeint

# Local Libs
from physicochemical_properties import *

liquor_prpty = liquor_properties()
water_prpty = water_properties()
vapor_prpty = vapor_properties()

class evaporator:
	'''
	Parameters:
	h, Calandria pipe heigth [m]
	A, Heat transfer area [m2]
	At, Transversal area [m2]
	V, Total volume of the evaporator [m3]
	Ne, Effect number []
	Op, Operation days [d]
	Ls, Heat losses [%]
	Lje, height of juice in the evaporator [] 0 to 1
	'''

	def __init__(self, h, A, At, V, Ne, Op, Ls, Lje):
		# Create evaporator desing properties
		self.h = h
		self.A = A
		self.At = At
		self.V = V
		self.Ne = Ne
		self.Op = Op
		self.Ls = Ls
		self.Lje = Lje
		self.mve0 = None

	def update(self, h, A, At, V, Ne, Op, Ls, Lje):
		# Update evaporator desing properties
		self.h = h
		self.A = A
		self.At = At
		self.V = V
		self.Ne = Ne
		self.Op = Op
		self.Ls = Ls
		self.Lje = Lje

	def in_out(self, juice_in, vapor_in, juice_out, vapor_out, vapor_use, condensate_out): #condensate_out
		self.juice_in = juice_in
		self.vapor_in = vapor_in
		self.juice_out = juice_out
		self.vapor_out = vapor_out
		self.vapor_use = vapor_use
		self.condensate_out = condensate_out

		
		if self.mve0 == None:
			deltaP0 = 62052.81563851526 # 9 psig
			self.mve0 = self.mve_init(vapor_in.Pv-deltaP0, self.V, self.At, self.h, self.Lje)

	def solve(self, time):

		#return self.juice_out, self.vapor_out #, self.condensate_out
		pass

	@classmethod # class method to be used with or without instance
	def htc_calc(cls, Op, Ne, Lje, Tjout, Bjout):
		pass

	# Internal use only, call in_out(...) method first
	def htc(self):
		pass

	@classmethod # class method to be used with or without instance
	def mass_vapor_in_calc(cls, A, Op, Ne, Lje, Tjout, Bjout, Pvin, Tvin):
		Hvin = vapor_prpty.enthalpy(Tvin,Pvin) - water_prpty.enthalpy(Tvin)
		U = cls.htc_calc(Op, Ne, Lje, Tjout, Bjout)

		Mvin = U*A*(Tvin - Tjout)/Hvin
		return Mvin

	def mass_vapor_in(self): 
		Tjout = self.juice_out.Tj
		Pvin = self.vapor_in.Pv
		Tvin = self.vapor_in.Tv

		Hvin = vapor_prpty.enthalpy(Tvin,Pvin) - water_prpty.enthalpy(Tvin)
		U = self.htc()

		Mvin = U*self.A*(Tvin - Tjout)/Hvin
		return Mvin

	def mass_vapor_out(self):
		U = self.htc()
		Mjin = self.juice_in.Mj
		Hjin = self.juice_in.Hj

		Hjout = self.juice_out.Hj

		Tvin = self.vapor_in.Tv
		Tjout = self.juice_out.Tj
		Hvv = self.vapor_out.Hv

		Mvv = (U*self.A*(Tvin - Tjout) + Mjin*Hjin - Mjin*Hjout)/(Hvv - Hjout)
		return Mvv

	@classmethod # class method to be used with or without instance
	def hydrostatic_pressure_calc(self, h, Tje, Bje, Zje):
		p = liquor_prpty.density(Tje, Bje, Zje)
		g = 9.7775 # Gravity in Cali, by latitude and height

		P_hyd = p*g*h
		return P_hyd

	def hydrostatic_pressure(self):
		Tje = self.juice_out.Tj
		Bje = self.juice_out.Bj
		Zje = self.juice_out.Zj

		p = liquor_prpty.density(Tje, Bje, Zje)
		g = 9.7775 # Gravity in Cali, by latitude and height
		h = self.h*self.Lje + self.hc

		self.P_hyd = p*g*h
		return self.P_hyd

	def residence_time(self):
		tr = 0
		return 0

	def sucrose_losses(self):
		#liquor_prpty.sucrose_losses()  
		#sucrose_losses(self, time, Temperature, Brix, SolIn, Purity, pH)
		return 0

	@staticmethod # static method to be used in scipy.integrate.odeint
	def model(x, t, A, h, At, Ls, Ne, Op,
						 Fjin, Tjin, Bjin, Zjin, Tvin, Fjout, Tjout, Pvv):

		# Initial conditions
		Bjout, Lje = x

		# Vapor in
		# Tvin = vapor_prpty.temperature(Pvin)
		# Hvin = vapor_prpty.enthalpy(Tvin,Pvin) - water_prpty.enthalpy(Tvin)

		# Vapor out
		Tvv = vapor_prpty.temperature(Pvv)
		Hvv = vapor_prpty.enthalpy(Tvv, Pvv) 

		# Heat capacity
		Cpjin = liquor_prpty.heat_capacity(Tjin, Bjin, Zjin)
		Cpjout = liquor_prpty.heat_capacity(Tjout, Bjout, Zjin)

		# Density
		pjin = liquor_prpty.density(Tjin, Bjin, Zjin)
		pjout = liquor_prpty.density(Tjout, Bjout, Zjin)

		# Heat transfer coefficient
		U = evaporator_roberts.htc_calc(Op, Ne, Lje, Tjout, Bjout)

		# Brix differential equation
		dBjout_dt = (1/(pjout*At*h*Lje))*( pjin*Fjin*Bjin + \
					pjin*Fjin*Bjout*((Cpjin*Tjin - Cpjout*Tjout)/(Hvv - Cpjout*Tjout) - 1) + \
					Bjout*U*A*(Tvin - Tjout)/(Hvv - Cpjout*Tjout))

		# Level differential equation
		dLje_dt = (1/(pjout*At*h))*( pjin*Fjin*(Hvv - Cpjin*Tjin)/(Hvv - Cpjout*Tjout) - \
					pjout*Fjout - U*A*(Tvin - Tjout)/(Hvv - Cpjout*Tjout))

		dx_dt = [dBjout_dt, dLje_dt]
		return dx_dt

	@staticmethod # static method to be used in scipy.integrate.odeint
	def model_ve(x, t, Mvv, Mvc):

		# Initial condition
		#mve = x

		# Massic flow differential equation
		dmve_dt = Mvv - Mvc

		return dmve_dt 

	def mve_init(self, Pvv, V, At, h, Lje):
		pvv = vapor_prpty.density_sat_low(Pvv)
		# print("pvv: " + str(pvv))
		Vve = V - At*h*Lje # Volume occupied by vapor inside the evaporator
		mve = pvv*Vve
		return mve

	def Pvv(self, mve): #V, At, h, Lje
		Vve = self.V - self.At*self.h*self.Lje # Volume occupied by vapor inside the evaporator
		pvv = mve/Vve
		# print("pvv: " + str(pvv))
		Pvv = vapor_prpty.pressure_sat_low(pvv)
		return Pvv

	def Tje(self, Pvv):
		Tje = self.juice_out.Tj
		Bje = self.juice_out.Bj
		Zje = self.juice_out.Zj
		h = self.h*self.Lje

		Ph = self.hydrostatic_pressure_calc(h, Tje, Bje, Zje)
		P = Pvv #+ 0.5*Ph
		Tje = liquor_prpty.boiling_point(P, Bje)
		return Tje


class evaporator_roberts(evaporator):
	'''
	Parameters:
	A, Heat transfer area [m2]
	h, Calandria pipe heigth [m]
	Np, Number of pipes []
	Di, Pipe internal diamenter [m]
	V, Total volume of the evaporator [m3]
	Dd, Downtake diameter [m]
	hc, Inferior cone heigth [m]
	Ne, Effect number []
	Op, Operation days [d]
	Ls, Heat losses [] 0 to 1
	Lje, height of juice in the evaporator [] 0 to 1
	'''

	def __init__(self, A, h, Np, Di, V, Dd, hc, Ne, Op, Ls, Lje):
		# Create evaporator desing properties
		self.Np = Np
		self.Di = Di
		self.Dd = Dd
		self.hc = hc

		At = math.pi*(Dd/2)**2 + Np*math.pi*(Di/2)**2
		evaporator.__init__(self, h, A, At, V, Ne, Op, Ls, Lje)

	def update(self, A, h, Np, Di, V, Dd, hc, Ne, Op, Ls, Lje):
		# Update evaporator desing properties
		self.Np = Np
		self.Di = Di
		self.Dd = Dd
		self.hc = hc

		At = math.pi*(Dd/2)**2 + Np*math.pi*(Di/2)**2
		evaporator.update(self, h, A, At, V, Ne, Op, Ls, Lje)
		# evaporator.__init__(self, h, A, At, V, Ne, Op, Ls, Lje)

	def solve(self, time):
		

		# Model parmeters
		u = (self.A, self.h, self.At, self.Ls, self.Ne, self.Op, self.juice_in.Fj, self.juice_in.Tj, self.juice_in.Bj, 
			self.juice_in.Zj, self.vapor_in.Tv, self.juice_out.Fj, self.juice_out.Tj, self.vapor_out.Pv)
		
		u_ve = (self.vapor_out.Mv, self.vapor_use.Mv)

		# Brix and Level Model
		x0 = self.juice_out.Bj, self.Lje

		sol1 = odeint(evaporator_roberts.model, x0, time, args=u)
		Bx = sol1[-1,0] # -1 = end, last value
		self.Lje = sol1[-1,1] # -1 = end, last value
		# self.x0 = Bx, self.Lv # ATTENTION define method for x0 and mve0

		sol2 = odeint(evaporator_roberts.model_ve, self.mve0, time, args=u_ve)
		mve = sol2[-1,0]
		self.mve0 = mve

		self.update(self.A, self.h,self.Np, self.Di, self.V, self.Dd, self.hc, self.Ne, self.Op, self.Ls, self.Lje)
		Mvin = self.mass_vapor_in()
		Mvv = self.mass_vapor_out()
		Pvv = self.Pvv(mve)
		Tjout = self.Tje(Pvv)

		self.vapor_in.Mv=Mvin
		self.vapor_in.update_()

		self.vapor_out.Mv=Mvv
		self.vapor_out.Pv=Pvv
		self.vapor_out.update_()

		self.juice_out.Tj=Tjout
		self.juice_out.Bj=Bx
		self.juice_out.update_()

		return self.juice_in, self.juice_out, self.vapor_in, self.vapor_out

	@classmethod # class method to be used with or without instance
	def htc_aus(cls, Bjout, Tje): # Australian typical OHTC for roberts evaporators, Wright 2008
		htc = 16.9390445*(Tje**1.0174)*(Bjout/(0.86 - Bjout))**-0.2695352
		return htc

	@classmethod # class method to be used with or without instance
	def htc_scaling(cls, Op, Ne): # Scale in evaporators based on Rosero 2008
		scale = {1: 0.0625,
					2: 0.0556,
					3: 0.0498,
					4: 0.0376,
					5: 0.0626,
					} #dictionary with scale values depending of effect
		htc = math.exp(-scale[Ne]*Op)
		return htc

	@classmethod # class method to be used with or without instance
	def htc_level(cls, Lje): # HTC factor depending on level, regression data from Hugot 1977
		htc = -6.1936*Lje**4 + 18.414*Lje**3 - 19.869*Lje**2 + 8.6037*Lje - 0.277
		htc = np.maximum(htc, 0.2) #Limit the minimum htc to 0.2
		return htc

		# if Lje > 0.07:
		# 	htc = -6.1936*Lje**4 + 18.414*Lje**3 - 19.869*Lje**2 + 8.6037*Lje - 0.277
		# else:
		# 	htc = 0.2
		# return htc

	@classmethod # class method to be used with or without instance
	def htc_calc(cls, Op, Ne, Lje, Tjout, Bjout):
		htc = cls.htc_aus(Bjout, Tjout)*cls.htc_scaling(Op, Ne)*cls.htc_level(Lje)
		return htc

	# Internal use only, call in_out(...) method first
	def htc(self):
		Bjout = self.juice_out.Bj
		Tjout = self.juice_out.Tj

		self.uhtc = self.htc_aus(Bjout, Tjout)*self.htc_scaling(self.Op, self.Ne)*self.htc_level(self.Lje)
		return self.uhtc