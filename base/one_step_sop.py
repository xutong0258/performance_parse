import json
from base import common
from base.helper import *
from base.cell_command import *


def one_process_run(fail_dir, pass_dir):
    rule_count = 10
    for idx in range(rule_count):
        function_name = f'check_rule_{idx+1}'
        return_dict = eval(function_name)(fail_dir, pass_dir)
        if return_dict:
            pass
            # break
    return