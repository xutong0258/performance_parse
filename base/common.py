# coding=utf-8

import json
import os
import shutil
import sys
import logging
import time
import datetime
import re
from base.helper import *
from base.contants import *
from base.read_csv_with_pandas import *
from base.read_csv_with_csv import *
from base.fileOP import *

path_dir = os.path.dirname(__file__)

file = r'GPU_parameters.yaml'
file_path = os.path.join(CONFIG_PATH, file)

GPU_parameters = read_file_dict(file_path)
# logger.info(f'GPU_parameters: {GPU_parameters}')

def get_log_case(input_dir):
    case_type = []
    tat_file = get_tat_file_with_dir(input_dir)
    if tat_file:
        case_type.append(Intel_Case)

    amd_file = get_amd_file_with_dir(input_dir)
    if amd_file:
        case_type.append(AMD_Case)

    is_gpu_case = check_gpu_case(input_dir)
    if is_gpu_case:
        case_type.append(GPU_Case)

    return case_type

def check_gpu_case(input_dir):
    is_gpu_case = False
    gpu_file = get_gpu_file_with_dir(input_dir)
    if gpu_file is None:
        gpu_file = get_performance_file_with_dir(input_dir)
    if gpu_file:
        is_gpu_case = True
    return is_gpu_case

def is_amd_case(input_dir):
    is_amd_case = False
    amd_file = get_performance_file_with_dir(input_dir)
    if gpu_file:
        is_amd_case = True
    return is_amd_case

def get_match_col_name(head_list, col_name):
    max_ratio = 0
    max_ratio_index = None
    col = None
    for idx, item in enumerate(head_list):
        curr_ratio = similarity_ratio(item, col_name)
        if curr_ratio > max_ratio:
            max_ratio = curr_ratio
            max_ratio_index = idx
    col = head_list[max_ratio_index]
    # logger.info(f'col:{col}')
    return col

def get_intel_file_head_list_by_dir(input_dir):
    intel_log_file = get_tat_file_with_dir(input_dir)
    logger.info(f'intel_log_file:{intel_log_file}')

    headers = get_head_with_csv(intel_log_file)
    logger.info(f'headers:{headers}')

    return headers

def get_gpu_file_head_list_by_dir(input_dir):
    gpu_log_file = get_gpu_file_with_dir(input_dir)
    logger.info(f'gpu_log_file:{gpu_log_file}')

    headers, new_list = get_gpu_data_with_csv(gpu_log_file)
    # logger.info(f'headers:{headers}')
    # new_file = os.path.join(input_dir, 'GPU_New.csv')
    # write_to_csv(new_file, new_list, headers)
    return headers

def get_amd_performance_file_head_list_by_dir(input_dir):
    amd_fail_file = get_amd_file_with_dir(input_dir)
    head_list = get_head_with_csv(amd_fail_file)
    return head_list

def get_amd_performance_file_data_frame_by_dir(input_dir):
    amd_fail_file = get_amd_file_with_dir(input_dir)
    data_frame = read_csv_with_pandas(amd_fail_file)
    return data_frame

def get_intel_tat_file_col_data_by_dir(input_dir, col_name):
    if input_dir is None:
        return None
    col_data = []
    tat_file = get_tat_file_with_dir(input_dir)
    file_data = read_csv_with_pandas(tat_file)
    col_data = file_data.get(col_name)
    return col_data

def get_amd_file_col_data_by_dir(input_dir, col_name):
    col_data = []
    amd_fail_file = get_amd_file_with_dir(input_dir)
    data_frame = read_csv_with_pandas(amd_fail_file)
    col_data = data_frame.get(col_name)
    return col_data, data_frame

def get_intel_tat_file_col_data_by_dir_ex(input_dir, col_name):
    col_data = []
    tat_file = get_tat_file_with_dir(input_dir)
    data_frame = read_csv_with_pandas(tat_file)
    col_data = data_frame.get(col_name)
    return col_data, data_frame

def get_intel_tat_file_data_frame_by_dir(input_dir):
    col_data = []
    tat_file = get_tat_file_with_dir(input_dir)
    data_frame = read_csv_with_pandas(tat_file)
    return data_frame

def get_gpu_file_col_data_by_dir(input_dir, col_name):
    col_data = []
    gpu_log_file = get_gpu_file_with_dir(input_dir)
    logger.info(f'gpu_log_file:{gpu_log_file}')

    headers, new_list = get_gpu_data_with_csv(gpu_log_file)
    new_file = os.path.join(input_dir, 'GPU_New.csv')
    write_to_csv(new_file, new_list, headers)

    is_new_gpu_tool = False
    if col_name in headers:
        is_new_gpu_tool = True

    if is_new_gpu_tool == False:
        col_name = GPU_parameters.get(col_name, None)
        logger.info(f'col_name:{col_name}')

    file_data = read_csv_with_pandas(new_file)
    col_data = None
    if col_name is not None:
        col_data = file_data.get(col_name)
    return col_data, file_data

def get_gpu_file_target_map_by_dir(input_dir, target_str):
    col_data = []
    gpu_log_file = get_gpu_file_with_dir(input_dir)

    target_map = get_gpu_target_map_with_csv(gpu_log_file, target_str)
    return target_map

def get_performance_file_col_data_by_dir(input_dir, col_name):
    col_data = None
    file_data = None
    performance_log_file = get_performance_file_with_dir(input_dir)

    if performance_log_file is not None:
        file_data = read_csv_with_pandas(performance_log_file)
        col_data = file_data.get(col_name)
    return col_data, file_data

def is_performance_ec_file_exist_by_dir(input_dir):
    is_exist = False
    performance_log_file = get_performance_file_with_dir(input_dir)
    logger.info(f'performance_log_file:{performance_log_file}')
    if performance_log_file is not None:
        is_exist = True
    return is_exist

def get_csv_file_col_data_by_file(input_file, col_name):
    col_data = []
    file_data = read_csv_with_pandas(input_file)
    col_data = file_data.get(col_name)
    return col_data

def get_csv_file_col_data_by_file_gpu(input_file, col_name, headers):
    is_new_gpu_tool = False
    if col_name in headers:
        is_new_gpu_tool = True

    if is_new_gpu_tool == False:
        col_name = GPU_parameters[col_name]
        logger.info(f'col_name:{col_name}')

    col_data = []
    file_data = read_csv_with_pandas(input_file)
    col_data = file_data.get(col_name)
    return col_data

def get_two_list_correlation(col_1, col_2):
    correlation = None
    if col_1 is not None and col_2 is not None:
        correlation = col_1.corr(col_2, method='pearson')
        logger.info(f"皮尔逊相关系数: {correlation:.4f}")
    return correlation


def get_two_data_frame_col_average(data_frame_1, data_frame_2, col_name, head_list):
    col_name = get_match_col_name(head_list, col_name)
    logger.info(f'col_name:{col_name}')

    col_amd_fail = data_frame_1[col_name]
    fail_average_data = get_list_average(col_amd_fail)
    logger.info(f"fail_average_data: {fail_average_data}")

    col_amd_pass = data_frame_2[col_name]
    pass_average_data = get_list_average(col_amd_pass)
    logger.info(f"pass_average_data: {pass_average_data}")

    return fail_average_data, pass_average_data

def get_col_idle_average(input_list):
    col_average = get_list_average(input_list, False)
    logger.info(f"col_average: {col_average}")
    idle_list = []
    for idx, line in enumerate(input_list):
        is_delta_larger_than_stand = is_two_data_delta_larger_than_threshold(line, col_average, 0.3)
        if is_delta_larger_than_stand:
            # logger.info(f"line: {line}")
            idle_list.append(line)

    idle_average = get_list_average(idle_list, False)
    logger.info(f"idle_average: {idle_average}")
    return idle_average

def get_cpu_log_content(log_dir, channel_str='Controller0-ChannelA-DIMM1'):
    channel_dict = {}
    log_file = get_CPUZ_log_file_with_dir(log_dir)
    if log_file is None:
        return None
    log_lines = get_file_content_list(log_file)
    # channel_str = 'Controller0-ChannelA-DIMM1'
    index = get_list_text_line_first_index(log_lines, channel_str)
    #
    if index is not None:
        type_index = index + 2
        type_line = log_lines[type_index]
        # logger.info(f'type_line:{type_line}')
        tmp_list = type_line.split('\t')
        # logger.info(f'tmp_list:{tmp_list}')

        new_list = remove_list_emptpy(tmp_list)
        # logger.info(f'new_list:{new_list}')
        channel_dict['type'] = new_list[1]

        # size
        type_index = index + 5
        line = log_lines[type_index]
        # logger.info(f'line:{line}')
        tmp_list = line.split('\t')
        # logger.info(f'tmp_list:{tmp_list}')

        new_list = remove_list_emptpy(tmp_list)
        # logger.info(f'new_list:{new_list}')
        channel_dict['size'] = new_list[1]

        # speed
        type_index = index + 5
        line = log_lines[type_index]
        # logger.info(f'line:{line}')
        tmp_list = line.split('\t')
        # logger.info(f'tmp_list:{tmp_list}')

        new_list = remove_list_emptpy(tmp_list)
        # logger.info(f'new_list:{new_list}')
        channel_dict['speed'] = new_list[1]

    # logger.info(f'channel_dict:{channel_dict}')
    return channel_dict

if __name__ == '__main__':
    logger.info('common hello')
    pass
