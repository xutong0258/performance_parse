import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_GPU_case\GPU_PPAB_rule11_ok'
    gpu_rule_12(parent_dir=parent_dir)
    pass