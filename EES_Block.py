# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:03:30 2024

@author: Mehrnoosh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def E_PV(E_total_request, Irradation, E_app, End_Time, Eta_PV, f_PV, C_batt):
    
    W = 35
    D = 15
    Area_Roof = W * D
    Eta = Eta_PV      # Efficiency of PV panels
    f_PV_roof = f_PV    # Fraction of PV on roof on non-transparent parts
    SOC_max_batt = C_batt
    SOC_ini = 0
    SOC_switch_battery = 0.33 * SOC_max_batt
    grid_capacity = 55  # Maximum charge power from the grid (kW)
    
    E_PV = np.zeros(End_Time)
    E_PV_or_tot_req = np.zeros(End_Time)
    E_remain = np.zeros(End_Time)
    E_PV_to_Batt = np.zeros(End_Time)
    E_Build_to_Grid = np.zeros(End_Time)
    E_req_after_PV = np.zeros(End_Time)
    E_Batt_req_after_PV = np.zeros(End_Time)
    E_Grid_to_Build = np.zeros(End_Time)
    E_SOC_array = np.zeros(End_Time)
    E_SOC = np.zeros(End_Time)  # Define E_SOC as a NumPy array
    
    times_G2B_greater_than_capacity = 0  # Counter for the number of times E_Grid_to_Build > grid_capacity
    times_B2G_greater_than_capacity = 0  # Counter for the number of times E_Grid_to_Build > grid_capacity
    
    for i in range(1, End_Time):
        E_SOC[0] = SOC_ini
        if i > 3600 or i < 6480:
            E_PV[i] = 1 * Area_Roof * f_PV_roof * Eta * Irradation[i, 4] / 1000
        else:
            E_PV[i] = Area_Roof * f_PV_roof * Eta * Irradation[i, 4] / 1000
            
        E_PV_or_tot_req[i] = min(E_PV[i], E_total_request[i] + E_app[i])
        E_remain[i] = E_PV[i] - E_PV_or_tot_req[i]
        potential_PV_to_Batt = min(SOC_max_batt - E_SOC[i - 1], E_remain[i])
        E_PV_to_Batt[i] = max(0, min(potential_PV_to_Batt, SOC_max_batt))
        E_Build_to_Grid[i] = E_remain[i] - E_PV_to_Batt[i]
        E_req_after_PV[i] = E_total_request[i] + E_app[i] - E_PV_or_tot_req[i]
        E_Batt_req_after_PV[i] = min(E_req_after_PV[i], E_SOC[i - 1])
        E_Grid_to_Build[i] = E_req_after_PV[i] - E_Batt_req_after_PV[i]
          
        E_SOC[i] = E_SOC[i - 1] + E_PV_to_Batt[i] - E_Batt_req_after_PV[i]
        # Update the battery state of charge based on SOC_switch_battery and off-peak hours
        if E_SOC[i] < SOC_switch_battery:
            # Charge the battery via the grid until SOC_max_batt is reached
            charge_from_grid = min(grid_capacity, SOC_max_batt - E_SOC[i])
            E_SOC[i] = E_SOC[i] + charge_from_grid
            E_Grid_to_Build[i] = E_req_after_PV[i] 

        E_SOC[i] = min(E_SOC[i], 1 * SOC_max_batt)
        
        if E_Grid_to_Build[i] > grid_capacity:  # Check if E_Grid_to_Build > grid_capacity
            times_G2B_greater_than_capacity += 1  
            
        if E_Build_to_Grid[i] > grid_capacity:  # Check if E_Build_to_Grid > grid_capacity
            times_B2G_greater_than_capacity += 1  

        E_SOC_array[i] = E_SOC[i]

    # Calculate total energy exchanged with grid
    grid2build = np.sum(E_Grid_to_Build)
    build2grid = np.sum(E_Build_to_Grid)
        
    # Create a DataFrame to store the results
    df_output = pd.DataFrame({
            'E_SOC_array': E_SOC_array,
            'E_app': E_app,
            'E_total_request': E_total_request,
            'E_PV': E_PV,
            'E_PV_or_tot_req': E_PV_or_tot_req,
            'E_remain': E_remain,
            'E_PV_to_Batt': E_PV_to_Batt,
            'E_req_after_PV': E_req_after_PV,
            'E_Batt_req_after_PV': E_Batt_req_after_PV,
            'E_Build_to_Grid': E_Build_to_Grid,
            'E_Grid_to_Build': E_Grid_to_Build,
        })
    
    # Export the DataFrame to an Excel file
    output_excel_file = 'EES_Output.xlsx'
    df_output.to_excel(output_excel_file, index=False)

    # Slice the DataFrame to include only steps 1000 to 1500
    df_slice = df_output.iloc[0:10000]

    # Plot the sliced data as dots
    plt.figure(figsize=(10, 6))
    plt.scatter(df_slice.index, df_slice['E_Build_to_Grid'], label='Electricity to Grid')  
    plt.scatter(df_slice.index, df_slice['E_Grid_to_Build'], label='Electricity from Grid')  
    plt.xlabel('Time')
    plt.ylabel('Electricity (kWh)')
    plt.title('Total Electricity vs. PV Electricity')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Plot pie chart
    labels = ['Electricity from Grid to Building', 'Electricity from Building to Grid']
    sizes = [grid2build, build2grid]
    colors = [ 'gray' , 'yellow']  
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)  # Add colors parameter
    plt.title('Distribution of Electricity')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()
    
    energy =  build2grid - grid2build
    
    return energy


