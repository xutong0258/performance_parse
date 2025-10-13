import ctypes
import sys
import os


def run_with_full_path():
    # 假设 AMDSystemDeck.exe 在特定位置，或者在 PATH 中
    amd_exe_path = "C:\\Path\\To\\AMDSystemDeck.exe"  # 替换为实际路径

    # 如果不确定路径，可以尝试在常见位置查找
    possible_paths = [
        "C:\\Program Files\\AMD\\AMDSystemDeck.exe",
        "C:\\Program Files (x86)\\AMD\\AMDSystemDeck.exe",
        "AMDSystemDeck.exe"  # 依赖 PATH
    ]

    # exe_path = None
    # for path in possible_paths:
    #     if os.path.exists(path):
    #         exe_path = path
    #         break
    #
    # if not exe_path:
    #     print("找不到 AMDSystemDeck.exe")
    #     return

    exe_path = r'AMDSystemDeck.exe'
    command = f'"{exe_path}" -unilog=PM -unilogallgroups -unilogperiod=1000 -unilogoutput=C:\\xxxx.csv'

    if ctypes.windll.shell32.IsUserAnAdmin():
        print(f'subprocess')
        # 直接执行
        import subprocess
        subprocess.run(command, shell=True)
    else:
        # 以管理员身份执行
        print(f'ShellExecuteW')
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", "cmd.exe", f'/c "{command}"', None, 1
        )


if __name__ == "__main__":
    run_with_full_path()