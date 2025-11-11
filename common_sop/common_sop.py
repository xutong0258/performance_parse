import os
from base import common
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    parent_dir = r'D:\BAK\0_intelcpu_case_1024\cpu Sample_rule1'
    one_process_run(parent_dir=parent_dir)
    pass