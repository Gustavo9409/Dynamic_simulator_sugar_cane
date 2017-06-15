import math

from physicochemical_properties import liquor_properties
from physicochemical_properties import water_properties
from physicochemical_properties import vapor_properties

liquor=liquor_properties()
water=water_properties()
vapor=vapor_properties()


class tank:
	@staticmethod
	def model_level(x, t, Dp,A,hmax,Fin,Pout,Tj,Bj,Zj):

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

		##Presion Ph=Pou
		##Pout para que flujo sea mayor al de entrada
		##Pout para que flujo sea menor al de entrada

		##Si Ltk<0% entonces fjin=fjout 

		dPout=Ph-Pout

		Rp=(8*uj*Lp)/(math.pi*(0.0127*Dp)**4)

		# rsd_time=(A*hmax)/((dPin)/Rp)
		# print (rsd_time)

		dLtk = (pj*(Fin-((dPout)/Rp)))/(pj*A*hmax)
		# print ("pj "+str(pj))
		# print ("hmax"+str(hmax))
		# print ("Rp "+str(Rp))
		# print ("Ph "+str(Ph))
		dy=dLtk

		return dy
