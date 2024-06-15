# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 19:43:09 2024

@author: Mehrnoosh
"""

import numpy as np

def Internal(Internal_Factor, Not_Heating, Month, Per_Schedule_year, App_Schedule_year,Time_step):
    app = App_Schedule_year[:]
    Heat_per = (Internal_Factor[0] * Internal_Factor[1] * Per_Schedule_year[:] / 1000)
    Heat_app = (Internal_Factor[2] * (app / 1))/1000
    E_app = Heat_app
    Heat = Heat_app+ Heat_per
    for i in range(len(Month)):
        if Not_Heating[0] <= Month[i] <= Not_Heating[1]:
            Heat[i] = 0
        Heat[i] = max(Heat[i], 0)
    Q_int = Heat
    Q_int_tot = (np.sum(Heat))/Time_step
    
    return Q_int_tot, Q_int, E_app 


