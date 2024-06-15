# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 19:27:37 2024

@author: Mehrnoosh
"""

import numpy as np

def Ventilation(Ventilation_Factor,Tout,Temp,Volume,Not_Heating,Month,Ven_Schedule_year, End_Time,Time_step):
    Heat = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Heat[i] = ( Ven_Schedule_year[i] * 1.2 * Volume * (1 - Ventilation_Factor[0]) * Ventilation_Factor[1] * (Temp - Tout[i])) / 3600
        if Not_Heating[0] <= Month[i] <= Not_Heating[1]:
            Heat[i] = 0
        Heat[i] = max(Heat[i], 0)
    Q_Ven = Heat
    Q_Vent_tot = (np.sum(Heat))/Time_step
    return Q_Vent_tot, Q_Ven








