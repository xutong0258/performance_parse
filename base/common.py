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

def is_two_list_delta_larger_than_threshold(col_fail, col_pass, threshold, df_fail):
    is_larger_than_threshold = False

    df_fail['deviation_%'] = calculate_deviation(col_fail, col_pass, base='col_pass')

    df_fail['exceed_threshold'] = df_fail['deviation_%'] > threshold
    # logger.info(f'df_fail:{df_fail}')

    count = get_list_text_count_bool(df_fail['exceed_threshold'], True)
    if count:
        is_larger_than_threshold = True
    return is_larger_than_threshold

if __name__ == '__main__':
    logger.info('common hello')
    pass
