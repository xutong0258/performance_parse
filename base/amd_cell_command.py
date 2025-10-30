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
from onnxslim.utils import check_point

from base.contants import *
from base.helper import *
from base.common import *
from base.read_csv_with_pandas import *
from base.read_csv_with_csv import *


def amd_check_rule_1(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_1')

    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_1',
        'Root cause': 'Thermal prochot',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': '',
    }

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')
        
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail.get('CPU0 CORES CORE0 Freq Eff', None)
    CPU0_INFRASTRUCTURE2_Value_THM_CORE_d = data_frame_fail.get('CPU0 INFRASTRUCTURE2 Value THM CORE', None)
    CPU0_MISC_PROCHOT_d = data_frame_fail.get('CPU0 MISC PROCHOT', None)
    CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d = data_frame_fail.get('CPU0 INFRASTRUCTURE2 Limit THM CORE', None)

    if CPU0_CORES_CORE0_Freq_Eff_d is None or CPU0_INFRASTRUCTURE2_Value_THM_CORE_d is None or CPU0_MISC_PROCHOT_d is None or CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d is None:
        return return_dict

    check_point_1 = False
    check_point_2 = False
    check_point_3 = False

    for idx, value in enumerate(CPU0_CORES_CORE0_Freq_Eff_d):
        # logger.info(f'Freq Eff:{value}')
        Value_THM = CPU0_INFRASTRUCTURE2_Value_THM_CORE_d[idx]
        Limit_THM = CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d[idx]
        MISC_PROCHOT = CPU0_MISC_PROCHOT_d[idx]

        if value <= 0.54 :
            check_point_1 = True
        if Value_THM >= Limit_THM :
            check_point_2 = True
        if CPU0_MISC_PROCHOT_d[idx] !=0:
            check_point_3 = True

    if check_point_1 and check_point_2 and check_point_3:
        return_dict = check_result_dict
    logger.info(f'return_dict:{return_dict}')

    # result_yaml_file = 'result.yaml'
    # result_yaml_file = os.path.join(parent_dir, result_yaml_file)
    #
    # dump_file(result_yaml_file, return_dict)
    return return_dict

def amd_check_rule_2(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_2')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_2',
        'Root cause': 'Charge AC prochot',
        'Component': 'EC',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')
        
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail.get('CPU0 CORES CORE0 Freq Eff', None)
    CPU0_INFRASTRUCTURE2_Value_THM_CORE_d = data_frame_fail.get('CPU0 INFRASTRUCTURE2 Value THM CORE', None)
    CPU0_MISC_PROCHOT_d = data_frame_fail.get('CPU0 MISC PROCHOT', None)
    CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d = data_frame_fail.get('CPU0 INFRASTRUCTURE2 Limit THM CORE', None)

    if CPU0_CORES_CORE0_Freq_Eff_d is None or CPU0_INFRASTRUCTURE2_Value_THM_CORE_d is None or CPU0_MISC_PROCHOT_d is None or CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d is None:
        return return_dict

    check_point_1 = False
    check_point_2 = False
    check_point_3 = False

    for idx, value in enumerate(CPU0_CORES_CORE0_Freq_Eff_d):
        Value_THM = CPU0_INFRASTRUCTURE2_Value_THM_CORE_d[idx]
        Limit_THM = CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d[idx]
        MISC_PROCHOT = CPU0_MISC_PROCHOT_d[idx]

        if value <= 0.54:
            check_point_1 = True
        if Value_THM < Limit_THM:
            check_point_2 = True
        if CPU0_MISC_PROCHOT_d[idx] != 0:
            check_point_3 = True

    if check_point_1 and check_point_2 and check_point_3:
        return_dict = check_result_dict
    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_3(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_3')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_3',
        'Root cause': 'CPU-Turbo Disabled',
        'Component': 'BIOS',
        'Solution': '更新BIOS开启Turbo重新测试',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    col = 'CPU0 CORES CORE0 Freq Eff'
    fail_col_data, fail_file_data = get_amd_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_amd_file_col_data_by_dir(pass_dir, col)

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    is_delta_larger = is_two_data_delta_larger_than_threshold(average_fail, average_pass, 0.1)
    logger.info(f'is_delta_larger:{is_delta_larger}')

    if is_delta_larger:
        return_dict = check_result_dict
    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_4(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_4')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_4',
        'Root cause': 'EPP value abnormal（power mode不一致）',
        'Component': 'SDE',
        'Solution': '将EPP更改成一样值后重新测试',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    col = 'CPU0 CORES CORE0 EPP'
    fail_col_data, fail_file_data = get_amd_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_amd_file_col_data_by_dir(pass_dir, col)

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    is_delta_larger = is_two_data_delta_larger_than_threshold(average_fail, average_pass, 0.1)
    logger.info(f'is_delta_larger:{is_delta_larger}')

    if is_delta_larger:
        return_dict = check_result_dict
    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_5(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_5')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_5',
        'Root cause': 'PowerSetting(SPL/SPPT/FPPT Limit) abnormal',
        'Component': 'SDE',
        'Solution': '将Power Setting更新成一样值后重新测试',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    head_list = get_amd_performance_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')

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
        logger.info(f'col:{col}')
        fail_average_data, pass_average_data = get_two_data_frame_col_average(data_frame_fail, data_frame_pass, col, head_list)
        is_delta_larger = is_two_data_delta_larger_than_threshold(fail_average_data, pass_average_data, 0.2)
        logger.info(f'is_delta_larger:{is_delta_larger}')

        if is_delta_larger:
            return_dict = check_result_dict
            break
    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_6(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_6')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_6',
        'Root cause': 'TimeConstant abnormal',
        'Component': 'SDE',
        'Solution': '将TimeConstant值更新成一样后重新测试',
        '修复及验证': '',
    }

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    head_list = get_amd_performance_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = ['CPU0 MISC STAPM Time Constant',
                    'CPU0 MISC Slow PPT Time Constant',]

    for col in content_list:
        fail_average_data, pass_average_data = get_two_data_frame_col_average(data_frame_fail, data_frame_pass, col, head_list)
        is_delta_larger = is_two_data_delta_larger_than_threshold(fail_average_data, pass_average_data, 0.2)
        if is_delta_larger:
            return_dict = check_result_dict
            break
    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_7(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_7')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_7',
        'Root cause': 'Idle  Power 高',
        'Component': 'EE',
        'Solution': 'check idle场景',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

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

    is_delta_larger_than_stand = is_two_data_delta_larger_than_threshold(idle_average_fail, idle_average_pass, 0.02)
    logger.info(f"is_delta_larger_than_stand: {is_delta_larger_than_stand}")
    if is_delta_larger_than_stand:
        return_dict = check_result_dict

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_8(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_8')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_8',
        'Root cause': 'TDC/EDC异常',
        'Component': 'Power',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if True:
        return return_dict
    head_list = get_amd_performance_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = ['CPU0 INFRASTRUCTURE Limit TDC VDD',
                    'CPU0 INFRASTRUCTURE Value TDC VDD',
                    'CPU0 INFRASTRUCTURE Limit TDC SOC',
                    'CPU0 INFRASTRUCTURE Value TDC SOC',
                    'CPU0 INFRASTRUCTURE Limit EDC VDD',
                    'CPU0 INFRASTRUCTURE Limit EDC SOC',]

    for col in content_list:
        fail_average_data, pass_average_data = get_two_data_frame_col_average(data_frame_fail, data_frame_pass, col, head_list)
        if fail_average_data != pass_average_data:
            return_dict = check_result_dict
            break

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_9(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_9')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_9',
        'Root cause': '环温高',
        'Component': 'TESTER',
        'Solution': '降低环境温度/增加Idle时间/出风口是否被阻挡',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if True:
        return return_dict

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

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_10(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_10')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_10',
        'Root cause': 'CPU本体可能异常',
        'Component': 'EE',
        'Solution': '',
        '修复及验证': '使用相同sku机台复制验证',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail['CPU0 CORES CORE0 Freq Eff']
    CPU0_CORES_CORE0_CPPC_MAX_Freq_d = data_frame_fail['CPU0 CORES CORE0 CPPC MAX Freq']

    CPU0_INFRASTRUCTURE2_Value_THM_d = data_frame_fail.get('CPU0 INFRASTRUCTURE Value THM', None)
    CPU0_INFRASTRUCTURE2_Limit_THM_d = data_frame_fail.get('CPU0 INFRASTRUCTURE Limit THM', None)


    if CPU0_INFRASTRUCTURE2_Value_THM_d is None or CPU0_CORES_CORE0_Freq_Eff_d is None:
        return return_dict

    check_point_1 = False
    check_point_2 = False
    check_point_3 = False

    for idx, value in enumerate(CPU0_CORES_CORE0_Freq_Eff_d):
        Freq_Eff = CPU0_CORES_CORE0_Freq_Eff_d[idx]
        MAX_Freq = CPU0_CORES_CORE0_CPPC_MAX_Freq_d[idx]

        Value_THM = CPU0_INFRASTRUCTURE2_Value_THM_d[idx]
        Limit_THM = CPU0_INFRASTRUCTURE2_Limit_THM_d[idx]

        if Freq_Eff < MAX_Freq :
            check_point_1 = True
        if Value_THM < Limit_THM :
            check_point_2 = True

    if check_point_1 and check_point_2:
        return_dict = check_result_dict
    logger.info(f'return_dict:{return_dict}')

    return return_dict

def amd_check_rule_11(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_11')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_11',
        'Root cause': 'CPU Ttie.lmt被触发(触发Tdie,lmt)',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': '使用相同sku机台复制验证',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail['CPU0 CORES CORE0 Freq Eff']
    CPU0_CORES_CORE0_CPPC_MAX_Freq_d = data_frame_fail['CPU0 CORES CORE0 CPPC MAX Freq']

    CPU0_INFRASTRUCTURE2_Value_THM_d = data_frame_fail.get('CPU0 INFRASTRUCTURE Value THM', None)
    CPU0_INFRASTRUCTURE2_Limit_THM_d = data_frame_fail.get('CPU0 INFRASTRUCTURE Limit THM', None)

    if CPU0_INFRASTRUCTURE2_Value_THM_d is None or CPU0_CORES_CORE0_Freq_Eff_d is None:
        return return_dict

    check_point_1 = False
    check_point_2 = False
    check_point_3 = False
    for idx, value in enumerate(CPU0_CORES_CORE0_Freq_Eff_d):
        Freq_Eff = CPU0_CORES_CORE0_Freq_Eff_d[idx]
        MAX_Freq = CPU0_CORES_CORE0_CPPC_MAX_Freq_d[idx]

        Value_THM = CPU0_INFRASTRUCTURE2_Value_THM_d[idx]
        Limit_THM = CPU0_INFRASTRUCTURE2_Limit_THM_d[idx]
        logger.info(f'Value_THM:{Value_THM}')
        logger.info(f'Limit_THM:{Limit_THM}')

        if Freq_Eff < MAX_Freq :
            check_point_1 = True
        if Value_THM > Limit_THM :
            check_point_2 = True

    if check_point_1 and check_point_2:
        return_dict = check_result_dict
    logger.info(f'return_dict:{return_dict}')

    return return_dict

def amd_check_rule_12(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_12')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_12',
        'Root cause': 'thermal module（STT）',
        'Component': 'Thermal',
        'Solution': '1、降低环境温度/增加Idle时间/出风口是否被阻挡；2、Thermal模组组装或散热膏涂抹异常',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if True:
        return return_dict

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

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_13(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_13')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_13',
        'Root cause': 'thermal module（STT）',
        'Component': 'Thermal',
        'Solution': '1、降低环境温度/增加Idle时间/出风口是否被阻挡；2、Thermal模组组装或散热膏涂抹异常',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')
    if True:
        return return_dict

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
    col_1 = get_match_col_name(head_list, col_1)
    logger.info(f'col_1:{col_1}')

    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_2 = get_match_col_name(head_list, col_2)
    logger.info(f'col_2:{col_2}')

    col_data_fail_1 = data_frame_fail[col_1]
    max_data_fail_1 = max(col_data_fail_1)
    logger.info(f'{col_1} max_data_fail_1:{max_data_fail_1}')

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)
    logger.info(f'{col_2} average_data_fail_2:{average_data_fail_2}')

    check_point_3 = False
    if max_data_fail_1 is not None and average_data_fail_2 is not None and max_data_fail_1 < average_data_fail_2 :
        check_point_3 = True
    logger.info(f'check_point_3:{check_point_3}')

    if check_point_1 and check_point_2 and check_point_3 :
        return_dict = check_result_dict

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_14(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_14')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_14',
        'Root cause': 'thermal module（STAPM）',
        'Component': 'Thermal',
        'Solution': '1、降低环境温度/增加Idle时间/出风口是否被阻挡；2、Thermal模组组装或散热膏涂抹异常',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict
    head_list = get_amd_performance_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')
    
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    col = 'CPU0 INFRASTRUCTURE2 Limit STT APU'  
    col = get_match_col_name(head_list, col)
    logger.info(f'col:{col}')


    # CPU0 INFRASTRUCTURE2 Limit STT APU
    # col = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_data_fail = data_frame_fail[col]
    average_data_fail_1 = get_list_average(col_data_fail)
    logger.info(f'average_data_fail_1:{average_data_fail_1}')

    check_point_1 = False
    if average_data_fail_1 == 0:
        check_point_1 = True
    logger.info(f'check_point_1:{check_point_1}')

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col = get_match_col_name(head_list, col)
    logger.info(f'col:{col}')

    col_data_fail = data_frame_fail[col]
    average_data_fail_1 = get_list_average(col_data_fail)
    logger.info(f'average_data_fail_1:{average_data_fail_1}')
    check_point_2 = False
    if average_data_fail_1 == 0:
        check_point_2 = True
    logger.info(f'check_point_2:{check_point_2}')

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col_1 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_1 = get_match_col_name(head_list, col_1)
    logger.info(f'col_1:{col_1}')

    col_2 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_2 = get_match_col_name(head_list, col_2)
    logger.info(f'col_2:{col_2}')

    col_data_fail_1 = data_frame_fail[col_1]
    max_data_fail_1 = max(col_data_fail_1)
    logger.info(f'{col_1} max_data_fail_1:{max_data_fail_1}')

    col_data_fail_2 = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail_2)
    logger.info(f'{col_2} average_data_fail_2:{average_data_fail_2}')

    check_point_3 = False
    if max_data_fail_1 is not None and average_data_fail_2 is not None and max_data_fail_1 >= average_data_fail_2 :
        check_point_3 = True
    logger.info(f'check_point_3:{check_point_3}')

    if check_point_1 and check_point_2 and check_point_3:
        return_dict = check_result_dict
        # logger.info(f"return_dict: {return_dict}")

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_15(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_15')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_15',
        'Root cause': 'Al Chip issue',
        'Component': 'SDE',
        'Solution': '',
        '修复及验证': '分别Disable/Enable AI chip功能验证结果',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')
    if True:
        return return_dict
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

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_16(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'amd_check_rule_16')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_16',
        'Root cause': '从AMDZlog中取',
        'Component': 'EE',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    channel_str = 'Controller0-ChannelA-DIMM1'
    channel_dict_fail = get_cpu_log_content(fail_dir, channel_str)
    channel_dict_pass = get_cpu_log_content(pass_dir, channel_str)

    if channel_dict_fail is None:
        return return_dict
    for key, value in channel_dict_fail.items():
        if key not in channel_dict_pass or value not in channel_dict_fail[key]:
            return_dict = check_result_dict

    channel_str = 'Controller0-ChannelB-DIMM1'
    channel_dict_fail = get_cpu_log_content(fail_dir, channel_str)
    channel_dict_pass = get_cpu_log_content(pass_dir, channel_str)

    for key, value in channel_dict_fail.items():
        if key not in channel_dict_pass or value not in channel_dict_fail[key]:
            return_dict = check_result_dict

    logger.info(f'return_dict:{return_dict}')
    return return_dict
if __name__ == '__main__':
    pass
