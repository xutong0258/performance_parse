import os
from base import common
from base.one_step_sop import *
from base.contants import *

path_dir = os.path.dirname(__file__)


if __name__ == '__main__':
    case_path_config_file = 'case_path_config.yaml'
    case_path_config_file = os.path.join(CONFIG_PATH, case_path_config_file)

    one_process_run_auto_log(case_path_config_file)
    pass