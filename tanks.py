import math

from physicochemical_properties import liquor_properties
from physicochemical_properties import water_properties
from physicochemical_properties import vapor_properties

liquor=liquor_properties()
water=water_properties()
vapor=vapor_properties()



class tank:
	'''
	Parameters:
	Dp, Diameter of pipe [in]
	A, Cross-sectional area [m]
	V, Tank volume [m3]

	'''
	def __init__(self, Dp, A, V,):
		self.Dp=Dp
		self.A=A
		self.V=V
		sel.hmax=V/A

	def in_out(self, fluid_in, fluid_out):
		self.fluid_in = fluid_in
		self.fluid_out = fluid_out

	def round_rsd_time(self,time,ts):
		A=time/ts
		B=math.ceil(A)
		round_time=B*ts
		return round_time

	@staticmethod
	def model_level(x, t, Dp, A, hmax, Fin, Pout, Tj, Bj, Zj):

		Ltk=x[0]

		# Juice viscosity
		pj=liquor.density(Tj,Bj,Zj)
		# Juice density
		uj=liquor.viscosity(Tj,Bj,Zj)

		#Lengh of out pipe
		Lp=5.0
		# Gravity
		g=9.80665 #[m/s2]
		# Athmosferic pressure
		Patm= 101325 #[Pa]

		# Hidrostatic pressure
		Ph=pj*g*Ltk*hmax

		dPout=Ph-Pout

		Rp=(8*uj*Lp)/(math.pi*(0.0127*Dp)**4)

		rsd_time=(A*hmax)/(Fin)

		if t-rsd_time>0.0:

			dLtk = (pj*(Fin-((dPout)/Rp)))/(pj*A*hmax)
			
		else:
			dLtk=0.0
		dy=dLtk

		return dy
