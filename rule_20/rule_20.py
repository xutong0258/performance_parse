import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    fail_dir = r'D:\小拉\0_peformance_验收\intel+nv_case-1021\CPU_case-环温sensor\Fail_环温sensor_CinebenchR23_2025-05-15_034755'
    pass_dir = r'D:\小拉\0_peformance_验收\intel+nv_case-1021\CPU_case-环温sensor\pass_环温sensor'
    check_rule_20(fail_dir)
    pass