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
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from base.des_api import *
from base.fileOP import *

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)
base_name = os.path.basename(path_dir)


# http = HandleRequest ()


WEB_IP = "http://10.159.252.128:9298"
# 登录的参数
login_data = {"loginName": "xinghuan", "password": "xinghuan@29"}
# 登录的请求头
header = {
    "Content-Type": "application/json"
}


def hello():
    username = "xinghuan"
    # 登录的参数
    login_data = {"loginName": "xinghuan", "password": "xinghuan@29"}

    timestamp = int(time.time() * 1000)  # 毫秒时间戳
    plaintext = f"{username}@{timestamp}"
    encrypted = des_encrypt_ecb(plaintext)
    logger.info(encrypted)

    WEB_IP = "http://10.159.252.128:9298"

    # url = f"{WEB_IP}/mbxApi/utp/queryReportdList? current=1&size=10"
    url = f"{WEB_IP}/utp/queryReportList?current=1&size=10"
    header = {
        "token": f'{encrypted}',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': '10.159.252.128:9298',
        'Connection': 'keep-alive',
    }
    file = 'hello.json'
    data = read_file_dict(file)
    try:
        # response = http.send(url=url, method="post", headers=header, json=login_data)
        # response = http.send(url=url, method="post", headers=header, json=login_data, data=data)
        pre_cmd = r'curl --location --request POST '
        header_str = f' --header \'token: {encrypted}\' '
        header_str = header_str + f' --header \'User-Agent: Apifox/1.0.0 (https://apifox.com)\''
        header_str = header_str + f' --header \'Content-Type: application/json\''
        header_str = header_str + f' --header \'Accept: */*\''
        header_str = header_str + f' --header \'Host: 10.159.252.128:9298\''
        header_str = header_str + f' --header \'Connection: keep-alive\''

        step_cmd = pre_cmd + f'{url}' + header_str + ' --data-raw ' + f'\'{json.dumps(data)}\''

        logger.info(f'cmd:{step_cmd}')

        result, errors, return_code = cmd_excute(step_cmd)
        logger.info(f'result:{result}')
        logger.info(f'errors:{errors}')
        logger.info(f'return_code:{return_code}')

        # # 检查响应状态码
        # if response.status_code == 200:
        #     # logger.info('文件上传成功')
        #     logger.info(f'响应内容:{response.text}')
        # else:
        #     logger.info(f'文件上传失败，状态码:{ response.status_code}')
        #     logger.info(f'响应内容:{response.text}')
    except Exception as e:
        logger.info(f'发生未知错误: {e}')
    return

def api_test():
    username = "xinghuan"
    # 登录的参数
    login_data = {"loginName": "xinghuan", "password": "xinghuan@29"}

    timestamp = int(time.time() * 1000)  # 毫秒时间戳
    plaintext = f"{username}@{timestamp}"
    encrypted = des_encrypt_ecb(plaintext)
    logger.info(encrypted)

    WEB_IP = "http://10.159.252.128:9298"

    # url = f"{WEB_IP}/mbxApi/utp/queryReportdList? current=1&size=10"
    url = f"{WEB_IP}/utp/queryReportList?current=1&size=10"
    header = {
        "token": f'{encrypted}',
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': '10.159.252.128:9298',
        'Connection': 'keep-alive',
    }
    file = 'hello.json'
    data = read_file_dict(file)
    try:
        # response = http.send(url=url, method="post", headers=header, json=login_data)
        # response = http.send(url=url, method="post", headers=header, json=login_data, data=data)
        pre_cmd = r'curl --location --request POST '
        header_str = f' --header \'token: {encrypted}\' '
        header_str = header_str + f' --header \'User-Agent: Apifox/1.0.0 (https://apifox.com)\''
        header_str = header_str + f' --header \'Content-Type: application/json\''
        header_str = header_str + f' --header \'Accept: */*\''
        header_str = header_str + f' --header \'Host: 10.159.252.128:9298\''
        header_str = header_str + f' --header \'Connection: keep-alive\''

        step_cmd = pre_cmd + f'{url}' + header_str + ' --data-raw ' + f'\'{json.dumps(data)}\''

        logger.info(f'cmd:{step_cmd}')

        result, errors, return_code = cmd_excute(step_cmd)
        logger.info(f'result:{result}')
        logger.info(f'errors:{errors}')
        logger.info(f'return_code:{return_code}')

        # # 检查响应状态码
        # if response.status_code == 200:
        #     # logger.info('文件上传成功')
        #     logger.info(f'响应内容:{response.text}')
        # else:
        #     logger.info(f'文件上传失败，状态码:{ response.status_code}')
        #     logger.info(f'响应内容:{response.text}')
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