import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_GPU_case_1027\GPU-thermal_module2_issue'
    gpu_rule_1(parent_dir=parent_dir)
    pass