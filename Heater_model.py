from physicochemical_properties import liquor_properties
from physicochemical_properties import water_properties
from physicochemical_properties import vapor_properties
from heat_transfer import htc_shell_tube
from heat_transfer import t_log
import math

liquor=liquor_properties()
water=water_properties()
vapor=vapor_properties()
Ht=htc_shell_tube()
Dt=t_log()

def heater_model(x,t,Np, Nst, Lp, dp, Dosp, Fjin, Bjin, Zjin, Tjin, Pvin, Ep, B, Hrop):
	
	Tjout=x[0]

	# Np = u[0]; Nst=u[1]; Lp = u[2]; dp = u[3]; Dosp = u[4]; Fjin=u[5]; Bjin = u[6]; 
	# Zjin = u[7]; Tjin = u[8]; Pvin = u[9];  Ep = u[10]; B=u[11]; Hrop= u[12];

	#Inside diameter of pipe
	Disp=Dosp-(2*(dp/25.4));

	#Inside and outside transfer heat area per step
	Aisc=0.0254*math.pi*Disp*Np*Lp*Nst;
	Aosc=0.0254*math.pi*Dosp*Np*Lp*Nst;
	#Heat exchanger heat transfer area.
	Ac=Aosc;

	# Media Temperature
	Tjc=(Tjin+Tjout)/2.0;

	# Vapor temperature
	Tvin=vapor.temperature(Pvin)

	# Media Heat capacitie
	Cpjc=liquor.heat_capacity(Tjc,Bjin,Zjin)

	# Media Densitie
	pjc=liquor.density(Tjc,Bjin,Zjin)

	# Mass of juice inside the heater
	mjc=pjc*Np*Nst*(math.pi*(((0.0254*Disp)/2.0)**2.0))*Lp

	U=Ht.overall_u(Fjin,Bjin,Zjin,Tjin,Tjc,Tvin,Pvin,Np,Aisc,Aosc,Disp,Dosp,Ep,Hrop,B)
	DeltaT=Dt.deltatlog(Tjin,Tjout,Tvin)
	
	dTjout = ((U*Ac*DeltaT)+(pjc*Fjin*Cpjc*Tjin)-(pjc*Fjin*Cpjc*Tjout))/(0.5*mjc*Cpjc);
	dy=dTjout
	return dy
