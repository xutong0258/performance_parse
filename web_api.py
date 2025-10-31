import requests
import json
import time
from datetime import datetime
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import binascii

# 固定 DES 密钥（Java 中会自动截断到 8 字节）
KEY = b"sgEsmU8F"  # 注意：原始字符串前 8 字节

def des_encrypt_ecb(plaintext: str) -> str:
    """
    DES ECB 模式加密，PKCS#5 填充，输出 hex 小写字符串
    :param plaintext: 明文字符串
    :return: 十六进制表示的密文
    """
    cipher = DES.new(KEY, DES.MODE_ECB)
    plaintext_bytes = plaintext.encode('utf-8')
    padded_text = pad(plaintext_bytes, DES.block_size)
    encrypted = cipher.encrypt(padded_text)
    return binascii.hexlify(encrypted).decode('utf-8')

# 动态生成 token
def generate_token():
    timestamp = int(time.time() * 1000)  # 当前毫秒时间戳
    plaintext = f"xinghuan@{timestamp}"
    return des_encrypt_ecb(plaintext)

# 请求 URL（包含查询参数）
url = "http://10.159.252.128:9298/utp/queryReportList"
url = "http://10.159.252.128:9298/utp/queryReportList?current=1&size=10"

params = {
    "current": 1,
    "size": 10
}

# 动态生成 token
dynamic_token = generate_token()

# 请求头（使用动态 token）
headers = {
    'token': f'{dynamic_token}',
    "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Host": "10.159.252.128:9298",
    "Connection": "keep-alive"
}

# 请求体（JSON 数据）
payload = {
    "status": ["Passed", "Failed"],
    "queryLikeKey": "sn",
    "queryLikeValue": "PF57GMRV",
    "hasErrorHistory": False,
    "project": ["X1FLEX9_MTL"],
    "model": ["KXCE0"],
    "phase": ["FVT"],
    "ac": "true",
    "hasOnLine": False,
    "startTime": "2025-10-31 08:54:03",
    "endTime": "2025-11-22 08:54:03"
}

def test_api():
    # 发送 POST 请求
    login_data = {"loginName": "xinghuan", "password": "xinghuan@29"}

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
        json=login_data,
    )
    # 输出响应
    print("Status Code:", response.status_code)
    print("Used Token:", dynamic_token)
    print("Response Body:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print("Non-JSON response or error:", response.text)
if __name__ == '__main__':
    test_api()