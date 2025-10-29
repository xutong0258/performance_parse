import time

import pandas as pd
import os
from base.helper import *
from base.read_csv_with_csv import *
from base.fileOP import *

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
        # logger.info(f"df.head(0):{df.head(0)}")
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
    file = r'总是顶着ThermalLimit.csv'
    read_csv_with_pandas(file)
    pass
    