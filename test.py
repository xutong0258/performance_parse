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