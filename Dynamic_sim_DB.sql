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

CREATE TABLE Physical_properties_heater (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  Heaters_id INTEGER UNSIGNED NOT NULL,
  Ext_pipe_diameter VARCHAR(50) NULL,
  Pipe_lenght VARCHAR(50) NULL,
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


