import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_intelcpu_case_1112\cpu Sample_rule1'
    check_rule_1(parent_dir=parent_dir, fail_dir=None, pass_dir=None)
    pass