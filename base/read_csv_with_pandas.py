import time

import pandas as pd
import os
from base.helper import *
from base.read_csv_with_csv import *
from base.fileOP import *

def read_excel_with_pandas_ex(file_path):
    """使用pandas库读取CSV文件"""
    missing_values = ["n/a", "na", "--", 'N/A', 'NA']
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.info(f"错误：文件 '{file_path}' 不存在")
            return

        # 读取CSV文件
        df = pd.read_csv(file_path, encoding='utf-8', na_values = missing_values)

        new_df = df.dropna()

        # 打印数据基本信息
        logger.info(f"df:{new_df.index}")
        return new_df
    except PermissionError:
        logger.info(f"错误：没有权限读取文件 '{file_path}'")
        return None
    except UnicodeDecodeError:
        logger.info(f"错误：文件编码不是utf-8，尝试其他编码如gbk：read_csv(file_path, encoding='gbk')")
        return None
    except Exception as e:
        logger.info(f"读取文件时发生错误：{e}")
        return None

def read_excel_with_pandas(file_path):
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.info(f"错误：文件 '{file_path}' 不存在")
            return

        # 读取CSV文件
        df = pd.read_csv(file_path, encoding='gbk')
        column = 'Parameters-old'
        col_old = df.get(column, None)
        logger.info(f"col_old:{col_old}")

        column = 'Parameters-new'
        col_new = df.get(column, None)
        logger.info(f"col_new:{col_new}")

        tmp_dict = {}
        for idx, line in enumerate(col_old):
            tmp_dict[col_new[idx]] = col_old[idx]

        dump_file('GPU_parameters.yaml', tmp_dict)

        # 打印数据基本信息
        logger.info(f"df:{df.index}")
        return df
    except PermissionError:
        logger.info(f"错误：没有权限读取文件 '{file_path}'")
        return None
    except UnicodeDecodeError:
        logger.info(f"错误：文件编码不是utf-8，尝试其他编码如gbk：read_csv(file_path, encoding='gbk')")
        return None
    except Exception as e:
        logger.info(f"读取文件时发生错误：{e}")
        return None

def read_csv_with_pandas(file_path, encoding='utf-8'):
    """使用pandas库读取CSV文件"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.info(f"错误：文件 '{file_path}' 不存在")
            return

        new_list = read_data_with_csv(file_path)

        new_file = 'new.csv'
        write_to_csv(new_file, new_list)
        time.sleep(3)

        # 读取CSV文件
        df = pd.read_csv(new_file, encoding='utf-8')

        # 打印数据基本信息
        logger.info(f"df:{df.index}")
        return df
    except PermissionError:
        logger.info(f"错误：没有权限读取文件 '{file_path}'")
        return None
    except UnicodeDecodeError:
        logger.info(f"错误：文件编码不是utf-8，尝试其他编码如gbk：read_csv(file_path, encoding='gbk')")
        return None
    except Exception as e:
        logger.info(f"读取文件时发生错误：{e}")
        return None

if __name__ == "__main__":
    src_dir = r'./'
    log_file = os.path.join(src_dir, 'GPU_parameters_2025_0827.csv')
    read_excel_with_pandas(log_file)
    