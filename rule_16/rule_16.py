import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    parent_dir = r'D:\0_intelcpu_case_1022\CPU_thermal_module_rule16'
    # parent_dir = r'D:\0_intelcpu_case_1022\cpu_TCC_rule16_ok'
    check_rule_16(parent_dir=parent_dir)
    pass