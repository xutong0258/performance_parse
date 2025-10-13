import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    src_dir = r'D:\小拉\0_peformance'
    log_file = os.path.join(src_dir, '2-IPTATLog-1722610856407_iPTAT_02-08-2024_23H-01-05S157.csv')
    fail_dir = r'D:\小拉\0_peformance\20250925-performance\case-环温sensor\Fail_环温sensor'
    pass_dir = r'D:\小拉\0_peformance\20250925-performance\case-环温sensor\pass_环温sensor'
    check_rule_16(fail_dir, pass_dir)
    pass