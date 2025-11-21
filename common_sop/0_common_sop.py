import os
import sys

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)

root_dir = os.path.join(path_dir, '../')
sys.path.append(root_dir)

from base import common
from base.one_step_sop import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    parent_dir = r'D:\0_intelcpu_case\cpu Sample_rule1'
    one_process_run(parent_dir=parent_dir)
    pass