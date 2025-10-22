import json
from base import common
from base.helper import *
from base.cell_command import *
from base.amd_cell_command import *
from base.fileOP import *


def intel_check_run(fail_dir, pass_dir):
    rule_count = 18
    check_result_list = []
    for idx in range(1, rule_count):
        function_name = f'check_rule_{idx}'
        return_dict = eval(function_name)(fail_dir, pass_dir)
        if return_dict:
            check_result_list.append(return_dict)
            pass
            # break
    dir_name = './'
    result_yaml_file = 'result.yaml'
    result_yaml_file = os.path.join(dir_name, result_yaml_file)
    dump_file(result_yaml_file, check_result_list)
    return

def gpu_check_run(fail_dir, pass_dir):
    rule_count = 33
    for idx in range(18, rule_count):
        function_name = f'check_rule_{idx}'
        return_dict = eval(function_name)(fail_dir, pass_dir)
        if return_dict:
            pass
            # break
    return

def amd_check_run(fail_dir, pass_dir):
    rule_count = 2
    for idx in range(1, rule_count):
        function_name = f'amd_check_rule_{idx}'
        return_dict = eval(function_name)(fail_dir, pass_dir)
        if return_dict:
            pass
            # break
    return

def one_process_run(fail_dir, pass_dir):
    case_type = get_log_case(fail_dir)
    if case_type == Intel_Case:
        intel_check_run(fail_dir, pass_dir)

    if case_type == GPU_Case:
        gpu_check_run(fail_dir, pass_dir)

    if case_type == AMD_Case:
        amd_check_run(fail_dir, pass_dir)
    return

def one_process_run_tmp(fail_dir, pass_dir):
    intel_check_run(fail_dir, pass_dir)
    # gpu_check_run(fail_dir, pass_dir)
    return