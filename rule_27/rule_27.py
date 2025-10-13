import os

from base.cell_command import *
from base.componet import *
from base.read_csv_with_pandas import *

path_dir = os.path.dirname(__file__)

if __name__ == '__main__':
    log_dir = r'D:\小拉\0_peformance\几种抓到的log类型'

    check_rule_27(log_dir)
    pass