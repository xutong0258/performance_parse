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

file = os.path.join(CONFIG_PATH, 'amd_check_rule.yaml')
amd_rule_dict = read_file_dict(file)

def amd_check_rule_1(parent_dir=None, fail_dir=None, pass_dir=None):
    rule_name = f'amd_check_rule_1'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')
        
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    col_1 = 'CPU0 CORES CORE0 Freq Eff'
    col_1 = rule_dict.get('col_1', col_1)

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail.get(col_1, None)

    col_2 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_2 = rule_dict.get('col_2', col_2)

    CPU0_INFRASTRUCTURE2_Value_THM_CORE_d = data_frame_fail.get(col_2, None)

    col_3 = 'CPU0 MISC PROCHOT'
    col_3 = rule_dict.get('col_3', col_3)

    CPU0_MISC_PROCHOT_d = data_frame_fail.get(col_3, None)

    col_4 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_4 = rule_dict.get('col_4', col_4)
    CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d = data_frame_fail.get(col_4, None)

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

    return return_dict

def amd_check_rule_2(parent_dir=None, fail_dir=None, pass_dir=None):
    rule_name = f'amd_check_rule_2'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')
        
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)


    col_1 = 'CPU0 CORES CORE0 Freq Eff'
    col_1 = rule_dict.get('col_1', col_1)

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail.get(col_1, None)

    col_2 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_2 = rule_dict.get('col_2', col_2)

    CPU0_INFRASTRUCTURE2_Value_THM_CORE_d = data_frame_fail.get(col_2, None)

    col_3 = 'CPU0 MISC PROCHOT'
    col_3 = rule_dict.get('col_3', col_3)

    CPU0_MISC_PROCHOT_d = data_frame_fail.get(col_3, None)

    col_4 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_4 = rule_dict.get('col_4', col_4)

    CPU0_INFRASTRUCTURE2_Limit_THM_CORE_d = data_frame_fail.get(col_4, None)

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
    rule_name = f'amd_check_rule_3'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        logger.info(f'pass_dir is not dir:{pass_dir}')
        return return_dict

    col_1 = 'CPU0 CORES CORE0 Freq Eff'
    col_1 = rule_dict.get('col_1', col_1)

    fail_col_data, fail_file_data = get_amd_file_col_data_by_dir(fail_dir, col_1)
    pass_col_data, pass_file_data = get_amd_file_col_data_by_dir(pass_dir, col_1)

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
    rule_name = f'amd_check_rule_4'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    col_1 = 'CPU0 CORES CORE0 EPP'
    col_1 = rule_dict.get('col_1', col_1)

    fail_col_data, fail_file_data = get_amd_file_col_data_by_dir(fail_dir, col_1)
    pass_col_data, pass_file_data = get_amd_file_col_data_by_dir(pass_dir, col_1)

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
    rule_name = f'amd_check_rule_5'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    head_list = get_amd_performance_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = []

    col_1 = 'CPU0 MISC STAPM Time Constant'
    col_1 = rule_dict.get('col_1', col_1)
    content_list.append(col_1)

    col_2 = 'CPU0 MISC Slow PPT Time Constant'
    col_2 = rule_dict.get('col_2', col_2)
    content_list.append(col_2)

    col_3 = 'CPU0 INFRASTRUCTURE Limit STAPM'
    col_3 = rule_dict.get('col_3', col_3)
    content_list.append(col_3)

    col_4 = 'CPU0 INFRASTRUCTURE Limit PPT FAST'
    col_4 = rule_dict.get('col_4', col_4)
    content_list.append(col_4)

    col_5 = 'CPU0 INFRASTRUCTURE Limit PPT SLOW'
    col_5 = rule_dict.get('col_5', col_5)
    content_list.append(col_5)

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
    rule_name = f'amd_check_rule_6'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    head_list = get_amd_performance_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = []

    col_1 = 'CPU0 MISC STAPM Time Constant'
    col_1 = rule_dict.get('col_1', col_1)
    content_list.append(col_1)

    col_2 = 'CPU0 MISC Slow PPT Time Constant'
    col_2 = rule_dict.get('col_2', col_2)
    content_list.append(col_2)

    for col in content_list:
        fail_average_data, pass_average_data = get_two_data_frame_col_average(data_frame_fail, data_frame_pass, col, head_list)
        is_delta_larger = is_two_data_delta_larger_than_threshold(fail_average_data, pass_average_data, 0.2)
        if is_delta_larger:
            return_dict = check_result_dict
            break
    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_7(parent_dir=None, fail_dir=None, pass_dir=None):
    rule_name = f'amd_check_rule_7'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        return return_dict

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    col_1 = 'CPU0 Power Correlation SOCKET Power'
    col_1 = rule_dict.get('col_1', col_1)

    col_data_fail = data_frame_fail[col_1]
    # logger.info(f"col_data: {col_data}")

    idle_average_fail = get_col_idle_average(col_data_fail)
    logger.info(f"idle_average_fail: {idle_average_fail}")

    col_data_pass = data_frame_pass[col_1]
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
    rule_name = f'amd_check_rule_8'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    # if True:
    #     return return_dict
    head_list = get_amd_performance_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = []

    col_1 = 'CPU0 INFRASTRUCTURE Limit TDC VDD'
    col_1 = rule_dict.get('col_1', col_1)
    content_list.append(col_1)

    col_2 = 'CPU0 INFRASTRUCTURE Value TDC VDD'
    col_2 = rule_dict.get('col_2', col_2)
    content_list.append(col_2)

    col_3 = 'CPU0 INFRASTRUCTURE Limit TDC SOC'
    col_3 = rule_dict.get('col_3', col_3)
    content_list.append(col_3)

    col_4 = 'CPU0 INFRASTRUCTURE Value TDC SOC'
    col_4 = rule_dict.get('col_4', col_4)
    content_list.append(col_4)

    col_5 = 'CPU0 INFRASTRUCTURE Limit EDC VDD'
    col_5 = rule_dict.get('col_5', col_5)
    content_list.append(col_5)

    col_5 = 'CPU0 INFRASTRUCTURE Limit EDC SOC'
    col_5 = rule_dict.get('col_5', col_5)
    content_list.append(col_5)

    for col in content_list:
        fail_average_data, pass_average_data = get_two_data_frame_col_average(data_frame_fail, data_frame_pass, col, head_list)
        if fail_average_data != pass_average_data:
            return_dict = check_result_dict
            break

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_9(parent_dir=None, fail_dir=None, pass_dir=None):
    rule_name = f'amd_check_rule_9'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    # if True:
    #     return return_dict

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col_1 = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_1 = rule_dict.get('col_1', col_1)

    col_data_fail = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail)
    check_point_1 = False
    if average_data_fail_1 != 0:
        check_point_1 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col_2 = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col_2 = rule_dict.get('col_2', col_2)
    col_data_fail = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail)
    check_point_2 = False
    if average_data_fail_2 >= average_data_fail_1 :
        check_point_2 = True

    # CPU0 INFRASTRUCTURE2 Limit STT APU
    col_3 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_3 = rule_dict.get('col_3', col_3)

    col_4 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_4 = rule_dict.get('col_4', col_4)
    col_data_fail_1 = data_frame_fail[col_3]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail.get(col_4, None)

    check_point_3 = False
    if col_data_fail_2 is not None:
        average_data_fail_2 = get_list_average(col_data_fail_2)
        if average_data_fail_1 < average_data_fail_2 :
            check_point_3 = True

    # check_point_4
    col_5 = 'CPU0 INFRASTRUCTURE2 Value THM GFX'
    col_5 = rule_dict.get('col_5', col_5)

    col_6 = 'CPU0 INFRASTRUCTURE2 Limit THM GFX'
    col_6 = rule_dict.get('col_6', col_6)

    col_data_fail_1 = data_frame_fail.get(col_5, None)
    check_point_4 = False
    if col_data_fail_1 is not None:
        average_data_fail_1 = get_list_average(col_data_fail_1)

        col_data_fail_2 = data_frame_fail[col_6]
        average_data_fail_2 = get_list_average(col_data_fail_2)

        if average_data_fail_1 < average_data_fail_2 :
            check_point_4 = True

    # check_point_5
    col_7 = 'CPU0 INFRASTRUCTURE2 Value THM SOC'
    col_7 = rule_dict.get('col_7', col_7)

    col_8 = 'CPU0 INFRASTRUCTURE2 Limit THM SOC'
    col_8 = rule_dict.get('col_8', col_8)

    col_data_fail_1 = data_frame_fail.get(col_7, None)
    check_point_5 = False
    if col_data_fail_1 is not None:
        average_data_fail_1 = get_list_average(col_data_fail_1)

        col_data_fail_2 = data_frame_fail[col_8]
        average_data_fail_2 = get_list_average(col_data_fail_2)

        if average_data_fail_1 < average_data_fail_2 :
            check_point_5 = True

    # sensor part
    col_9 = 'Environment Sensor Temp'
    col_9 = rule_dict.get('col_9', col_9)

    col_data, file_data = get_performance_file_col_data_by_dir(fail_dir, col_9)
    Sensor_Temp = 0
    if col_data is not None:
        Sensor_Temp = get_list_average(col_data)
        logger.info(f'Sensor_Temp:{Sensor_Temp}')

    if check_point_1 and check_point_2 and check_point_3 and check_point_4 and check_point_5 and Sensor_Temp >30:
        return_dict = check_result_dict

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_10(parent_dir=None, fail_dir=None, pass_dir=None):
    rule_name = f'amd_check_rule_10'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        logger.info(f'pass_dir:{pass_dir}')
        return return_dict

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    col_1 = 'CPU0 CORES CORE0 Freq Eff'
    col_1 = rule_dict.get('col_1', col_1)
    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail[col_1]

    col_2 = 'CPU0 CORES CORE0 CPPC MAX Freq'
    col_2 = rule_dict.get('col_2', col_2)
    CPU0_CORES_CORE0_CPPC_MAX_Freq_d = data_frame_fail[col_2]

    col_3 = 'CPU0 INFRASTRUCTURE Value THM'
    col_3 = rule_dict.get('col_3', col_3)

    CPU0_INFRASTRUCTURE2_Value_THM_d = data_frame_fail.get(col_3, None)

    col_4 = 'CPU0 INFRASTRUCTURE Limit THM'
    col_4 = rule_dict.get('col_4', col_4)

    CPU0_INFRASTRUCTURE2_Limit_THM_d = data_frame_fail.get(col_4, None)

    if CPU0_INFRASTRUCTURE2_Value_THM_d is None or CPU0_CORES_CORE0_Freq_Eff_d is None:
        logger.info(f'return')
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
    rule_name = f'amd_check_rule_11'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    col_1 = 'CPU0 CORES CORE0 Freq Eff'
    col_1 = rule_dict.get('col_1', col_1)

    CPU0_CORES_CORE0_Freq_Eff_d = data_frame_fail[col_1]

    col_2 = 'CPU0 CORES CORE0 CPPC MAX Freq'
    col_2 = rule_dict.get('col_2', col_2)

    CPU0_CORES_CORE0_CPPC_MAX_Freq_d = data_frame_fail[col_2]

    col_3 = 'CPU0 INFRASTRUCTURE Value THM'
    col_3 = rule_dict.get('col_3', col_3)

    CPU0_INFRASTRUCTURE2_Value_THM_d = data_frame_fail.get(col_3, None)

    col_4 = 'CPU0 INFRASTRUCTURE Limit THM'
    col_4 = rule_dict.get('col_4', col_4)
    CPU0_INFRASTRUCTURE2_Limit_THM_d = data_frame_fail.get(col_4, None)

    if CPU0_INFRASTRUCTURE2_Value_THM_d is None or CPU0_CORES_CORE0_Freq_Eff_d is None:
        logger.info(f'return')
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
    rule_name = f'amd_check_rule_12'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if True:
        return return_dict

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    col_1 = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_1 = rule_dict.get('col_1', col_1)

    col_data_fail = data_frame_fail.get(col_1, None)
    check_point_1 = False
    if col_data_fail is not None:
        average_data_fail_1 = get_list_average(col_data_fail)
        if average_data_fail_1 != 0:
            check_point_1 = True

    col_2 = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col_2 = rule_dict.get('col_2', col_2)

    col_data_fail = data_frame_fail.get(col_2, None)
    average_data_fail_2 = get_list_average(col_data_fail)
    check_point_2 = False
    if average_data_fail_2 >= average_data_fail_1 :
        check_point_2 = True

    col_3 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_3 = rule_dict.get('col_3', col_3)

    col_4 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_4 = rule_dict.get('col_4', col_4)

    col_data_fail_1 = data_frame_fail[col_3]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_4]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_3 = False
    if average_data_fail_1 > average_data_fail_2 :
        check_point_3 = True

    # check_point_4
    col_5 = 'CPU0 INFRASTRUCTURE2 Value THM GFX'
    col_5 = rule_dict.get('col_5', col_5)

    col_6 = 'CPU0 INFRASTRUCTURE2 Limit THM GFX'
    col_6 = rule_dict.get('col_6', col_6)
    col_data_fail_1 = data_frame_fail[col_5]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_6]
    average_data_fail_2 = get_list_average(col_data_fail_2)

    check_point_4 = False
    if average_data_fail_1 > average_data_fail_2 :
        check_point_4 = True

    # check_point_5
    col_7 = 'CPU0 INFRASTRUCTURE2 Value THM SOC'
    col_7 = rule_dict.get('col_7', col_7)

    col_8 = 'CPU0 INFRASTRUCTURE2 Limit THM SOC'
    col_8 = rule_dict.get('col_8', col_8)

    col_data_fail_1 = data_frame_fail[col_7]
    average_data_fail_1 = get_list_average(col_data_fail_1)

    col_data_fail_2 = data_frame_fail[col_8]
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
    rule_name = f'amd_check_rule_13'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')
    if True:
        return return_dict

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    col_1 = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_1 = rule_dict.get('col_1', col_1)
    col_data_fail = data_frame_fail[col_1]
    average_data_fail_1 = get_list_average(col_data_fail)
    check_point_1 = False
    if average_data_fail_1 != 0:
        check_point_1 = True


    col_2 = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col_2 = rule_dict.get('col_2', col_2)
    col_data_fail = data_frame_fail[col_2]
    average_data_fail_2 = get_list_average(col_data_fail)
    check_point_2 = False
    if average_data_fail_2 >= average_data_fail_1 :
        check_point_2 = True

    col_3 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_3 = rule_dict.get('col_3', col_3)
    col_3 = get_match_col_name(head_list, col_3)
    logger.info(f'col_1:{col_3}')

    col_4 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_4 = rule_dict.get('col_4', col_4)
    col_4 = get_match_col_name(head_list, col_4)
    logger.info(f'col_4:{col_4}')

    col_data_fail_1 = data_frame_fail[col_3]
    max_data_fail_1 = max(col_data_fail_1)
    logger.info(f'{col_3} max_data_fail_1:{max_data_fail_1}')

    col_data_fail_2 = data_frame_fail[col_4]
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
    rule_name = f'amd_check_rule_14'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if os.path.isdir(pass_dir) == False:
        logger.info(f'return')
        return return_dict
    head_list = get_amd_performance_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')
    
    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    col_1 = 'CPU0 INFRASTRUCTURE2 Limit STT APU'
    col_1 = rule_dict.get('col_1', col_1)
    col = get_match_col_name(head_list, col_1)
    logger.info(f'col_1:{col_1}')

    col_data_fail = data_frame_fail.get(col_1, None)
    average_data_fail_1 = get_list_average(col_data_fail)
    logger.info(f'average_data_fail_1:{average_data_fail_1}')

    check_point_1 = False
    if average_data_fail_1 == 0:
        check_point_1 = True
    logger.info(f'check_point_1:{check_point_1}')

    col_2 = 'CPU0 INFRASTRUCTURE2 Value STT APU'
    col_2 = rule_dict.get('col_2', col_2)
    col_2 = get_match_col_name(head_list, col_2)
    logger.info(f'col_2:{col_2}')

    col_data_fail = data_frame_fail[col_2]
    average_data_fail_1 = get_list_average(col_data_fail)
    logger.info(f'average_data_fail_1:{average_data_fail_1}')
    check_point_2 = False
    if average_data_fail_1 == 0:
        check_point_2 = True
    logger.info(f'check_point_2:{check_point_2}')

    col_3 = 'CPU0 INFRASTRUCTURE2 Value THM CORE'
    col_3 = rule_dict.get('col_3', col_3)
    col_3 = get_match_col_name(head_list, col_3)
    logger.info(f'col_1:{col_3}')

    col_4 = 'CPU0 INFRASTRUCTURE2 Limit THM CORE'
    col_4 = rule_dict.get('col_4', col_4)
    col_4 = get_match_col_name(head_list, col_4)
    logger.info(f'col_4:{col_4}')

    col_data_fail_1 = data_frame_fail[col_3]
    max_data_fail_1 = max(col_data_fail_1)
    logger.info(f'{col_3} max_data_fail_1:{max_data_fail_1}')

    col_data_fail_2 = data_frame_fail[col_4]
    average_data_fail_2 = get_list_average(col_data_fail_2)
    logger.info(f'{col_4} average_data_fail_2:{average_data_fail_2}')

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
    rule_name = f'amd_check_rule_15'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')
    if True:
        return return_dict
    CPU0_CORES_CORE0_CPPC_EPP = 'CPU0 INFRASTRUCTURE Limit STAPM'

    data_frame_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)
    data_frame_pass = get_amd_performance_file_data_frame_by_dir(pass_dir)

    content_list = []

    col_1 = 'CPU0 INFRASTRUCTURE Limit STAPM'
    col_1 = rule_dict.get('col_1', col_1)
    content_list.append(col_1)

    col_2 = 'CPU0 INFRASTRUCTURE Limit PPT FAST'
    col_2 = rule_dict.get('col_2', col_2)
    content_list.append(col_2)

    col_2 = 'CPU0 INFRASTRUCTURE Limit PPT SLOW'
    col_2 = rule_dict.get('col_2', col_2)
    content_list.append(col_2)

    for col in content_list:
        col_fail = data_frame_fail[col]
        col_pass = data_frame_pass[col]
        is_two_coloum_same = is_two_col_same(col_fail, col_pass)
        if is_two_coloum_same == False:
            return_dict = check_result_dict
            break

    logger.info(f'return_dict:{return_dict}')
    return return_dict

def amd_check_rule_16(parent_dir=None, fail_dir=None, pass_dir=None):
    rule_name = f'amd_check_rule_16'
    logger.info(f'{rule_name}')
    return_dict = None
    check_result_dict = {}
    rule_dict = amd_rule_dict.get(rule_name, None)

    check_result_dict['rule name'] = rule_name
    check_result_dict['Root cause'] = rule_dict.get('Root cause')
    check_result_dict['Component'] = rule_dict.get('Component')
    check_result_dict['Solution'] = rule_dict.get('Solution')
    check_result_dict['修复及验证'] = rule_dict.get('修复及验证')
    check_result_dict['判断标准'] = rule_dict.get('判断标准')
    check_result_dict['对比规则'] = rule_dict.get('对比规则')

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
