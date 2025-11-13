import subprocess

import platform

cpu_info = platform.processor()
print("CPU 型号:", cpu_info)

def get_cpu_model():
    try:
        result = subprocess.run(
            ["wmic", "cpu", "get", "name"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        output = result.stdout.strip()
        # 提取实际的 CPU 型号（跳过标题行 "Name"）
        lines = output.split('\n')
        for line in lines:
            if line.strip() and line.strip().lower() != "name":
                return line.strip()
    except Exception as e:
        return f"获取 CPU 型号失败: {e}"

cpu_model = get_cpu_model()
print("CPU 型号:", cpu_model)

import subprocess

def get_cpu_model_powershell():
    try:
        result = subprocess.run(
            ["powershell", "-Command", "Get-WmiObject Win32_Processor | Select-Object -ExpandProperty Name"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"获取失败: {e}"

cpu_model = get_cpu_model_powershell()
print("CPU 型号:", cpu_model)