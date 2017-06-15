import math

from physicochemical_properties import liquor_properties
from physicochemical_properties import water_properties
from physicochemical_properties import vapor_properties

liquor=liquor_properties()
water=water_properties()
vapor=vapor_properties()


class heater_shell_tube:
	# Heater parameters:
	# Np, Number of pipes per step []
	# Nst, Number of steps []
	# Dosp, Pipe external diamenter [in]
	# Lp, Pipe Length [m]
	# Ip, Pipe thickness [mm]
	# Ep, Pipe roughness [mm]
	# Gf, Scale factor (fouling) []
	# Op, Operation hours [hr]

	def __init__(self, Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op):
		self.Np = Np
		self.Nst = Nst
		self.Dosp = Dosp
		self.Lp = Lp
		self.Ip = Ip
		self.Ep = Ep
		self.Gf = Gf
		self.Op = Op
		self.properties()

	def properties(self):
		# Compute heater design properties
		# Pipe internal diameter [in]
		self.Disp = Dosp - (2*(Ip/25.4))

		# Internal heat transfer area [m2]
		self.Aisc=0.0254*math.pi*self.Disp*self.Np*self.Lp*self.Nst

		# External heat transfer area [m2]
		self.Aosc=0.0254*math.pi*self.Dosp*self.Np*self.Lp*self.Nst

		# Internal HTC
		self.Ui=self.internal_u(self.Np, self.Dosp, self.Ip, self.Ep, 
						self.Fjin,self.Tjin,self.Bjin,self.Zjin)

		# External HTC
		self.Uo=self.external_u(self.Dosp, self.Tvin, self.Pvin, self.Tjc)

	def fluid_properties(self):

		#Juice density
		self.pjin = liquor.density(self.Tjin,self.Bjin,self.Zjin)

		# Juice velocity
		self.vj = (4*((self.Fjin*self.pjin)))/(self.Np*self.pjin*math.pi*((0.0254*self.Disp)**2))

		#Scale resistance
		self.Ri = ((3.5*10**-6)*(self.Op**self.Gf))*(1+(10.73/(self.vj**3)))



	def update(self, Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op):
		# Update hearer desing properties
		self.Np = Np
		self.Nst = Nst
		self.Dosp = Dosp
		self.Lp = Lp
		self.Ip = Ip
		self.Ep = Ep
		self.Gf = Gf
		self.Op = Op
		self.properties()

	@staticmethod
	def model_temperature(x, t, Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op,
						 Fjin, Tjin, Bjin, Zjin, Pvin):
		
		#Initial output of juice temperature
		Tjout=x[0]

		# Np = u[0]; Nst=u[1]; Lp = u[2]; dp = u[3]; Dosp = u[4]; Fjin=u[5]; Bjin = u[6]; 
		# Zjin = u[7]; Tjin = u[8]; Pvin = u[9];  Ep = u[10]; B=u[11]; Hrop= u[12];

		# Inside diameter of pipe
		Disp = Dosp - (2*(Ip/25.4))
		
		# Heat exchanger heat transfer area.
		Ac = 0.0254*math.pi*Dosp*Np*Lp*Nst

		# Medium Temperature
		Tjc = (Tjin + Tjout)/2.0

		# Vapor temperature
		Tvin = vapor.temperature(Pvin)

		# Media Heat capacitie
		Cpjc = liquor.heat_capacity(Tjc,Bjin,Zjin)

		# Media Densitie
		pjc = liquor.density(Tjc,Bjin,Zjin)

		# Mass of juice inside the heater
		mjc = pjc*Np*Nst*(math.pi*(((0.0254*Disp)/2.0)**2.0))*Lp

		# Hear Transfer Coeficient
		htc1=htc_shell_tube()
		U = htc1.overall_u(Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op,
					  			Fjin, Tjin, Bjin, Zjin, Tvin, Pvin, Tjc)
		
		delta_t = deltatlog(Tjin, Tjout, Tvin)
		
		dTjout = ((U*Ac*delta_t)+(pjc*Fjin*Cpjc*Tjin)-(pjc*Fjin*Cpjc*Tjout))/(0.5*mjc*Cpjc)
		if t>0.0:
			dy=dTjout
		else:
			dy=0		
		return dy



class htc_shell_tube: #Heat Transfer Coefficient (HTC)
	'''
	Heat transfer coefficient for shell and tube heaters. 
	Based on Kreith, Frank, Raj M Manglik, Mark S Bohn, and S G Kandlikar. 2012. 
	Handbook of Phase Change: Boiling and Condensation Principles of Heat Transfer.

	Heater variables:
	Np, Number of pipes per step []
	Nst, Number of steps []
	Dosp, Pipe external diamenter [in]
	Lp, Pipe Length [m]
	Ip, Pipe thickness [mm]
	Ep, Pipe roughness [mm]
	Gf, Scale factor (fouling) []
	Op, Operation hours [hr]

	Juice variables:
	Fjin, Juice volumetric flow inlet [m3/s]
	Tjin, Juice temperature inlet [C]
	Bjin, Juice Brix inlet [kg/kg]
	Zjin, Juice purity inlet [kg/kg]

	Vapor variables:
	Tvin, Vapor temperature inlet [C]
	Pvin, Vapor pressure inlet [Pa]
	Tjc, Medium temperature in heater [C]
	
	Calculated variables:
	Aisc, Internal heat transfer area [m2]
	Aosc, External heat transfer area [m2]
	Disp, Pipe internal diameter [in]
	'''
	def update_juice_properties(self):
		self.Fjin = Fjin
		self.Tjin = Tjin
		self.Bjin = Bjin
		self.Zjin = Zjin
		self.Tvin = Tvin
		self.Pvin = Pvin

	
	def internal_u(self, Np, Dosp, Ip, Ep, Fjin, Tjin, Bjin, Zjin):
		self.Np = Np
		self.Dosp = Dosp
		self.Ip = Ip
		self.Ep = Ep
		self.Fjin = Fjin
		self.Tjin = Tjin
		self.Bjin = Bjin
		self.Zjin = Zjin

		# Pipe internal diameter [in]
		self.Disp = Dosp - (2*(Ip/25.4))

		# Juice viscosity
		self.ujin = liquor.viscosity(self.Tjin, self.Bjin, self.Zjin)
		# Juice density
		self.pjin = liquor.density(self.Tjin, self.Bjin, self.Zjin)
		# Juice thermal conductivity
		self.Yjin = liquor.thermal_conductivity(self.Tjin, self.Bjin)
		# Juice Specific Heat
		self.Cpjin = liquor.heat_capacity(self.Tjin, self.Bjin, self.Zjin)

		# Relative roughness
		Er = self.Ep/(25.4*self.Disp)
		# Reynolds
		Re = (4*((self.Fjin*self.pjin)/self.Np))/(0.0254*math.pi*self.Disp*self.ujin)
		# Friction factor
		f = 0.25/((math.log((Er/3.7)+(5.74/(Re**0.9))))**2.0)
		# Prandlt
		Pr = (self.Cpjin*self.ujin)/self.Yjin
		# Nusselt-Gnilinski
		Nu = ((f/8.0)*(Re-1000.0)*Pr)/(1+(12.7*((f/8.0)**0.5)*((Pr**(2.0/3.0))-1.0)))

		# Internal HTC
		Ui = (Nu*self.Yjin)/((25.4*self.Disp)/1000)
		return Ui

	def external_u(self, Dosp, Tvin, Pvin, Tjc):
		self.Dosp = Dosp
		self.Tvin = Tvin
		self.Pvin = Pvin
		self.Tjc = Tjc

		# Temperature beetween satured vapor and pipe wall
		self.Tvp = self.Tvin-((self.Tjc+self.Tvin)/2)

		# Vapor viscosity
		self.uvin = vapor.viscosity(self.Tvin)
		# Vapor enthalpy
		self.Hvin = vapor.enthalpy(self.Tvin, self.Pvin) - water.enthalpy(self.Tvin)
		# Vapor thermal conductivity
		self.Yvin = vapor.thermal_conductivity(self.Tvin)
		
		# Water density
		self.pw = water.density(self.Tvin)
		
		# Gravity
		g=9.80665

		# External HTC
		Uo=0.725*(((g*(self.Yvin**3)*(self.pw**2)*self.Hvin)/(0.0254*self.Dosp*self.Tvp*self.uvin))**0.25)
		return Uo

	def overall_u(self, Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op,
				  Fjin, Tjin, Bjin, Zjin, Tvin, Pvin, Tjc):

		self.Np = Np
		self.Nst = Nst
		self.Dosp = Dosp
		self.Lp = Lp
		self.Ip = Ip
		self.Ep = Ep
		self.Gf = Gf
		self.Op = Op

		self.Fjin = Fjin
		self.Tjin = Tjin
		self.Bjin = Bjin
		self.Zjin = Zjin
		self.Tvin = Tvin
		self.Pvin = Pvin
		self.Tjc = Tjc

		# Pipe internal diameter [in]
		self.Disp = Dosp - (2*(Ip/25.4))

		# Internal heat transfer area [m2]
		self.Aisc=0.0254*math.pi*self.Disp*self.Np*self.Lp*self.Nst

		# External heat transfer area [m2]
		self.Aosc=0.0254*math.pi*self.Dosp*self.Np*self.Lp*self.Nst

		# Internal HTC
		Ui=self.internal_u(self.Np, self.Dosp, self.Ip, self.Ep, 
						self.Fjin,self.Tjin,self.Bjin,self.Zjin)

		# External HTC
		Uo=self.external_u(self.Dosp, self.Tvin, self.Pvin, self.Tjc)

		#Juice density
		self.pjin = liquor.density(self.Tjin,self.Bjin,self.Zjin)

		# Juice velocity
		self.vj = (4*((self.Fjin*self.pjin)))/(self.Np*self.pjin*math.pi*((0.0254*self.Disp)**2))

		#Scale resistance
		self.Ri = ((3.5*10**-6)*(self.Op**self.Gf))*(1+(10.73/(self.vj**3)))

		#Overall HTC
		U = (self.Aisc*Ui*Uo)/((self.Aisc*Ui)+(self.Aosc*Uo*((Ui*self.Ri)+1)))
		return U

def deltatlog(Tjin, Tjout, Tvin):
	'''
	Temperature change between incoming and outgoing juices. 
	Based on Rein, Peter. 2012. Ingenieria de La Cana de Azucar.

	Parameters:
	Tjin, Juice temperature inlet [C]
	Tvin, Vapor temperature inlet [C]
	Tjout, Juice temperature outlet [C]
	'''

	t1 = Tvin - Tjin
	t2 = Tvin - Tjout
	delta_t = (t1-t2)/(math.log(t1/t2))
	return delta_t