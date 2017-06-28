#-*- coding: utf-8 -*-
#! python

# Installed Libs
import numpy as np

# Local Libs
from streams import *


# ============================================================================================
#                                       Testing Classes
# ============================================================================================

Juice1 = juice(100.0, 400.0*(10**3), 75.0, 0.15, 0.87, 0.008, 5.0)
Mj = (Juice1.water_f + Juice1.insoluble_f + Juice1.sucrose_f + Juice1.nosucrose_f )
Solj = Juice1.sucrose_f + Juice1.nosucrose_f

print("=================================================================================")
print("                                  Juice Stream                                   ")
print("=================================================================================")
print("Mass components calculation")
print("Juice1: 100 [t/h], 400 [kPa], 75 [C], 15 [%Brix], 87 [%Pur], 0.8 [%Ins], 5.0 [pH]")
print("Juice1 Mass: " + str(Juice1.Mj))
print("Juice1 Water: " + str(Juice1.water_f))
print("Juice1 Sucrose: " + str(Juice1.sucrose_f))
print("Juice1 Nosucorese: " + str(Juice1.nosucrose_f))
print("Juice1 Insoluble: " + str(Juice1.insoluble_f))
print("Juice1 Pressure: " + str(Juice1.Pj))
print("Juice1 Temperature: " + str(Juice1.Tj))
print("Juice1 pH: " + str(Juice1.pHj))
print("Juice1 Mass: " + str(Juice1.Mj) + "\tJuice1 Mass probe: "  + str(Mj))
print("Juice1 Solids: " + str(Juice1.solids_f) + "\tJuice1 Solids probe: "  + str(Solj))

Juice2 = juice(50.0, 410.0*(10**3), 90.0, 0.17, 0.83, 0.01, 7.0)
print("\nJuice2: 50 [t/h], 410 [kPa], 90 [C], 17 [%Brix], 83 [%Pur], 1.0 [%Ins], 7.0 [pH]")
print("Juice2 Mass: " + str(Juice2.Mj))
print("Juice2 Water: " + str(Juice2.water_f))
print("Juice2 Sucrose: " + str(Juice2.sucrose_f))
print("Juice2 Nosucorese: " + str(Juice2.nosucrose_f))
print("Juice2 Insoluble: " + str(Juice2.insoluble_f))
print("Juice2 Pressure: " + str(Juice2.Pj))
print("Juice2 Temperature: " + str(Juice2.Tj))
print("Juice2 pH: " + str(Juice2.pHj))

Juice3 = Juice1 + Juice2
print("\nTest Add, Juice3 = Juice1 + Juice2:")
print("Juice3 Mass: " + str(Juice3.Mj))
print("Juice3 Water: " + str(Juice3.water_f))
print("Juice3 Sucrose: " + str(Juice3.sucrose_f))
print("Juice3 Nosucorese: " + str(Juice3.nosucrose_f))
print("Juice3 Insoluble: " + str(Juice3.insoluble_f))
print("Juice3 Pressure: " + str(Juice3.Pj))
print("Juice3 Temperature: " + str(Juice3.Tj))
print("Juice3 pH: " + str(Juice3.pHj))
print("")

print("=================================================================================")
print("                                  Water Stream                                   ")
print("=================================================================================")
Water1 = water(100.0, 200.0*(10**3), 110.0, 6.0)
print("Water1: 100.0 [t/h], 200.0 [kPa], 110.0 [C], 6.0 [pH]")
print("Water1 Mass: " + str(Water1.Mw))
print("Water1 Water: " + str(Water1.water_f))
print("Water1 Sucrose: " + str(Water1.sucrose_f))
print("Water1 Nosucorese: " + str(Water1.nosucrose_f))
print("Water1 Insoluble: " + str(Water1.insoluble_f))
print("Water1 Pressure: " + str(Water1.Pw))
print("Water1 Temperature: " + str(Water1.Tw))
print("Water1 pH: " + str(Water1.pHj))
print("Water1 density: " + str(Water1.pw) + "\tWater1 density probe: "  + str(Water1.properties_calc(110.0)[0]))
print("Water1 enthalpy: " + str(Water1.Hw) + "\tWater1 enthalpy probe: "  + str(Water1.properties_calc(110.0)[1]))

Water2 = water(110.0, 250*(10**3), 70.0, 8.0)
print("\nWater2: 110.0 [t/h], 250.0 [kPa], 70.0 [C], 8.0 [pH]")
print("Water2 Mass: " + str(Water2.Mw))
print("Water2 Water: " + str(Water2.water_f))
print("Water2 Sucrose: " + str(Water2.sucrose_f))
print("Water2 Nosucorese: " + str(Water2.nosucrose_f))
print("Water2 Insoluble: " + str(Water2.insoluble_f))
print("Water2 Pressure: " + str(Water2.Pw))
print("Water2 Temperature: " + str(Water2.Tw))
print("Water2 pH: " + str(Water2.pHj))

Water3 = Water1 + Water2
print("\nTest Add, Water3 = Water1 + Water2:")
print("Water3 Mass: " + str(Water3.Mj))
print("Water3 Water: " + str(Water3.water_f))
print("Water3 Sucrose: " + str(Water3.sucrose_f))
print("Water3 Nosucorese: " + str(Water3.nosucrose_f))
print("Water3 Insoluble: " + str(Water3.insoluble_f))
print("Water3 Pressure: " + str(Water3.Pj))
print("Water3 Temperature: " + str(Water3.Tj))
print("Water3 pH: " + str(Water3.pHj))
