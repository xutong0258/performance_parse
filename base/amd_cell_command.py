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

    df_amd_fail = get_amd_performance_file_data_frame_by_dir(fail_dir)

    amd_pass_file = get_SystemDeckPM_file_with_dir(pass_dir)
    df_amd_pass = read_csv_with_pandas(amd_pass_file)

    content_list = ['CPU0 MISC STAPM Time Constant',
                    'CPU0 MISC Slow PPT Time Constant',
                    'CPU0 INFRASTRUCTURE Limit STAPM',
                    'CPU0 INFRASTRUCTURE Limit PPT FAST',
                    'CPU0 INFRASTRUCTURE Limit PPT SLOW',
                    'CPU0 MISC STAPM Time Constant',
                    'CPU0 MISC Slow PPT Time Constant',]

    for col in content_list:
        fail_average_data, pass_average_data = get_two_data_frame_col_average(df_amd_fail, df_amd_pass, col)
        is_delta_larger = is_two_data_delta_larger_than_threshold(fail_average_data, pass_average_data, 0.02)
        if is_delta_larger:
            return_dict = check_result_dict
            logger.info(f"return_dict: {return_dict}")
            break
    return return_dict
if __name__ == '__main__':
    pass
