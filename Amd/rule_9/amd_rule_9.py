import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *
from base.amd_cell_command import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_AMD\rule7——与pass机器比较Idle场景CPU Power高'
    amd_check_rule_9(parent_dir=parent_dir)
    pass