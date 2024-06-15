# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 19:54:58 2024

@author: Mehrnoosh
"""

import numpy as np

def Demand(Q_Trans,Q_Ven,Q_Solar,Q_int, End_Time,Time_step):
    Demand = np.zeros_like(Q_Trans)
    for i in range(End_Time):
        Demand[i, 0] = Q_Trans[i] + Q_Ven[i]  - Q_Solar[i] - Q_int[i]

        if Demand[i] < 0:
            Demand[i] = 0
            
    Q_Demand = Demand
    Q_Demand_tot = (np.sum(Demand))/Time_step
    return Q_Demand_tot, Q_Demand


