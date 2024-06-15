# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 11:30:30 2024

@author: Mehrnoosh
"""

import numpy as np

def Q_DHW(DHW_Schedule_year, Tout, End_Time):
    Litre_day_per=45
    N_person=156
    T_supply=45
    
    sum_dhw = np.sum(DHW_Schedule_year)

    Q_DHW_yr = 365 * Litre_day_per * N_person * 4200 * (T_supply - 10) / (1000000 * 3.6)
    P_DHW = Q_DHW_yr / (365 * 24)

    Q_DHW_need = np.zeros(End_Time)    
    for i in range(End_Time):       
        Q_DHW_need[i] = (DHW_Schedule_year[i] / sum_dhw) * Q_DHW_yr
      
    Q_DHW_need_tot = np.sum(Q_DHW_need)

    return Q_DHW_need_tot,Q_DHW_need

