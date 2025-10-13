import csv
import os
from base.helper import *

def write_to_csv(filename, data, headers=None):
    try:
        # 使用with语句打开文件，确保文件正确关闭
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            # 创建CSV写入器
            writer = csv.writer(csvfile)

            # 如果提供了表头，先写入表头
            if headers:
                writer.writerow(headers)

            # 写入数据行
            writer.writerows(data)

        # logger.info(f"成功将{len(data)}行数据写入到{filename}")
        return True

    except IOError as e:
        logger.info(f"写入文件时发生错误: {e}")
    except Exception as e:
        logger.info(f"发生意外错误: {e}")
    return False

def get_gpu_data_with_csv(file_path):
    """使用内置csv模块读取CSV文件"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.info(f"错误：文件 '{file_path}' 不存在")
            return
        
        # 打开CSV文件并读取
        with open(file_path, 'r', encoding='utf-8') as file:
            # 创建CSV读取器
            csv_reader = csv.reader(file)

            headers = []
            new_list = []
            # 读取并打印行数据
            row_count = 0
            for row in csv_reader:
                row_count += 1
                # logger.info(f"行 {row_count}：", row)
                if 'Timestamp' in row:
                    headers = row
                    continue
                if headers:
                    new_list.append(row)
                
            # logger.info("\n读取完成，共", row_count, "行数据")
            return headers, new_list
    except PermissionError:
        logger.info(f"错误：没有权限读取文件 '{file_path}'")
    except UnicodeDecodeError:
        logger.info(f"错误：文件编码不是utf-8，请尝试其他编码格式")
    except Exception as e:
        logger.info(f"读取文件时发生错误：{e}")


def get_gpu_head_data_with_csv(file_path, header_str='VRAM Strap'):
    """使用内置csv模块读取CSV文件"""
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.info(f"错误：文件 '{file_path}' 不存在")
            return

        # 打开CSV文件并读取
        with open(file_path, 'r', encoding='utf-8') as file:
            # 创建CSV读取器
            csv_reader = csv.reader(file)

            headers = []
            new_list = []
            # 读取并打印行数据
            row_count = 0
            for row in csv_reader:
                row_count += 1
                # logger.info(f"行 {row_count}：", row)
                if header_str in row:
                    headers = row
                    continue
                if headers:
                    new_list.append(row)
                    break

            # logger.info("\n读取完成，共", row_count, "行数据")
            return headers, new_list
    except PermissionError:
        logger.info(f"错误：没有权限读取文件 '{file_path}'")
    except UnicodeDecodeError:
        logger.info(f"错误：文件编码不是utf-8，请尝试其他编码格式")
    except Exception as e:
        logger.info(f"读取文件时发生错误：{e}")

if __name__ == "__main__":
    # 示例文件路径（Windows系统）
    csv_file_path = "4-GPUMonLog_NvGPUMon.csv"  # 可以替换为实际的CSV文件路径，如 "C:\\data\\example.csv"
    # get_gpu_data_with_csv(csv_file_path)

    headers, new_list = get_gpu_data_with_csv(csv_file_path)

    write_to_csv("new.csv", new_list, headers)
    