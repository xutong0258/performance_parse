import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_intelcpu_case_1112\cpu_PL4_PL4建议加rule13'
    check_rule_14(parent_dir=parent_dir)
    pass