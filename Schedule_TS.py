# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:05:00 2024

@author: Mehrnoosh
"""

import numpy as np
import pandas as pd

def Schedule_year(Schedule,Time_step):
    
    Hour_Schedule = Schedule.iloc[:, 0]     
    Per_Schedule = Schedule.iloc[:, 1]  
    Ven_Schedule = Schedule.iloc[:, 2]   
    App_Schedule = Schedule.iloc[:, 6]
    DHW_Schedule = Schedule.iloc[:, 7]

    new_t_step = 1 / Time_step
    ET = len(Hour_Schedule) + 1

    # Interpolate 
    original_Per_Schedule = Per_Schedule
    original_ven_Schedule = Ven_Schedule
    original_app_Schedule = App_Schedule
    original_DHW_Schedule = DHW_Schedule

    Hour = np.arange(0+new_t_step, 24+new_t_step, new_t_step)
    Per = np.interp(Hour, np.arange(1, ET), original_Per_Schedule)
    Ven = np.interp(Hour, np.arange(1, ET), original_ven_Schedule)
    App = np.interp(Hour, np.arange(1, ET), original_app_Schedule)
    DHW = np.interp(Hour, np.arange(1, ET), original_DHW_Schedule)

    Hour_Schedule_year = np.tile(Hour, 365)
    Per_Schedule_year = np.tile(Per, 365)
    Ven_Schedule_year = np.tile(Ven, 365)
    App_Schedule_year = np.tile(App, 365)
    DHW_Schedule_year = np.tile(DHW, 365)

# .............................Plot_Schedule_TS................................. 

    df_output = pd.DataFrame({
        'Hour_Schedule': Hour_Schedule_year,
        'Per_Schedule': Per_Schedule_year,
        'Ven_Schedule': Ven_Schedule_year,
        'App_Schedule': App_Schedule_year,
        'DHW_Schedule': DHW_Schedule_year,

    })

    # Specify the file path where you want to save the Excel file
    output_excel_file = 'Schedule_TS_Out.xlsx'

    # Export the DataFrame to an Excel file
    df_output.to_excel(output_excel_file, index=False)
    
    return Hour_Schedule_year, Per_Schedule_year, Ven_Schedule_year, App_Schedule_year,DHW_Schedule_year



    