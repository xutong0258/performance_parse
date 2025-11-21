# coding=utf-8
import os
import sys
import re
import platform
import datetime

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)

ROOT_DIR = os.path.dirname(path_dir)
print(ROOT_DIR)


CONFIG_PATH = os.path.join(path_dir, '../config')

sys.path.append(path_dir)

Intel_Case = 'Intel_Case'
GPU_Case = 'GPU_Case'
AMD_Case = 'AMD_Case'


