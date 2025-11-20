import os

from base.amd_cell_command import *
from base.componet import *


path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_AMD\rule14——与pass机器比较CPU温度总是触发limit'
    amd_check_rule_16(parent_dir=parent_dir)
    pass