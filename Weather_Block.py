# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 06:52:20 2024

@author: Mehrnoosh
"""

import numpy as np
import pandas as pd

def New_NEN(NEN5060,Time_step):
    
    # input from NEN5060    
    time = NEN5060.iloc[:, 0]
    gg=NEN5060.iloc[:, 5]
    gd=NEN5060.iloc[:, 6]
    gb=NEN5060.iloc[:, 7]
    to=NEN5060.iloc[:, 9]
    to_array = to.values
    tout= to_array * 0.1
    
    ET = len(time) + 1
    t_step = Time_step
    new_t_step = 1 / t_step

    # New Time
    new_time_steps = np.arange(0 + new_t_step, 8760 + new_t_step, new_t_step)
    
    # New Month
    new_months = np.zeros(len(new_time_steps))

    for i, step in enumerate(new_time_steps):
        if step <= 744:
            new_months[i] = 1   
        elif step <= 1416:
            new_months[i] = 2   
        elif step <= 2160:
            new_months[i] = 3   
        elif step <= 2880:
            new_months[i] = 4    
        elif step <= 3624:
            new_months[i] = 5    
        elif step <= 4344:
            new_months[i] = 6    
        elif step <= 5088:
            new_months[i] = 7     
        elif step <= 5832:
            new_months[i] = 8     
        elif step <= 6552:
            new_months[i] = 9   
        elif step <= 7296:
            new_months[i] = 10    
        elif step <= 8016:
            new_months[i] = 11      
        else:
            new_months[i] = 12    
    
    # New Hour
    new_hour = np.arange(1, 25, new_t_step)
    Hour = np.tile(new_hour, 365)

    # New GG,GD,GB,Tout
    original_data_GG = gg
    original_data_GD = gd
    original_data_GB = gb
    original_data_Tout = tout

    # Interpolate to fill in missing values and expand the dataset
    Time=new_time_steps
    Month=new_months
    GG=np.interp(new_time_steps, np.arange(1, ET), original_data_GG)
    GD=np.interp(new_time_steps, np.arange(1, ET), original_data_GD)
    GB= np.interp(new_time_steps, np.arange(1, ET), original_data_GB)
    
    Tout= np.interp(new_time_steps, np.arange(1, ET), original_data_Tout)
    End_Time = len(Time)
    
# .............................Print_NEN5060_TS.................................    
    
    df_output = pd.DataFrame({
        'Time': Time,
        'Month': Month,
        'Hour': Hour,
        'GG': GG,
        'GD': GD,
        'GB': GB,
        'Tout': Tout
    })

    output_excel_file = 'NEN5060_TS_Out.xlsx'

    df_output.to_excel(output_excel_file, index=False)
    
    return Time, Month, Hour, GG, GD, GB, Tout, End_Time 
    