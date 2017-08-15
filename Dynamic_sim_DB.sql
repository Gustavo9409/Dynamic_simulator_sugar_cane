CREATE TABLE Controllers (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Time_exec_id INTEGER UNSIGNED NOT NULL,
  Name VARCHAR(50) NULL,
  Ans_type VARCHAR(50) NULL,
  KP VARCHAR(50) NULL,
  KI VARCHAR(50) NULL,
  KD VARCHAR(50) NULL,
  SP VARCHAR(50) NULL,
  MV VARCHAR(50) NULL,
  PV VARCHAR(50) NULL,
  MV_type VARCHAR(50) NULL,
  Control_type VARCHAR(50) NULL,
  Control_type_value VARCHAR(50) NULL,
  PRIMARY KEY(id),
  INDEX Controllers_FKIndex1(Time_exec_id)
);

CREATE TABLE Evaporators (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Name VARCHAR(50) NULL,
  _Type VARCHAR(50) NULL,
  Brix_init VARCHAR(50) NULL,
  Flow_init VARCHAR(50) NULL,
  Level_init VARCHAR(50) NULL,
  Heat_area VARCHAR(50) NULL,
  Pipe_length VARCHAR(50) NULL,
  N_pipes VARCHAR(50) NULL,
  Intl_pipe_diameter VARCHAR(50) NULL,
  Volumen VARCHAR(50) NULL,
  Downtake_diameter VARCHAR(50) NULL,
  Bottom_cone_heigth VARCHAR(50) NULL,
  N_effect VARCHAR(50) NULL,
  Operation_days VARCHAR(50) NULL,
  Heat_losses VARCHAR(50) NULL,
  PRIMARY KEY(id)
);

CREATE TABLE Flow_inputs (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Time_exec_id INTEGER UNSIGNED NOT NULL,
  Name VARCHAR(50) NULL,
  _Type VARCHAR(50) NULL,
  Flow VARCHAR(50) NULL,
  Temperature VARCHAR(50) NULL,
  Brix VARCHAR(50) NULL,
  Purity VARCHAR(50) NULL,
  Insoluble_solids VARCHAR(50) NULL,
  pH VARCHAR(50) NULL,
  Pressure VARCHAR(50) NULL,
  Saturated_vapor VARCHAR(50) NULL,
  PRIMARY KEY(id),
  INDEX Flow_inputs_FKIndex1(Time_exec_id)
);

CREATE TABLE Heaters (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Name VARCHAR(50) NULL,
  _Type VARCHAR(50) NULL,
  Tjout_init VARCHAR(50) NULL,
  PRIMARY KEY(id)
);

CREATE TABLE Outputs_evaporator (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Time_exec_id INTEGER UNSIGNED NOT NULL,
  Evaporators_id INTEGER UNSIGNED NOT NULL,
  Out_juice_temperature VARCHAR(50) NULL,
  Out_juice_brix VARCHAR(50) NULL,
  Out_juice_flow VARCHAR(50) NULL,
  Out_juice_pH VARCHAR(50) NULL,
  Out_juice_pressure VARCHAR(50) NULL,
  Out_juice_insoluble_solids VARCHAR(50) NULL,
  Out_juice_purity VARCHAR(50) NULL,
  Out_vapor_flow VARCHAR(50) NULL,
  Out_vapor_temperature VARCHAR(50) NULL,
  Out_vapor_pressure VARCHAR(50) NULL,
  Condensed_vapor_flow VARCHAR(50) NULL,
  Condensed_vapor_temperature VARCHAR(50) NULL,
  Condensed_vapor_pressure VARCHAR(50) NULL,
  Evaporator_level VARCHAR(50) NULL,
  PRIMARY KEY(id),
  INDEX Outputs_evaporator_FKIndex1(Evaporators_id),
  INDEX Outputs_evaporator_FKIndex2(Time_exec_id)
);

CREATE TABLE Outputs_heater (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Heaters_id INTEGER UNSIGNED NOT NULL,
  Time_exec_id INTEGER UNSIGNED NOT NULL,
  Out_fluid_temperature VARCHAR(50) NULL,
  Out_fluid_brix VARCHAR(50) NULL,
  Out_fluid_flow VARCHAR(50) NULL,
  Out_fluid_pH VARCHAR(50) NULL,
  Out_fluid_pressure VARCHAR(50) NULL,
  Out_fluid_insoluble_solids VARCHAR(50) NULL,
  Out_fluid_purity VARCHAR(50) NULL,
  Condensed_vapor_flow VARCHAR(50) NULL,
  Condensed_vapor_temperature VARCHAR(50) NULL,
  Condensed_vapor_pressure VARCHAR(50) NULL,
  PRIMARY KEY(id),
  INDEX Outputs_heater_FKIndex1(Time_exec_id),
  INDEX Outputs_heater_FKIndex2(Heaters_id)
);

CREATE TABLE Outputs_valve (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Time_exec_id INTEGER UNSIGNED NOT NULL,
  Valves_id INTEGER UNSIGNED NOT NULL,
  Out_temperature VARCHAR(50) NULL,
  Out_brix VARCHAR(50) NULL,
  Out_flow VARCHAR(50) NULL,
  Out_pH VARCHAR(50) NULL,
  Out_pressure VARCHAR(50) NULL,
  Out_insoluble_solids VARCHAR(50) NULL,
  Out_purity VARCHAR(50) NULL,
  Out_saturated_vapor VARCHAR(50) NULL,
  PRIMARY KEY(id),
  INDEX Outputs_valve_FKIndex1(Valves_id),
  INDEX Outputs_valve_FKIndex2(Time_exec_id)
);

CREATE TABLE Physical_properties_heater (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Heaters_id INTEGER UNSIGNED NOT NULL,
  Ext_pipe_diameter VARCHAR(50) NULL,
  Pipe_length VARCHAR(50) NULL,
  Pipe_thickness VARCHAR(50) NULL,
  Pipe_rough VARCHAR(50) NULL,
  Pipe_x_Step VARCHAR(50) NULL,
  N_steps VARCHAR(50) NULL,
  Operation_time VARCHAR(50) NULL,
  Heat_area VARCHAR(50) NULL,
  Scalling_coeff VARCHAR(50) NULL,
  Scalling_resistance VARCHAR(50) NULL,
  Juice_velocity VARCHAR(50) NULL,
  Inside_U VARCHAR(50) NULL,
  Outside_U VARCHAR(50) NULL,
  Overall_U VARCHAR(50) NULL,
  PRIMARY KEY(id),
  INDEX Physical_properties_heater_FKIndex1(Heaters_id)
);

CREATE TABLE Time_exec (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Ts VARCHAR(50) NULL,
  time VARCHAR(50) NULL,
  PRIMARY KEY(id)
);

CREATE TABLE Valves (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Name VARCHAR(50) NULL,
  _Type VARCHAR(50) NULL,
  Ap_init VARCHAR(50) NULL,
  Diameter VARCHAR(50) NULL,
  Coeff_type VARCHAR(50) NULL,
  Coeff_min VARCHAR(50) NULL,
  Coeff_max VARCHAR(50) NULL,
  In_flow VARCHAR(50) NULL,
  Ap VARCHAR(50) NULL,
  PRIMARY KEY(id)
);


