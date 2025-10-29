# coding=utf-8

import os
import sys
import json
import time
import warnings
import platform
import shutil
import datetime
from base.handle_request import *
import time
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)
base_name = os.path.basename(path_dir)


http = HandleRequest ()


WEB_IP = "http://10.159.252.128:9298"
# 登录的参数
login_data = {"loginName": "15168284827", "password": "Rio4827"}
# 登录的请求头
header = {
    "Content-Type": "application/json"
}

def generate_token(username: str) -> str:
    """
    生成 token：username@13位时间戳，AES-192-ECB 加密，Base64 编码
    """
    # 1. 构造明文：username@13位时间戳（毫秒）
    timestamp = int(time.time() * 1000)  # 13位时间戳
    plaintext = f"{username}@{timestamp}"

    # 2. 密钥（24字节，用于AES-192）
    key = "sgEsmU8FdP8W7j5H03695286".encode('utf-8')  # 24 bytes

    # 3. 确保密钥长度正确（AES-192 需要 24 字节）
    if len(key) != 24:
        raise ValueError("密钥长度必须为24字节（AES-192）")

    # 4. 使用 AES-192-ECB 加密
    cipher = AES.new(key, AES.MODE_ECB)

    # 5. 对明文进行 PKCS7 填充，并加密
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_data)

    # 6. Base64 编码为字符串
    token = base64.b64encode(encrypted_bytes).decode('utf-8')

    return token

def hello():
    logger.info(f'Enter hello')
    url = f"{WEB_IP}/mbxApi/utp/queryReportdList? current=1&size=10"

    username = "alice"
    token = generate_token(username)
    print("Generated token:", token)

    header = {
        "token": f'{token}'
    }

    try:
        # response = http.send(url=url, method="post", headers=header, json=login_data)
        response = http.send(url=url, method="post", headers=header, json=login_data)
        # 检查响应状态码
        if response.status_code == 200:
            logger.info('文件上传成功')
            logger.info(f'响应内容:{response.text}')
        else:
            logger.info(f'文件上传失败，状态码:{ response.status_code}')
            logger.info(f'响应内容:{response.text}')
    except Exception as e:
        logger.info(f'发生未知错误: {e}')
    return

def uploadZIP(headers, file_path):
    logger.info("第一步：老师登录AI智能操场平台")

    url = f"{WEB_IP}/scp-data/openApi/receive/uploadZIP"
    try:
        # 打开文件并作为二进制数据读取
        with open(file_path, 'rb') as file:
            # 构建文件参数，参数名 'file' 需依据接口文档确定
            files = {'file': file}
            response = http.send(url=url, method="post", headers=headers, json=LOGIN_DATA, files=files)
        # 检查响应状态码
        if response.status_code == 200:
            logger.info('文件上传成功')
            logger.info(f'响应内容:{response.text}')
        else:
            logger.info(f'文件上传失败，状态码:{ response.status_code}')
            logger.info(f'响应内容:{response.text}')

    except FileNotFoundError:
        logger.info('错误: 文件未找到，请检查文件路径。')
    except Exception as e:
        logger.info(f'发生未知错误: {e}')
    return

def creat_test():
    headers = {
        "appId": "71bc83db980d4400aa6a7841216e7991",
        "sign": "b6e0e80b3be8347641b7af518e3c4ac3",
        "fileMD5": "cb2047f9c7300a06e60d4c27066d712975f6b78ee0b063babd7099d891ecbe55",
        "timestamp": "create",
        'schoolId': '8098',
    }
    file_path = r'D:\11\71bc83db980d4400aa6a7841216e7991_create.zip'

    uploadZIP(headers, file_path)
    return

if __name__ == '__main__':
    hello()
    # del_test()
    # change_file_format()
    # disable_project()
    pass