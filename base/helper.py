# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re
import subprocess
import pandas as pd
import numpy as np
from base.logger import *


# file = os.path.abspath(__file__)
path_dir = os.path.dirname(__file__)

import difflib

def similarity_ratio(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).ratio()


def get_list_target_text_index_list(input_list, target_text):
    target_text = target_text.lower()
    target_index_list = []
    for idx, item in enumerate(input_list):
        item = item.lower()
        if target_text in item:
            target_index_list.append(idx)

    return target_index_list

def get_list_lower_index(input_list, bench_mark):
    target_index = None
    for idx, item in enumerate(input_list):
        if float(item) < bench_mark:
            target_index = idx
            break
    return target_index

def get_list_lower_index_list(input_list, bench_mark):
    target_index_list = []
    for idx, item in enumerate(input_list):
        if float(item) < bench_mark:
            target_index_list.append(idx)
            break
    return target_index_list

def get_list_lower_equal_index(input_list, bench_mark):
    target_index = None
    for idx, item in enumerate(input_list):
        # logger.info(f"item: {item}")
        if float(item) <= bench_mark:
            target_index = idx
            break
    return target_index

def remove_list_na(input_list, target_str='NA'):
    out_list = []
    if input_list is None:
        return out_list
    for item in input_list:
        if target_str not in str(item) and 'nan' not in str(item) and 'Invalid' not in str(item):
            out_list.append(item)
    return out_list

def get_amd_file_exact_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        logger.info(f'get_amd_file_with_dir return None')
        return None
    SystemDeckPM_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'SystemDeckPM' in filename and '.csv' in filename:
            SystemDeckPM_file = os.path.join(dir_name, filename)
            logger.info(f'SystemDeckPM_file:{SystemDeckPM_file}')
            break
    logger.info(f'SystemDeckPM_file:{SystemDeckPM_file}')
    return SystemDeckPM_file

def get_amd_file_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        logger.info(f'get_amd_file_with_dir return None')
        return None
    SystemDeckPM_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'SystemDeckPM' in filename and '.csv' in filename:
            SystemDeckPM_file = os.path.join(dir_name, filename)
            logger.info(f'SystemDeckPM_file:{SystemDeckPM_file}')
            break
    if SystemDeckPM_file is None:
        for filename in file_list:
            if '.csv' in filename:
                SystemDeckPM_file = os.path.join(dir_name, filename)
                # logger.info(f'SystemDeckPM_file:{SystemDeckPM_file}')
                break
    logger.info(f'SystemDeckPM_file:{SystemDeckPM_file}')
    return SystemDeckPM_file

def get_tat_file_with_dir(dir_name):
    logger.info(f'dir_name:{dir_name}')
    if dir_name is None:
        logger.info(f'get_tat_file_with_dir return None')
        return None
    if not os.path.isdir(dir_name):
        logger.info(f'get_tat_file_with_dir return None')
        return None
    tat_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'PTAT' in filename and '.csv' in filename:
            tat_file = os.path.join(dir_name, filename)
            logger.info(f'tat_file:{tat_file}')
            return tat_file

    for filename in file_list:
        if '.csv' in filename:
            tat_file = os.path.join(dir_name, filename)
            logger.info(f'tat_file:{tat_file}')
            break
    return tat_file

def get_gpu_file_exact_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        return None
    gpu_log_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'NvGPUMon' in filename and '.csv' in filename:
            gpu_log_file = os.path.join(dir_name, filename)
            logger.info(f'gpu_log_file:{gpu_log_file}')
            break
    return gpu_log_file

def get_gpu_file_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        return None
    gpu_log_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if 'NvGPUMon' in filename and '.csv' in filename:
            gpu_log_file = os.path.join(dir_name, filename)
            logger.info(f'gpu_log_file:{gpu_log_file}')
            break

    if gpu_log_file is None:
        for filename in file_list:
            if '.csv' in filename:
                gpu_log_file = os.path.join(dir_name, filename)
                logger.info(f'gpu_log_file:{gpu_log_file}')
                break
    return gpu_log_file

def get_CPUZ_log_file_with_dir(dir_name):
    if not os.path.isdir(dir_name):
        return None
    CPUZ_log_file = None
    file_list = os.listdir(dir_name)
    for filename in file_list:
        if '.txt' in filename:
            CPUZ_log_file = os.path.join(dir_name, filename)
            logger.info(f'CPUZ_log_file:{CPUZ_log_file}')
            break
    return CPUZ_log_file

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

def get_list_text_count(result, text):
    text = text.lower()

    text_line = None
    count = 0
    if result is None:
        return count

    data_list = remove_list_na(result, target_str='nan')
    # logger.info(f"data_list: {data_list}")

    for item in data_list:
        item = item.lower()
        # logger.info(f'item:{item}')
        if item and text in item:
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

def is_digital_item(cell_item):
    number_list = ['0','1','2','3','4','5','6','7','8','9']
    is_number = True
    for item in cell_item:
        # logger.info(f"item:{item}")
        if item not in number_list:
            is_number = False
            break
    # logger.info(f"is_number:{is_number}")
    return is_number

def get_list_average(input_list, debug = False):
    output_list = []
    average = None
    total = 0
    if input_list is None:
        return average

    input_list = remove_list_na(input_list, 'nan')

    # logger.info(f"input_list:{input_list}")
    for item in input_list:
        type_str = type(item)
        # logger.info(f"type_str:{type_str}")
        if type(item) is str:
            is_number = is_digital_item(item)
            if is_number:
                item = float(item)
                output_list.append(item)
        if type(item) is int or type(item) is float:
            output_list.append(item)
        if debug:
            logger.info(f"item:{item}")

    # logger.info(f"output_list:{output_list}")
    if len(output_list):
        average = sum(output_list) / len(output_list)
    return average


def is_col_data_all_same_with_target(col_data, target_str):
    logger.info(f'col_data:{col_data}')
    is_match_target = False
    for item in col_data:
        if target_str.lower() in item.strip().lower():
            is_match_target = True
        if target_str.lower() not in item.strip().lower():
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
        # logger.info(f"item:{item}")
        if type(item) is str:
            item = item.replace('%', '')
            if is_digital_item(item) == False:
                return False
        item = float(item)
        if target_min<=item<=target_max:
            has_match = True
        if target_min<=item<=target_max:
            has_match = True
            break
        if item>target_max or item<target_min:
            has_match = False
    return has_match


def is_two_col_data_delta_larger_than_threshold(col_1_data, col_2_data, threshold):
    is_delta_larger_than_stand = False
    if col_1_data is not None and col_2_data is not None:
        col_1_data = remove_list_na(col_1_data, target_str='nan')
        col_2_data = remove_list_na(col_2_data, target_str='nan')

        average_1 = get_list_average(col_1_data, False)
        average_2 = get_list_average(col_2_data, False)
        delta = abs(average_1 - average_2)
        logger.info(f'delta:{delta}')
        logger.info(f'threshold:{threshold}')
        if delta >= threshold:
            is_delta_larger_than_stand = True
    return is_delta_larger_than_stand

def is_two_data_delta_larger_than_threshold(data_fail, data_pass, threshold):
    is_delta_larger_than_stand = False
    # logger.info(f'data_fail:{data_fail}, data_pass:{data_pass}')

    if data_fail is None or data_pass is None:
        return is_delta_larger_than_stand

    delta = abs(data_fail - data_pass)
    # logger.info(f'delta:{delta}')
    if data_pass > 0:
        delta_ratio = delta/data_pass
    else:
        is_delta_larger_than_stand = True
        return is_delta_larger_than_stand
    # logger.info(f'delta_ratio:{delta_ratio}')
    if delta_ratio > threshold:
        is_delta_larger_than_stand = True
    return is_delta_larger_than_stand

def get_loading_index(data_fail_list, data_average, threshold):
    loading_index = 0
    for idx, item in enumerate(data_fail_list):
        is_delta_larger = is_two_data_delta_larger_than_threshold(item, data_average, threshold)
        if is_delta_larger:
            loading_index = idx
    return loading_index

def is_two_col_same(col_fail, col_pass):
    is_two_coloum_same = True

    for idx, value in enumerate(col_fail):
        if value != col_pass[idx]:
            is_two_coloum_same = False
            break

    return is_two_coloum_same

def get_list_text_line_first_index(input_list, text):
    index = None
    if input_list is None:
        return index

    for idx, line in enumerate(input_list):
        if text in line:
            index = idx
            break
    return index

def get_list_text_line_last_index(input_list, text):
    index = None
    if input_list is None:
        return index

    for idx, line in enumerate(input_list):
        if text in line:
            index = idx
    return index

def remove_list_emptpy(input_list):
    new_list = []
    index = None
    if input_list is None:
        return index
    # logger.info(f'input_list:{input_list}')


    for line in input_list:
        # logger.info(f'xutong:{line}')
        line = line.replace('\n', '')
        # line = line.replace('\t', '')
        new_line = line.strip()
        length = len(new_line)
        # logger.info(f'line:{line}, new_line:{new_line}, length:{length}')
        if length > 0:
            new_list.append(new_line)
    return new_list

if __name__ == '__main__':
    is_digital_item('170')
    pass
