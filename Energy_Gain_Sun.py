# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 18:56:01 2024

@author: Mehrnoosh
"""

import numpy as np

def Solar(Irradation, Area, ZTA_Window, Not_Heating, Month, End_Time,Time_step):
    # Front
    Heat_f = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Heat_f[i] = (Area[6] * ZTA_Window * Irradation[i, 0]) / 1000
        if Not_Heating[0] <= Month[i] <= Not_Heating[1]:
            Heat_f[i] = 0
        Heat_f[i] = max(Heat_f[i], 0)
    Q_Solar_f = Heat_f
    Q_Solar_f_tot = np.sum(Heat_f)/Time_step
    
    # Back
    Heat_b = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Heat_b[i] = (Area[7] * ZTA_Window * Irradation[i, 1]) / 1000
        if Not_Heating[0] <= Month[i] <= Not_Heating[1]:
            Heat_b[i] = 0
        Heat_b[i] = max(Heat_b[i], 0)
    Q_Solar_b = Heat_b
    Q_Solar_b_tot = np.sum(Heat_b)/Time_step
    
    # Left
    Heat_l = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Heat_l[i] = (Area[8] * ZTA_Window * Irradation[i, 2]) / 1000
        if Not_Heating[0] <= Month[i] <= Not_Heating[1]:
            Heat_l[i] = 0
        Heat_l[i] = max(Heat_l[i], 0)
    Q_Solar_l = Heat_l
    Q_Solar_l_tot = np.sum(Heat_l)/Time_step
    
    # Right
    Heat_r = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Heat_r[i] = (Area[9] * ZTA_Window * Irradation[i, 3]) / 1000
        if Not_Heating[0] <= Month[i] <= Not_Heating[1]:
            Heat_r[i] = 0
        Heat_r[i] = max(Heat_r[i], 0)
    Q_Solar_r = Heat_r
    Q_Solar_r_tot = np.sum(Heat_r)/Time_step
    
    Q_Solar = Q_Solar_f + Q_Solar_b + Q_Solar_l + Q_Solar_r
    Q_Solar_tot = (Q_Solar_f_tot + Q_Solar_b_tot + Q_Solar_l_tot + Q_Solar_r_tot)
    
    return Q_Solar, Q_Solar_tot


