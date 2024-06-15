# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 12:04:59 2024

@author: Mehrnoosh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Schedule_TS import Schedule_year
from Input_Area_Value import Area_value

def Building_Block (Time, Month, Hour, GG, GD, GB, Tout, End_Time, Time_step):
    
    Schedule = pd.read_csv('Schedule.csv')     # Read scedule profile from csv file
    Hour_Schedule_year, Per_Schedule_year, Ven_Schedule_year, App_Schedule_year, DHW_Schedule_year  = Schedule_year(Schedule,Time_step)
    
    #---------------------------Input data for building-----------------------
    
    # Location-longitude(phi),Latitude(lambda),Latitude-0(lambda0)
    # Reflection Environment of the Builging (Ro)
    ph=52.1; lambda1=5.18; lambda0=15; Ro=0.2; 
    ph = np.array([ph])
    lambda1 = np.array([lambda1])
    lambda0 = np.array([lambda0])

    #Orientation(Facade(Front,Back,Right,Left),Roof)
    beta_FF=90;gama_FF=120;
    beta_FB=90;gama_FB=300;
    beta_FL=90;gama_FL=210;
    beta_FR=90;gama_FR=30;
    beta_R=0;gama_R=0;
    beta_FF = np.array([beta_FF])
    gama_FF = np.array([gama_FF])
    beta_FB = np.array([beta_FB])
    gama_FB = np.array([gama_FB])
    beta_FL = np.array([beta_FL])
    gama_FL = np.array([gama_FL])
    beta_FR = np.array([beta_FR])
    gama_FR = np.array([gama_FR])
    beta_R = np.array([beta_R])
    gama_R = np.array([gama_R])

    #Dimensions(width,depth,height)
    W=35; D=15; H=24;

    #Area of windows(Front,Back,Right,Left)
    Area_WF=480; Area_WB=480; Area_WR=0 ;Area_WL=0;

    # R_Value and U_Value
    R_Value_Floor=3.5; R_Value_Roof=3.5; R_Value_Facade=1.7 ;U_Value_Window=1.4; ZTA_Window=0.55;

    # Others relevent factors 
    f_correction_floor=0.5;             #Correction factor for Floor Transmission toward ground 
    N_app=50;                           #Number of appartment
    N_person=100;                       #Number of Person
    Not_Heating=[5,9];                  #Not Heating Month(start,end)
    Temp=19;                            #Inside temperature
    Ventilation_Factor=[0,0.7];         # Heat recuperation efficiency ventilation,ventilation rate in building
    E_per_person=75 ;  E_app=5;         #GEnergy of person and applience per m2

    Location = np.concatenate((ph, lambda1, lambda0), axis=0)
    Orientation = np.concatenate((beta_FF, gama_FF, beta_FB, gama_FB, beta_FL, gama_FL, beta_FR, gama_FR, beta_R, gama_R), axis=0)    
    Area, Volume, Values = Area_value(W, D, H, Area_WF, Area_WB, Area_WR, Area_WL, f_correction_floor, R_Value_Floor, R_Value_Roof, R_Value_Facade, U_Value_Window)

    E_app_tot = 8 * E_app  * Area[5]    # Total energy of appliances    
    Internal_Factor=[N_person,E_per_person,E_app_tot]
 
    #----------------------------------Functions-----------------------------------

    from Irradiation import Irradiation
    Irradation = Irradiation(Orientation, Location, Ro, Time, Hour, GB, GD, GG, End_Time,Time_step)

    from Energy_Gain_Sun import Solar
    Q_Solar, Q_Solar_tot = Solar(Irradation, Area, ZTA_Window, Not_Heating, Month, End_Time,Time_step)

    from Energy_Loss_Transmission import Transmission
    Q_Trans_tot, Q_Trans = Transmission(Area, Values, Temp, Tout, Not_Heating, Month, End_Time,Time_step)

    from Energy_Loss_Ventilation import Ventilation
    Q_Vent_tot,Q_Ven = Ventilation(Ventilation_Factor,Tout,Temp,Volume,Not_Heating,Month,Ven_Schedule_year, End_Time,Time_step)

    from Energy_Gain_Internal import Internal
    Q_int_tot, Q_int, E_app = Internal(Internal_Factor, Not_Heating, Month, Per_Schedule_year, App_Schedule_year,Time_step)

    from Space_Heating_Energy import Demand
    Q_Demand_tot,Q_Demand = Demand(Q_Trans,Q_Ven,Q_Solar,Q_int, End_Time,Time_step)

    df_output = pd.DataFrame({
    'Q_Demand': Q_Demand.flatten(),
    'Q_Trans': Q_Trans.flatten(),
    'Q_Ven': Q_Ven.flatten(),
    'Q_int': Q_int.flatten(),
    'Q_Sun': Q_Solar.flatten(),
      })
    output_excel_file = 'Space_Heating_Output.xlsx'
    df_output.to_excel(output_excel_file, index=False)

    # ------------------------------------Plot--------------------------------------

    fig, axs = plt.subplots(5, 1, figsize=(10, 15), sharex=True)

    # Plot Demand
    axs[0].plot(Time, Q_Demand, 'b-', linewidth=0.5)
    axs[0].set_title('Heat Demand')
    axs[0].set_ylabel('Demand (kWh/h)')
    axs[0].grid(True)

    # Plot Transmission
    axs[1].plot(Time, Q_Trans, 'b-', linewidth=0.5)
    axs[1].set_title('Transmission')
    axs[1].set_ylabel('Transmission (kWh/h)')
    axs[1].grid(True)

    # Plot Ventilation
    axs[2].plot(Time, Q_Ven, 'b-', linewidth=0.5)
    axs[2].set_title('Ventilation')
    axs[2].set_ylabel('Ventilation (kWh/h)')
    axs[2].grid(True)

    # Plot Internal
    axs[3].plot(Time, Q_int, 'b-', linewidth=0.5)
    axs[3].set_title('Internal')
    axs[3].set_ylabel('Internal (kWh/h)')
    axs[3].grid(True)

    # Plot Solar
    axs[4].plot(Time, Q_Solar, 'b-', linewidth=0.5)
    axs[4].set_title('Solar')
    axs[4].set_ylabel('Solar (kWh/h)')
    axs[4].grid(True)


    plt.xlabel('Time (h)')
    plt.tight_layout()
    plt.show()  
   
    ##------------------------------Domestic Hot Water-----------------------------

    from Domestic_Hot_Water import Q_DHW
    Q_DHW_need_tot,Q_DHW_need = Q_DHW(DHW_Schedule_year, Tout, End_Time)

    
    return Q_Demand, Irradation, E_app