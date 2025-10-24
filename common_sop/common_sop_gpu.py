import os
from base import common
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    parent_dir = r'D:\BAK\GPU'
    gpu_check_run(parent_dir=parent_dir)
    pass