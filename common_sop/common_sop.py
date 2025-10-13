import os
from base import common
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    fail_dir = r'D:\小拉\0_peformance\GPU_FAIL'
    pass_dir = r'D:\小拉\0_peformance\GPU_PASS'
    one_process_run(fail_dir, pass_dir)
    pass