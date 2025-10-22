import os
from base import common
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    fail_dir = r'D:\小拉\0_peformance\GPU_FAIL'
    pass_dir = r'D:\小拉\0_peformance\GPU_PASS'

    fail_dir = r'D:\0_intel+nv_case-1021\CPU_case-环温sensor\Fail_环温sensor_CinebenchR23_2025-05-15_034755'
    pass_dir = r'D:\0_intel+nv_case-1021\CPU_case-环温sensor\pass_环温sensor'

    # one_process_run(fail_dir, pass_dir)
    intel_check_run(fail_dir, pass_dir)

    # fail_dir = r'D:\0_intel+nv_case-1021\CPU_Max_Frequency\fail'
    # pass_dir = r'D:\0_intel+nv_case-1021\CPU_Max_Frequency\pass'
    # intel_check_run(fail_dir, pass_dir)
    pass