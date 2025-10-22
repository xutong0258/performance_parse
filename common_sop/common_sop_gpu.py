import os
from base import common
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    # fail_dir = r'D:\0_intel+nv_case-1021\GPUmode_HDDG\fail'
    # pass_dir = r'D:\0_intel+nv_case-1021\GPUmode_HDDG\pass'
    # gpu_check_run(fail_dir, pass_dir)

    parent_dir = r'D:\0_intel+nv_case-1021\GPUmode_HDDG'
    gpu_check_run(parent_dir=parent_dir)
    pass