# -*- coding: utf-8 -*-
"""
Created on Thu May 30 11:05:58 2024

@author: Mehrnoosh
"""
import numpy as np
import pandas as pd

def charge_discharge_SH_storage(SH_SOC_max, SH_SOC_min, SH_SOC_switch, SH_SOC, P_HP, Q_SH_need, i, HP, Hour):
    SH_discharged_heat = 0
    SH_charged_HP = 0
    SH_charged_EH = 0
    
    # Discharging
    if Q_SH_need[i] > 0 and SH_SOC > SH_SOC_min:
        SH_discharged_heat = min(SH_SOC - SH_SOC_min, Q_SH_need[i])
        SH_SOC -= SH_discharged_heat
    
    # Charging, Heat pump start
    if 10 < Hour < 18:
        HP = 1  # Set HP to 1 to indicate that the heat pump is charging
        SH_charged_HP = P_HP
        SH_SOC += SH_charged_HP
        if SH_SOC >= SH_SOC_max:
            HP = 0  # Reset HP to 0 if SH_SOC reaches or exceeds SH_SOC_max
            SH_SOC = SH_SOC_max  # Ensure SOC does not exceed the maximum
    
    # Electric heater fallback if SOC is below buffer
    extra_heat_needed = Q_SH_need[i] - SH_discharged_heat
    if extra_heat_needed > 0:
        SH_charged_EH = max(0, extra_heat_needed)  # Ensure it's non-negative
        if SH_SOC > SH_SOC_max:
            SH_SOC = SH_SOC_max
    
    return SH_discharged_heat, SH_SOC, SH_charged_HP, SH_charged_EH, HP

# ..................................................................................

def Q_heat_pump(Q_Demand, Tout, End_Time, C_th, Hour):
    Beta_HP = 0.7 
    Efficiency_HP = 0.46
    thermal_storage_volume = C_th  # Thermal storage volume (in m^3)
    specific_heat_capacity = 4.2  # Specific heat capacity of water (in kJ/kg°C)
    T_max = 90
    T_min = 25
    T_switch = 40
   
    # SOC=state of the charge=thermal_storage_capacity
    SH_SOC_max = thermal_storage_volume * specific_heat_capacity * (T_max - T_min) / (3.6 * 1000)  # Convert from kJ to kWh, Maximum storage capacity (in kWh)
    SH_SOC_min = 0   # Minimum storage capacity (in kWh)
    SH_SOC_switch = thermal_storage_volume * specific_heat_capacity * (T_switch - T_min) / (3.6 * 1000)  # Convert from kJ to kWh, Maximum storage capacity (in kWh)

    max_P_HP = np.max(Q_Demand)
    P_HP = max_P_HP * Beta_HP
    
    # Initial state of charge
    SH_SOC = SH_SOC_max
    HP = 0
    Q_SH_need = Q_Demand
        
    SOC_Q_HP = np.zeros(End_Time)
    COP = np.zeros(End_Time)
    Electricity_HP = np.zeros(End_Time)
    SOC_Q_EH = np.zeros(End_Time)
    COP = np.ones(End_Time)
    Electricity_EH = np.zeros(End_Time)
    SH_discharged_array = np.zeros(End_Time)  # Array to store SH_discharge
    SH_charged_HP_array = np.zeros(End_Time)  # Array to store SH_charged_hp
    SH_charged_EH_array = np.zeros(End_Time)  # Array to store SH_charged_eh
    SH_SOC_array = np.zeros(End_Time)  # Array to store SH_SOC

    for i in range(End_Time):
        # Current hour for charging condition
        current_hour = Hour[i % 24]
        
        # Call the function to get charging heat, discharging heat, updated SOC
        SH_discharged_heat, SH_SOC, SH_charged_HP, SH_charged_EH, HP = charge_discharge_SH_storage(
            SH_SOC_max, SH_SOC_min, SH_SOC_switch, SH_SOC, P_HP, Q_SH_need, i, HP, current_hour
        )

        # Store SH_charged_hp and SH_charged_eh directly in arrays
        SH_discharged_array[i] = SH_discharged_heat
        SH_charged_HP_array[i] = SH_charged_HP
        SH_charged_EH_array[i] = SH_charged_EH
        SH_SOC_array[i] = SH_SOC
        
        # Calculate total heat produced by the heat pump
        total_heat_produced = SH_charged_HP
        
        # Calculate COP based on total heat produced and electricity consumed
        cop = min(6, (Efficiency_HP * (T_max + 273) / (T_max - Tout[i])))
        
        # Calculate electricity consumption of the heat pump
        SOC_Q_HP[i] = total_heat_produced
        COP[i] = cop
        Electricity_HP[i] = total_heat_produced / cop
        
        # Calculate electricity consumption of the Electric Heater 
        SOC_Q_EH[i] = SH_charged_EH
        # EH has COP=1
        Electricity_EH[i] = SH_charged_EH
        
    # Total Electricity used by thermal storage and heat pump
    E_total_request = Electricity_HP + Electricity_EH

    # Create a DataFrame to store the results including SH_charged_hp and SH_charged_eh
    df_output = pd.DataFrame({
        'Q_Demand': Q_Demand.flatten(),
        'SH_discharged': SH_discharged_array,
        'SH_charged_hp': SH_charged_HP_array,
        'SH_charged_eh': SH_charged_EH_array,
        'SH_SOC': SH_SOC_array,
        'Heat_release_HP': SOC_Q_HP,
        'COP': COP,
        'Electricity_needed_HP': Electricity_HP,
        'Electricity_needed_EH': Electricity_EH,
        'Total_Electricity_needed': E_total_request
    })

    # Export the DataFrame to an Excel file
    output_excel_file = 'TES_Output.xlsx'
    df_output.to_excel(output_excel_file, index=False)
    
    return E_total_request
