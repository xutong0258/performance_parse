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

def get_log_case(input_dir):
    case_type = None
    tat_file = get_tat_file_with_dir(input_dir)
    if tat_file:
        case_type = Intel_Case

    SystemDeckPM_file = get_SystemDeckPM_file_with_dir(input_dir)
    if SystemDeckPM_file:
        case_type = AMD_Case

    is_gpu_case = check_gpu_case(input_dir)
    if is_gpu_case:
        case_type = GPU_Case

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

def get_amd_performance_file_data_frame_by_dir(input_dir):
    amd_fail_file = get_SystemDeckPM_file_with_dir(input_dir)
    data_frame = read_csv_with_pandas(amd_fail_file)
    return data_frame

def get_tat_file_col_data_by_dir(input_dir, col_name):
    col_data = []
    tat_file = get_tat_file_with_dir(input_dir)
    file_data = read_csv_with_pandas(tat_file)
    col_data = file_data.get(col_name)
    return col_data

def get_tat_file_col_data_by_dir_ex(input_dir, col_name):
    col_data = []
    tat_file = get_tat_file_with_dir(input_dir)
    file_data = read_csv_with_pandas(tat_file)
    col_data = file_data.get(col_name)
    return col_data, file_data


def get_gpu_file_col_data_by_dir(input_dir, col_name):
    col_data = []
    gpu_log_file = get_gpu_file_with_dir(input_dir)
    logger.info(f'gpu_log_file:{gpu_log_file}')

    headers, new_list = get_gpu_data_with_csv(gpu_log_file)
    new_file = os.path.join(input_dir, 'GPU_New.csv')
    write_to_csv(new_file, new_list, headers)

    file_data = read_csv_with_pandas(new_file)
    col_data = file_data.get(col_name)
    return col_data, file_data

def get_gpu_file_head_col_data_by_dir(input_dir, col_name):
    col_data = []
    gpu_log_file = get_gpu_file_with_dir(input_dir)

    headers, new_list = get_gpu_head_data_with_csv(gpu_log_file)
    new_file = os.path.join(input_dir, 'GPU_header.csv')
    write_to_csv(new_file, new_list, headers)

    file_data = read_csv_with_pandas(new_file)
    col_data = file_data.get(col_name)
    return col_data, file_data

def get_performance_file_col_data_by_dir(input_dir, col_name):
    col_data = []
    performance_log_file = get_performance_file_with_dir(input_dir)

    file_data = read_csv_with_pandas(performance_log_file)
    col_data = file_data.get(col_name)
    return col_data, file_data

def get_csv_file_col_data_by_file(input_file, col_name):
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


def get_two_data_frame_col_average(data_frame_1, data_frame_2, col_name):
    col_amd_fail = data_frame_1[col_name]
    fail_average_data = get_list_average(col_amd_fail)
    logger.info(f"fail_average_data: {fail_average_data}")

    col_amd_pass = data_frame_2[col_name]
    pass_average_data = get_list_average(col_amd_pass)
    logger.info(f"pass_average_data: {pass_average_data}")

    return fail_average_data, pass_average_data

if __name__ == '__main__':
    logger.info('common hello')
    pass
