from physicochemical_properties import liquor_properties, water_properties, vapor_properties
liquor_prop=liquor_properties()
water_prop=water_properties()
vapor_prop=vapor_properties()

class update_flow_data():

	def update_vapor(self,Pvin):
		Tvin=vapor.temperature(Pvin)

		pv=vapor_prop.density(Pvin)

		uv=vapor_prop.viscosity(Tvin)

		Hv=vapor_prop.enthalpy(Tvin,Pvin)

		Yv=vapor_prop.thermal_conductivity(Tvin)

		Cpv=Hv/Tvin

		Hvw=Hv-water_prop.enthalpy(Tvin)

		return Tvin,pv,uv,Hv,Yv,Cpv,Hvw


	def update_juice(self,Bj,Zj,Tj):


		Cpj=liquor_prop.heat_capacity(Tj,Bj,Zj)

		pj=liquor_prop.density(Tj,Bj,Zj)

		uj=liquor_prop.viscosity(Tj,Bj,Zj)

		Hj=Cpj*Tj

		Yj=liquor_prop.thermal_conductivity(Tj,Bj)

		return Cpj,pj,uj,Hj,Yj

	def update_water(self,Tw):
		pw=water_prop.density(Tw)

		Hw=water_prop.enthalpy(Tw)

		return pw,Hw


class juice():
	'''
	Juice calculations and properties

	Parameters:
	mj 	: Juice mass flow [t/h]
	Pj 	: Juice pressure [Pa]
	Tj 	: Juice temperature [C]
	Bj	: Juice brix [kg/kg]
	Zj	: Juice purity [kg/kg]
	Ij 	: Insolubles of the juice [kg/kg]
	pHj : Juice pH

	'''
	def __init__(self,mj,Pj,Tj,Bj,Zj,Ij,pHj):
		self.mj = mj
		self.Pj = Pj
		self.Tj = Tj
		self.Bj = Bj
		self.Zj = Zj
		self.Ij = Ij
		self.pHj = pHj

		#Instance properties
		self.properties()
		#Volumetric flow [m3/s]
		self.Fj=(self.mj/3.6)/self.pj
		#Instance mass components
		self.mass()
		

	def update(self,mj,Pj,Tj,Bj,Zj,Ij,pHj):
		''' Update class parameters '''

		self.mj = mj
		self.Pj = Pj
		self.Tj = Tj
		self.Bj = Bj
		self.Zj = Zj
		self.Ij = Ij
		self.pHj = pHj

		#Instance properties
		self.properties()
		#Volumetric flow [m3/s]
		self.Fj=(self.mj/3.6)/self.pj
		#Instance mass components
		self.mass()

		pass

	def properties(self):
		''' Calculate juice properties'''

		#Juice density [kg/m3]
		self.pj= liquor_prop.density(self.Tj,self.Bj,self.Zj)
		#Juice viscosity [Pa s]
		self.uj = liquor_prop.viscosity(self.Tj,self.Bj,self.Zj)
		#Juice specific heat capacity [J/(kg.K)]
		self.Cpj = liquor_prop.heat_capacity(self.Tj,self.Bj,self.Zj)
		#Juice Enthalpy [J/kg]
		self.Hj = self.Cpj*self.Tj
		#Juice thermal conductivity [W/(m.K)]
		self.Yj = liquor_prop.thermal_conductivity(self.Tj,self.Bj)



	def properties_calc(self,Tj,Bj,Zj):
		''' Calculate juice properties without update class parameters'''

		#Juice density [kg/m3]
		pj= liquor_prop.density(Tj,Bj,Zj)
		#Juice viscosity [Pa s]
		uj = liquor_prop.viscosity(Tj,Bj,Zj)
		#Juice specific heat capacity [J/(kg.K)]
		Cpj = liquor_prop.heat_capacity(Tj,Bj,Zj)
		#Juice Enthalpy [J/kg]
		Hj = Cpj*Tj
		#Juice thermal conductivity [W/(m.K)]
		Yj = liquor_prop.thermal_conductivity(Tj,Bj)

		return Cpj,pj,uj,Hj,Yj

		pass

	def mass(self):
		'''Calculate mass components of juice'''

		#Water component of juice [m3/s]
		self.water_f = self.mj*(1 - self.Bj - self.Ij)
		#Insoluble solides component of juice [m3/s]
		self.insoluble_f = self.mj*self.Ij
		#Sucrose component of juice [m3/s]
		self.sucrose_f = self.mj*(self.Bj*self.Zj)
		#No sucrose component of juice [m3/s]
		self.nosucrose_f =self.mj*(self.Bj*(1-self.Zj))
		#Solids component of juice [m3/s]
		self.solids_f = self.mj*self.Bj
		# mj = water_f + insoluble_f + sucrose_f + self.nosucrose_f
		# solids_f = sucrose_f + self.nosucrose_f
	
	def mass_calc(self,mj,Bj,Zj,Ij):
		'''Calculate mass components of juice without update class parameters'''

		#Water component of juice [m3/s]
		water_f = mj*(1 - Bj - Ij)
		#Insoluble solides component of juice [m3/s]
		insoluble_f = mj*Ij
		#Sucrose component of juice [m3/s]
		sucrose_f = mj*(Bj*Zj)
		#No sucrose component of juice [m3/s]
		nosucrose_f = mj*(Bj*(1-Zj))
		#Solids component of juice [m3/s]
		solids_f = mj*(Bj)

		return water_f,insoluble_f,sucrose_f,nosucrose_f,solids_f

	def __add__(self,other):
		total_mj=self.mj+other.mj

		total_Pj=max(self.Pj,other.Pj)
		total_Tj=((self.mj*self.Tj*self.Cpj)+(other.mj*other.Tj*other.Cpj))/(self.Cpj*self.mj+other.Cpj*other.mj)
		total_pHj=(self.pHj*(self.mj/(self.mj+other.mj)))+(other.pHj*(other.mj/(self.mj+other.mj)))

		total_water_f=self.water_f+other.water_f
		total_insoluble_f=self.insoluble_f+other.insoluble_f
		total_sucrose_f=self.sucrose_f+other.sucrose_f
		total_solids_f=self.solids_f+other.solids_f
		
		
		total_Ij=(total_insoluble_f/total_mj)
		total_Bj=(total_solids_f/total_mj)
		total_Zj=((total_sucrose_f/total_mj)+total_Ij)/total_Bj

		return juice(total_mj,total_Pj,total_Tj,total_Bj,total_Zj,total_Ij,total_pHj)

		pass

class vapor():
	'''
	Vapor calculations and properties

	Parameters:
	mv 	: Vapor mass flow [t/h]
	Pv 	: Vapor pressure [Pa]
	Tv 	: Vapor temperature [C]

	'''
	def __init__(self,mv,Pv,Tv):
		self.mv = mv
		self.Pv = Pv
		self.Tv = Tv

		if self.Tv==None:
			#Instance properties of saturated vapor
			self.saturated_properties()
			#Volumetric flow [m3/s]
			self.Fv=(self.mv/3.6)/self.pv
		

	def update(self,mv,Pv,Tv):
		''' Update class parameters '''
		self.mv = mv
		self.Pv = Pv
		self.Tv = Tv

		if self.Tv==None:
			#Instance properties of saturated vapor
			self.saturated_properties()
			#Volumetric flow [m3/s]
			self.Fv=(self.mv/3.6)/self.pv

	def saturated_properties(self):
		''' Calculate vapor properties'''

		#Vapor temperature [C]
		self.Tv=vapor_prop.temperature(self.Pv)
		#Vapor density [kg/m3]
		self.pv=vapor_prop.density(self.Pv)
		#Vapor viscosity [Pa s]
		self.uv=vapor_prop.viscosity(self.Tv)
		#Vapor Enthalpy [J/kg]
		self.Hv=vapor_prop.enthalpy(self.Tv,self.Pv)
		#Vapor thermal conductivity [W/(m.K)]
		self.Yv=vapor_prop.thermal_conductivity(self.Tv)
		#Vapor specific heat capacity [J/(kg.K)]
		self.Cpv=self.Hv/self.Tv
		#Vapor evaporation enthalpy [J/kg]
		self.Hvw=self.Hv-water_prop.enthalpy(self.Tv)

	def saturated_properties_calc(self,Pv):
		''' Calculate vapor properties without update class parameters'''

		#Vapor temperature [C]
		Tv=vapor_prop.temperature(Pv)
		#Vapor density [kg/m3]
		pv=vapor_prop.density(Pv)
		#Vapor viscosity [Pa s]
		uv=vapor_prop.viscosity(Tv)
		#Vapor Enthalpy [J/kg]
		Hv=vapor_prop.enthalpy(Tv,Pv)
		#Vapor thermal conductivity [W/(m.K)]
		Yv=vapor_prop.thermal_conductivity(Tv)
		#Vapor specific heat capacity [J/(kg.K)]
		Cpv=Hv/Tv
		#Vapor evaporation enthalpy [J/kg]
		Hvw=Hv-water_prop.enthalpy(Tv)

		return Tv,pv,uv,Hv,Yv,Cpv,Hvw

class water(juice):
	'''
	Water calculations and properties

	Parameters:
	mw 	: Water mass flow [t/h]
	Pw 	: Water pressure [Pa]
	Tw 	: Water temperature [C]
	pHw : Water pH

	'''
	def __init__(self,mw,Pw,Tw,pHw):
		juice.__init__(self,mw,Pw,Tw,0.0,1.0,0.0,pHw)
		self.mw = mw
		self.Pw = Pw
		self.Tw = Tw
		self.pHw= pHw
		self.Fw=self.Fj
		self.Hw=self.Hj
		self.pw=self.pj
		self.Cpw=self.Cpj

	def update(self,mw,Pw,Tw,pHw):
		juice.__init__(self,mw,Pw,Tw,0.0,1.0,0.0,pHw)
		self.mw = mw
		self.Pw = Pw
		self.Tw = Tw
		self.pHw= pHw
		self.Fw=self.Fj
		self.Hw=self.Hj
		self.pw=self.pj
		self.Cpw=self.Cpj

	def properties_calc(self,Tw):
		''' Calculate water properties without update class parameters'''

		#Water density [kg/m3]
		pw=water_prop.density(Tw)
		#Water Enthalpy [J/kg]
		Hw=water_prop.enthalpy(Tw)

		return pw,Hw

	def __add__(self,other):

		self.mw = self.mj
		self.Pw = self.Pj
		self.Tw = self.Tj
		self.pHw= self.pHj
		self.Fw=self.Fj
		self.Hw=self.Hj
		self.pw=self.pj
		self.Cpw=self.Cpj


		total_mw=self.mw+other.mw

		total_Pw=max(self.Pw,other.Pw)
		total_Tw=((self.mw*self.Tw*self.Cpw)+(other.mw*other.Tw*other.Cpw))/(self.Cpw*self.mw+other.Cpw*other.mw)
		total_pHw=(self.pHw*(self.mw/(self.mw+other.mw)))+(other.pHw*(other.mw/(self.mw+other.mw)))

		return water(total_mw,total_Pw,total_Tw,total_pHw)

	

Juice=juice(103,400*(10**3),77, 0.15,0.87,0.008,7.5)
mj=(Juice.water_f + Juice.insoluble_f + Juice.sucrose_f + Juice.nosucrose_f )
print(Juice.mj)
print(mj)
####
print(Juice.solids_f)
print(Juice.sucrose_f + Juice.nosucrose_f )

Juice2=juice(105,410*(10**3),78, 0.17,0.97,0.01,8)

Juice3=Juice+Juice2
print(Juice3.Tj)

Water=water(100,200*(10**3),120,2.0)
print(Water.pw)
print(Water.Hw)
print(Water.properties_calc(120))

Water2=water(100,200*(10**3),70,2.0)
Water3=Water+Water2
print(Water3.Tw)







