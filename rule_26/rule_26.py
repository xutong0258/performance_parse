import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    fail_dir = r'D:\小拉\0_peformance\GPU_FAIL'
    pass_dir = r'D:\小拉\0_peformance\GPU_PASS'
    check_rule_26(fail_dir, pass_dir)
    pass