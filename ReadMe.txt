Main 
•	import library and modules
•	weather-Block, import csv file, Timestep (if you want to have 30 min instead of 1 hour, we should choose Timestep=2)
•	TES-Block, C-th (capacity of the thermal storage)
•	EES-Block, Eta-PV (efficiency of PV), f-PV (PV area respect to roof area), C-batt (capacity of the battery)
Weather-Block
Building-Block
•	Input data (location and orientation, surfaces area, factors, …)
•	Export output as xlsx
•	Plot graphs (transmission, ventilation, sun, internal, total demand)
•	Output (Q-demand)
TES-Block
•	Input (TES specifications, heat pump, electric heater)
•	Functions (charging and discharging of thermal storage)
•	Export output as xlsx
•	Output (total electricity needs for TES-Block)
EES-Block
•	Input (EES specifications)
•	Functions (charging and discharging of electrochemical storage)
•	Export output as xlsx
•	Plot graphs (grid dependency, distribution of electricity)
