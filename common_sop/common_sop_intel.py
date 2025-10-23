import os
from base import common
from base.one_step_sop import *
from base.fileOP import *

path_dir = os.path.dirname(__file__)

file = r'D:\input_p.yaml'
src_dir_list = get_file_content_list(file)
logger.info(f'src_dir_list: {src_dir_list}')

if __name__ == '__main__':
    parent_dir = r'D:\0_intelcpu_case_1022\CPU-hwp_rule17'

    intel_check_run(parent_dir=parent_dir, fail_dir=None, pass_dir=None)

    # fail_dir = r'D:\0_intelcpu_case_1022\cpu Sample_rule1\fail'
    # intel_check_run(parent_dir=None, fail_dir=fail_dir, pass_dir=None)
    # for src_dir in src_dir_list:
    #     src_dir = src_dir.strip()
    #     if src_dir == '':
    #         continue
    #     intel_check_run(parent_dir=src_dir)
    pass