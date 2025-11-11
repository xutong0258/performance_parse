import json
from base import common
from base.helper import *
from base.cell_command import *
from base.amd_cell_command import *
from base.fileOP import *


def intel_check_run(parent_dir,fail_dir=None, pass_dir=None):
    rule_count = 18
    check_result_list = []
    for idx in range(1, rule_count):
        function_name = f'check_rule_{idx}'
        return_dict = eval(function_name)(parent_dir, fail_dir, pass_dir)
        if return_dict:
            check_result_list.append(return_dict)
            pass
            # break
    # dir_name = './'
    result_yaml_file = 'result.yaml'
    result_dir = None
    if parent_dir is not None:
        result_dir = parent_dir
    else:
        result_dir = fail_dir
    result_yaml_file = os.path.join(result_dir, result_yaml_file)

    dump_file(result_yaml_file, check_result_list)
    logger.info(f'check_result_list:{check_result_list}')
    return

def gpu_check_run(parent_dir,fail_dir=None, pass_dir=None):
    rule_count = 17
    check_result_list = []
    for idx in range(1, rule_count):
        function_name = f'gpu_rule_{idx}'
        return_dict = eval(function_name)(parent_dir, fail_dir, pass_dir)
        if return_dict:
            check_result_list.append(return_dict)
            pass
            # break
    dir_name = './'
    result_yaml_file = 'result.yaml'
    result_yaml_file = os.path.join(parent_dir, result_yaml_file)
    dump_file(result_yaml_file, check_result_list)
    logger.info(f'check_result_list:{check_result_list}')
    return

def amd_check_run(parent_dir,fail_dir=None, pass_dir=None):
    rule_count = 16
    check_result_list = []
    for idx in range(1, rule_count):
        function_name = f'amd_check_rule_{idx}'
        return_dict = eval(function_name)(parent_dir, fail_dir, pass_dir)
        if return_dict:
            check_result_list.append(return_dict)
            pass
            # break
    dir_name = './'
    result_yaml_file = 'result.yaml'
    result_yaml_file = os.path.join(parent_dir, result_yaml_file)
    dump_file(result_yaml_file, check_result_list)
    logger.info(f'check_result_list:{check_result_list}')
    return

def one_process_run(parent_dir=None, fail_dir=None, pass_dir=None):
    if parent_dir is not None:
        fail_dir = os.path.join(parent_dir, 'fail')
        pass_dir = os.path.join(parent_dir, 'pass')

    case_type = get_log_case(fail_dir)
    logger.info(f'case_type:{case_type}')
    if Intel_Case in case_type :
        intel_check_run(parent_dir,fail_dir, pass_dir)

    if GPU_Case in case_type:
        gpu_check_run(parent_dir, fail_dir, pass_dir)

    if AMD_Case in case_type:
        amd_check_run(parent_dir, fail_dir, pass_dir)
    return

def one_process_run_tmp(parent_dir=None, fail_dir=None, pass_dir=None):
    intel_check_run(fail_dir, pass_dir)
    # gpu_check_run(fail_dir, pass_dir)
    return