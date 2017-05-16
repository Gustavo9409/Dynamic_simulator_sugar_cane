from physicochemical_properties import liquor_properties, water_properties, vapor_properties
liquor=liquor_properties()
water=water_properties()
vapor=vapor_properties()

class update_flow_data():

	def update_vapor(self,Pvin):
		Tvin=vapor.temperature(Pvin)

		pv=vapor.density(Pvin)

		uv=vapor.viscosity(Tvin)

		Hv=vapor.enthalpy(Tvin,Pvin)

		Yv=vapor.thermal_conductivity(Tvin)

		Cpv=Hv/Tvin

		Hvw=Hv-water.enthalpy(Tvin)

		return Tvin,pv,uv,Hv,Yv,Cpv,Hvw


	def update_juice(self,Bjin,Zjin,Tjin):	
		Cpj=liquor.heat_capacity(Tjin,Bjin,Zjin)

		pj=liquor.density(Tjin,Bjin,Zjin)

		uj=liquor.viscosity(Tjin,Bjin,Zjin)

		Hj=Cpj*Tjin

		Yj=liquor.thermal_conductivity(Tjin,Bjin)

		return Cpj,pj,uj,Hj,Yj

	def update_water(self,Tw):
		pw=water.density(Tw)

		Hw=water.enthalpy(Tw)

		return pw,Hw
