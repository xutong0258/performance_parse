import os

from base.cell_command import *
from base.componet import *


path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_GPU_case\GPU_whisper_mode_rule15_log异常_OK'
    gpu_rule_15(parent_dir=parent_dir)
    pass