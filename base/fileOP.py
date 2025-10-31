# coding=utf-8

import yaml
import json
import os
import platform
import re
from base.helper import *


def read_file_by_line(file_name: str) -> list:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    with open (file_name, "r") as file:
        for line in file:
            # my_log.info (line.strip ())
            pass
    return


def read_file_dict(file_name: str) -> dict:
    record_dic = {}
    if '.yaml' in file_name:
        with open(file_name, 'r', encoding='utf-8') as wf:
            record_dic = yaml.safe_load(wf)
    elif '.json' in file_name:
        with open (file_name, 'r') as wf:
            record_dic = json.load (wf)
    else:
        # my_log.info(f'file not support:{read_file_dict}')
        pass
    return record_dic

def dump_file(file_name, data) -> int:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    # file_name = os.path.join(file_path, file_name)
    with open(file_name, 'w', encoding='utf-8') as wf:
        yaml.safe_dump(data, wf, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return 0


def read_json_dict(file_name: str) -> dict:
    """
    读取文本用例数据
    :param file_name: 文件路径
    :return: list
    """
    data_dic = {}
    with open(file_name, 'r') as wf:
        data_dic = json.load(wf)
    return data_dic


def wrtie_file(file_name, content) -> None:
    # 打开文件，如果文件不存在，会创建文件；'a' 表示追加模式，如果文件已存在，则会在文件末尾追加内容
    with open (file_name, 'w') as file:
        # 追加文本数据
        file.write(content)
    return

def add_string_to_first_line(file_path, new_string):
    try:
        # 以只读模式打开文件并读取所有内容
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 在内容开头插入新的字符串，并添加换行符
        lines.insert(0, new_string + '\n')

        # 以写入模式打开文件并将更新后的内容写回
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        # logger.info(f"成功在文件 {file_path} 的第一行添加字符串。")
    except FileNotFoundError:
        logger.info(f"未找到文件: {file_path}")
    except Exception as e:
        logger.info(f"发生错误: {e}")
    return

def get_file_content_list(file_path):
    log_lines = []
    try:
        # 以只读模式打开文件并读取所有内容
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            log_lines = f.readlines()  # 列表形式存储每一行日志，保留换行符
    except FileNotFoundError:
        logger.info(f"未找到文件: {file_path}")
    except Exception as e:
        logger.info(f"发生错误: {e}")
    return log_lines


if __name__ == '__main__':
    # change_file_format()
    # change_file_dict()
    # covert_rope_cfg()
    # rope_analysis()
    current_enable = False
    if current_enable:
        data_dict = {}
        file = r'D:/hello.yaml'
        dump_file(file, data_dict)
    else:
        pass