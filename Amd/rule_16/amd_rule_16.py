import os

from base.amd_cell_command import *
from base.componet import *


path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    fail_dir = r'D:\CASE_FAIL'
    pass_dir = r'D:\CASE_PASS'
    amd_check_rule_16(fail_dir, pass_dir)
    pass