import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    # src_dir = r'D:\小拉\0_peformance'
    # log_file = os.path.join(src_dir, '2-IPTATLog-1722610856407_iPTAT_02-08-2024_23H-01-05S157.csv')
    # file_dir = r'D:\小拉\0_peformance\几种抓到的log类型'
    # check_rule_18(file_dir)

    fail_dir = r'D:\小拉\0_peformance_验收\intel+nv_case-1021\CPU_case-环温sensor\Fail_环温sensor_CinebenchR23_2025-05-15_034755'
    pass_dir = r'D:\小拉\0_peformance_验收\intel+nv_case-1021\CPU_case-环温sensor\pass_环温sensor'
    check_rule_18(fail_dir)
    pass