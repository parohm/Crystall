temperature = '298K' # температура в формате '143K'
cryst_number = '43' # номер кристалла в формате '1'

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

    # 16, 23
    agilent_n6701a.set_settings(channel=vdd_blt_channel, voltage=vdd_voltage, current=vdd_current, output=True)
    agilent_n6701a.set_settings(channel=vdd_blf_channel, voltage=vdd_voltage, current=vdd_current, output=True)
    agilent_n6701a.set_settings(channel=vdd_int_gates_i_common_channel, voltage=vdd_voltage, current=vdd_current, output=True)

    # 2, 3, 4, 12, 17 - colsel
    for col in colsel_channels:
        agilent_34980a.close_channel(channel=col)

    # 5, 6
    rohde_schwarz_2.channel_config(channel=1, voltage=vdd_voltage, current=vdd_current, output=True)
    rohde_schwarz_2.channel_config(channel=2, voltage=vdd_voltage, current=vdd_current, output=True)


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
    rohde_schwarz_2.channel_config(channel=3, voltage=0, current=0.001, output=True)
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

def test_0():
    crystall_initial_state_new()
    agilent_34980a.open_channel(channel=arraysel_1_channel)
    agilent_34980a.open_channel(channel=arraysel_0_channel)

    print(f"Started at: ", datetime.datetime.now())
    for iter in range(30)
        for c, col in enumerate(['00000']):
            for bl_blb in ['01', '10']:
                print(f"=====================")
                print(f'Iter: ', iter, ", bl_blb=", bl_blb)
                if bl_blb[0] == '0':
                    rohde_schwarz_2.channel_config(channel=1, voltage=0, current=0.001, output=True)
                elif bl_blb[0] == '1':
                    rohde_schwarz_2.channel_config(channel=1, voltage=vdd_voltage, current=vdd_current, output=True)

                if bl_blb[1] == '0':
                    rohde_schwarz_2.channel_config(channel=2, voltage=0, current=0.001, output=True)
                elif bl_blb[1] == '1':
                    rohde_schwarz_2.channel_config(channel=2, voltage=vdd_voltage, current=vdd_current, output=True)

                rowcel_and_colsel_positions(rowcel_config='00000', colcel_config=col)
                time.sleep(1) # ожидание установки адреса
                agilent_34980a.close_channel(channel=ce_channel)
                time.sleep(1) # запись
                agilent_34980a.open_channel(channel=ce_channel)
                time.sleep(1) # отключение записи

                rohde_schwarz_2.channel_config(channel=1, voltage=vdd_voltage, current=vdd_current, output=True)
                rohde_schwarz_2.channel_config(channel=2, voltage=vdd_voltage, current=vdd_current, output=True)
                time.sleep(1) # ожидание отключения записывающих напряжений
                agilent_34980a.close_channel(channel=ce_channel)

                time.sleep(1) # включение чтения
                bl_current = agilent_34980a.current_measurement(channel=bl_current_channel, console_output=True)
                blb_current = agilent_34980a.current_measurement(channel=blb_current_channel, console_output=True)

                time.sleep(1) # повторное чтение через 1 сек
                bl_current = agilent_34980a.current_measurement(channel=bl_current_channel, console_output=True)
                blb_current = agilent_34980a.current_measurement(channel=blb_current_channel, console_output=True)

    print(f"Ended at: ", datetime.datetime.now())
    open_all()

test_0()