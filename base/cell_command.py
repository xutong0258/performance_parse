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
from base.fileOP import *
from base.read_csv_with_pandas import *
from base.read_csv_with_csv import *

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
    cpu_list = []
    for item in head_list:
        if 'CPU' in item and '-Frequency(MHz)' in item:
            cpu_list.append(item)

    for item in cpu_list:
        # col_1 = 'CPU0-Frequency(MHz)'
        col_2 = 'Power-Package Power(Watts)'

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
    cpu_list = []
    for item in head_list:
        if 'CPU' in item and '-Frequency(MHz)' in item:
            cpu_list.append(item)

    check_flag = False
    bench_mark = 400
    for item in cpu_list:
        # col_1 = 'CPU0-Frequency(MHz)'
        col_list = df.get(item)
        lower_index = get_list_lower_index(df[item], bench_mark)
        logger.info(f"lower_index: {lower_index}")
        if lower_index is not None:
            break

    col_2 = 'Turbo Parameters-IA Clip Reason'
    
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

    fail_tat_file = get_tat_file_with_dir(fail_dir)

    df = read_csv_with_pandas(fail_tat_file)
    head_list = df.head()
    cpu_list = []
    for item in head_list:
        if 'CPU' in item and '-Frequency(MHz)' in item:
            cpu_list.append(item)

    check_flag = False
    bench_mark = 400
    for item in cpu_list:
        logger.info(f"col: {item}")
        col_list = df.get(item)
        lower_index = get_list_lower_equal_index(df[item], bench_mark)
        logger.info(f"lower_index: {lower_index}")
        if lower_index is not None:
            break

    col_2 = 'Turbo Parameters-IA Clip Reason'

    if lower_index is not None:
        check_list = []
        item = df[col_2][lower_index]
        check_list.append(item)

        if lower_index >= 1:
            item = df[col_2][lower_index - 1]
            check_list.append(item)

        item = df[col_2][lower_index + 1]
        check_list.append(item)

        logger.info(f"check_list: {check_list}")
        count = get_list_text_count(check_list, 'Thermal event')
        if count:
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
    cpu_list = []
    for item in head_list:
        if 'CPU' in item and '-Turbo Capability' in item:
            cpu_list.append(item)

    for item in cpu_list:
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
        'Root cause': ' Max Frequency Wrong',
        'Component': 'BIOS',
        'Solution': 'further check Intel code base',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    df = read_csv_with_pandas(fail_tat_file)

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

    col = 'Power-Package Power(Watts)'
    fail_col_data, fail_file_data = get_tat_file_col_data_by_dir_ex(fail_dir, col)
    pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'nan')
    # logger.info(f"fail_col_data: {fail_col_data}")

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    pass_col_data = remove_list_na(pass_col_data, 'nan')
    # logger.info(f"pass_col_data: {pass_col_data}")

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
    col = 'Power-Rest of Package Power(Watts)'
    fail_col_data, fail_file_data = get_tat_file_col_data_by_dir_ex(fail_dir, col)
    pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'nan')
    # logger.info(f"fail_col_data: {fail_col_data}")

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    pass_col_data = remove_list_na(pass_col_data, 'nan')
    # logger.info(f"pass_col_data: {pass_col_data}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    is_larger_than_threshold = is_two_data_delta_larger_than_threshold(average_fail,
                                                                       average_pass,
                                                                       0.03)
    logger.info(f"is_larger_than_threshold: {is_larger_than_threshold}")

    if is_larger_than_threshold:
        return_dict = check_result_dict
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

    col = 'Power-Package Power(Watts)'
    fail_col_data, fail_file_data = get_tat_file_col_data_by_dir_ex(fail_dir, col)
    pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'nan')
    # logger.info(f"fail_col_data: {fail_col_data}")

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    pass_col_data = remove_list_na(pass_col_data, 'nan')
    # logger.info(f"pass_col_data: {pass_col_data}")

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
    col = 'Power-MSR EWMA Package Power(Watts)'
    fail_col_data, fail_file_data = get_tat_file_col_data_by_dir_ex(fail_dir, col)
    pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'nan')
    # logger.info(f"fail_col_data: {fail_col_data}")

    average_fail = get_list_average(fail_col_data, False)
    logger.info(f"average_fail: {average_fail}")

    pass_col_data = remove_list_na(pass_col_data, 'nan')
    # logger.info(f"pass_col_data: {pass_col_data}")

    average_pass = get_list_average(pass_col_data, False)
    logger.info(f"average_pass: {average_pass}")

    is_larger_than_threshold = is_two_data_delta_larger_than_threshold(average_fail,
                                                                       average_pass,
                                                                       0.03)
    logger.info(f"is_larger_than_threshold: {is_larger_than_threshold}")

    if is_larger_than_threshold:
        return_dict = check_result_dict
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
    if pass_dir is None:
        return None

    col = 'Power-Package Power(Watts)'
    fail_col_data = get_tat_file_col_data_by_dir(fail_dir, col)
    pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

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
    col = 'Turbo Parameters-IA Clip Reason'
    data_list = df[col].tolist()

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
    col = 'Turbo Parameters-IA Clip Reason'
    data_list = df[col].tolist()

    data_list = remove_list_na(data_list, target_str='nan')
    logger.info(f"data_list: {data_list}")

    count = get_list_text_count(data_list, 'VR TDC Clip-Power')

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

    fail_tat_file = get_tat_file_with_dir(fail_dir)

    col = 'Turbo Parameters-IA Clip Reason'
    col_data = get_csv_file_col_data_by_file(fail_tat_file, col)
    count = get_list_text_count(col_data, text='PL1')
    logger.info(f"count: {count}")
    if count:
        col = 'Power-Package Power(Watts)'
        fail_col_data, fail_file_data = get_tat_file_col_data_by_dir_ex(fail_dir, col)
        pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

        fail_col_data = remove_list_na(fail_col_data, 'nan')
        # logger.info(f"fail_col_data: {fail_col_data}")

        average_fail = get_list_average(fail_col_data, False)
        logger.info(f"average_fail: {average_fail}")

        pass_col_data = remove_list_na(pass_col_data, 'nan')
        # logger.info(f"pass_col_data: {pass_col_data}")

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

    fail_tat_file = get_tat_file_with_dir(fail_dir)

    col = 'Turbo Parameters-IA Clip Reason'
    col_data = get_csv_file_col_data_by_file(fail_tat_file, col)
    count = get_list_text_count(col_data, text='Thermal Event')
    logger.info(f"count: {count}")
    if count:
        col = 'Miscellaneous-TCC Offset Temperature(Degree C)'
        fail_col_data, fail_file_data = get_tat_file_col_data_by_dir_ex(fail_dir, col)
        pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

        fail_col_data = remove_list_na(fail_col_data, 'nan')
        # logger.info(f"fail_col_data: {fail_col_data}")

        average_fail = get_list_average(fail_col_data, False)
        logger.info(f"average_fail: {average_fail}")

        pass_col_data = remove_list_na(pass_col_data, 'nan')
        logger.info(f"pass_col_data: {pass_col_data}")

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

def check_rule_12_ex(parent_dir=None, fail_dir=None, pass_dir=None):
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

    if pass_dir is None:
        return None

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    pass_tat_file = get_tat_file_with_dir(pass_dir)

    df_pass = read_csv_with_pandas(pass_tat_file)

    df_fail = read_csv_with_pandas(fail_tat_file)
    col = 'Turbo Parameters-IA Clip Reason'
    data_list = df_fail[col]
    logger.info(f'data_list[0]:{data_list[0]}')

    if 'Thermal Event' == data_list[0] or True:
        col = 'Miscellaneous-TCC Offset Temperature(Degree C)'

        # 计算偏差百分比（以平均值为基准）
        col_fail = df_fail.get(col, None)
        col_pass = df_pass.get(col, None)
        if col_fail is not None and col_pass is not None:
            df_fail['deviation_%'] = calculate_deviation(col_fail, col_fail, base='col_pass')

            # 设定阈值（例如：判断是否超过5%）
            threshold = 3
            df_fail['exceed_threshold'] = df_fail['deviation_%'] > threshold
            logger.info(df_fail)
            count = get_list_equal_count(df_fail['exceed_threshold'], True)
            if count:
                return_dict = check_result_dict
                logger.info(return_dict)

    return return_dict

def check_rule_13(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_13',
        'Root cause': 'PL1/PL2 abnormal',
        'Component': 'Thermal',
        'Solution': '',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if pass_dir is None:
        return None

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    pass_tat_file = get_tat_file_with_dir(pass_dir)

    df_pass = read_csv_with_pandas(pass_tat_file)
    df_fail = read_csv_with_pandas(fail_tat_file)
    col = 'Turbo Parameters-IA Clip Reason'
    # data_list = df_fail[col]
    # logger.info(f'data_list[0]:{data_list[0]}')

    # logger.info(return_dict)

    return return_dict


def check_rule_14(parent_dir=None, fail_dir=None, pass_dir=None):
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

    if pass_dir is None:
        return None

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

    if pass_dir is None:
        return None

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    logger.info(f'fail_tat_file:{fail_tat_file}')

    pass_tat_file = get_tat_file_with_dir(pass_dir)

    df_pass = read_csv_with_pandas(pass_tat_file)
    df_fail = read_csv_with_pandas(fail_tat_file)
    col = 'Turbo Parameters-lA clip Reason'
    col = 'Turbo Parameters-IA Clip Reason'
    data_list = df_fail.get(col, None)

    logger.info(f'data_list:{data_list}')
    count = get_list_text_count(data_list, 'Thermal event')
    logger.info(f'count:{count}')

    delta = 0
    fail_PerformanceLog_file = get_performance_file_with_dir(fail_dir)
    logger.info(f'fail_PerformanceLog_file:{fail_PerformanceLog_file}')

    pass_PerformanceLog_file = get_performance_file_with_dir(pass_dir)

    if count and fail_PerformanceLog_file is not None:
        df_pass = read_csv_with_pandas(pass_PerformanceLog_file)
        df_fail = read_csv_with_pandas(fail_PerformanceLog_file)

        col = 'Environment Sensor Temp'
        col_data = df_pass.get(col, None)
        # logger.info(f'col_data:{col_data}')

        pass_max = max(df_pass.get(col, None))
        logger.info(f'pass_max:{pass_max}')

        fail_max = max(df_fail.get(col, None))
        logger.info(f'fail_max:{fail_max}')

        delta = abs(fail_max - pass_max)

    if delta > 2:
        return_dict = check_result_dict

    logger.info(return_dict)

    return return_dict

def check_rule_16(parent_dir=None, fail_dir=None, pass_dir=None):
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

    if pass_dir is None:
        return None

    col = 'Miscellaneous-MSR Package Temperature(Degree C)'
    fail_col_data = get_tat_file_col_data_by_dir(fail_dir, col)
    pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

    correlation = get_two_list_correlation(fail_col_data, pass_col_data)
    if correlation:
        delta_correlation = abs(1 - correlation)
        logger.info(f'delta_correlation:{delta_correlation}')
        if delta_correlation > 0.05:
            return_dict = check_result_dict
            logger.info(return_dict)

    col = 'Miscellaneous-MMO Package Temperature(Degree C)'
    fail_col_data = get_tat_file_col_data_by_dir(fail_dir, col)
    pass_col_data = get_tat_file_col_data_by_dir(pass_dir, col)

    correlation = get_two_list_correlation(fail_col_data, pass_col_data)
    if correlation:
        delta_correlation = abs(1 - correlation)
        logger.info(f'delta_correlation:{delta_correlation}')
        if delta_correlation > 0.05:
            return_dict = check_result_dict
            logger.info(return_dict)

    return return_dict

def check_rule_17(parent_dir=None, fail_dir=None, pass_dir=None):
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

    if pass_dir is None:
        return None

    fail_tat_file = get_tat_file_with_dir(fail_dir)
    pass_tat_file = get_tat_file_with_dir(pass_dir)

    df_fail = read_csv_with_pandas(fail_tat_file)
    df_pass = read_csv_with_pandas(pass_tat_file)

    col = 'HWP-pCore OSPM Requested Energy Performance Preference'
    data_list = df_fail.get(col, None)
    if data_list is None:
        return return_dict

    min_data = min(data_list)
    max_data = max(data_list)
    if min_data != max_data:
        return_dict = check_result_dict
        logger.info(return_dict)
        return return_dict

    col = 'HWP-eCore OSPM Requested Energy Performance Preference'
    data_list = df_fail.get(col, None)
    min_data = min(data_list)
    max_data = max(data_list)
    if min_data != max_data:
        return_dict = check_result_dict
        logger.info(return_dict)
        return return_dict

    # average part
    col = 'HWP-pCore OSPM Requested Energy Performance Preference'
    fail_data_list = df_fail.get(col, None)
    pass_data_list = df_pass.get(col, None)

    # logger.info(f'fail_data_list:{fail_data_list}')
    fail_average = get_list_average(fail_data_list)

    # logger.info(f'pass_data_list:{pass_data_list}')
    pass_average = get_list_average(pass_data_list, debug=False)
    if fail_average != pass_average:
        return_dict = check_result_dict
        logger.info(return_dict)
        return return_dict

    col = 'HWP-eCore OSPM Requested Energy Performance Preference'
    fail_data_list = df_fail.get(col, None)
    pass_data_list = df_pass.get(col, None)

    fail_average = get_list_average(fail_data_list)
    pass_average = get_list_average(pass_data_list)
    if fail_average != pass_average:
        return_dict = check_result_dict
        logger.info(return_dict)
        return return_dict

    return return_dict

def check_rule_18(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_18',
        'Root cause': 'GPU sample difference',
        'Component': 'EE',
        'Solution': 'Please EE check ,if the gap is acceptable by Sample difference',
        '修复及验证': 'change to pass EPP value to verify, furhter check PPM version',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    if pass_dir is None:
        return None

    col = '1:GPC Clock (MHz)'
    fail_col_data_gpu, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data_gpu, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    correlation = get_two_list_correlation(fail_col_data_gpu, pass_col_data_gpu)
    logger.info(correlation)
    if correlation and correlation > 0.03:
        return_dict = check_result_dict

    col = '1:TGP (W)'
    fail_col_data_gpu, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data_gpu, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    correlation = get_two_list_correlation(fail_col_data_gpu, pass_col_data_gpu)
    logger.info(correlation)
    if correlation and correlation > 0.03:
        return_dict = check_result_dict

    return return_dict

def check_rule_19(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_19',
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
    col_data_2 = get_csv_file_col_data_by_file_gpu(gpu_log_file, col, headers)

    if col_data_1 is None:
        return return_dict

    for idx, item in enumerate(col_data_1):
        item = int(item)
        col_2_data = int(col_data_2[idx])

        if item == 210 and col_2_data == 25:
            return_dict = check_result_dict
            break
        else:
            # logger.info(f'{col_2_data}, {item}')
            pass
    return return_dict

def check_rule_20(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_20',
        'Root cause': 'NV Graphic driver',
        'Component': 'NV driver',
        'Solution': 'need confirm if current driver lock CPU clk',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    gpu_log_file = get_gpu_file_with_dir(fail_dir)

    # headers, new_list = get_gpu_data_with_csv(gpu_log_file)
    # new_file = os.path.join(fail_dir, 'GPU_New.csv')
    # write_to_csv(new_file, new_list, headers)

    col = '1:GPC Clock (MHz)'
    col_data_1 = get_csv_file_col_data_by_file(gpu_log_file, col)
    logger.info(f'col_data_1:{col_data_1}')

    if col_data_1 is None:
        return return_dict

    min_value = min(col_data_1)
    logger.info(f'min_value:{min_value}')

    max_value = max(col_data_1)
    logger.info(f'max_value:{max_value}')

    if min_value == max_value:
        col = '1:GPU Utilization (%)'
        col_data_2 = get_csv_file_col_data_by_file(new_file, col)
        for idx, item in enumerate(col_data_2):
            if item < 100:
                return_dict = check_result_dict
    return return_dict

def check_rule_21(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_21',
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

    fail_average = np.average(fail_col_data)
    pass_average = np.average(pass_col_data)
    if fail_average > pass_average:
        return_dict = check_result_dict
        logger.info(f'{return_dict}%')

    return return_dict

def check_rule_22(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_22',
        'Root cause': 'Max TGP',
        'Component': 'BIOS',
        'Solution': 'Please BIOS check if max TGP configuration meet Fn+Q spec',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    return return_dict

def check_rule_23(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_23',
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

def check_rule_24(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_24',
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
    if is_larger_than_threshold_FBVDD_P and (not is_larger_than_threshold_TGP and not is_larger_than_threshold_NVVDD_Power):
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def check_rule_25(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_25',
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

    item_data = fail_col_data[0].strip()
    item_data = item_data.lower()
    if item_data == 'thml' or item_data == 'thml pwr':
        col = 'Environment Sensor Temp'
        fail_col_data, fail_file_data = get_performance_file_col_data_by_dir(fail_dir, col)
        pass_col_data, pass_file_data = get_performance_file_col_data_by_dir(pass_dir, col)
        is_delta_larger_than_stand = is_two_col_data_delta_larger_than_threshold(fail_col_data, pass_col_data, 1)


    # 只有1:NVVDD Power (W)明显差异
    if is_delta_larger_than_stand:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def check_rule_26(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_26',
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
    col = '1:Capping Reason'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_col_data_by_dir(pass_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    # logger.info(f'fail_col_data: {fail_col_data}')

    pass_col_data = remove_list_na(pass_col_data, 'N/A')
    # logger.info(f'pass_col_data: {pass_col_data}')

    item_data = fail_col_data[0].strip()
    item_data = item_data.lower()
    if item_data == 'thml' or item_data == 'thml pwr':
        col = '1:Temperature GPU (C)'
        fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
        Temperature_GPU = fail_col_data[0]
        logger.info(f'Temperature_GPU:{Temperature_GPU}')
        if Temperature_GPU > 87:
            is_match_rule = True

        col = 'GPU Sensor Temp'
        fail_col_data, fail_file_data = get_performance_file_col_data_by_dir(fail_dir, col)
        GPU_sensor_Temp = fail_col_data[0]

        col = 'Environment Sensor Temp'
        fail_col_data, fail_file_data = get_performance_file_col_data_by_dir(fail_dir, col)
        min_data = min(fail_col_data)
        max_data = max(fail_col_data)
        is_delta_larger_than_stand = is_two_data_delta_larger_than_threshold(min_data, max_data, 0.1)
        logger.info(f'GPU_sensor_Temp:{GPU_sensor_Temp}')
        if GPU_sensor_Temp > 87 and not is_delta_larger_than_stand:
            is_match_rule = True


    # 只有1:NVVDD Power (W)明显差异
    if is_match_rule:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict


def check_rule_27(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_27',
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

    cell_data = fail_col_data[0].strip()
    is_ac = False

    if cell_data == 'AC':
        is_ac = True

    col = '1:D-Notifier Limit'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    logger.info(f'fail_col_data: {fail_col_data}')

    cell_data = fail_col_data[0].strip()
    is_d2_d5 = False
    logger.info(f'cell_data: {cell_data}')

    if 'D2' in cell_data or 'D3' in cell_data or 'D4' in cell_data or 'D5' in cell_data:
        is_d2_d5 = True

    if is_d2_d5 and is_ac:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def check_rule_28(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_28',
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
    # logger.info(f'fail_col_data: {fail_col_data}')

    is_all_enabled = is_col_data_all_same_with_target(fail_col_data, 'enable')

    col = '1:Capping Reason'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    # logger.info(f'fail_col_data: {fail_col_data}')

    is_all_pwr = is_col_data_all_same_with_target(fail_col_data, 'pwr')

    col = '1:AC Target TPP Limit (mW)'
    fail_col_data, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)

    fail_col_data = remove_list_na(fail_col_data, 'N/A')
    # logger.info(f'fail_col_data: {fail_col_data}')

    min_data = min(fail_col_data)
    max_data = max(fail_col_data)
    is_data_const = False
    if min_data == max_data:
        is_data_const = True

    if is_data_const and is_all_pwr and is_all_enabled:
        return_dict = check_result_dict
        logger.info(f'return_dict: {return_dict}')

    return return_dict

def check_rule_29(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_29',
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

def check_rule_30(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_30',
        'Root cause': 'VBIOS',
        'Component': 'EE',
        'Solution': 'please EE check VBIOS version',
        '修复及验证': '',
    }
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

def check_rule_31(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_31',
        'Root cause': 'Vram vendor',
        'Component': 'EE',
        'Solution': 'Please EE check Vram vendor difference',
        '修复及验证': '',
    }
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    col = 'VRAM Strap'
    fail_col_data, fail_file_data = get_gpu_file_head_col_data_by_dir(fail_dir, col)
    pass_col_data, pass_file_data = get_gpu_file_head_col_data_by_dir(pass_dir, col)

    logger.info(f'fail_col_data: {fail_col_data}')
    logger.info(f'pass_col_data: {pass_col_data}')

    return return_dict

def check_rule_32(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_32',
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
    cell_data_platform = fail_col_data_platform[0]

    col = '1:WM2 Driver Enabled'
    fail_col_data_driver, fail_file_data = get_gpu_file_col_data_by_dir(fail_dir, col)
    cell_data_driver = fail_col_data_platform[0]

    if cell_data_platform != 'No' and cell_data_driver != 'No':
        return_dict = check_result_dict
        logger.info(f'cell_data_platform: {cell_data_platform}')

    return return_dict

def check_rule_33(parent_dir=None, fail_dir=None, pass_dir=None):
    return_dict = None
    check_result_dict = {
        'rule name': 'check_rule_33',
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
