
from physicochemical_properties import liquor_properties
from physicochemical_properties import water_properties
from physicochemical_properties import vapor_properties
#from heat_transfer import htc_shell_tube
#from heat_transfer import htc_plate_ff
#from heat_transfer import t_log

from heaters import *

liquor=liquor_properties()
water=water_properties()
vapor=vapor_properties()
htc_s=htc_shell_tube()
#htc_p=htc_plate_ff()
#Dt=t_log()


print("\nPhysicochemical properties test")
print("-----------------------------------------------------------------")
print("\nTest liquor properties")
print("---------------------")
print("\n->Liquor specific heat:")
print("Test1:")
print("Temperature[C]: 100")
print("Brix[kg/kg]: 0.8")
print("Purity[kg/kg]: 0.7")
print("Matlab liquor specific heat[J/(kg.K)]: "+"2.6648e+03")
Cl=liquor.heat_capacity(100,0.8,0.7)
print("Python liquor specific heat[J/(kg.K)]: "+str(Cl))

print("\nTest2:")
print("Temperature[C]: 90")
print("Brix[kg/kg]: 0.3")
print("Purity[kg/kg]: 0.9")
print("Matlab liquor specific heat[J/(kg.K)]: "+"3.6194e+03")
Cl=liquor.heat_capacity(90,0.3,0.9)
print("Python liquor specific heat[J/(kg.K)]: "+str(Cl))


print("\n->Sucrose solution density:")
print("Test1:")
print("Temperature[C]: 100")
print("Brix[kg/kg]: 0.8")
print("Matlab sucrose solution density[kg/m3]: "+"1.3641e+03")
ps=liquor.sucrose_solution_density(0.8,100)
print("Python sucrose solution density[kg/m3]: "+str(ps))

print("\nTest2:")
print("Temperature[C]: 150")
print("Brix[kg/kg]: 0.3")
print("Matlab sucrose solution density[kg/m3]: "+"1.0435e+03")
ps=liquor.sucrose_solution_density(0.3,150)
print("Python sucrose solution density[kg/m3]: "+str(ps))


print("\n->Liquor density:")
print("Test1:")
print("Temperature[C]: 100")
print("Brix[kg/kg]: 0.8")
print("Purity[kg/kg]: 0.7")
print("Matlab liquor density[kg/m3]: "+"1.3681e+03")
pl=liquor.density(100,0.8,0.7)
print("Python liquor density[kg/m3]: "+str(pl))

print("\nTest2:")
print("Temperature[C]: 90")
print("Brix[kg/kg]: 0.1")
print("Purity[kg/kg]: 0.9")
print("Matlab liquor density[kg/m3]: "+"1.0037e+03")
pl=liquor.density(90,0.1,0.9)
print("Python liquor density[kg/m3]: "+str(pl))


print("\n->Liquor viscosity:")
print("Test1:")
print("Temperature[C]: 100")
print("Brix[kg/kg]: 0.8")
print("Purity[kg/kg]: 0.7")
print("Matlab liquor viscosity[Pa s]: "+"3.1001e-04")
vl=liquor.viscosity(100,0.8,0.7)
print("Python liquor viscosity[Pa s]: "+str(vl))

print("\nTest2:")
print("Temperature[C]: 90")
print("Brix[kg/kg]: 0.4")
print("Purity[kg/kg]: 0.9")
print("Matlab liquor viscosity[Pa s]: "+"3.3553e-04")
vl=liquor.viscosity(90,0.4,0.9)
print("Python liquor viscosity[Pa s]: "+str(vl))


print("\n->Liquor thermal conductivity:")
print("Test1:")
print("Temperature[C]: 100")
print("Brix[kg/kg]: 0.8")
print("Matlab liquor thermal conductivity[W/(m.K)]: "+"0.3899")
Tcl=liquor.thermal_conductivity(100,0.8)
print("Python liquor thermal conductivity[W/(m.K)]: "+str(Tcl))

print("\nTest2:")
print("Temperature[C]: 150")
print("Brix[kg/kg]: 0.3")
print("Matlab liquor thermal conductivity[W/(m.K)]: "+"0.5761")
Tcl=liquor.thermal_conductivity(150,0.3)
print("Python liquor thermal conductivity[W/(m.K)]: "+str(Tcl))


print("-----------------------------------------------------------------")

print("\nTest water properties")
print("---------------------")
print("\n->Water density:")
print("Test1:")
print("Temperature[C]: 150")
print("Matlab water density[kg/m3]: "+"916.7957")
pw=water.density(150)
print("Python water density[kg/m3]: "+str(pw))

print("\nTest2:")
print("Temperature[C]: 50")
print("Matlab water density[kg/m3]: "+"988.0304")
pw=water.density(50)
print("Python water density[kg/m3]: "+str(pw))

print("\n->Water enthalpy:")
print("Test1:")
print("Temperature[C]: 150")
print("Matlab water enthalpy[J/kg]: "+"6.1833e+05")
hw=water.enthalpy(150)
print("Python water enthalpy[J/kg]: "+str(hw))

print("\nTest2:")
print("Temperature[C]: 50")
print("Matlab water enthalpy[J/kg]: "+"2.0766e+05")
hw=water.enthalpy(50)
print("Python water enthalpy[J/kg]: "+str(hw))


print("-----------------------------------------------------------------")

print("\nTest vapor properties")
print("---------------------")
print("\n->Vapor temperature:")
print("Test1:")
print("Pressure[Pa]: 10*10^3")
print("Matlab vapor temperature[C]: "+"45.8128")
Ts=vapor.temperature(10000)
print("Python vapor temperature[C]: "+str(Ts))

print("\nTest2:")
print("Pressure[Pa]: 20*10^4")
print("Matlab vapor temperature[C]: "+"120.3328")
Ts=vapor.temperature(200000)
print("Python vapor temperature[C]: "+str(Ts))


print("\n->Vapor density:")
print("Test1:")
print("Pressure[Pa]: 22*10^3")
print("Matlab vapor density[kg/m3]: "+"0.1444")
pv=vapor.density(22000)
print("Python vapor density[kg/m3]: "+str(pv))

print("\nTest2:")
print("Pressure[Pa]: 45*10^3")
print("Matlab vapor density[kg/m3]: "+"0.2814")
pv=vapor.density(45000)
print("Python vapor density[kg/m3]: "+str(pv))


print("\n->Vapor enthalpy:")
print("Test1:")
print("Temperature[C]: 130")
print("Pressure[Pa]: 60*10^3")
print("Matlab vapor enthalpy[J/kg]: "+"2.7396e+06")
hv=vapor.enthalpy(130,60000)
print("Python vapor enthalpy[J/kg]: "+str(hv))

print("\nTest2:")
print("Temperature[C]: 50")
print("Pressure[Pa]: 45*10^3")
print("Matlab vapor enthalpy[J/kg]: "+"2.5860e+06")
hv=vapor.enthalpy(50,45000)
print("Python vapor enthalpy[J/kg]: "+str(hv))


print("\n->Vapor thermal conductivity:")
print("Test1:")
print("Temperature[C]: 150")
print("Matlab vapor thermal conductivity[W/(m.K)]: "+"0.6740")
Tcv=vapor.thermal_conductivity(150)
print("Python vapor thermal conductivity[W/(m.K)]: "+str(Tcv))

print("\nTest2:")
print("Temperature[C]: 50")
print("Matlab vapor thermal conductivity[W/(m.K)]: "+"0.6425")
Tcv=vapor.thermal_conductivity(50)
print("Python vapor thermal conductivity[W/(m.K)]: "+str(Tcv))


print("\n->Vapor viscosity:")
print("Test1:")
print("Temperature[C]: 150")
print("Matlab vapor viscosity[Pa s]: "+"3.1752e-04")
vv=vapor.viscosity(150)
print("Python vapor viscosity[Pa s]: "+str(vv))

print("\nTest2:")
print("Temperature[C]: 50")
print("Matlab vapor viscosity[Pa s]: "+"5.3977e-04")
vv=vapor.viscosity(50)
print("Python vapor viscosity[Pa s]: "+str(vv))


print("\n--------------------U COEFFICIENT SHELL & TUBES-----------------------------")
print("Disp[in]: 1.9055")
print("Dosp[in]: 2.0")
print("Aisc[m2]: 5.9939")
print("Aosc[m2]: 6.2912")
print("Np[]: 6.0")
print("Ip[mm]: 1.2" )
print("Ep[mm]: 0.090")
print("Fjin[kg/s]: 0.0277")
print("Pvin[Pa]: 134020")
print("Tjin[C]: 77")
print("Tjc[C]: 78.4456")
print("Tvin[C]: 108.0609")
print("Bjin[kg/kg]: 0.15")
print("Zjin[kg/kg]: 0.87")
print("Op[hr]: 100")
print("Gf[]: 0.8")

#Ip = 25.4*(2.0 - 1.9055)/2;
#print("Ip: " + str(Ip))

LpNst= 5.9939/0.0254*math.pi*2.0*6.0
print("Lp: " + str(LpNst/16.0))

print("\nTest Ui")
print("---------------------")
print("Matlab internal U[W/(m2.K)]: "+"4.5267e+03")
#(self, Np, Dosp, Ip, Ep, Fjin, Tjin, Bjin, Zjin):
Ui=htc_s.internal_u(6.0, 2.0, 1.2, 0.090, 0.0277, 77, 0.15, 0.87)
print("Python internal U[W/(m2.K)]: "+str(Ui))

print("\nTest Uo")
print("---------------------")
print("Matlab external U[W/(m2.K)]: "+"9.7742e+03")
#(self, Dosp, Tvin, Pvin, Tjc):
Uo=htc_s.external_u(2.0, 108.0609, 134020, 78.4456)
print("Python external U[W/(m2.K)]: "+str(Uo))

print("\nTest U")
print("---------------------")
print("Matlab overall U[W/(m2.K)]: "+"1.7249e+03")
#overall_u(self, Np, Nst, Dosp, Lp, Ip, Ep, Gf, Op,
#				  Fjin, Tjin, Bjin, Zjin, Tvin, Pvin, Tjc):
U=htc_s.overall_u(6.0, 16.0, 2.0, 556.015517904, 1.2, 0.090, 0.8, 
			100, 0.0277, 77, 0.15, 0.87, 108.0609, 134020, 78.4456)
print("Python overall U[W/(m2.K)]: "+str(U))

print("\n--------------------DELTA T LOGARITHMIC-----------------------")
print("Tjin[C]: 77")
print("Tjout[C]: 78")
print("Tvin[C]: 108.0609")
print("\nTest DtLog")
print("---------------------")
print("Matlab dtLog: "+"30.5582")
dt=deltatlog(77,78,108.0609)
print("Python dtLog: "+str(dt))


# print("\n--------------------U COEFFICIENT PLATES-----------------------------")
# print("HEATING WITH HEAT WATER")
# print("Np, Number of plates []: 4")
# print("hp, heigth of plate [m]: 0.391")
# print("wp, width of plate [m]: 0.1")
# print("dp, distance between plates [m]: 0.005")
# print("tp, plate thickness [m]: 0.004")
# print("ht_a Parameter of thermal transfer a: 0.18")
# print("ht_b Parameter of thermal transfer b: -0.24 ")
# print("Km, Thermal conductivity of material [W/m.K]: 16")
# print("ffi, fouling factor internal side [m2.K/W]: 0.0001")
# print("ffo, fouling factor external side [m2.K/W]: 0.0001")
# print("Fjin, Juice volumetric flow inlet [m3/s]: 0.1")
# print("Tjin, Juice temperature inlet [C]: 17")
# print("Bjin, Juice Brix inlet [kg/kg]: 0.15")
# print("Zjin, Juice purity inlet [kg/kg]: 0.87")
# print("Fwin, Water volumetric flow inlet [m3/s]: 0.127")
# print("Twin, Water temperature inlet [C]: 70")

# print("\nTest Ui")
# print("---------------------")
# print("Excel internal U[W/(m2.K)]: "+"3.737e+03")
# Ui=htc_p.internal_u(0.1,0.005,0.18,-0.24,0.1,17,0.15,0.87)
# print("Python internal U[W/(m2.K)]: "+str(Ui))

