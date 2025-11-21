import json
from base import common
from base.helper import *
from base.cell_command import *
from base.amd_cell_command import *
from base.fileOP import *
from base.folder_file import *


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

    file_walk_delete_file(file_format='.csv')
    return


def one_process_run_auto_log(case_path_config_file):
    table_dict = read_file_dict(case_path_config_file)
    performance_dict = table_dict.get('02_performance')

    # intel_path_pass = performance_dict.get('Intel').get('PATH_PASS')
    # intel_path_fail = performance_dict.get('Intel').get('PATH_FAIL')
    # intel_check_run(parent_dir=None, fail_dir=intel_path_fail, pass_dir=intel_path_pass)

    # gpu_path_pass = performance_dict.get('GPU').get('PATH_PASS')
    # gpu_path_fail = performance_dict.get('GPU').get('PATH_FAIL')
    # gpu_check_run(parent_dir=None, fail_dir=gpu_path_fail, pass_dir=gpu_path_pass)
    #
    amd_path_pass = performance_dict.get('AMD').get('PATH_PASS')
    amd_path_fail = performance_dict.get('AMD').get('PATH_FAIL')
    amd_check_run(parent_dir=None, fail_dir=amd_path_fail, pass_dir=amd_path_pass)

    file_walk_delete_file(file_format='.csv')
    return