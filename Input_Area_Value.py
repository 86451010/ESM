# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 17:31:19 2024

@author: Mehrnoosh
"""

import numpy as np
def Area_value(W, D, H, Area_WF, Area_WB, Area_WR, Area_WL, f_correction_floor,
               R_Value_Floor, R_Value_Roof, R_Value_Facade, U_Value_Window):

    Area_Floor = f_correction_floor * W * D
    Area_Roof = W * D
    Area_Facade_F = (W * H) - Area_WF
    Area_Facade_B = (W * H) - Area_WB
    Area_Facade_R = (D * H) - Area_WR
    Area_Facade_L = (D * H) - Area_WL
    Volume = (W * D) * (H)

    Area = np.array([Area_Floor, Area_Facade_F, Area_Facade_B, Area_Facade_L,
                     Area_Facade_R, Area_Roof, Area_WF, Area_WB, Area_WL, Area_WR])

    Values = np.array([(1 / (R_Value_Floor + 0.17)),
                       (1 / (R_Value_Facade + 0.17)),
                       (1 / (R_Value_Facade + 0.17)),
                       (1 / (R_Value_Facade + 0.17)),
                       (1 / (R_Value_Facade + 0.17)),
                       (1 / (R_Value_Roof + 0.17)),
                       U_Value_Window, U_Value_Window, U_Value_Window, U_Value_Window])

    return Area, Volume, Values
