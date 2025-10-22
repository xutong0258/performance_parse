import os
from base import common
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    fail_dir = r'D:\小拉\0_peformance\GPU_FAIL'
    pass_dir = r'D:\小拉\0_peformance\GPU_PASS'

    fail_dir = r'D:\小拉\0_peformance_验收\intel+nv_case-1021\CPU_case-环温sensor\Fail_环温sensor_CinebenchR23_2025-05-15_034755'
    pass_dir = r'D:\小拉\0_peformance_验收\intel+nv_case-1021\CPU_case-环温sensor\pass_环温sensor'

    one_process_run_tmp(fail_dir, pass_dir)
    pass