# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re
import cv2
import subprocess
import pandas as pd
import numpy as np
from base.logger import *


# file = os.path.abspath(__file__)
path_dir = os.path.dirname(__file__)

global current_enable
current_enable = False

def get_list_lower_index(input_list, bench_mark):
    target_index = None
    for idx, item in enumerate(input_list):
        if float(item) < bench_mark:
            target_index = idx
            break
    return target_index

def remove_list_na(input_list, target_str='NA'):
    out_list = []
    for item in input_list:
        if target_str not in str(item) and 'nan' not in str(item):
            out_list.append(item)
    return out_list

def get_SystemDeckPM_file_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        return None
    SystemDeckPM_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'SystemDeckPM' in filename and '.csv' in filename:
            SystemDeckPM_file = os.path.join(dir_name, filename)
            logger.info(f'SystemDeckPM_file:{SystemDeckPM_file}')
            break
    return SystemDeckPM_file

def get_tat_file_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        return None
    tat_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'PTAT' in filename and '.csv' in filename:
            tat_file = os.path.join(dir_name, filename)
            logger.info(f'tat_file:{tat_file}')
            break
    return tat_file

def get_gpu_file_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        return None
    gpu_log_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'GPUMon' in filename and '.csv' in filename:
            gpu_log_file = os.path.join(dir_name, filename)
            logger.info(f'gpu_log_file:{gpu_log_file}')
            break
    return gpu_log_file

def get_performance_file_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        return None
    PerformanceLog_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'PerformanceLog' in filename and '.csv' in filename:
            PerformanceLog_file = os.path.join(dir_name, filename)
            logger.info(f'PerformanceLog:{PerformanceLog_file}')
            break
    return PerformanceLog_file

def calculate_deviation(col_fail, col_pass, base='average'):
    """
    计算两列值的偏差百分比

    参数:
        col_fail, col_pass: 要比较的两列数据
        base: 基准值选择，'col_fail'（以col1为基准）、'col_pass'（以col2为基准）、'average'（以两列平均值为基准）

    返回:
        偏差百分比（%），处理了除零情况
    """
    abs_diff = np.abs(col_fail - col_pass)  # 计算绝对差值

    # 根据基准值计算分母
    if base == 'col_fail':
        denominator = col_fail
    elif base == 'col_pass':
        denominator = col_pass
    else:  # average
        denominator = (col_fail + col_pass) / 2

    # 处理除零情况（避免除以0导致的错误）
    with np.errstate(divide='ignore', invalid='ignore'):
        deviation = (abs_diff / denominator) * 100

    # 当分母为0且分子也为0时，偏差为0%；否则为NaN（无意义）
    deviation = np.where((denominator == 0) & (abs_diff == 0), 0, deviation)
    # logger.info(f'deviation:{deviation}')
    return deviation

def get_list_text_count(result, text):
    text_line = None
    count = 0
    if result is None:
        return count

    for item in result:
        if text in item:
            count = count + 1
    return count

def get_list_equal_count(result, text):
    text_line = None
    count = 0
    if result is None:
        return count

    for item in result:
        if text == item:
            count = count + 1
    return count

def get_list_lower_than_stand_average(input_list, stand, debug = False):
    output_list = []
    average = None
    total = 0
    if input_list is None:
        return average

    for item in input_list:
        if item < stand:
            output_list.append(item)
            if debug:
                logger.info(f"item:{item}")
    average = sum(output_list) / len(output_list)
    return average

def get_list_average(input_list, debug = False):
    output_list = []
    average = None
    total = 0
    if input_list is None:
        return average

    for item in input_list:
        if item:
            output_list.append(item)
            if debug:
                logger.info(f"item:{item}")
    average = sum(output_list) / len(output_list)
    return average


def is_col_data_all_same_with_target(col_data, target_str):
    is_match_target = False
    for item in col_data:
        if target_str in item.strip():
            is_match_target = True
        if target_str not in item.strip():
            is_match_target = False
            break
    return is_match_target

def is_col_data_all_match_range(col_data, target_min, target_max):
    is_all_match = False
    for item in col_data:
        item = float(item.strip())
        if target_min<=item<=target_max:
            is_all_match = True
        if item>target_max or item<target_min:
            is_all_match = False
            break
    return is_all_match

def is_col_data_has_data_match_range(col_data, target_min, target_max):
    has_match = False
    for item in col_data:
        if target_min<=item<=target_max:
            has_match = True
            break
        if item>target_max or item<target_min:
            has_match = False

    return has_match

def is_two_list_delta_larger_than_threshold(col_fail, col_pass, threshold, df_fail):
    is_larger_than_threshold = False

    df_fail['deviation_%'] = calculate_deviation(col_fail, col_pass, base='col_pass')

    df_fail['exceed_threshold'] = df_fail['deviation_%'] > threshold
    # logger.info(f'df_fail:{df_fail}')

    count = get_list_equal_count(df_fail['exceed_threshold'], True)
    if count:
        is_larger_than_threshold = True
    return is_larger_than_threshold

def is_two_col_data_delta_larger_than_threshold(col_1_data, col_2_data, threshold):
    is_delta_larger_than_stand = False
    if col_1_data is not None and col_2_data is not None:
        delta = abs(col_1_data[0] - col_2_data[0])
        logger.info(f'delta:{delta}')
        logger.info(f'threshold:{threshold}')
        if delta >= threshold:
            is_delta_larger_than_stand = True
    return is_delta_larger_than_stand

def is_two_data_delta_larger_than_threshold(data_1, data_2, threshold):
    is_delta_larger_than_stand = False
    # logger.info(f'data_1:{data_1}, data_2:{data_2}')

    delta = abs(data_1 - data_2)
    # logger.info(f'delta:{delta}')
    delta_ratio = delta/data_1
    # logger.info(f'delta_ratio:{delta_ratio}')
    if delta_ratio > threshold:
        is_delta_larger_than_stand = True
    return is_delta_larger_than_stand

if __name__ == '__main__':
    pass
