from physicochemical_properties import liquor_properties
from physicochemical_properties import water_properties
from physicochemical_properties import vapor_properties
import math
liquor=liquor_properties()
water=water_properties()
vapor=vapor_properties()

class htc_shell_tube: #Heat Transfer Coefficient (HTC)
	'''
	Heat transfer coefficient. 
	Based on Kreith, Frank, Raj M Manglik, Mark S Bohn, and S G Kandlikar. 2012. Handbook of Phase Change: Boiling and Condensation Principles of Heat Transfer.

	Fjin, Juice volumetric flow inlet [m3/s]
	Bjin, Juice Brix inlet [kg/kg]
	Zjin, Juice purity inlet [kg/kg]
	Tjin, Juice temperature inlet [C]
	Tjc, Media temperature in heater [C]
	Tvin, Vapor temperature inlet [C]
	Pvin, Vapor pressure inlet [Pa]
	Np, Number of pipes []
	Aisc, Transfer heat inside area [m2]
	Aosc, Transfer heat outside area [m2]
	Disp, Inside diameter of pipe [in]
	Dosp, Outside diameter of pipe [in]
	Ep, Pipe roughness [mm]
	Hrop, Operation hours [hr]
	B, Evolution factor of fouling []
	'''
	
	def internal_u(self,Disp,Dosp,Np,Ep,Fjin,Tjin,Bjin,Zjin):
		self.Disp=Disp
		self.Dosp=Dosp
		self.Np=Np
		self.Ep=Ep
		self.Fjin=Fjin
		self.Tjin=Tjin
		self.Bjin=Bjin
		self.Zjin=Zjin

		#Juice viscosity
		self.ujin=liquor.viscosity(self.Tjin,self.Bjin,self.Zjin)
		#Juice density
		self.pjin=liquor.density(self.Tjin,self.Bjin,self.Zjin)
		#Juice thermal conductivity
		self.Yjin=liquor.thermal_conductivity(self.Tjin,self.Bjin)
		#Juice Specific Heat
		self.Cpjin=liquor.heat_capacity(self.Tjin,self.Bjin,self.Zjin)


		#Relative roughness
		Er=self.Ep/(25.4*self.Disp)
		#Reynolds
		Re=(4*((self.Fjin*self.pjin)/self.Np))/(0.0254*math.pi*self.Disp*self.ujin)
		#Friction factor
		f=0.25/((math.log((Er/3.7)+(5.74/(Re**0.9))))**2.0)
		#Prandlt
		Pr=(self.Cpjin*self.ujin)/self.Yjin
		#Nusselt-Gnilinski
		Nu=((f/8.0)*(Re-1000.0)*Pr)/(1+(12.7*((f/8.0)**0.5)*((Pr**(2.0/3.0))-1.0)))

		#Internal HTC
		Ui=(Nu*self.Yjin)/((25.4*self.Disp)/1000)
		return Ui

	def external_u(self,Dosp,Tjc,Tvin,Pvin):
		self.Dosp=Dosp
		self.Tjc=Tjc
		self.Tvin=Tvin
		self.Pvin=Pvin

		#Temperature beetween satured vapor and pipe wall
		self.Tvp = self.Tvin-((self.Tjc+self.Tvin)/2)

		#Vapor viscosity
		self.uvin=vapor.viscosity(self.Tvin)
		#Vapor enthalpy
		self.Hvin=vapor.enthalpy(self.Tvin,self.Pvin)-water.enthalpy(self.Tvin)
		#Vapor thermal conductivity
		self.Yvin=vapor.thermal_conductivity(self.Tvin)
		
		#Water density
		self.pw=water.density(self.Tvin)
		
		#Gravity
		g=9.80665

		#External HTC
		Uo=0.725*(((g*(self.Yvin**3)*(self.pw**2)*self.Hvin)/(0.0254*self.Dosp*self.Tvp*self.uvin))**0.25)
		return Uo

	def overall_u(self,Fjin,Bjin,Zjin,Tjin,Tjc,Tvin,Pvin,Np,Aisc,Aosc,Disp,Dosp,Ep,Hrop,B):
		self.Fjin=Fjin
		self.Bjin=Bjin
		self.Zjin=Zjin
		self.Tjin=Tjin
		self.Tjc=Tjc
		self.Tvin=Tvin
		self.Pvin=Pvin
		self.Np=Np
		self.Aisc=Aisc
		self.Aosc=Aosc
		self.Disp=Disp
		self.Dosp=Dosp
		self.Ep=Ep
		self.Hrop=Hrop
		self.B=B

		Uo=self.external_u(self.Dosp,self.Tjc,self.Tvin,self.Pvin)
		Ui=self.internal_u(self.Disp,self.Dosp,self.Np,self.Ep,self.Fjin,self.Tjin,self.Bjin,self.Zjin)

		#Juice density
		self.pjin=liquor.density(self.Tjin,self.Bjin,self.Zjin)

		# Juice velocity
		vj=(4*((self.Fjin*self.pjin)))/(self.Np*self.pjin*math.pi*((0.0254*self.Disp)**2));

		#Scale resistance
		Ri=((3.5*10**-6)*(self.Hrop**self.B))*(1+(10.73/(vj**3)));

		#Overall HTC
		U=(self.Aisc*Ui*Uo)/((self.Aisc*Ui)+(self.Aosc*Uo*((Ui*Ri)+1)))
		return U

class t_log:
	'''
	Temperature change between incoming and outgoing juices. 
	Based on Rein, Peter. 2012. Ingenieria de La Cana de Azucar.

	Parameters:
	Tjin, Juice temperature inlet [C]
	Tvin, Vapor temperature inlet [C]
	Tjout, Juice temperature outlet [C]
	'''

	def deltatlog(self,Tjin,Tjout,Tvin):
		self.Tjin=Tjin
		self.Tjout=Tjout
		self.Tvin=Tvin

		T1=self.Tvin-self.Tjin
		T2=self.Tvin-self.Tjout
		DeltaT=(T1-T2)/(math.log(T1/T2))
		return DeltaT