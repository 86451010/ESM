# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 17:47:19 2024

@author: Mehrnoosh
"""
import numpy as np
import pandas as pd

def Irradiation(Orientation, Location, Ro, Time, Hour, GB, GD, GG, End_Time,Time_step):
    # Facade Front
    n = ((Time-0.5) / End_Time) * 365* Time_step
    Delta = 23.45 * np.sin(2 * np.pi * ((284 + n) / 365))
    Omega = (Hour - 12) * 15 + (Location[1] - Location[2])
    Sin_Phi = np.sin((Location[0]) * np.pi / 180)
    Cos_Phi = np.cos((Location[0]) * np.pi / 180)
    Sin_Beta = np.sin((Orientation[0]) * np.pi / 180)
    Cos_Beta = np.cos((Orientation[0]) * np.pi / 180)
    Sin_Gama = np.sin(Orientation[1] * np.pi / 180)
    Cos_Gama = np.cos(Orientation[1] * np.pi / 180)
    Sin_Delta = np.sin(Delta * np.pi / 180)
    Cos_Delta = np.cos(Delta * np.pi / 180)
    Sin_Omega = np.sin(Omega * np.pi / 180)
    Cos_Omega = np.cos(Omega * np.pi / 180)
    Cos_p = 0.5 + 0.5 * Cos_Beta
    Cos_n = 0.5 - 0.5 * Cos_Beta
    Cos_Teta = np.zeros((End_Time, 1))
    Cos_Teta_z = np.zeros((End_Time, 1))
    R_b = np.zeros((End_Time, 1))
    I_t = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Cos_Teta[i] = (Sin_Delta[i] * Sin_Phi * Cos_Beta) - (Sin_Delta[i] * Cos_Phi * Sin_Beta * Cos_Gama) + \
            (Cos_Delta[i] * Cos_Phi * Cos_Beta * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Phi * Sin_Beta * Cos_Gama * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Beta * Sin_Gama * Sin_Omega[i])
        Cos_Teta_z[i] = (Cos_Phi * Cos_Delta[i] * Cos_Omega[i]) + (Sin_Phi * Sin_Delta[i])
        R_b[i] = (Cos_Teta[i]) / (Cos_Teta_z[i])
        I_t[i] = (GB[i] * R_b[i]) + (GD[i] * Cos_p) + (GG[i] * Cos_n * Ro)
    Cos_Teta_z = Cos_Teta_z
    Cos_Teta = Cos_Teta
    I_tt = np.zeros((End_Time, 1))
    for i in range(End_Time):
        if (I_t[i, 0] > 0) and (I_t[i, 0] < 1360):
            I_tt[i, 0] = I_t[i, 0]
        else:
            I_tt[i, 0] = 0
    # # Overhang
    # dep = 1.5
    # top = 0.2
    # high = 2.3
    # Sin_Teta_z = np.zeros((End_Time, 1))
    # Tan_Teta_z = np.zeros((End_Time, 1))
    # Gama_s = np.zeros((End_Time, 1))
    # H_shade = np.zeros((End_Time, 1))
    # F_T = np.zeros((End_Time, 1))
    # for i in range(End_Time):
    #     Sin_Teta_z[i] = np.sqrt(1 - (Cos_Teta_z[i]) ** 2)
    #     Tan_Teta_z[i] = Sin_Teta_z[i] / Cos_Teta_z[i]
    #     Gama_s[i] = (180 / np.pi) * (np.sign(Omega[i])) * \
    #         np.abs(np.arccos(((Cos_Teta_z[i] * Sin_Phi) - Sin_Delta[i]) / (Sin_Teta_z[i] * Cos_Phi)))
    #     H_shade[i] = np.abs((1 / (Sin_Teta_z[i] / Cos_Teta_z[i])) *
    #                             (dep / np.cos(((Orientation[1]) - (Gama_s[i])) * (np.pi / 180))))
    #     if H_shade[i] > top:
    #         F_T[i] = (H_shade[i] - top) / high
    # F_T[i] = 1
    # F_TT = np.zeros((End_Time, 1))
    # I_F_T = np.zeros((End_Time, 1))
    # for i in range(End_Time):
    #     F_TT[i] = max(min(F_T[i], 1), 0)
    #     I_F_T[i] = (1 - F_TT[i]) * I_tt[i]
    I_t_Facade_Front = I_tt

    # Facade Back
    n = ((Time - 0.5) / End_Time) * 365* Time_step
    Delta = 23.45 * np.sin(2 * np.pi * ((284 + n) / 365))
    Omega = (Hour - 12) * 15 + (Location[1] - Location[2])
    Sin_Phi = np.sin((Location[0]) * np.pi / 180)
    Cos_Phi = np.cos((Location[0]) * np.pi / 180)
    Sin_Beta = np.sin((Orientation[2]) * np.pi / 180)
    Cos_Beta = np.cos((Orientation[2]) * np.pi / 180)
    Sin_Gama = np.sin(Orientation[3] * np.pi / 180)
    Cos_Gama = np.cos(Orientation[3] * np.pi / 180)
    Sin_Delta = np.sin(Delta * np.pi / 180)
    Cos_Delta = np.cos(Delta * np.pi / 180)
    Sin_Omega = np.sin(Omega * np.pi / 180)
    Cos_Omega = np.cos(Omega * np.pi / 180)
    Cos_p = 0.5 + 0.5 * Cos_Beta
    Cos_n = 0.5 - 0.5 * Cos_Beta
    Cos_Teta = np.zeros((End_Time, 1))
    Cos_Teta_z = np.zeros((End_Time, 1))
    R_b = np.zeros((End_Time, 1))
    I_t = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Cos_Teta[i] = (Sin_Delta[i] * Sin_Phi * Cos_Beta) - (Sin_Delta[i] * Cos_Phi * Sin_Beta * Cos_Gama) + \
            (Cos_Delta[i] * Cos_Phi * Cos_Beta * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Phi * Sin_Beta * Cos_Gama * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Beta * Sin_Gama * Sin_Omega[i])
        Cos_Teta_z[i] = (Cos_Phi * Cos_Delta[i] * Cos_Omega[i]) + (Sin_Phi * Sin_Delta[i])
        R_b[i] = (Cos_Teta[i]) / (Cos_Teta_z[i])
        I_t[i] = (GB[i] * R_b[i]) + (GD[i] * Cos_p) + (GG[i] * Cos_n * Ro)
    Cos_Teta_z = Cos_Teta_z
    Cos_Teta = Cos_Teta
    I_tt = np.zeros((End_Time, 1))
    for i in range(End_Time):
        if (I_t[i] > 0) and (I_t[i] < 1360):
            I_tt[i] = I_t[i]
        else:
            I_tt[i] = 0
    # # Overhang
    # dep = 1.5
    # top = 0.2
    # high = 2.3
    # Sin_Teta_z = np.zeros((End_Time, 1))
    # Tan_Teta_z = np.zeros((End_Time, 1))
    # Gama_s = np.zeros((End_Time, 1))
    # H_shade = np.zeros((End_Time, 1))
    # F_T = np.zeros((End_Time, 1))
    # for i in range(End_Time):
    #     Sin_Teta_z[i] = np.sqrt(1 - (Cos_Teta_z[i]) ** 2)
    #     Tan_Teta_z[i] = Sin_Teta_z[i] / Cos_Teta_z[i]
    #     Gama_s[i] = (180 / np.pi) * (np.sign(Omega[i])) * \
    #         np.abs(np.arccos(((Cos_Teta_z[i] * Sin_Phi) - Sin_Delta[i]) / (Sin_Teta_z[i] * Cos_Phi)))
    #     H_shade[i] = np.abs((1 / (Sin_Teta_z[i] / Cos_Teta_z[i])) *
    #                             (dep / np.cos(((Orientation[3]) - (Gama_s[i])) * (np.pi / 180))))
    #     if H_shade[i] > top:
    #         F_T[i] = (H_shade[i] - top) / high
    # F_T[i] = 1
    # F_TT = np.zeros((End_Time, 1))
    # I_F_T = np.zeros((End_Time, 1))
    # for i in range(End_Time):
    #     F_TT[i] = max(min(F_T[i], 1), 0)
    #     I_F_T[i] = (1 - F_TT[i]) * I_tt[i]
    I_t_Facade_Back = I_tt

    # Facade Left
    n = ((Time-0.5) / End_Time) * 365* Time_step
    Delta = 23.45 * np.sin(2 * np.pi * ((284 + n) / 365))
    Omega = (Hour - 12) * 15 + (Location[1] - Location[2])
    Sin_Phi = np.sin((Location[0]) * np.pi / 180)
    Cos_Phi = np.cos((Location[0]) * np.pi / 180)
    Sin_Beta = np.sin((Orientation[4]) * np.pi / 180)
    Cos_Beta = np.cos((Orientation[4]) * np.pi / 180)
    Sin_Gama = np.sin(Orientation[5] * np.pi / 180)
    Cos_Gama = np.cos(Orientation[5] * np.pi / 180)
    Sin_Delta = np.sin(Delta * np.pi / 180)
    Cos_Delta = np.cos(Delta * np.pi / 180)
    Sin_Omega = np.sin(Omega * np.pi / 180)
    Cos_Omega = np.cos(Omega * np.pi / 180)
    Cos_p = 0.5 + 0.5 * Cos_Beta
    Cos_n = 0.5 - 0.5 * Cos_Beta
    Cos_Teta = np.zeros((End_Time, 1))
    Cos_Teta_z = np.zeros((End_Time, 1))
    R_b = np.zeros((End_Time, 1))
    I_t = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Cos_Teta[i] = (Sin_Delta[i] * Sin_Phi * Cos_Beta) - (Sin_Delta[i] * Cos_Phi * Sin_Beta * Cos_Gama) + \
            (Cos_Delta[i] * Cos_Phi * Cos_Beta * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Phi * Sin_Beta * Cos_Gama * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Beta * Sin_Gama * Sin_Omega[i])
        Cos_Teta_z[i] = (Cos_Phi * Cos_Delta[i] * Cos_Omega[i]) + (Sin_Phi * Sin_Delta[i])
        R_b[i] = (Cos_Teta[i]) / (Cos_Teta_z[i])
        I_t[i] = (GB[i] * R_b[i]) + (GD[i] * Cos_p) + (GG[i] * Cos_n * Ro)
    Cos_Teta_z = Cos_Teta_z
    Cos_Teta = Cos_Teta
    I_tt = np.zeros((End_Time, 1))
    for i in range(End_Time):
        if (I_t[i] > 0) and (I_t[i] < 1360):
            I_tt[i] = I_t[i]
        else:
            I_tt[i] = 0
    # # Overhang
    # dep = 1.5
    # top = 0.2
    # high = 2.3
    # Sin_Teta_z = np.zeros((End_Time, 1))
    # Tan_Teta_z = np.zeros((End_Time, 1))
    # Gama_s = np.zeros((End_Time, 1))
    # H_shade = np.zeros((End_Time, 1))
    # F_T = np.zeros((End_Time, 1))
    # for i in range(End_Time):
    #     Sin_Teta_z[i] = np.sqrt(1 - (Cos_Teta_z[i]) ** 2)
    #     Tan_Teta_z[i] = Sin_Teta_z[i] / Cos_Teta_z[i]
    #     Gama_s[i] = (180 / np.pi) * (np.sign(Omega[i])) * \
    #         np.abs(np.arccos(((Cos_Teta_z[i] * Sin_Phi) - Sin_Delta[i]) / (Sin_Teta_z[i] * Cos_Phi)))
    #     H_shade[i] = np.abs((1 / (Sin_Teta_z[i] / Cos_Teta_z[i])) *
    #                             (dep / np.cos(((Orientation[5]) - (Gama_s[i])) * (np.pi / 180))))
    #     if H_shade[i] > top:
    #         F_T[i] = (H_shade[i] - top) / high
    # F_T[i] = 1
    # F_TT = np.zeros((End_Time, 1))
    # I_F_T = np.zeros((End_Time, 1))
    # for i in range(End_Time):
    #     F_TT[i] = max(min(F_T[i], 1), 0)
    #     I_F_T[i] = (1 - F_TT[i]) * I_tt[i]
    I_t_Facade_Left = I_tt

    # Facade Right
    n = ((Time-0.5) / End_Time) * 365* Time_step
    Delta = 23.45 * np.sin(2 * np.pi * ((284 + n) / 365))
    Omega = (Hour - 12) * 15 + (Location[1] - Location[2])
    Sin_Phi = np.sin((Location[0]) * np.pi / 180)
    Cos_Phi = np.cos((Location[0]) * np.pi / 180)
    Sin_Beta = np.sin((Orientation[6]) * np.pi / 180)
    Cos_Beta = np.cos((Orientation[6]) * np.pi / 180)
    Sin_Gama = np.sin(Orientation[7] * np.pi / 180)
    Cos_Gama = np.cos(Orientation[7] * np.pi / 180)
    Sin_Delta = np.sin(Delta * np.pi / 180)
    Cos_Delta = np.cos(Delta * np.pi / 180)
    Sin_Omega = np.sin(Omega * np.pi / 180)
    Cos_Omega = np.cos(Omega * np.pi / 180)
    Cos_p = 0.5 + 0.5 * Cos_Beta
    Cos_n = 0.5 - 0.5 * Cos_Beta
    Cos_Teta = np.zeros((End_Time, 1))
    Cos_Teta_z = np.zeros((End_Time, 1))
    R_b = np.zeros((End_Time, 1))
    I_t = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Cos_Teta[i] = (Sin_Delta[i] * Sin_Phi * Cos_Beta) - (Sin_Delta[i] * Cos_Phi * Sin_Beta * Cos_Gama) + \
            (Cos_Delta[i] * Cos_Phi * Cos_Beta * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Phi * Sin_Beta * Cos_Gama * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Beta * Sin_Gama * Sin_Omega[i])
        Cos_Teta_z[i] = (Cos_Phi * Cos_Delta[i] * Cos_Omega[i]) + (Sin_Phi * Sin_Delta[i])
        R_b[i] = (Cos_Teta[i]) / (Cos_Teta_z[i])
        I_t[i] = (GB[i] * R_b[i]) + (GD[i] * Cos_p) + (GG[i] * Cos_n * Ro)
    Cos_Teta_z = Cos_Teta_z
    Cos_Teta = Cos_Teta
    I_tt = np.zeros((End_Time, 1))
    for i in range(End_Time):
        if (I_t[i] > 0) and (I_t[i] < 1360):
            I_tt[i] = I_t[i]
        else:
            I_tt[i] = 0
    # # Overhang
    # dep = 1.5
    # top = 0.2
    # high = 2.3
    # Sin_Teta_z = np.zeros((End_Time, 1))
    # Tan_Teta_z = np.zeros((End_Time, 1))
    # Gama_s = np.zeros((End_Time, 1))
    # H_shade = np.zeros((End_Time, 1))
    # F_T = np.zeros((End_Time, 1))
    # for i in range(End_Time):
    #     Sin_Teta_z[i] = np.sqrt(1 - (Cos_Teta_z[i]) ** 2)
    #     Tan_Teta_z[i] = Sin_Teta_z[i] / Cos_Teta_z[i]
    #     Gama_s[i] = (180 / np.pi) * (np.sign(Omega[i])) * \
    #         np.abs(np.arccos(((Cos_Teta_z[i] * Sin_Phi) - Sin_Delta[i]) / (Sin_Teta_z[i] * Cos_Phi)))
    #     H_shade[i] = np.abs((1 / (Sin_Teta_z[i] / Cos_Teta_z[i])) *
    #                             (dep / np.cos(((Orientation[7]) - (Gama_s[i])) * (np.pi / 180))))
    #     if H_shade[i] > top:
    #         F_T[i] = (H_shade[i] - top) / high
    # F_T[i] = 1
    # F_TT = np.zeros((End_Time, 1))
    # I_F_T = np.zeros((End_Time, 1))
    # for i in range(End_Time):
    #     F_TT[i] = max(min(F_T[i], 1), 0)
    #     I_F_T[i] = (1 - F_TT[i]) * I_tt[i]
    I_t_Facade_Right = I_tt

    # Roof
    n = ((Time-0.5) / End_Time) * 365* Time_step
    Delta = 23.45 * np.sin(2 * np.pi * ((284 + n) / 365))
    Omega = (Hour - 12) * 15 + (Location[1] - Location[2])
    Sin_Phi = np.sin((Location[0]) * np.pi / 180)
    Cos_Phi = np.cos((Location[0]) * np.pi / 180)
    Sin_Beta = np.sin((Orientation[8]) * np.pi / 180)
    Cos_Beta = np.cos((Orientation[8]) * np.pi / 180)
    Sin_Gama = np.sin(Orientation[9] * np.pi / 180)
    Cos_Gama = np.cos(Orientation[9] * np.pi / 180)
    Sin_Delta = np.sin(Delta * np.pi / 180)
    Cos_Delta = np.cos(Delta * np.pi / 180)
    Sin_Omega = np.sin(Omega * np.pi / 180)
    Cos_Omega = np.cos(Omega * np.pi / 180)
    Cos_p = 0.5 + 0.5 * Cos_Beta
    Cos_n = 0.5 - 0.5 * Cos_Beta
    Cos_Teta = np.zeros((End_Time, 1))
    Cos_Teta_z = np.zeros((End_Time, 1))
    R_b = np.zeros((End_Time, 1))
    I_t = np.zeros((End_Time, 1))
    for i in range(End_Time):
        Cos_Teta[i] = (Sin_Delta[i] * Sin_Phi * Cos_Beta) - (Sin_Delta[i] * Cos_Phi * Sin_Beta * Cos_Gama) + \
            (Cos_Delta[i] * Cos_Phi * Cos_Beta * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Phi * Sin_Beta * Cos_Gama * Cos_Omega[i]) + \
            (Cos_Delta[i] * Sin_Beta * Sin_Gama * Sin_Omega[i])
        Cos_Teta_z[i] = (Cos_Phi * Cos_Delta[i] * Cos_Omega[i]) + (Sin_Phi * Sin_Delta[i])
        R_b[i] = (Cos_Teta[i]) / (Cos_Teta_z[i])
        I_t[i] = (GB[i] * R_b[i]) + (GD[i] * Cos_p) + (GG[i] * Cos_n * Ro)
    Cos_Teta_z = Cos_Teta_z
    Cos_Teta = Cos_Teta
    I_tt = np.zeros((End_Time, 1))
    for i in range(End_Time):
        if (I_t[i] > 0) and (I_t[i] < 1360):
            I_tt[i] = I_t[i]
        else:
            I_tt[i] = 0
    I_t_Roof = I_tt

    Irradation = np.concatenate((I_t_Facade_Front, I_t_Facade_Back, I_t_Facade_Left, I_t_Facade_Right, I_t_Roof), axis=1) 
    
    # # Export to Excel
    # df_output = pd.DataFrame({
    # 'I_t_Facade_Front': I_t_Facade_Front.flatten(),
    # 'I_t_Facade_Back': I_t_Facade_Back.flatten(),
    # 'I_t_Facade_Left': I_t_Facade_Left.flatten(),
    # 'I_t_Facade_Right': I_t_Facade_Right.flatten(),
    # 'I_t_Roof': I_t_Roof.flatten(),
    #  })

    # output_excel_file = 'Irradation.xlsx'
    # df_output.to_excel(output_excel_file, index=False)
   
    return Irradation