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
from base.fileOP import *
from base.read_csv_with_pandas import *
from base.read_csv_with_csv import *

path_dir = os.path.dirname(__file__)

file = os.path.join(path_dir, 'intel_check_rule.yaml')
intel_rule_dict = read_file_dict(file)

file = os.path.join(path_dir, 'gpu_check_rule.yaml')
gpu_rule_dict = read_file_dict(file)

def check_rule_1(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_1')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_1',
        'Root cause': 'CPU sample difference',
        'Component': 'EE',
        'Solution': 'Please EE confirm, if the gap is acceptable by Sample difference',
        '修复及验证': '硬件不需要修复，更换硬件',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    logger.info(f'fail_tat_file={fail_tat_file}')

    df = read_csv_with_pandas(fail_tat_file)
    head_list = df.head()
    col_list = []
    for item in head_list:
        if 'CPU' in item and '-Frequency(MHz)' in item:
            col_list.append(item)

    for item in col_list:
        col_2 = 'Power-Package Power(Watts)'
        col_dict = intel_rule_dict.get('check_rule_1', None)
        col_2 = col_dict.get('col_2', col_2)

        logger.info(f"col_2:{col_2}")
        pearson_corr = df[item].corr(df[col_2], method='pearson')
        logger.info(f"皮尔逊相关系数: {pearson_corr:.4f}")
        if pearson_corr < 0.56 and pearson_corr > 0:
            logger.info(f"check_result_dict: {check_result_dict}")
            return_dict = check_result_dict
            break
    return return_dict


def check_rule_2(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_2')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_2',
        'Root cause': 'Power prochot',
        'Component': 'Power',
        'Solution': 'Please power check prochot reason further',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    fail_tat_file = get_tat_file_with_dir(fail_dir)

    df = read_csv_with_pandas(fail_tat_file)
    head_list = df.head()
    col_list = []
    for item in head_list:
        if 'CPU' in item and '-Frequency(MHz)' in item:
            col_list.append(item)

    check_flag = False
    bench_mark = 400
    for item in col_list:
        # col_1 = 'CPU0-Frequency(MHz)'
        col_list = df.get(item)
        lower_index = get_list_lower_index(df[item], bench_mark)
        logger.info(f"lower_index: {lower_index}")
        if lower_index is not None:
            break

    col_2 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_2', None)
    col_2 = col_dict.get('col_2', col_2)
    
    if lower_index is not None:
        check_list = []
        item = df[col_2][lower_index]
        check_list.append(item)

        if lower_index >= 1:
            item = df[col_2][lower_index-1]
            check_list.append(item)

        item = df[col_2][lower_index+1]
        check_list.append(item)

        logger.info(f"check_list: {check_list}")
        count = get_list_text_count(check_list, 'prochot')
        if count:
            logger.info(f"check_result_dict: {check_result_dict}")
            return_dict = check_result_dict
    return return_dict

Processor_Base_Core_Frequency = 2400
def check_rule_3(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_3')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_3',
        'Root cause': 'Thermal prochot',
        'Component': 'Thermal',
        'Solution': 'Please power Thermal prochot reason further.',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    col_1 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_3', None)
    col_1 = col_dict.get('col_1', col_1)
    fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col_1)

    target_index_list = get_list_target_text_index_list(fail_col_data, 'prochot')
    logger.info(f"prochot count: {len(target_index_list)}")

    fail_tat_file = get_tat_file_with_dir(fail_dir)

    df = read_csv_with_pandas(fail_tat_file)

    head_list = df.head()
    col_list = []
    for item in head_list:
        if 'CPU' in item and '-Frequency(MHz)' in item:
            col_list.append(item)

    # logger.info(f"col_list: {col_list}")

    col_2 = 'Miscellaneous-MSR Package Temperature(Degree C)'
    # col_dict = intel_rule_dict.get('check_rule_3', None)
    col_2 = col_dict.get('col_2', col_2)

    col_3 = 'Miscellaneous-TJMAX Temperature(Degree C)'
    col_3 = col_dict.get('col_3', col_3)

    col_4 = 'Miscellaneous-TCC Offset Temperature(Degree C)'
    col_4 = col_dict.get('col_4', col_4)

    col_2_list = df.get(col_2, None)

    if col_2_list is None:
        return return_dict

    check_point_1 = False
    for idx, item in enumerate(col_2_list):
        col_2_cell = df[col_2][idx]
        logger.info(f"col_2_cell: {col_2_cell}")

        col_3_cell = df[col_3][idx]
        logger.info(f"col_3_cell: {col_3_cell}")

        col_4_cell = df[col_4][idx]
        logger.info(f"col_4_cell: {col_4_cell}")

        delta = col_3_cell - col_4_cell
        logger.info(f"delta: {delta}")
        if col_3_cell > delta:
            check_point_1 = True
            break

    check_point_2 = False
    for idx in target_index_list:
        for item in col_list:
            cell_data = df[item][idx]
            # logger.info(f"cell_data: {cell_data}")
            if cell_data < Processor_Base_Core_Frequency:
                check_point_2 = True
                break

    if check_point_2 and check_point_1:
        logger.info(f"check_result_dict: {check_result_dict}")
        return_dict = check_result_dict


    return return_dict

def check_rule_4(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_4',
        'Root cause': 'Thermal prochot',
        'Component': 'Thermal',
        'Solution': 'Please power Thermal prochot reason further.',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    df_fail = read_csv_with_pandas(fail_tat_file)

    head_list = df_fail.head()
    col_list = []
    for item in head_list:
        if 'CPU' in item and '-Turbo Capability' in item:
            col_list.append(item)

    for item in col_list:
        col_data = df_fail.get(item)
        count = get_list_text_count(col_data, 'Supported and Disabled')
        if count:
            logger.info(f"{item}: CPUx Turbo capability=supported and disabled")
            return_dict = check_result_dict
            logger.info(f"check_result_dict: {check_result_dict}")
            break

    return return_dict

def check_rule_5(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_5',
        'Root cause': 'Max Frequency Wrong',
        'Component': 'BIOS',
        'Solution': 'further check Intel code base',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    logger.info(f'fail_tat_file={fail_tat_file}')

    df = read_csv_with_pandas(fail_tat_file)
    head_list = df.head()
    col_list = []
    for item in head_list:
        # logger.info(f"item: {item}")
        if 'CPU-Info-' in item and 'pCore Active(MHz)' in item:
            col_list.append(item)

    logger.info(f"col_list: {col_list}")

    for col in col_list:
        fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col)
        average_fail = get_list_average(fail_col_data)
        logger.info(f"average_fail: {average_fail}")
    
        pass_col_data, pass_file_data = get_intel_tat_file_col_data_by_dir_ex(pass_dir, col)
        average_pass = get_list_average(pass_col_data)
        logger.info(f"average_pass: {average_pass}")
    
        if average_fail != average_pass:
            return_dict = check_result_dict
            logger.info(f"check_result_dict: {check_result_dict}")
            return return_dict

    col_list = []
    for item in head_list:
        if 'CPU-Info-' in item and 'eCore Active(MHz)' in item:
            col_list.append(item)

    for col in col_list:
        fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col)
        average_fail = get_list_average(fail_col_data)
        logger.info(f"average_fail: {average_fail}")

        pass_col_data, pass_file_data = get_intel_tat_file_col_data_by_dir_ex(pass_dir, col)
        average_pass = get_list_average(pass_col_data)
        logger.info(f"average_pass: {average_pass}")

        if average_fail != average_pass:
            return_dict = check_result_dict
            logger.info(f"check_result_dict: {check_result_dict}")
            return return_dict

    return return_dict

def check_rule_6(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_6',
        'Root cause': 'Rest power higher',
        'Component': 'Power',
        'Solution': 'check any other function behvior calls CPU power during benchmark',
        '修复及验证': 'change Tcc offset value to pass, verify',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    col_1 = 'Power-Package Power(Watts)'
    col_dict = intel_rule_dict.get('check_rule_6', None)
    col_1 = col_dict.get('col_1', col_1)

    fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col_1)
    pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_1)

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    is_larger_than_threshold = is_two_data_delta_larger_than_threshold(average_fail,
                                                                       average_pass,
                                                                       0.03)
    logger.info(f"is_larger_than_threshold: {is_larger_than_threshold}")

    if is_larger_than_threshold:
        return_dict = check_result_dict
        return return_dict

    #
    # Power-Rest of Package Power
    col_2 = 'Power-Rest of Package Power(Watts)'
    col_dict = intel_rule_dict.get('check_rule_6', None)
    col_2 = col_dict.get('col_2', col_2)
    fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col_2)
    pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_2)

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    is_larger_than_threshold = is_two_data_delta_larger_than_threshold(average_fail,
                                                                       average_pass,
                                                                       0.03)
    logger.info(f"is_larger_than_threshold: {is_larger_than_threshold}")

    if is_larger_than_threshold:
        return_dict = check_result_dict
        logger.info(f"return_dict: {return_dict}")

    return return_dict

def check_rule_7(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_7',
        'Root cause': 'Idle power higher',
        'Component': 'EE',
        'Solution': 'PHM logs check idle power high reason',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    col_1 = 'Power-Package Power(Watts)'
    col_dict = intel_rule_dict.get('check_rule_7', None)
    col_1 = col_dict.get('col_1', col_1)

    fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col_1)
    pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_1)

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    is_larger_than_threshold = is_two_data_delta_larger_than_threshold(average_fail,
                                                                       average_pass,
                                                                       0.03)
    logger.info(f"is_larger_than_threshold: {is_larger_than_threshold}")

    if is_larger_than_threshold:
        return_dict = check_result_dict
        return return_dict

    #
    #
    col_2 = 'Power-MSR EWMA Package Power(Watts)'
    col_2 = col_dict.get('col_2', col_2)
    fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col_2)
    pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_2)

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    is_larger_than_threshold = is_two_data_delta_larger_than_threshold(average_fail,
                                                                       average_pass,
                                                                       0.03)
    logger.info(f"is_larger_than_threshold: {is_larger_than_threshold}")

    if is_larger_than_threshold:
        return_dict = check_result_dict
        logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_8(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_8',
        'Root cause': 'GT power higher',
        'Component': '',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    col_1 = 'Power-Package Power(Watts)'
    col_dict = intel_rule_dict.get('check_rule_8', None)
    col_1 = col_dict.get('col_1', col_1)
    fail_col_data = get_intel_tat_file_col_data_by_dir(fail_dir, col_1)
    pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_1)

    fail_average = get_list_average(fail_col_data)
    pass_average = get_list_average(pass_col_data)

    is_larger = is_two_data_delta_larger_than_threshold(fail_average, pass_average, 0.03)

    if is_larger:
        return_dict = check_result_dict

    logger.info(return_dict)
    return return_dict

def check_rule_9(parent_dir=None, fail_dir=None, pass_dir=None):
    check_result_dict = {
        'rule name': 'check_rule_9',
        'Root cause': 'VR thermal alert-thermal',
        'Component': 'Thermal',
        'Solution': 'Please check if VR temperature over spec during benchmark',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    fail_tat_file = get_tat_file_with_dir(fail_dir)

    df = read_csv_with_pandas(fail_tat_file)
    col_1 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_9', None)
    col_1 = col_dict.get('col_1', col_1)

    logger.info(f"col_1: {col_1}")

    data_list = df.get(col_1)

    data_list = remove_list_na(data_list, target_str='nan')
    logger.info(f"data_list: {data_list}")

    count = get_list_text_count(data_list, 'VR thermal alert')

    return_dict = None
    if count:
        logger.info(f"check_result_dict: {check_result_dict}")
        return_dict = check_result_dict

    return return_dict

def check_rule_10(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_10',
        'Root cause': 'VR TDC Clip-Power',
        'Component': 'Power',
        'Solution': 'Please power check  if VR TDC meet sepc',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    df = read_csv_with_pandas(fail_tat_file)
    col_1 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_10', None)
    col_1 = col_dict.get('col_1', col_1)

    data_list = df.get(col_1)

    data_list = remove_list_na(data_list, target_str='nan')
    logger.info(f"data_list: {data_list}")

    count = get_list_text_count(data_list, 'VR_TDC')

    if count:
        return_dict = check_result_dict

    logger.info(f"return_dict: {return_dict}")
    return return_dict


def check_rule_11(parent_dir=None, fail_dir=None, pass_dir=None):
    # PL1_value and PL2_value come from spec
    PL1_value = 100
    PL2_value = 200
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_11',
        'Root cause': 'Tau abnormal',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    fail_tat_file = get_tat_file_with_dir(fail_dir)

    col_1 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_11', None)
    col_1 = col_dict.get('col_1', col_1)

    col_data = get_csv_file_col_data_by_file(fail_tat_file, col_1)
    count = get_list_text_count(col_data, text='PL1')
    logger.info(f"count: {count}")
    if count:
        col_2 = 'Power-Package Power(Watts)'
        col_2 = col_dict.get('col_2', col_2)
        logger.info(f"col_2: {col_2}")

        head_list = get_intel_file_head_list_by_dir(fail_dir)

        col_1 = get_match_col_name(head_list, col_2)
        logger.info(f'col_2:{col_2}')

        fail_col_data = get_intel_tat_file_col_data_by_dir(fail_dir, col_2)
        # logger.info(f"fail_col_data: {fail_col_data}")

        pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_2)
        # logger.info(f"pass_col_data: {pass_col_data}")

        average_fail = get_list_average(fail_col_data, True)
        logger.info(f"average_fail: {average_fail}")

        average_pass = get_list_average(pass_col_data, True)
        logger.info(f"average_pass: {average_pass}")

        is_larger_than_threshold = is_two_data_delta_larger_than_threshold(average_fail,
                                                                           average_pass,
                                                                           0.03)
        logger.info(f"is_larger_than_threshold: {is_larger_than_threshold}")

        if is_larger_than_threshold:
            return_dict = check_result_dict

    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_12(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f"check_rule_12")

    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_12',
        'Root cause': 'TCC offset abnormal',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': 'change Tcc offset value to pass, verify',
    }

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    fail_tat_file = get_tat_file_with_dir(fail_dir)

    col_1 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_12', None)
    col_1 = col_dict.get('col_1', col_1)

    col_data = get_csv_file_col_data_by_file(fail_tat_file, col_1)
    count = get_list_text_count(col_data, text='Thermal Event')
    logger.info(f"count: {count}")
    if count:
        col_2 = 'Miscellaneous-TCC Offset Temperature(Degree C)'
        col_2 = col_dict.get('col_2', col_2)

        fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col_2)
        pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_2)

        average_fail = get_list_average(fail_col_data, False)
        logger.info(f"average_fail: {average_fail}")

        average_pass = get_list_average(pass_col_data, False)
        logger.info(f"average_pass: {average_pass}")

        is_larger_than_threshold = is_two_data_delta_larger_than_threshold(average_fail,
                                                                           average_pass,
                                                                           0.03)
        logger.info(f"is_larger_than_threshold: {is_larger_than_threshold}")

        if is_larger_than_threshold:
            return_dict = check_result_dict

    logger.info(f"return_dict: {return_dict}")
    return return_dict

def check_rule_13(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_13')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_13',
        'Root cause': 'PL1/PL2 abnormal',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': '',
    }
    detail_list = []

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    col_1 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_13', None)
    col_1 = col_dict.get('col_1', col_1)
    fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col_1)

    count = get_list_text_count(fail_col_data, 'Thermal Event')

    if count > 0:
        return return_dict

    fail_file_data = get_intel_tat_file_data_frame_by_dir(fail_dir)
    pass_file_data = get_intel_tat_file_data_frame_by_dir(pass_dir)

    col_list = []

    col_2 = 'Turbo Parameters-MMIO Power Limit_1 Power(Watts)'
    col_2 = col_dict.get('col_2', col_2)
    col_list.append(col_2)

    col_3 = 'Turbo Parameters-MMIO Power Limit_2 Power(Watts)'
    col_3 = col_dict.get('col_3', col_3)
    col_list.append(col_3)

    col_4 = 'Turbo Parameters-MSR Power Limit_4 Power(Watts)'
    col_4 = col_dict.get('col_4', col_4)
    col_list.append(col_4)

    # col_list = ['Turbo Parameters-MMIO Power Limit_1 Power(Watts)',
    #             'Turbo Parameters-MMIO Power Limit_2 Power(Watts)',
    #             'Turbo Parameters-MSR Power Limit_4 Power(Watts)']

    for col in col_list:
        fail_col_data = fail_file_data.get(col, None)
        pass_col_data = pass_file_data.get(col, None)

        # logger.info(f"fail_col_data:{fail_col_data}")
        average_fail = get_list_average(fail_col_data, False)
        logger.info(f"average_fail: {average_fail}")

        # logger.info(f"pass_col_data:{pass_col_data}")
        average_pass = get_list_average(pass_col_data, False)
        logger.info(f"average_pass: {average_pass}")

        if average_pass != average_fail:
            if col == col_2:
                detail_list.append('PL1 abnormal')
            if col == col_3:
                detail_list.append('PL2 abnormal')
            if col == col_4:
                detail_list.append('PL4 abnormal')
            continue
    if detail_list is not None:
        check_result_dict['Root cause'] = detail_list
        return_dict = check_result_dict
        logger.info(f"return_dict: {return_dict}")

    return return_dict

def check_rule_14(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_14')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_14',
        'Root cause': 'Al Chip issue',
        'Component': 'EE',
        'Solution': 'Please EE confirm AI FW further',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    pass_tat_file = get_tat_file_with_dir(pass_dir)

    df_pass = read_csv_with_pandas(pass_tat_file)
    df_fail = read_csv_with_pandas(fail_tat_file)
    col = 'Turbo Parameters-IA Clip Reason'
    # data_list = df_fail[col]
    # logger.info(f'data_list[0]:{data_list[0]}')

    # logger.info(return_dict)

    return return_dict

def check_rule_15(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_15')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_15',
        'Root cause': 'Enviroment issue',
        'Component': 'Thermal',
        'Solution': 'Please retest with the same Enviorment',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    logger.info(f'fail_tat_file:{fail_tat_file}')

    pass_tat_file = get_tat_file_with_dir(pass_dir)

    df_pass = read_csv_with_pandas(pass_tat_file)
    df_fail = read_csv_with_pandas(fail_tat_file)

    col_1 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_15', None)
    col_1 = col_dict.get('col_1', col_1)
    logger.info(f'col_1:{col_1}')

    head_list = get_intel_file_head_list_by_dir(fail_dir)

    col_1 = get_match_col_name(head_list, col_1)
    # logger.info(f'col_1:{col_1}')

    data_list = df_fail.get(col_1, None)
    # logger.info(f'data_list:{data_list}')

    # logger.info(f'data_list:{data_list}')
    count = get_list_text_count(data_list, 'Thermal event')
    logger.info(f'Thermal event count:{count}')

    delta = 0
    fail_PerformanceLog_file = get_performance_file_with_dir(fail_dir)
    logger.info(f'fail_PerformanceLog_file:{fail_PerformanceLog_file}')

    pass_PerformanceLog_file = get_performance_file_with_dir(pass_dir)

    if count and fail_PerformanceLog_file is not None:
        df_pass = read_csv_with_pandas(pass_PerformanceLog_file)
        df_fail = read_csv_with_pandas(fail_PerformanceLog_file)

        col_2 = 'Environment Sensor Temp'
        col_2 = col_dict.get('col_2', col_2)

        col_data = df_pass.get(col_2, None)
        # logger.info(f'col_data:{col_data}')

        pass_max = max(df_pass.get(col_2, None))
        logger.info(f'pass_max:{pass_max}')

        fail_max = max(df_fail.get(col_2, None))
        logger.info(f'fail_max:{fail_max}')

        delta = abs(fail_max - pass_max)

    if delta > 2:
        return_dict = check_result_dict

    logger.info(return_dict)

    return return_dict

def check_rule_16(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_16')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_16',
        'Root cause': 'Enviroment issue',
        'Component': 'Thermal',
        'Solution': 'Please retest with the same Enviorment',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    col_1 = 'Miscellaneous-MSR Package Temperature(Degree C)'
    col_dict = intel_rule_dict.get('check_rule_16', None)
    col_1 = col_dict.get('col_1', col_1)

    fail_col_data = get_intel_tat_file_col_data_by_dir(fail_dir, col_1)
    pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_1)

    correlation = get_two_list_correlation(fail_col_data, pass_col_data)
    if correlation:
        delta_correlation = abs(1 - correlation)
        logger.info(f'delta_correlation:{delta_correlation}')
        if delta_correlation > 0.05:
            return_dict = check_result_dict
            logger.info(return_dict)
            return return_dict

    col_2 = 'Miscellaneous-MMO Package Temperature(Degree C)'
    col_2 = col_dict.get('col_2', col_2)
    fail_col_data = get_intel_tat_file_col_data_by_dir(fail_dir, col_2)
    pass_col_data = get_intel_tat_file_col_data_by_dir(pass_dir, col_2)

    correlation = get_two_list_correlation(fail_col_data, pass_col_data)
    if correlation:
        delta_correlation = abs(1 - correlation)
        logger.info(f'delta_correlation:{delta_correlation}')
        if delta_correlation > 0.05:
            return_dict = check_result_dict
            logger.info(return_dict)

    return return_dict

def check_rule_17(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_17')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_17',
        'Root cause': 'EPP value abnormal',
        'Component': 'OS',
        'Solution': '',
        '修复及验证': 'change to pass EPP value to verify, furhter check PPM version',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    pass_tat_file = get_tat_file_with_dir(pass_dir)

    df_fail = read_csv_with_pandas(fail_tat_file)
    df_pass = read_csv_with_pandas(pass_tat_file)

    col_1 = 'HWP-pCore OSPM Requested Energy Performance Preference'
    col_dict = intel_rule_dict.get('check_rule_17', None)
    col_1 = col_dict.get('col_1', col_1)

    data_list = df_fail.get(col_1, None)
    if data_list is None:
        return return_dict

    min_data = min(data_list)
    max_data = max(data_list)
    if min_data != max_data:
        return_dict = check_result_dict
        logger.info(return_dict)
        # return return_dict

    col_2 = 'HWP-eCore OSPM Requested Energy Performance Preference'
    col_2 = col_dict.get('col_2', col_2)
    logger.info(f'col_2:{col_2}')

    data_list = df_fail.get(col_2, None)
    min_data = min(data_list)
    max_data = max(data_list)
    if min_data != max_data:
        return_dict = check_result_dict
        logger.info(return_dict)
        # return return_dict

    # average part
    col_1 = 'HWP-pCore OSPM Requested Energy Performance Preference'
    col_1 = col_dict.get('col_1', col_1)

    fail_data_list = df_fail.get(col_1, None)
    pass_data_list = df_pass.get(col_1, None)

    # logger.info(f'fail_data_list:{fail_data_list}')
    fail_average = get_list_average(fail_data_list)

    # logger.info(f'pass_data_list:{pass_data_list}')
    pass_average = get_list_average(pass_data_list, debug=False)
    if fail_average != pass_average:
        return_dict = check_result_dict
        logger.info(return_dict)
        # return return_dict

    col_2 = 'HWP-eCore OSPM Requested Energy Performance Preference'
    col_2 = col_dict.get('col_2', col_2)

    fail_data_list = df_fail.get(col_2, None)
    pass_data_list = df_pass.get(col_2, None)

    fail_average = get_list_average(fail_data_list)
    pass_average = get_list_average(pass_data_list)
    if fail_average != pass_average:
        return_dict = check_result_dict
        logger.info(return_dict)
        # return return_dict

    return return_dict

def check_rule_18(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'check_rule_18')
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_18',
        'Root cause': 'VR_TDC',
        'Component': 'power',
        'Solution': 'please reteset with temperature 0C envrioment',
        '修复及验证': '0度环境下复测',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if pass_dir is None:
        logger.info(f'return None')
        return None

    col_1 = 'Turbo Parameters-IA Clip Reason'
    col_dict = intel_rule_dict.get('check_rule_18', None)
    col_1 = col_dict.get('col_1', col_1)
    logger.info(f'col_1:{col_1}')

    fail_col_data, fail_file_data = get_intel_tat_file_col_data_by_dir_ex(fail_dir, col_1)
    # logger.info(f'fail_col_data:{fail_col_data}')

    count = get_list_text_count(fail_col_data, 'TVB')
    logger.info(f'count:{count}')
    if count > 0:
        return_dict = check_result_dict
    logger.info(return_dict)

    return return_dict

def gpu_rule_1(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_1')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_1',
        'Root cause': 'GPU sample difference',
        'Component': 'EE',
        'Solution': 'Please EE check ,if the gap is acceptable by Sample difference',
        '修复及验证': 'change to pass EPP value to verify, furhter check PPM version',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if not os.path.exists(pass_dir):
        return return_dict

    col = '1:GPC Clock (MHz)'
    fail_col_data_gpu, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data_gpu, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    correlation = get_two_list_correlation(fail_col_data_gpu, pass_col_data_gpu)
    logger.info(correlation)
    if correlation :
        delta_correlation = 1 - correlation
        if delta_correlation > 0.03:
            return_dict = check_result_dict
            logger.info(return_dict)
            return return_dict

    col = '1:TGP (W)'
    fail_col_data_gpu, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data_gpu, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    correlation = get_two_list_correlation(fail_col_data_gpu, pass_col_data_gpu)
    logger.info(correlation)
    if correlation :
        delta_correlation = 1 - correlation
        if delta_correlation > 0.03:
            return_dict = check_result_dict
            logger.info(return_dict)

    logger.info(return_dict)
    return return_dict

def gpu_rule_2(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_2')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_2',
        'Root cause': 'GPU prochot',
        'Component': 'EC',
        'Solution': 'EC log first check the prochot reason',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    gpu_log_file = get_gpu_file_with_dir(fail_dir)

    headers, new_list = get_gpu_data_with_csv(gpu_log_file)
    new_file = os.path.join(fail_dir, 'GPU_New.csv')
    write_to_csv(new_file, new_list, headers)

    col = '1:GPC Clock (MHz)'
    col_data_1 = get_csv_file_col_data_by_file_gpu(gpu_log_file, col, headers)

    col = '1:GPC Slowdown Factor (%)'
    col_data_pass = get_csv_file_col_data_by_file_gpu(gpu_log_file, col, headers)

    if col_data_1 is None:
        return return_dict

    for idx, item in enumerate(col_data_1):
        # logger.info(item)
        if type(item) is str and item != '':
            item = item.replace('%', '')
            item = int(item)
        cell_2_data = col_data_pass[idx]
        # logger.info(f'cell_2_data: {cell_2_data}')
        if type(cell_2_data) is str and cell_2_data != ' ':
            cell_2_data = cell_2_data.replace('%', '')
            cell_2_data = int(cell_2_data)
        if item == 210 and cell_2_data == 25:
            return_dict = check_result_dict
            break
        else:
            # logger.info(f'{col_2_data}, {item}')
            pass
    return return_dict

def gpu_rule_3(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_3')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_3',
        'Root cause': 'NV Graphic driver',
        'Component': 'NV driver',
        'Solution': 'need confirm if current driver lock CPU clk',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    gpu_log_file = get_gpu_file_with_dir(fail_dir)

    headers, new_list = get_gpu_data_with_csv(gpu_log_file)
    new_file = os.path.join(fail_dir, 'GPU_New.csv')
    write_to_csv(new_file, new_list, headers)

    col = '1:GPC Clock (MHz)'
    col_data_1 = get_csv_file_col_data_by_file_gpu(gpu_log_file, col, headers)
    # logger.info(f'col_data_1:{col_data_1}')

    if col_data_1 is None:
        return return_dict

    min_value = min(col_data_1)
    logger.info(f'min_value:{min_value}')

    max_value = max(col_data_1)
    logger.info(f'max_value:{max_value}')

    if min_value == max_value:
        col = '1:GPU Utilization (%)'
        col_data_pass = get_csv_file_col_data_by_file_gpu(gpu_log_file, col, headers)
        for idx, item in enumerate(col_data_pass):
            if item < 100:
                return_dict = check_result_dict
    return return_dict

def gpu_rule_4(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_4')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_4',
        'Root cause': 'GPU OC related',
        'Component': 'BIOS',
        'Solution': 'Retest with the same OC settings',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    col = '1:Memory Clock (MHz)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    # fail_average = np.average(fail_col_data)
    fail_average = get_list_average(fail_col_data, False)
    logger.info(f"fail_average: {fail_average}")

    # pass_average = np.average(pass_col_data)
    pass_average = get_list_average(pass_col_data, False)
    logger.info(f"pass_average: {pass_average}")

    is_delta_larger = is_two_data_delta_larger_than_threshold(fail_average, pass_average, 0.0005)

    if is_delta_larger:
        return_dict = check_result_dict
        logger.info(f'{return_dict}')

    return return_dict

def gpu_rule_5(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_5')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_5',
        'Root cause': 'Max TGP',
        'Component': 'BIOS',
        'Solution': 'Please BIOS check if max TGP configuration meet Fn+Q spec',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    return return_dict

def gpu_rule_6(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_6')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_6',
        'Root cause': '1:NVVDD Power (W) abnormal',
        'Component': 'EE',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    # 1:NVVDD Power (W)
    col = '1:NVVDD Power (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    is_larger_than_threshold_NVVDD_Power = is_two_col_data_delta_larger_than_threshold(fail_col_data,
                                                                       pass_col_data,
                                                                       0.1)

    # 1:TGP (W)
    col = '1:TGP (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    is_larger_than_threshold_TGP = is_two_col_data_delta_larger_than_threshold(fail_col_data,
                                                                       pass_col_data,
                                                                       0.1)

    # 1:FBVDD Power (W)
    col = '1:FBVDD Power (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    is_larger_than_threshold_FBVDD_P = is_two_col_data_delta_larger_than_threshold(fail_col_data,
                                                                       pass_col_data,
                                                                       0.1)
    # 只有1:NVVDD Power (W)明显差异
    if is_larger_than_threshold_NVVDD_Power and (not is_larger_than_threshold_TGP and not is_larger_than_threshold_FBVDD_P):
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def gpu_rule_7(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_7')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_7',
        'Root cause': '1:FBVDD Power (W) abnormal',
        'Component': 'EE',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    # 1:NVVDD Power (W)
    col = '1:NVVDD Power (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    is_larger_than_threshold_NVVDD_Power = is_two_col_data_delta_larger_than_threshold(fail_col_data,
                                                                       pass_col_data,
                                                                       0.1)
    logger.info(f'is_larger_than_threshold_NVVDD_Power: {is_larger_than_threshold_NVVDD_Power}')

    # 1:TGP (W)
    col = '1:TGP (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    is_larger_than_threshold_TGP = is_two_col_data_delta_larger_than_threshold(fail_col_data,
                                                                       pass_col_data,
                                                                       0.1)
    logger.info(f'is_larger_than_threshold_TGP: {is_larger_than_threshold_TGP}')

    # 1:FBVDD Power (W)
    col = '1:FBVDD Power (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    is_larger_than_threshold_FBVDD_P = is_two_col_data_delta_larger_than_threshold(fail_col_data,
                                                                       pass_col_data,
                                                                       0.1)
    logger.info(f'is_larger_than_threshold_FBVDD_P: {is_larger_than_threshold_FBVDD_P}')

    # 只有1:NVVDD Power (W)明显差异
    if is_larger_than_threshold_FBVDD_P and (is_larger_than_threshold_TGP and is_larger_than_threshold_NVVDD_Power):
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def gpu_rule_8(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_8')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_8',
        'Root cause': 'enviroment issue',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    # 1:NVVDD Power (W)
    is_delta_larger_than_stand = False
    col = '1:Capping Reason'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    # logger.info(f'fail_col_data: {fail_col_data}')

    pass_col_data = remove_list_na(pass_col_data, 'N/A')
    # logger.info(f'pass_col_data: {pass_col_data}')
    item_data = None
    if len(fail_col_data) > 1 :
        item_data = fail_col_data[0].strip()
        item_data = item_data.lower()
    # if item_data == 'thml' or item_data == 'thml pwr':
    if is_performance_ec_file_exit_by_dir(fail_dir):
        col = 'Environment Sensor Temp'
        fail_col_data, fail_file_data = get_performance_file_col_data_by_dir(fail_dir, col)
        pass_col_data, pass_file_data = get_performance_file_col_data_by_dir(pass_dir, col)
        is_delta_larger_than_stand = is_two_col_data_delta_larger_than_threshold(fail_col_data, pass_col_data, 1)


        # 只有1:NVVDD Power (W)明显差异
        if is_delta_larger_than_stand:
            return_dict = check_result_dict
            logger.info(f'return_dict: {return_dict}')

    return return_dict

def gpu_rule_9(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_9')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_9',
        'Root cause': 'thermal module',
        'Component': 'Please themal check module differrence',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    # 1:NVVDD Power (W)
    is_match_rule = False
    is_delta_larger_than_stand = False

    head_list = get_gpu_file_head_list_by_dir(fail_dir)

    col = '1:t_gpu'
    col = get_match_col_name(head_list, col)
    logger.info(f'col:{col}')
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    logger.info(f'fail_col_data:{fail_col_data}')

    continue_flag_1 = False
    for idx, value in enumerate(fail_col_data):
        if value > 86:
            continue_flag_1 = True
            break

    col = 'GPU Sensor Temp'
    fail_col_data, fail_file_data = get_performance_file_col_data_by_dir(fail_dir, col)
    logger.info(f'fail_col_data:{fail_col_data}')

    continue_flag_2 = False
    for idx, value in enumerate(fail_col_data):
        if value > 86:
            continue_flag_2 = True
            break

    logger.info(f'continue_flag_1:{continue_flag_1}')
    logger.info(f'continue_flag_2:{continue_flag_2}')
    if continue_flag_1 == False and continue_flag_2 == False:
        return return_dict
    #
    col = '1:t_gpu'
    col = get_match_col_name(head_list, col)
    logger.info(f'col:{col}')
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    check_point_1 = True
    for idx, value in enumerate(fail_col_data):
        if value > 86:
            check_point_1 = False
            break

    col = 'GPU Sensor Temp'
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    check_point_2 = True
    for idx, value in enumerate(fail_col_data):
        if value > 86:
            check_point_2 = False
            break

    if check_point_1 and check_point_2:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict


def gpu_rule_10(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_10')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_10',
        'Root cause': 'D-notifier',
        'Component': 'EC',
        'Solution': 'Please EC check D-notifer first',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    col = 'Power Supply Mode'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    # logger.info(f'fail_col_data: {fail_col_data}')

    pass_col_data = remove_list_na(pass_col_data, 'N/A')
    # logger.info(f'pass_col_data: {pass_col_data}')

    cell_data = None
    if len(fail_col_data) > 1 :
        cell_data = fail_col_data[0].strip()
    is_ac = False

    # if cell_data == 'AC':
    is_ac = True

    col = '1:D-Notifier Limit'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    logger.info(f'fail_col_data: {fail_col_data}')

    if len(fail_col_data) == 0:
        return return_dict

    is_d2_d5 = False
    for cell_data in fail_col_data:
        logger.info(f'cell_data: {cell_data}')
        if 'D2' in cell_data or 'D3' in cell_data or 'D4' in cell_data or 'D5' in cell_data:
            is_d2_d5 = True
            break

    if is_d2_d5 and is_ac:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def gpu_rule_11(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_11')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_11',
        'Root cause': 'PPAB issue',
        'Component': 'Driver',
        'Solution': 'Need driver confirm if current PPAB behvior is normal',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    col = '1:PPAB State'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    logger.info(f'fail_col_data: {fail_col_data}')

    is_all_enabled = is_col_data_all_same_with_target(fail_col_data, 'Enabled')
    logger.info(f'is_all_enabled: {is_all_enabled}')

    if is_all_enabled == False:
        return return_dict

    head_list = get_gpu_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')

    col = '1:pwr_tgp'
    col = get_match_col_name(head_list, col)
    logger.info(f'col:{col}')

    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    loading_index = get_loading_index(fail_col_data, average_fail, 0.5)
    logger.info(f"loading_index: {loading_index}")

    col = '1:Capping Reason'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    logger.info(f'fail_col_data: {fail_col_data}')

    is_all_pwr = is_col_data_all_same_with_target(fail_col_data[loading_index: ], 'pwr')
    logger.info(f'is_all_pwr: {is_all_pwr}')

    if is_all_pwr == False:
        return return_dict

    # 1:AC_Target_TPP_Limit
    # 1:AC Target TPP Limit (mW)
    head_list = get_gpu_file_head_list_by_dir(fail_dir)
    # logger.info(f'head_list:{head_list}')

    col = '1:AC_Target_TPP_Limit'
    col = get_match_col_name(head_list, col)
    logger.info(f'col:{col}')

    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    if average_fail != average_pass:
        return return_dict

    col = '1:pwr_tgp'
    col = get_match_col_name(head_list, col)
    logger.info(f'col:{col}')

    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    fail_min = min(fail_col_data)
    fail_max = max(fail_col_data)
    average_fail = get_list_average(fail_col_data, False)

    is_delta_larger = is_two_data_delta_larger_than_threshold(fail_min, fail_max, 0.3)
    logger.info(f'is_delta_larger:{is_delta_larger}')

    if is_delta_larger == True:
        return_dict = check_result_dict

    logger.info(f'return_dict: {return_dict}')
    return return_dict

def gpu_rule_12(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_12')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_12',
        'Root cause': '1:GPC Slowdown Factor (%)',
        'Component': 'Thermal',
        'Solution': 'further thermal protect behavior',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    col = '1:GPC Slowdown Factor (%)'
    col_data, file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    has_match = is_col_data_has_data_match_range(col_data, 25, 97)

    if has_match:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def gpu_rule_13(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_13')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_13',
        'Root cause': 'VBIOS',
        'Component': 'EE',
        'Solution': 'please EE check VBIOS version',
        '修复及验证': '',
    }
    if True:
        return return_dict

    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    col = '1:TGP (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    # logger.info(f'fail_col_data: {fail_col_data}')
    which_type = type(fail_col_data)
    # logger.info(f'which_type: {which_type}')

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    # logger.info(f'fail_col_data: {fail_col_data}')

    pass_col_data = remove_list_na(pass_col_data, 'N/A')
    # logger.info(f'pass_col_data: {pass_col_data}')

    fail_average_TGP = np.average(fail_col_data)
    pass_average_TGP = np.average(pass_col_data)

    small_TGP = False
    if fail_average_TGP < pass_average_TGP:
        small_TGP = True

    col = '1:FBVDD Power (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    pass_col_data = remove_list_na(pass_col_data, 'N/A')

    fail_average_FBVDD = np.average(fail_col_data)
    pass_average_FBVDD = np.average(pass_col_data)
    small_FBVDD = False
    if fail_average_FBVDD < pass_average_FBVDD:
        small_FBVDD = True

    col = '1:NVVDD Power (W)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    pass_col_data = remove_list_na(pass_col_data, 'N/A')

    fail_average_NVVDD_P = np.average(fail_col_data)
    pass_average_NVVDD_P = np.average(pass_col_data)
    small_NVVDD_P = False
    if fail_average_NVVDD_P < pass_average_NVVDD_P:
        small_NVVDD_P = True

    col = '1:NVVDD Voltage (uV)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)
    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    pass_col_data = remove_list_na(pass_col_data, 'N/A')

    fail_average_NVVDD_V = np.average(fail_col_data)
    pass_average_NVVDD_V = np.average(pass_col_data)
    small_NVVDD_V = False
    if fail_average_NVVDD_V < pass_average_NVVDD_V:
        small_NVVDD_V = True

    if small_TGP and small_FBVDD and small_NVVDD_P and fail_average_NVVDD_V:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def gpu_rule_14(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_14')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_14',
        'Root cause': 'Vram vendor',
        'Component': 'EE',
        'Solution': 'Please EE check Vram vendor difference',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if True:
        return return_dict

    target_str = 'VRAM Strap'
    target_map_fail = get_gpu_file_target_map_by_dir(fail_dir, target_str)
    target_map_pass = get_gpu_file_target_map_by_dir(pass_dir, target_str)

    logger.info(f'target_map_fail: {target_map_fail}')
    logger.info(f'target_map_pass: {target_map_pass}')

    if target_map_fail is not None and [target_str] != target_map_pass[target_str]:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def gpu_rule_15(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_15')
    return_dict = None
    check_result_dict = {
        'rule name': 'gpu_rule_15',
        'Root cause': 'Whisper mode',
        'Component': 'Driver',
        'Solution': 'check why non-quiet AC mode, Whisper mode is on',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    col = '1:WM2 Platform Enabled'
    fail_col_data_platform, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    cell_data_platform = None
    if fail_col_data_platform is not None:
        cell_data_platform = fail_col_data_platform[0]

    col = '1:WM2 Driver Enabled'
    fail_col_data_driver, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    cell_data_driver = None
    if fail_col_data_driver is not None:
        cell_data_driver = fail_col_data_driver[0]

    if cell_data_platform != 'No' and cell_data_driver != 'No':
        return_dict = check_result_dict
        logger.info(f'cell_data_platform: {cell_data_platform}')

    return return_dict

def gpu_rule_16(parent_dir=None, fail_dir=None, pass_dir=None):
    logger.info(f'gpu_rule_16')
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
        return None

    for key, value in channel_dict_fail.items():
        if key not in channel_dict_pass or value not in channel_dict_fail[key]:
            return_dict = check_result_dict
            logger.info(f'return_dict: {return_dict}')

    channel_str = 'Controller0-ChannelB-DIMM1'
    channel_dict_fail = get_cpu_log_content(fail_dir, channel_str)
    channel_dict_pass = get_cpu_log_content(pass_dir, channel_str)

    for key, value in channel_dict_fail.items():
        if key not in channel_dict_pass or value not in channel_dict_fail[key]:
            return_dict = check_result_dict
            logger.info(f'return_dict: {return_dict}')

    return return_dict

if __name__ == '__main__':
    # cmd = " ".join(args)
    # result, errors, return_code = cmd_excute(cmd)
    # logger.info(f'result:{result}, errors:{errors}, return_code:{return_code}')
    #
    # cmd = 'qqd'
    # result, errors, return_code = cmd_excute(cmd)
    # logger.info(f'result:{result}, errors:{errors}, return_code:{return_code}')
    pass
