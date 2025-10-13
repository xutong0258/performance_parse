import os

from base.cell_command import *
from base.componet import *


path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    log_dir = r'D:\小拉\0_peformance\GPU_FAIL'
    check_rule_32(log_dir)
    pass