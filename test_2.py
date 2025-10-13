import ctypes
import sys
import os
from base.util import *

def run_as_admin(exe_path):
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",          # 关键：请求管理员权限
            exe_path,
            None,             # 参数（可为 None）
            None,             # 工作目录（可为 None）
            1                 # SW_SHOWNORMAL
        )
        print("已请求以管理员身份运行程序。")
    except Exception as e:
        print(f"启动失败: {e}")

# 使用示例
cmd = r'AMDSystemDeck.exe -unilog=PM -unilogallgroups -unilogperiod=1000 -unilogoutput=C:\xxxx.csv'
result, errors, return_code = cmd_excute(cmd)
logger.info (f'result:{result}, errors:{errors}, return_code:{return_code}')

