import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_intelcpu_case_1024_verify\cpu_PL1_rule13_spec'
    parent_dir = r'D:\0_intelcpu_case_1024_verify\cpu_PL2_rule13_spec'
    parent_dir = r'D:\0_intelcpu_case_1024_verify\cpu_PL4_PL4建议加rule13_spec'
    check_rule_13(parent_dir=parent_dir)
    pass