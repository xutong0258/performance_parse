import os

from base.cell_command import *
from base.componet import *


path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    fail_dir = r'D:\CASE_FAIL'
    pass_dir = r'D:\CASE_PASS'
    check_rule_33(fail_dir, pass_dir)
    pass