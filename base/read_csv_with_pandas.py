import pandas as pd
import os
from base.helper import *

def read_csv_with_pandas(file_path):
    """使用pandas库读取CSV文件"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.info(f"错误：文件 '{file_path}' 不存在")
            return
        
        # 读取CSV文件
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # 打印数据基本信息
        logger.info(f"df:{df.index}")
        # logger.info("数据基本信息：")
        # logger.info(f"形状：{df.shape}")
        # logger.info(f"形状：{df.shape[0]}行，{df.shape[1]}列")
        # logger.info("\n前5行数据：")
        # logger.info(df.head())

        # 2. 访问指定列的两种常用方法

        # 方法1：使用方括号 + 列名（最推荐，适用性最广）
        # 适用于列名有空格、特殊字符或与pandas关键字冲突的情况
        # col_1 = 'CPU0-Frequency(MHz)'
        # col_2 = 'Power-Package Power(Watts)'
        # column1 = df[col_1]  # 替换为你的实际列名
        # logger.info("\n方法1访问的列：")
        # logger.info(column1.head())  # 打印前5行

        # 方法2：使用点符号 + 列名（简洁但有局限性）
        # 仅适用于列名无空格、无特殊字符（如@#$）、且不与pandas内置方法重名（如sum、count等）
        # if "Power-Package Power(Watts)" in df.columns:  # 确保列名存在
            # column2 = df.列名2  # 替换为你的实际列名（无空格/特殊字符）
            # column2 = df[col_2]  # 替换为你的实际列名（无空格/特殊字符）
            # logger.info("\n方法2访问的列：")
            # logger.info(column2.head())

        # 方法1：使用pandas计算皮尔逊相关系数（默认）
        # pearson_corr = df[col_1].corr(df[col_2], method='pearson')
        # logger.info(f"皮尔逊相关系数: {pearson_corr:.4f}")

        # 获取列的描述性统计（均值、标准差等）
        # logger.info("\n列的统计信息：")
        # logger.info(column1.describe())
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
    src_dir = r'D:\小拉\0_peformance'
    log_file = os.path.join(src_dir, '2-IPTATLog-1722610856407_iPTAT_02-08-2024_23H-01-05S157.csv')
    read_csv_with_pandas(log_file)
    