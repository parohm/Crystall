temperature = 'room'
arrsel_config = '00'

# # Генератор индексов (полная матрица 32х32)
# indexes = ['{0:05b}'.format(i) for i in range(32)]
# values = ['{0:05b}'.format(i) for i in range(32)]

# Свои индексы матрицы (в стоке - матрица 5х5), indexes = rowsel, values = colsel
indexes = ['00000', '00000', '11111', '11111', '01111']
values = ['00000', '11111', '00000', '11111', '01111']


import Agilent_N6701A
import Agilent_34980a
import Rohde_Schwarz_1
import Rohde_Schwarz_2

import numpy as np
import pandas as pd

import datetime
import os


# Agilent 34980a channels
arraysel_1_channel = 1012
arraysel_0_channel = 1011
colsel_channels = [1005, 1004, 1003, 1002, 1001]
rowcel_channels = [1010, 1009, 1008, 1007, 1006]
ce_channel = 1013
bl_voltage_channel = 1014
bl_current_channel = 1041
blb_voltage_channel = 1015
blb_current_channel = 1042
blt_current_channel = 1043
blf_current_channel = 1044
wl_snm_common_channel = 1016
monitor_channel = 1021

# Agilent n6701a channels
vdd_vss_channel = 1
vdd_array_channel = 2
logic_channel = 3

# Rohde schwarz channels
vdd_blt_channel = 1
vdd_blf_channel = 2
vdd_int_gates_i_common_channel = 3

# Level of VDD voltage
vdd_voltage = 1.8
vdd_current = 0.1

# Hardware
agilent_34980a = Agilent_34980a.Agilent_34980a()
agilent_n6701a = Agilent_N6701A.Agilent_n6701a()
rohde_schwarz_1 = Rohde_Schwarz_1.Rohde_Schwarz()
rohde_schwarz_2 = Rohde_Schwarz_2.Rohde_Schwarz()

config_matrix = pd.DataFrame(index=indexes, columns=values)

def rowcel_and_colsel_positions(rowcel_config: str, colcel_config: str):
    for started_index in range(len(colsel_channels)):
        if rowcel_config[started_index] == '1':
            agilent_34980a.close_channel(channel=rowcel_channels[started_index])
        elif rowcel_config[started_index] == '0':
            agilent_34980a.open_channel(channel=rowcel_channels[started_index])

        if colcel_config[started_index] == '1':
            agilent_34980a.close_channel(channel=colsel_channels[started_index])
        elif colcel_config[started_index] == '0':
            agilent_34980a.open_channel(channel=colsel_channels[started_index])

def open_all():
    for channel in [channel for channel in np.arange(1001, 1041, 1)]:
        agilent_34980a.open_channel(channel=channel)

    agilent_n6701a.set_settings(channel=vdd_blt_channel, voltage=0, current=0, output=False)
    agilent_n6701a.set_settings(channel=vdd_blf_channel, voltage=0, current=0, output=False)
    agilent_n6701a.set_settings(channel=logic_channel, voltage=0, current=0, output=False)

    rohde_schwarz_1.channel_config(channel=vdd_blt_channel, voltage=0, current=0, output=False)
    rohde_schwarz_1.channel_config(channel=vdd_blf_channel, voltage=0, current=0, output=False)
    rohde_schwarz_1.channel_config(channel=vdd_int_gates_i_common_channel, voltage=0, current=0, output=False)

    rohde_schwarz_2.channel_config(channel=1, voltage=0, current=0, output=False)
    rohde_schwarz_2.channel_config(channel=2, voltage=0, current=0, output=False)
    rohde_schwarz_2.channel_config(channel=3, voltage=0, current=0, output=False)

def crystall_initial_state_new():
    """
    Инициализируем начальное состояние кристалла по таблице 78
    """
    open_all()

    #######################################################################################
    #                               VDD voltages array                                    #
    #######################################################################################

    # 16, 23, colsel
    agilent_n6701a.set_settings(channel=vdd_blt_channel, voltage=vdd_voltage, current=vdd_current, output=True)
    agilent_n6701a.set_settings(channel=vdd_blf_channel, voltage=vdd_voltage, current=vdd_current, output=True)
    agilent_n6701a.set_settings(channel=vdd_int_gates_i_common_channel, voltage=vdd_voltage, current=vdd_current, output=True)

    # 2, 3, 4, 12, 17
    for col in colsel_channels:
        agilent_34980a.close_channel(channel=col)


    #######################################################################################
    #                               VSS voltages array                                    #
    #######################################################################################

    # 7..11
    for row in rowcel_channels:
        agilent_34980a.open_channel(channel=row)

    # 13, 14, 15
    agilent_34980a.open_channel(channel=arraysel_1_channel)
    agilent_34980a.open_channel(channel=arraysel_0_channel)
    agilent_34980a.open_channel(channel=ce_channel)

    # 20, 21
    agilent_34980a.open_channel(channel=wl_snm_common_channel)
    rohde_schwarz_1.channel_config(channel=vdd_int_gates_i_common_channel, voltage=0, current=0.001, output=True)

    #######################################################################################
    #                                   Not controlled                                    #
    #######################################################################################

    #18, 19, 22
    rohde_schwarz_1.channel_config(channel=vdd_blt_channel, voltage=0, current=0.001, output=True)
    rohde_schwarz_1.channel_config(channel=vdd_blf_channel, voltage=0, current=0.001, output=True)

    agilent_34980a.open_channel(channel=monitor_channel)


    print(80*'*')
    print(30*' ' + 'Начальное состояние')
    print(80 * '*' + '\n')

def test_79(temperature: str, arrsel: str):
    print(80 * '*')
    print(30 * ' ' + 'ТЕСТ 79')
    print(80 * '*' + '\n')

    bl_matrix = pd.DataFrame(index=indexes, columns=values)
    blb_matrix = pd.DataFrame(index=indexes, columns=values)
    monitor_matrix = pd.DataFrame(index=indexes, columns=values)

    crystall_initial_state_new()

    rohde_schwarz_1.channel_config(channel=vdd_blt_channel, voltage=0, current=0.001, output=True)
    rohde_schwarz_1.channel_config(channel=vdd_blf_channel, voltage=0, current=0.001, output=True)
    rohde_schwarz_1.channel_config(channel=vdd_int_gates_i_common_channel, voltage=0, current=0.001, output=True)

    rohde_schwarz_2.channel_config(channel=1, voltage=1.8, current=0.001, output=True)
    rohde_schwarz_2.channel_config(channel=2, voltage=1.8, current=0.001, output=True)
    rohde_schwarz_2.channel_config(channel=3, voltage=0, current=0.001, output=True)

    if arrsel[0] == '0':
        agilent_34980a.open_channel(channel=arraysel_1_channel)
    elif arrsel[0] == '1':
        agilent_34980a.close_channel(channel=arraysel_1_channel)

    if arrsel[1] == '0':
        agilent_34980a.open_channel(channel=arraysel_0_channel)
    elif arrsel[1] == '1':
        agilent_34980a.close_channel(channel=arraysel_0_channel)

    for i, row_label in enumerate(config_matrix.index):
        for j, col_label in enumerate(config_matrix.columns):

            rowcel_and_colsel_positions(rowcel_config=row_label, colcel_config=col_label)

            agilent_34980a.close_channel(channel=ce_channel)

            bl_current = agilent_34980a.current_measurement(channel=bl_current_channel)
            blb_current = agilent_34980a.current_measurement(channel=blb_current_channel)
            monitor_voltage = agilent_34980a.voltage_measurement(channel=monitor_channel)

            bl_matrix.iloc[i, j] = bl_current
            blb_matrix.iloc[i, j] = blb_current
            monitor_matrix.iloc[i, j] = monitor_voltage

            print(f'ROWSEL[4:0] = {row_label}')
            print(f'COLSEL[4:0] = {col_label}')
            print(f'BL current = {round(10**6*bl_current, 3)} uA')
            print(f'BLB current = {round(10**6*blb_current, 3)} uA')
            print(f'MONITOR voltage = {round(monitor_voltage, 3)} V\n')

    open_all()

    current_datetime = datetime.datetime.now()
    path = f'Cryst_measurements/{current_datetime.year}Y{current_datetime.month}M{current_datetime.day}D_Test79_{current_datetime.hour}h{current_datetime.minute}m{current_datetime.second}s_{temperature}K_arrsel{arrsel}'
    os.mkdir(path)
    bl_matrix.to_excel(path + '/BL_current.xlsx')
    blb_matrix.to_excel(path + '/BLB_current.xlsx')
    monitor_matrix.to_excel(path + '/monitor_voltage.xlsx')

test_79(temperature=str(temperature), arrsel=str(arrsel_config))