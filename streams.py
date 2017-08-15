#-*- coding: utf-8 -*-
#! python

# Local Libs
from physicochemical_properties import liquor_properties, water_properties, vapor_properties

liquor_prpty=liquor_properties()
water_prpty=water_properties()
vapor_prpty=vapor_properties()


class juice():
	'''
	Juice calculations and properties

	Parameters:
	Mj 	: Juice mass flow [kg/s]
	Pj 	: Juice pressure [Pa]
	Tj 	: Juice temperature [C]
	Bj	: Juice brix [kg/kg]
	Zj	: Juice purity [kg/kg]
	Ij 	: Insolubles of the juice [kg/kg]
	pHj : Juice pH

	'''
	def __init__(self, Mj, Pj, Tj, Bj, Zj, Ij, pHj):
		self.Mj = Mj
		self.Pj = Pj
		self.Tj = Tj
		self.Bj = Bj
		self.Zj = Zj
		self.Ij = Ij
		self.pHj = pHj

		#Instance properties
		self.properties()
		#Volumetric flow [m3/s]
		self.Fj = (self.Mj)/self.pj
		#Instance mass components
		self.mass()
	
	def comparation(self, juice_data):

		
		result =(self.Mj !=float(juice_data[0]) or
			self.Tj !=float(juice_data[1]) or
			self.Bj !=float(juice_data[2]) or
			self.Zj !=float(juice_data[3]) or
			self.Ij !=float(juice_data[4]) or
			self.pHj !=float(juice_data[5]) or
			self.Pj !=float(juice_data[6]) )

		return result

	def update(self, Mj, Pj, Tj, Bj, Zj, Ij, pHj):
		''' Update class parameters '''

		self.Mj = Mj
		self.Pj = Pj
		self.Tj = Tj
		self.Bj = Bj
		self.Zj = Zj
		self.Ij = Ij
		self.pHj = pHj

		#Instance properties
		self.properties()
		#Volumetric flow [m3/s]
		self.Fj = (self.Mj)/self.pj
		#Instance mass components
		self.mass()

	def update_(self):
		#Instance properties
		self.properties()
		#Volumetric flow [m3/s]
		self.Fj = (self.Mj)/self.pj
		#Instance mass components
		self.mass()

	def properties(self):
		''' Calculate juice properties'''

		#Juice density [kg/m3]
		self.pj = liquor_prpty.density(self.Tj,self.Bj,self.Zj)
		#Juice viscosity [Pa s]
		self.uj = liquor_prpty.viscosity(self.Tj,self.Bj,self.Zj)
		#Juice specific heat capacity [J/(kg.K)]
		self.Cpj = liquor_prpty.heat_capacity(self.Tj,self.Bj,self.Zj)
		#Juice Enthalpy [J/kg]
		self.Hj = self.Cpj*self.Tj
		#Juice thermal conductivity [W/(m.K)]
		self.Yj = liquor_prpty.thermal_conductivity(self.Tj,self.Bj)



	def properties_calc(self, Tj, Bj, Zj):
		''' Calculate juice properties without update class parameters'''

		#Juice density [kg/m3]
		pj = liquor_prpty.density(Tj,Bj,Zj)
		#Juice viscosity [Pa s]
		uj = liquor_prpty.viscosity(Tj,Bj,Zj)
		#Juice specific heat capacity [J/(kg.K)]
		Cpj = liquor_prpty.heat_capacity(Tj,Bj,Zj)
		#Juice Enthalpy [J/kg]
		Hj = Cpj*Tj
		#Juice thermal conductivity [W/(m.K)]
		Yj = liquor_prpty.thermal_conductivity(Tj,Bj)

		return Cpj,pj,uj,Hj,Yj
		pass

	def mass(self):
		'''Calculate mass components of juice'''

		#Water component of juice [m3/s]
		self.water_f = self.Mj*(1 - self.Bj - self.Ij)
		#Insoluble solides component of juice [m3/s]
		self.insoluble_f = self.Mj*self.Ij
		#Sucrose component of juice [m3/s]
		self.sucrose_f = self.Mj*(self.Bj*self.Zj)
		#No sucrose component of juice [m3/s]
		self.nosucrose_f =self.Mj*(self.Bj*(1-self.Zj))
		#Solids component of juice [m3/s]
		self.solids_f = self.Mj*self.Bj
		# Mj = water_f + insoluble_f + sucrose_f + self.nosucrose_f
		# solids_f = sucrose_f + self.nosucrose_f
	
	def mass_calc(self, Mj, Bj, Zj, Ij):
		'''Calculate mass components of juice without update class parameters'''

		#Water component of juice [m3/s]
		water_f = Mj*(1 - Bj - Ij)
		#Insoluble solides component of juice [m3/s]
		insoluble_f = Mj*Ij
		#Sucrose component of juice [m3/s]
		sucrose_f = Mj*(Bj*Zj)
		#No sucrose component of juice [m3/s]
		nosucrose_f = Mj*(Bj*(1-Zj))
		#Solids component of juice [m3/s]
		solids_f = Mj*(Bj)

		return water_f, insoluble_f, sucrose_f, nosucrose_f, solids_f

	def __add__(self, other):
		total_Mj = self.Mj+other.Mj

		total_Pj = max(self.Pj,other.Pj)
		total_Tj = ((self.Mj*self.Tj*self.Cpj)+(other.Mj*other.Tj*other.Cpj))/(self.Cpj*self.Mj+other.Cpj*other.Mj)
		total_pHj = (self.pHj*(self.Mj/(self.Mj+other.Mj))) + (other.pHj*(other.Mj/(self.Mj+other.Mj)))

		total_water_f = self.water_f + other.water_f
		total_insoluble_f = self.insoluble_f + other.insoluble_f
		total_sucrose_f = self.sucrose_f + other.sucrose_f
		total_solids_f = self.solids_f + other.solids_f
		
		total_Ij = (total_insoluble_f/total_Mj)
		total_Bj = (total_solids_f/total_Mj)
		total_Zj = ((total_sucrose_f/total_Mj) + total_Ij)/total_Bj

		return juice(total_Mj, total_Pj, total_Tj, total_Bj, total_Zj, total_Ij, total_pHj)
		pass

class water(juice):
	'''
	Water calculations and properties

	Parameters:
	Mw 	: Water mass flow [kg/s]
	Pw 	: Water pressure [Pa]
	Tw 	: Water temperature [C]
	pHw : Water pH

	'''
	def __init__(self, Mw, Pw, Tw, pHw):
		juice.__init__(self, Mw, Pw, Tw, 0.0, 0.0, 0.0, pHw)
		self.Mw = Mw
		self.Pw = Pw
		self.Tw = Tw
		self.pHw= pHw
		self.Fw = self.Fj
		self.Hw = self.Hj
		self.pw = self.pj
		self.Cpw = self.Cpj

	def update(self, Mw, Pw, Tw, pHw):
		juice.__init__(self, Mw, Pw, Tw, 0.0, 0.0, 0.0, pHw)
		self.Mw = Mw
		self.Pw = Pw
		self.Tw = Tw
		self.pHw = pHw
		self.Fw = self.Fj
		self.Hw = self.Hj
		self.pw = self.pj
		self.Cpw = self.Cpj


	def properties_calc(self,Tw):
		''' Calculate water properties without update class parameters'''

		#Water density [kg/m3]
		pw=water_prpty.density(Tw)
		#Water Enthalpy [J/kg]
		Hw=water_prpty.enthalpy(Tw)

		return pw,Hw

	def __add__(self,other):

		self.Mw = self.Mj
		self.Pw = self.Pj
		self.Tw = self.Tj
		self.pHw = self.pHj
		self.Fw = self.Fj
		self.Hw = self.Hj
		self.pw = self.pj
		self.Cpw = self.Cpj


		total_Mw = self.Mw + other.Mw

		total_Pw = max(self.Pw,other.Pw)
		total_Tw = ((self.Mw*self.Tw*self.Cpw) + (other.Mw*other.Tw*other.Cpw))/(self.Cpw*self.Mw+other.Cpw*other.Mw)
		total_pHw = (self.pHw*(self.Mw/(self.Mw+other.Mw))) + (other.pHw*(other.Mw/(self.Mw+other.Mw)))

		return water(total_Mw,total_Pw,total_Tw,total_pHw)

class vapor():
	'''
	Vapor calculations and properties

	Parameters:
	mv 	: Vapor mass flow [kg/s]
	Pv 	: Vapor pressure [Pa]
	Tv 	: Vapor temperature [C]

	'''
	def __init__(self, Mv, Pv, Tv):
		self.Mv = Mv
		self.Pv = Pv
		self.Tv = Tv

		if self.Tv==None:
			#Instance properties of saturated vapor
			self.saturated_properties()
			#Volumetric flow [m3/s]
			self.Fv = (self.Mv)/self.pv
		

	def update(self, Mv, Pv, Tv):
		''' Update class parameters '''
		self.Mv = Mv
		self.Pv = Pv
		self.Tv = Tv

		if self.Tv==None:
			#Instance properties of saturated vapor
			self.saturated_properties()
			#Volumetric flow [m3/s]
			self.Fv = (self.Mv)/self.pv

	def update_(self):
		if self.Tv==None:
			#Instance properties of saturated vapor
			self.saturated_properties()
			#Volumetric flow [m3/s]
			self.Fv = (self.Mv)/self.pv

	def comparation(self, vapor_data):
			
		result =(round(self.Mv,4) !=round(float(vapor_data[0]),4) or
			self.Pv !=float(vapor_data[6]) )

		return result


	def saturated_properties(self):
		''' Calculate vapor properties'''

		#Vapor temperature [C]
		self.Tv = vapor_prpty.temperature(self.Pv)
		#Vapor density [kg/m3]
		self.pv = vapor_prpty.density(self.Pv)
		#Vapor viscosity [Pa s]
		self.uv = vapor_prpty.viscosity(self.Tv)
		#Vapor Enthalpy [J/kg]
		self.Hv = vapor_prpty.enthalpy(self.Tv,self.Pv)
		#Vapor thermal conductivity [W/(m.K)]
		self.Yv = vapor_prpty.thermal_conductivity(self.Tv)
		#Vapor specific heat capacity [J/(kg.K)]
		self.Cpv = self.Hv/self.Tv
		#Vapor evaporation enthalpy [J/kg]
		self.Hvw = self.Hv - water_prpty.enthalpy(self.Tv)

	def saturated_properties_calc(self,Pv):
		''' Calculate vapor properties without update class parameters'''

		#Vapor temperature [C]
		Tv = vapor_prpty.temperature(Pv)
		#Vapor density [kg/m3]
		pv = vapor_prpty.density(Pv)
		#Vapor viscosity [Pa s]
		uv = vapor_prpty.viscosity(Tv)
		#Vapor Enthalpy [J/kg]
		Hv = vapor_prpty.enthalpy(Tv,Pv)
		#Vapor thermal conductivity [W/(m.K)]
		Yv = vapor_prpty.thermal_conductivity(Tv)
		#Vapor specific heat capacity [J/(kg.K)]
		Cpv = Hv/Tv
		#Vapor evaporation enthalpy [J/kg]
		Hvw = Hv - water_prpty.enthalpy(Tv)

		return Tv,pv,uv,Hv,Yv,Cpv,Hvw