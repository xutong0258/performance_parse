import os
from base import common
from base.one_step_sop import *
from base.fileOP import *

path_dir = os.path.dirname(__file__)

file = r'D:\input_p.yaml'
src_dir_list = get_file_content_list(file)
logger.info(f'src_dir_list: {src_dir_list}')

if __name__ == '__main__':
    parent_dir = r'D:\0_intel+nv_case-1021\15_CPU_case-环温sensor'
    intel_check_run(parent_dir=parent_dir)

    # for src_dir in src_dir_list:
    #     src_dir = src_dir.strip()
    #     if src_dir == '':
    #         continue
    #     intel_check_run(parent_dir=src_dir)
    pass