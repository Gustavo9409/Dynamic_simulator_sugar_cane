
# Installed Libs
import math

from scipy import *
from scipy.integrate import odeint
from scipy.integrate import ode

# Local Libs
from physicochemical_properties import liquor_properties
from physicochemical_properties import water_properties
from physicochemical_properties import vapor_properties

liquor_prpty=liquor_properties()
water_prpty=water_properties()
vapor_prpty=vapor_properties()


class heater_shell_tube:
	'''
	Parameters:
	Np, Number of pipes per step []
	Nst, Number of steps []
	Dosp, Pipe external diamenter [in]
	Lp, Pipe Length [m]
	Ip, Pipe thickness [mm]
	Ep, Pipe roughness [mm]
	Gf, Scale factor (fouling) []
	Op, Operation hours [h]
	'''

	def __init__(self, Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op,Tjout):
		self.Np = Np
		self.Nst = Nst
		self.Dosp = Dosp
		self.Lp = Lp
		self.Ip = Ip
		self.Ep = Ep
		self.Gf = Gf
		self.Op = Op
		self.Tjout=Tjout
		self.properties()
		self.Ht=htc_shell_tube()

	# def __init__(self, time,u,init_cond):
	# 	self.time=time
	# 	self.u=tuple(u)
	# 	self.initial_condition=[init_cond]
		

	def properties(self):
		# Compute heater design properties

		# Pipe internal diameter [in]
		self.Disp = self.Dosp - (2*(self.Ip/25.4))

		# Internal heat transfer area [m2]
		self.Aisc=0.0254*math.pi*self.Disp*self.Np*self.Lp*self.Nst

		# External heat transfer area [m2]
		self.Aosc=0.0254*math.pi*self.Dosp*self.Np*self.Lp*self.Nst


	def in_out(self, fluid_in, fluid_out, vapor_in, vapor_out):
		self.fluid_in = fluid_in
		self.fluid_out = fluid_out

		self.vapor_in=vapor_in
		self.vapor_out=vapor_out

		self.Tjout0 = self.Tjout
		# self.Tjout = Tjout

	def solve(self, time):
		fluid_in = self.fluid_in
		fluid_out = self.fluid_out

		vapor_in=self.vapor_in
		vapor_out=self.vapor_out

		# Init condition
		x0 = self.Tjout0
		# Model parmeters
		u =(self.Np, self.Nst, self.Dosp, self.Lp, self.Ip, self.Ep, self.Gf, self.Op, fluid_in.Fj, fluid_in.Tj, fluid_in.Bj, fluid_in.Zj, vapor_in.Pv)

		# Solve temperature model
		sol = odeint(self.model_temperature, x0, time, args=u)
		self.Tjout = sol[1,0]
		self.Tjout0 = [sol[1,0]]		

		fluid_out.Tj=self.Tjout
		fluid_out.Zj=self.fluid_purity_loss()
		fluid_out.Pj=self.fluid_pressure_loss()
		fluid_out.update_()

		vapor_in.Mv=self.vapor_mass_flow()
		vapor_in.update_()

		vapor_out.Mv=vapor_in.Mv
		vapor_out.update_()

		return fluid_in, fluid_out, vapor_in, vapor_out

	def vapor_mass_flow(self):
		# Vapor flow consumed for heater

		fluid_in = self.fluid_in
		fluid_out = self.fluid_out

		vapor_in=self.vapor_in
		vapor_out=self.vapor_out

		Tjc=(fluid_in.Tj+fluid_out.Tj)/2.0

		OvU=self.Ht.overall_u(self.Np, self.Nst, self.Dosp, self.Lp, self.Ip, self.Ep, self.Gf, self.Op,
		fluid_in.Fj, fluid_in.Tj, fluid_in.Bj, fluid_in.Zj, vapor_in.Tv, vapor_in.Pv,Tjc)


		DT=float(deltatlog(self.fluid_in.Tj,self.fluid_out.Tj,self.vapor_in.Tv))		
		
		Mv= (OvU*self.Aosc*(DT))/self.vapor_in.Hvw #kg/s

		return Mv

	def fluid_pressure_loss(self):
		# Pressure losses in fluid 

		fluid_in = self.fluid_in
		vapor_in = self.vapor_in

		Er=self.Ep/self.Dosp
		Tjc=(fluid_in.Tj+self.Tjout)/2.0

		#Moody Friction factor
		f1=(1.4+2*math.log(Er))**-2
		f=((-2*math.log((Er/3.7)+(2.51/(self.htc.Re*(f1**0.5)))))**-2.0)

		#Viscosity of pipe fluid at wall temperature
		up_tube_wall=liquor_prpty.viscosity(((Tjc+vapor_in.Tv)/2.0),fluid_in.Bj,fluid_in.Zj)

		#Drop pressure pipe side (REIN)
		Delta_drop_pressure=(self.Nst*f*self.Lp*(((fluid_in.pj)*(self.htc.vj**2.0))))/(2.0*self.Disp*((fluid_in.uj/up_tube_wall)**0.14))

		Out_pressure=fluid_in.Pj-Delta_drop_pressure
		
		return Out_pressure

	def fluid_purity_loss(self):
		# Purity losses in fluid for residence time

		fluid_in = self.fluid_in

		self.rsd_time=(self.Nst*self.Lp)/self.htc.vj

		lss_sac=liquor_prpty.sucrose_losses(self.rsd_time,fluid_in.Tj,fluid_in.Bj,fluid_in.Ij,fluid_in.Zj,fluid_in.pHj)
		Loss_purity=(lss_sac/100.0)/(fluid_in.Bj)
		Outpurity=(fluid_in.Zj)-Loss_purity
		
		return Outpurity

	def update_model(self,time,u):
		#Update parameters to solve model

		self.time=time
		self.u=tuple(u)
		self.solve_model()

	def solve_model(self):
		#Solve model

		yout = odeint(self.model_temperature,self.initial_condition,self.time,self.u)

		self.initial_condition=[yout[1,0]]
		self.Tjout=yout[1,0]


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

	# @staticmethod  #static method to be used in scipy.integrate.odeint
	def model_temperature(self,x, t, Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op,
						 Fjin, Tjin, Bjin, Zjin, Pvin):
		
		#Initial output of juice temperature
		Tjout = x[0]

		# Np = u[0]; Nst=u[1]; Lp = u[2]; dp = u[3]; Dosp = u[4]; Fjin=u[5]; Bjin = u[6]; 
		# Zjin = u[7]; Tjin = u[8]; Pvin = u[9];  Ep = u[10]; B=u[11]; Hrop= u[12];

		# Inside diameter of pipe
		Disp = Dosp - (2*(Ip/25.4))
		
		# Heat exchanger heat transfer area.
		Ac = 0.0254*math.pi*Dosp*Np*Lp*Nst

		# Medium Temperature
		Tjc = (Tjin + Tjout)/2.0

		# Vapor temperature
		Tvin = vapor_prpty.temperature(Pvin)

		# Media Heat capacity
		Cpjc = liquor_prpty.heat_capacity(Tjc,Bjin,Zjin)
		Cpjin = liquor_prpty.heat_capacity(Tjin,Bjin,Zjin)
		Cpjout = liquor_prpty.heat_capacity(Tjout,Bjin,Zjin)

		# Density
		pjc = liquor_prpty.density(Tjc,Bjin,Zjin)
		pjin = liquor_prpty.density(Tjin,Bjin,Zjin)
		pjout = liquor_prpty.density(Tjout,Bjin,Zjin)

		# Mass of juice inside the heater
		mjc = pjc*Np*Nst*(math.pi*(((0.0254*Disp)/2.0)**2.0))*Lp

		# Heat Transfer Coefficient
		self.htc=htc_shell_tube()
		self.U = self.htc.overall_u(Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op,
					  			Fjin, Tjin, Bjin, Zjin, Tvin, Pvin, Tjc)

		# Logarithmic delta of temperature
		delta_t = deltatlog(Tjin, Tjout, Tvin)
		
		# Differential equation modeling temperature
		dTjout_dt = ( (self.U*Ac*delta_t) + (pjin*Fjin*Cpjin*Tjin) - (pjout*Fjin*Cpjout*Tjout) )/(0.5*mjc*Cpjc)

		if t>0.0:
			dy = dTjout_dt
		else:
			dy = 0
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
		self.ujin = liquor_prpty.viscosity(self.Tjin, self.Bjin, self.Zjin)
		# Juice density
		self.pjin = liquor_prpty.density(self.Tjin, self.Bjin, self.Zjin)
		# Juice thermal conductivity
		self.Yjin = liquor_prpty.thermal_conductivity(self.Tjin, self.Bjin)
		# Juice Specific Heat
		self.Cpjin = liquor_prpty.heat_capacity(self.Tjin, self.Bjin, self.Zjin)

		# Relative roughness
		Er = self.Ep/(25.4*self.Disp)
		# Reynolds
		self.Re = (4*((self.Fjin*self.pjin)/self.Np))/(0.0254*math.pi*self.Disp*self.ujin)
		# Friction factor
		f = 0.25/((math.log((Er/3.7)+(5.74/(self.Re**0.9))))**2.0)
		# Prandlt
		Pr = (self.Cpjin*self.ujin)/self.Yjin
		# Nusselt-Gnilinski
		Nu = ((f/8.0)*(self.Re-1000.0)*Pr)/(1+(12.7*((f/8.0)**0.5)*((Pr**(2.0/3.0))-1.0)))

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
		self.uvin = vapor_prpty.viscosity(self.Tvin)
		# Vapor enthalpy
		self.Hvin = vapor_prpty.enthalpy(self.Tvin, self.Pvin) - water_prpty.enthalpy(self.Tvin)
		# Vapor thermal conductivity
		self.Yvin = vapor_prpty.thermal_conductivity(self.Tvin)
		
		# Water density
		self.pw = water_prpty.density(self.Tvin)
		
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
		self.Ui=self.internal_u(self.Np, self.Dosp, self.Ip, self.Ep, 
						self.Fjin,self.Tjin,self.Bjin,self.Zjin)

		# External HTC
		self.Uo=self.external_u(self.Dosp, self.Tvin, self.Pvin, self.Tjc)

		#Juice density
		self.pjin = liquor_prpty.density(self.Tjin,self.Bjin,self.Zjin)

		# Juice velocity
		self.vj = (4*((self.Fjin*self.pjin)))/(self.Np*self.pjin*math.pi*((0.0254*self.Disp)**2))

		#Scale resistance
		self.Ri = ((3.5*10**-6)*(self.Op**self.Gf))*(1+(10.73/(self.vj**3)))

		#Overall HTC
		U = (self.Aisc*self.Ui*self.Uo)/((self.Aisc*self.Ui)+(self.Aosc*self.Uo*((self.Ui*self.Ri)+1)))
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


# ============================================================================================
#                                       Testing
# ============================================================================================
# class htc_plate_ff: #Heat Transfer Coefficient (HTC) Heating juice with water
# 	'''
# 	Heat transfer coefficient. 
# 	Based on Thesis??

# 	Fjin, Juice volumetric flow inlet [m3/s]
# 	Tjin, Juice temperature inlet [C]
# 	Bjin, Juice Brix inlet [kg/kg]
# 	Zjin, Juice purity inlet [kg/kg]
# 	Fvin, Vapor volumetric flow inlet [m3/s]
# 	Tvin, Vapor temperature inlet [C]
# 	Pvin, Vapor pressure inlet [Pa]
# 	Np, Number of plates []
# 	hp, heigth of plate [m]
# 	wp, width of plate [m]
# 	dp, distance between plates [m]
# 	tp, plate thickness [m]
# 	ht_a Parameter of thermal transfer a
# 	ht_b Parameter of thermal transfer b
# 	Km, Thermal conductivity of material [W/m.K]
# 	ffi, fouling factor internal side [m2.K/W]
# 	ffo, fouling factor external side [m2.K/W]

# 	Drop, Operation hours [hr]
# 	B, Evolution factor of fouling []
# 	'''
	
# 	def internal_u(self,wp,dp,ht_a,ht_b,Fjin,Tjin,Bjin,Zjin):
# 		self.wp=wp
# 		self.dp=dp
# 		self.ht_a=ht_a
# 		self.ht_b=ht_b
# 		self.Fjin=Fjin
# 		self.Tjin=Tjin
# 		self.Bjin=Bjin
# 		self.Zjin=Zjin

# 		#Juice viscosity
# 		self.ujin=liquor.viscosity(self.Tjin,self.Bjin,self.Zjin)
# 		print("ujin: "+str(self.ujin))
# 		#Juice density
# 		self.pjin=liquor.density(self.Tjin,self.Bjin,self.Zjin)
# 		print("pjin: "+str(self.pjin))
# 		#Juice thermal conductivity
# 		self.Yjin=liquor.thermal_conductivity(self.Tjin,self.Bjin)
# 		#Juice Specific Heat
# 		self.Cpjin=liquor.heat_capacity(self.Tjin,self.Bjin,self.Zjin)


# 		#Velocity vjin
# 		vjin=(self.Fjin*self.pjin)/(self.dp*self.wp)
# 		print("vjin: "+str(vjin))
# 		#Reynolds
# 		Re=(vjin*2*self.dp)/(self.ujin)
# 		print("Re: "+str(Re))
# 		#heat transfer factor Jh
# 		Jh = self.ht_a*math.pow(Re,self.ht_b)
# 		print("Jh: "+str(Jh))
# 		#Prandlt Pr
# 		Pr=(self.Cpjin*self.ujin)/self.Yjin

# 		#Internal HTC
# 		Ui=(1000/3600)*vjin*Jh*self.Cpjin/(math.pow(Pr,2/3))
# 		return Ui

# 	def external_u(self,wp,dp,ht_a,ht_b,Km,Fwin,Twin):
# 		self.wp=wp
# 		self.dp=dp
# 		self.ht_a=ht_a
# 		self.ht_b=ht_b
# 		self.Km=Km
# 		self.Fwin=Fwin
# 		self.Twin=Twin

# 		#Water viscosity
# 		self.uwin=liquor.viscosity(self.Twin,0.01,0)
# 		#Water density
# 		self.pwin=water.density(self.Twin)
# 		#Water thermal conductivity
# 		self.Ywin=liquor.thermal_conductivity(self.Twin,0.01)
# 		#Water specific heat
# 		self.Cpwin=liquor.heat_capacity(self.Twin,0.01,0)
		

# 		#Velocity vvin
# 		vwin=(self.Fwin*self.pwin)/(self.dp*self.wp)
# 		#Reynolds
# 		Re=(vwin*2*self.dp)/(self.uwin)
# 		#heat transfer factor Jh
# 		Jh = self.ht_a*Re^self.ht_b
# 		#Prandlt Pr
# 		Pr=(self.Cpwin*self.uwin)/self.Ywin

# 		#External HTC
# 		Uo=(1000/3600)*vwin*Jh*self.Cpwin/(Pr^(2/3))
# 		return Uo

# 	def overall_u(self,Fjin,Tjin,Bjin,Zjin,Fvin,Tvin,Pvin,Np,hp,wp,dp,tp,ht_a,ht_b,Km,ffi,ffo):
# 		self.Fjin=Fjin
# 		self.Tjin=Tjin
# 		self.Bjin=Bjin
# 		self.Zjin=Zjin
		
# 		self.Fvin=Fvin
# 		self.Tvin=Tvin
# 		self.Pvin=Pvin
		
# 		self.Np=Np
# 		self.hp=hp
# 		self.wp=wp
# 		self.dp=dp
# 		self.tp=tp

# 		self.Km=Km
# 		self.ht_a=ht_a
# 		self.ht_b=ht_b

# 		self.ffi=ffi
# 		self.ffo=ffo

# 		Uo=self.external_u(self.wp,self.dp,self.ht_a,self.ht_b,self.Km,self.Fvin,self.Tvin,self.Pvin)
# 		Ui=self.internal_u(self.wp,self.dp,self.ht_a,self.ht_b,self.Fjin,self.Tjin,self.Bjin,self.Zjin)

# 		#Overall HTC
# 		U=1/(1/Uo + 1/Ui + self.tp/self.Km +  self.ffi + self.ffo)
# 		return U