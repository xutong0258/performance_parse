import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *
from base.amd_cell_command import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    fail_dir = r'D:\AMD_FAIL'
    pass_dir = r'D:\AMD_PASS'
    amd_check_rule_5(fail_dir, pass_dir)
    pass