import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *
from base.amd_cell_command import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_AMD\rule14——与pass机器比较CPU温度总是触发limit'
    amd_check_rule_15(parent_dir=parent_dir)
    pass