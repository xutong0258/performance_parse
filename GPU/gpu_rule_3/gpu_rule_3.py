import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_GPU_case\GPU_Sample_rule1_OK\case_1'
    gpu_rule_3(parent_dir=parent_dir)
    pass