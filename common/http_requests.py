"""
============================
author:MuSen
time:2019/6/12
E-mail:3247119728@qq.com
============================
"""
import requests


class HTTPRequest(object):
    """直接发请求不记录cookies信息的 """

    def request(self, method, url,data=None, headers=None):
        """GET   get"""
        # 发送请求的方法
        method = method.lower()
        if method == 'post':
            # 判断是否使用json来传参（适用于项目中接口参数有使用json传参的）
            return requests.post(url=url, data=data, headers=headers)
        elif method == 'get':
            return requests.get(url=url, params=data, headers=headers)


class HTTPSession(object):
    """使用session对象发送请求，自动记录cookies信息 """

    def __init__(self):
        # 创建一个session对象
        self.session = requests.session()

    def request(self, method, url,data=None, headers=None):
        # 判断请求的方法
        method = method.lower()
        if method == 'post':
            return self.session.post(url=url, data=data, headers=headers)
        elif method == 'get':
            return self.session.get(url=url, params=data, headers=headers)

    def close(self):
        self.session.close()
