# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re

import numpy as np

from base.contants import *
from base.helper import *
from base.common import *
from base.read_csv_with_pandas import *
from base.read_csv_with_csv import *


def amd_check_rule_1(fail_dir, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_1',
        'Root cause': 'Thermal prochot',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': '',
    }

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    CPU0_CORES_CORE0_Freq_Eff = 'CPU0 CORES CORE0 Freq Eff'
    CPU0_INFRASTRUCTURE2_Value_THM_CORE = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    CPU0_MISC_PROCHOT = 'CPU0 MISC PROCHOT'
    CPU0_INFRASTRUCTURE2_Limit_THM_CORE = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail[CPU0_CORES_CORE0_Freq_Eff]
    CPU0_INFRASTRUCTURE2_Value_THM_CORE_d = data_frame_fail[CPU0_INFRASTRUCTURE2_Value_THM_CORE]
    CPU0_MISC_PROCHOT_d = data_frame_fail[CPU0_MISC_PROCHOT]
    CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d = data_frame_fail[CPU0_INFRASTRUCTURE2_Limit_THM_CORE]

    for idx, value in enumerate(CPU0_CORES_CORE0_Freq_Eff_d):
        if value <= 0.4:
            if CPU0_INFRASTRUCTURE2_Value_THM_CORE_d[idx] >= CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d[idx] and CPU0_MISC_PROCHOT_d[idx] !=0:
                return_dict = check_result_dict
                break

    return return_dict

def amd_check_rule_2(fail_dir, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_2',
        'Root cause': 'Charge AC prochot',
        'Component': 'EC',
        'Solution': '',
        '修复及验证': '',
    }

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    CPU0_CORES_CORE0_Freq_Eff = 'CPU0 CORES CORE0 Freq Eff'
    CPU0_INFRASTRUCTURE2_Value_THM_CORE = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    CPU0_MISC_PROCHOT = 'CPU0 MISC PROCHOT'
    CPU0_INFRASTRUCTURE2_Limit_THM_CORE = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail[CPU0_CORES_CORE0_Freq_Eff]
    CPU0_INFRASTRUCTURE2_Value_THM_CORE_d = data_frame_fail[CPU0_INFRASTRUCTURE2_Value_THM_CORE]
    CPU0_MISC_PROCHOT_d = data_frame_fail[CPU0_MISC_PROCHOT]
    CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d = data_frame_fail[CPU0_INFRASTRUCTURE2_Limit_THM_CORE]

    for idx, value in enumerate(CPU0_CORES_CORE0_Freq_Eff_d):
        if value <= 0.4:
            if CPU0_INFRASTRUCTURE2_Value_THM_CORE_d[idx] < CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d[idx] and CPU0_MISC_PROCHOT_d[idx] !=0:
                return_dict = check_result_dict
                break

    return return_dict

def amd_check_rule_3(fail_dir, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_3',
        'Root cause': 'CPU-Turbo Disabled',
        'Component': 'BIOS',
        'Solution': '更新BIOS开启Turbo重新测试',
        '修复及验证': '',
    }

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    CPU0_CORES_CORE0_Freq_Eff = 'CPU0 CORES CORE0 Freq Eff'
    return return_dict

def amd_check_rule_4(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_4',
        'Root cause': 'EPP value abnormal（power mode不一致）',
        'Component': 'SDE',
        'Solution': '将EPP更改成一样值后重新测试',
        '修复及验证': '',
    }

    CPU0_CORES_CORE0_CPPC_EPP = 'CPU0 CORES CORE0 CPPC EPP'

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    col_fail = data_frame_fail[CPU0_CORES_CORE0_CPPC_EPP]
    col_pass = data_frame_pass[CPU0_CORES_CORE0_CPPC_EPP]

    for idx, value in enumerate(col_fail):
        if value != col_pass[idx]:
            return_dict = check_result_dict
            break
    return return_dict

def amd_check_rule_5(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_5',
        'Root cause': 'PowerSetting(SPL/SPPT/FPPT Limit) abnormal',
        'Component': 'SDE',
        'Solution': '将Power Setting更新成一样值后重新测试',
        '修复及验证': '',
    }
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = ['CPU0 MISC STAPM Time Constant',
                    'CPU0 MISC Slow PPT Time Constant',
                    'CPU0 INFRASTRUCTURE Limit STAPM',
                    'CPU0 INFRASTRUCTURE Limit PPT FAST',
                    'CPU0 INFRASTRUCTURE Limit PPT SLOW',
                    'CPU0 MISC STAPM Time Constant',
                    'CPU0 MISC Slow PPT Time Constant',]

    for col in content_list:
        fail_average_data, pass_average_data = get_two_data_frame_col_average(data_frame_fail, data_frame_pass, col)
        is_delta_larger = is_two_data_delta_larger_than_threshold(fail_average_data, pass_average_data, 0.02)
        if is_delta_larger:
            return_dict = check_result_dict
            logger.info(f"return_dict: {return_dict}")
            break
    return return_dict

def amd_check_rule_6(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_6',
        'Root cause': 'TimeConstant abnormal',
        'Component': 'SDE',
        'Solution': '将TimeConstant值更新成一样后重新测试',
        '修复及验证': '',
    }

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = ['CPU0 MISC STAPM Time Constant',
                    'CPU0 MISC Slow PPT Time Constant',]

    for col in content_list:
        fail_average_data, pass_average_data = get_two_data_frame_col_average(data_frame_fail, data_frame_pass, col)
        is_delta_larger = is_two_data_delta_larger_than_threshold(fail_average_data, pass_average_data, 0.02)
        if is_delta_larger:
            return_dict = check_result_dict
            logger.info(f"return_dict: {return_dict}")
            break
    return return_dict

def amd_check_rule_7(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_7',
        'Root cause': 'Idle  Power 高',
        'Component': 'EE',
        'Solution': 'check idle场景',
        '修复及验证': '',
    }
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    col = 'CPU0 Power Correlation SOCKET Power'

    col_data_fail = data_frame_fail[col]
    # logger.info(f"col_data: {col_data}")

    idle_average_fail = get_col_idle_average(col_data_fail)
    logger.info(f"idle_average_fail: {idle_average_fail}")

    col_data_pass = data_frame_pass[col]
    # logger.info(f"col_data: {col_data}")

    idle_average_pass = get_col_idle_average(col_data_pass)
    logger.info(f"idle_average_pass: {idle_average_pass}")

    is_delta_larger_than_stand = is_two_data_delta_larger_than_threshold(idle_average_fail, idle_average_pass, 2)
    if is_delta_larger_than_stand:
        return_dict = check_result_dict
        logger.info(f"return_dict: {return_dict}")
    return return_dict

def amd_check_rule_8(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_8',
        'Root cause': 'TDC/EDC异常',
        'Component': 'Power',
        'Solution': '',
        '修复及验证': '',
    }
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = ['CPU0 INFRASTRUCTURE Limit TDC VDD',
                    'CPU0 INFRASTRUCTURE Value TDC VDD',
                    'CPU0 INFRASTRUCTURE Limit TDC SOC',
                    'CPU0 INFRASTRUCTURE Value TDC SOC',
                    'CPU0 INFRASTRUCTURE Limit EDC VDD',
                    'CPU0 INFRASTRUCTURE Limit EDC SOC',]

    for col in content_list:
        fail_average_data, pass_average_data = get_two_data_frame_col_average(data_frame_fail, data_frame_pass, col)
        if fail_average_data != pass_average_data:
            return_dict = check_result_dict
            logger.info(f"return_dict: {return_dict}")
            break
    return return_dict

def amd_check_rule_9(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_9',
        'Root cause': '环温高',
        'Component': 'TESTER',
        'Solution': '降低环境温度/增加Idle时间/出风口是否被阻挡',
        '修复及验证': '',
    }
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_1 = get_list_average(col_data_fail)
    check_point_1 = False
    if average_data_fail_1 != 0:
        check_point_1 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_2 = get_list_average(col_data_fail)
    check_point_2 = False
    if average_data_fail_2 >= average_data_fail_1 :
        check_point_2 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_3 = False
    if average_data_fail_1 < average_data_fail_2 :
        check_point_3 = True

    # check_point_4
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM GFX'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM GFX'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_4 = False
    if average_data_fail_1 < average_data_fail_2 :
        check_point_4 = True

    # check_point_5
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM SOC'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM SOC'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_5 = False
    if average_data_fail_1 < average_data_fail_2 :
        check_point_5 = True

    # sensor part
    col = 'Environment Sensor Temp'
    col_data, file_data = get_performance_file_col_data_by_dir(fail_dir, col)
    Sensor_Temp = get_list_average(col_data)
    logger.info(f'Sensor_Temp:{Sensor_Temp}')

    if check_point_1 and check_point_2 and check_point_3 and check_point_4 and check_point_5 and Sensor_Temp >30:
        return_dict = check_result_dict
        logger.info(f"return_dict: {return_dict}")

    return return_dict

def amd_check_rule_10(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_10',
        'Root cause': 'CPU本体可能异常',
        'Component': 'EE',
        'Solution': '',
        '修复及验证': '使用相同sku机台复制验证',
    }
    return return_dict
def amd_check_rule_11(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_11',
        'Root cause': 'CPU Ttie.lmt被触发(触发Tdie,lmt)',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': '使用相同sku机台复制验证',
    }
    return return_dict

def amd_check_rule_12(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_12',
        'Root cause': 'thermal module（STT）',
        'Component': 'Thermal',
        'Solution': '1、降低环境温度/增加Idle时间/出风口是否被阻挡；2、Thermal模组组装或散热膏涂抹异常',
        '修复及验证': '',
    }
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_1 = get_list_average(col_data_fail)
    check_point_1 = False
    if average_data_fail_1 != 0:
        check_point_1 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_2 = get_list_average(col_data_fail)
    check_point_2 = False
    if average_data_fail_2 >= average_data_fail_1 :
        check_point_2 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_3 = False
    if average_data_fail_1 > average_data_fail_2 :
        check_point_3 = True

    # check_point_4
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM GFX'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM GFX'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_4 = False
    if average_data_fail_1 > average_data_fail_2 :
        check_point_4 = True

    # check_point_5
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM SOC'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM SOC'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_5 = False
    if average_data_fail_1 > average_data_fail_2 :
        check_point_5 = True

    # sensor part
    col = 'Environment Sensor Temp'
    col_data, file_data = get_performance_file_col_data_by_dir(fail_dir, col)
    Sensor_Temp = get_list_average(col_data)
    logger.info(f'Sensor_Temp:{Sensor_Temp}')

    if check_point_1 and check_point_2 and check_point_3 and check_point_4 and check_point_5 and Sensor_Temp >= 20 and Sensor_Temp <= 30:
        return_dict = check_result_dict
        logger.info(f"return_dict: {return_dict}")

    return return_dict

def amd_check_rule_13(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_13',
        'Root cause': 'thermal module（STT）',
        'Component': 'Thermal',
        'Solution': '1、降低环境温度/增加Idle时间/出风口是否被阻挡；2、Thermal模组组装或散热膏涂抹异常',
        '修复及验证': '',
    }
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_1 = get_list_average(col_data_fail)
    check_point_1 = False
    if average_data_fail_1 != 0:
        check_point_1 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_2 = get_list_average(col_data_fail)
    check_point_2 = False
    if average_data_fail_2 >= average_data_fail_1 :
        check_point_2 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_3 = False
    if average_data_fail_1 < average_data_fail_2 :
        check_point_3 = True

    # check_point_4
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM GFX'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM GFX'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_4 = False
    if average_data_fail_1 < average_data_fail_2 :
        check_point_4 = True

    # check_point_5
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM SOC'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM SOC'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_5 = False
    if average_data_fail_1 < average_data_fail_2 :
        check_point_5 = True

    # sensor part
    col = 'Environment Sensor Temp'
    col_data, file_data = get_performance_file_col_data_by_dir(fail_dir, col)
    Sensor_Temp = get_list_average(col_data)
    logger.info(f'Sensor_Temp:{Sensor_Temp}')

    if check_point_1 and check_point_2 and check_point_3 and check_point_4 and check_point_5 and Sensor_Temp >= 20 and Sensor_Temp <= 30:
        return_dict = check_result_dict
        logger.info(f"return_dict: {return_dict}")
    return return_dict

def amd_check_rule_14(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_14',
        'Root cause': 'thermal module（STAPM）',
        'Component': 'Thermal',
        'Solution': '1、降低环境温度/增加Idle时间/出风口是否被阻挡；2、Thermal模组组装或散热膏涂抹异常',
        '修复及验证': '',
    }
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_1 = get_list_average(col_data_fail)
    check_point_1 = False
    if average_data_fail_1 == 0:
        check_point_1 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_1 = get_list_average(col_data_fail)
    check_point_2 = False
    if average_data_fail_1 == 0:
        check_point_2 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_3 = False
    if average_data_fail_1 > average_data_fail_2 :
        check_point_3 = True

    # check_point_4
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM GFX'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM GFX'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_4 = False
    if average_data_fail_1 > average_data_fail_2 :
        check_point_4 = True

    # check_point_5
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM SOC'
    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM SOC'
    col_data_fail_1 = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_5 = False
    if average_data_fail_1 > average_data_fail_2 :
        check_point_5 = True

    # sensor part
    col = 'Environment Sensor Temp'
    col_data, file_data = get_performance_file_col_data_by_dir(fail_dir, col)
    Sensor_Temp = get_list_average(col_data)
    logger.info(f'Sensor_Temp:{Sensor_Temp}')

    if check_point_1 and check_point_2 and check_point_3 and check_point_4 and check_point_5 and Sensor_Temp >= 20 and Sensor_Temp <= 30:
        return_dict = check_result_dict
        logger.info(f"return_dict: {return_dict}")
    return return_dict

def amd_check_rule_15(fail_dir, pass_dir):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_15',
        'Root cause': 'Al Chip issue',
        'Component': 'SDE',
        'Solution': '',
        '修复及验证': '分别Disable/Enable AI chip功能验证结果',
    }

    CPU0_CORES_CORE0_CPPC_EPP = 'CPU0 INFRASTRUCTURE Limit STAPM'

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    col_list = ['CPU0 INFRASTRUCTURE Limit STAPM',
                'CPU0 INFRASTRUCTURE Limit PPT FAST',
                'CPU0 INFRASTRUCTURE Limit PPT SLOW']
    for col in col_list:
        col_fail = data_frame_fail[col]
        col_pass = data_frame_pass[col]
        is_two_coloum_same = is_two_col_same(col_fail, col_pass)
        if is_two_coloum_same == False:
            return_dict = check_result_dict
            break
    return return_dict

if __name__ == '__main__':
    pass
