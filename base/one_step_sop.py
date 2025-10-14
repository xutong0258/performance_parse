import json
from base import common
from base.helper import *
from base.cell_command import *

def intel_check_run(fail_dir, pass_dir):
    rule_count = 18
    for idx in range(1, rule_count):
        function_name = f'check_rule_{idx}'
        return_dict = eval(function_name)(fail_dir, pass_dir)
        if return_dict:
            pass
            # break
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

def one_process_run(fail_dir, pass_dir):
    case_type = get_log_case(fail_dir)
    if case_type == Intel_Case:
        intel_check_run(fail_dir, pass_dir)

    if case_type == GPU_Case:
        gpu_check_run(fail_dir, pass_dir)

    return