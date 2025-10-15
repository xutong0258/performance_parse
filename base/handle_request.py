# coding=utf-8

import requests
from base.logger import *

file_path = os.path.abspath(__file__)
path_dir = os.path.dirname(file_path)
base_name = os.path.basename(path_dir)


class HandleRequest:
    def send(self, url, method, params=None, data=None, json=None, headers=None, log_print=False, files=None):
        # 将请求的方法转换为小写
        logger.info("请求的url: {}".format(url))
        logger.info("请求的headers: {}".format(headers))
        method = method.lower()
        if method == "post":
            logger.info("请求入参json：{}".format(json))
            http_res = requests.post(url=url, json=json, data=data, headers=headers, files=files)
        elif method == "put":
            http_res = requests.put(url=url, data=data, headers=headers)
        elif method == "get":
            logger.info("请求入参params：{}".format(params))
            http_res = requests.get(url=url, params=params, headers=headers)
        else:
            http_res = requests.request(method=method, url=url, params=params, headers=headers)
        logger.info("返回状态码：{}".format(http_res.status_code))
        if log_print:
            logger.info("返回数据：{}".format(http_res.json()))
        return http_res


if __name__ == '__main__':
    # 登录接口地址
    login_url = "http://192.168.2.202/api/login"

    # 登录的参数
    login_data = {"loginName": "15168284827", "password": "Rio4827"}
    # 登录的请求头
    header = {
        "Content-Type": "application/json"
    }

    http = HandleRequest()
    res = http.send(url=login_url, method="post", json=login_data, headers=header)

    print(res.json())
    print(res.json()['token'])
