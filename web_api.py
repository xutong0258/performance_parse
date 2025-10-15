# coding=utf-8

import os
import sys
import json
import time
import warnings
import platform
import shutil
import datetime
import requests
from base.handle_request import *

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)
base_name = os.path.basename(path_dir)

# sys.path.append(path_dir)

# from common.rtsp import *
# 
# from common.contants import *
# from mylogger import *
# from component.ai_sport import *
# from component.mysql import Mysql
# from common.contants import *
# from util import *
# from component.wexin_sport import *

http = HandleRequest ()


WEB_IP = "http://192.168.2.202"
# 登录的参数
login_data = {"loginName": "15168284827", "password": "Rio4827"}
# 登录的请求头
header = {
    "Content-Type": "application/json"
}

def hello():
    logger.info(f'Enter hello')
    url = f"{WEB_IP}/scp-data/openApi/receive/uploadZIP"
    url = f"{WEB_IP}/mbxApi/utp/queryReportdList? current=1&size=10"

    try:
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

def del_test():
    headers = {
        "appId": "71bc83db980d4400aa6a7841216e7991",
        "sign": "b6e0e80b3be8347641b7af518e3c4ac3",
        "fileMD5": "cb2047f9c7300a06e60d4c27066d712975f6b78ee0b063babd7099d891ecbe55",
        "timestamp": "delete",
        'schoolId': '8098',
    }
    file_path = r'D:\11\71bc83db980d4400aa6a7841216e7991_delete.zip'

    uploadZIP(headers, file_path)
    return
if __name__ == '__main__':
    hello()
    # del_test()
    # change_file_format()
    # disable_project()
    pass