import os
from base import common
from base.one_step_sop import *
from base.fileOP import *

path_dir = os.path.dirname(__file__)

# file = r'D:\input_p.yaml'
# src_dir_list = get_file_content_list(file)
# logger.info(f'src_dir_list: {src_dir_list}')

def list_subfolders():
    root_path = r'D:\0_intelcpu_case_1024'
    list_folders = os.listdir(root_path)
    full_list = []
    for folder in list_folders:
        path = os.path.join(root_path, folder)
        full_list.append(path)
    dump_file('hello.yaml',full_list)
    return full_list

if __name__ == '__main__':
    parent_dir = r'D:\0_intelcpu_case_1024\cpu Sample_rule1\fail'

    intel_check_run(parent_dir=None, fail_dir=parent_dir, pass_dir=None)
    #
    # fail_dir = r'D:\0_intelcpu_case_1022\cpu Sample_rule1\fail'
    # intel_check_run(parent_dir=None, fail_dir=fail_dir, pass_dir=None)
    # src_dir_list = list_subfolders()
    # for src_dir in src_dir_list:
    #     src_dir = src_dir.strip()
    #     if src_dir == '' or 'bak' in src_dir:
    #         continue
    #     intel_check_run(parent_dir=src_dir)
    pass