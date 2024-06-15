# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 09:46:44 2024

@author: Mehrnoosh
"""

#-----------------------------------Import---------------------------------------

import pandas as pd
from Weather_Block import New_NEN
from Building_Block import Building_Block
from TES_Block import Q_heat_pump
from EES_Block import E_PV

#---------------------------------Weather File-----------------------------------

NEN5060 = pd.read_csv('NEN5060.csv')     # Read weather data from csv file
Time_step=1                              # Choose the timestep
Time, Month, Hour, GG, GD, GB, Tout, End_Time  = New_NEN(NEN5060,Time_step)

#-------------------------------Building Block-----------------------------------

Q_Demand, Irradation, E_app = Building_Block(Time, Month, Hour, GG, GD, GB, Tout, End_Time, Time_step)

#----------------------------TES  Block--------------------------------

C_th = 10000         # Capacity of thermal storage
E_total_request = Q_heat_pump(Q_Demand,Tout, End_Time, C_th, Hour)

#----------------------------------Electricity Block--------------------------------------

Eta_PV = 0.216        # Efficiendy of PV
f_PV = 2.29           # Fraction of PV area
C_batt = 500          # Capacity of electrochemical storage  
energy = E_PV(E_total_request, Irradation, E_app, End_Time, Eta_PV, f_PV, C_batt)



