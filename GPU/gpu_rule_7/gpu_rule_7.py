import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_GPU_case\GPU_NVVDD_rule7_OK'
    gpu_rule_7(parent_dir=parent_dir)
    pass