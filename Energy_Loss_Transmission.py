# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 19:03:12 2024

@author: Mehrnoosh
"""

import numpy as np

def Transmission(Area, Values, Temp, Tout, Not_Heating, Month, End_Time,Time_step):
    UA = Area * Values
    UA_total = np.sum(UA)
    Heat = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Heat[i] = (UA_total * (Temp - Tout[i])) / 1000
        if Month[i] >= Not_Heating[0] and Month[i] <= Not_Heating[1]:
            Heat[i] = 0
        Heat[i] = max(Heat[i], 0)
    Q_Trans = Heat
    Q_Trans_tot = (np.sum(Heat))/Time_step
    return Q_Trans_tot, Q_Trans


