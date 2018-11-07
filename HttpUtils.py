import json
import os
import random
import re
import socket
from collections import OrderedDict
from time import sleep

import execjs
import requests
from requests_toolbelt import MultipartEncoder
import Utils as U

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


def _set_header_default():
    header_dict = OrderedDict()
    header_dict["Accept"] = "*/*"
    header_dict["Accept-Encoding"] = "gzip, deflate"
    header_dict[
        "User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Mobile/15D100 VMCHybirdAPP-iOS/2.2.4/"
    header_dict["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    header_dict["Referer"] = "https://mall.phicomm.com/m/item-5.html"
    header_dict["X-Requested-With"] = "XMLHttpRequest"
    header_dict["Connection"] = "keep-alive"
    return header_dict


class HttpClient(object):

    def __init__(self):
        """
        :param method:
        :param headers: Must be a dict. Such as headers={'Content_Type':'text/html'}
        """
        self.initS()
        self._cdn = ["113.107.238.206", "117.21.219.111", "117.21.219.76", "117.21.219.99", "117.21.219.73",
                     "113.107.238.133", "122.228.238.92", "58.58.81.142", "112.90.216.63", "113.107.238.193",
                     "106.42.25.225", "117.21.219.112", "112.90.216.104", "1.31.128.230", "1.31.128.140",
                     "111.202.98.6", "1.31.128.153", "111.13.147.233", "111.47.226.25", "1.31.128.216", "1.31.128.231",
                     "113.207.76.18",
                     "1.31.128.213", "1.31.128.139", "183.222.96.250", "1.31.128.217", "111.13.147.234",
                     "112.90.216.82", "111.47.226.161", "183.222.96.234", "1.31.128.245", "1.31.128.203",
                     "111.13.147.215"]

    def initS(self):
        self._s = requests.Session()
        self._s.headers.update(_set_header_default())
        return self

    def set_cookies(self, **kwargs):
        """
        设置cookies
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            self._s.cookies.set(k, v)

    def del_cookies(self):
        """
        删除所有的key
        :return:
        """
        self._s.cookies.clear()

    def del_cookies_by_key(self, key):
        """
        删除指定key的session
        :return:
        """
        self._s.cookies.set(key, None)

    def setHeaders(self, headers):
        self._s.headers.update(headers)
        return self

    def resetHeaders(self):
        self._s.headers.clear()
        self._s.headers.update(_set_header_default())

    def getHeadersHost(self):
        return self._s.headers["Host"]

    def setHeadersHost(self, host):
        self._s.headers.update({"Host": host})
        return self

    def getHeadersReferer(self):
        return self._s.headers["Referer"]

    def setHeadersReferer(self, referer):
        self._s.headers.update({"Referer": referer})
        return self

    @property
    def cdn(self):
        return self._cdn

    @cdn.setter
    def cdn(self, cdn):
        self._cdn = cdn

    def send(self, urls, data=None, **kwargs):
        """send request to url.If response 200,return response, else return None."""
        allow_redirects = False
        is_logger = urls["is_logger"]
        error_data = {"code": 99999, "message": "重试次数达到上限", }
        if "Referer" in urls:
            self.setHeadersReferer(urls["Referer"])
        if data:
            method = "post"
            # self.setHeaders({"Content-Length": "{0}".format(len(data))})
        else:
            method = "get"
            self.resetHeaders()
        if "is_multipart_data" in urls and urls["is_multipart_data"]:
            data = MultipartEncoder(data)
            self.setHeaders({"Content-Type": data.content_type})
            self.setHeaders(urls.get("headers", {}))
        if is_logger:
            U.Logging.info(
                "url: {0}\n入参: {1}\n请求方式: {2}\n".format(urls["req_url"], data, method, ))
        self.setHeadersHost(urls["Host"])
        for i in range(urls["re_try"]):
            try:
                sleep(urls.get("s_time", 0.001))
                requests.packages.urllib3.disable_warnings()
                response = self._s.request(method=method,
                                           timeout=20,
                                           url="https://" + self._cdn[random.randint(0, len(self._cdn) - 1)] + urls[
                                               "req_url"],
                                           data=data,
                                           allow_redirects=allow_redirects,
                                           verify=False,
                                           **kwargs)
                if response.status_code == 521:
                    txt_521 = ''.join(re.findall('<script>(.*?)</script>', response.content.decode()))
                    func_return = txt_521.replace('eval', 'return')
                    content = execjs.compile(func_return)
                    evaled_func = content.call('f').replace("document.cookie=", "return ").split("{document.addEventListener")[0].split(";if((function(){try{return")[0]\
                        .replace("window", """[]["filter"]["constructor"]("return this")()""")\
                        .replace("setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\\'\\')',1500);", "")
                    evaled_func_re = re.findall('var (.*?)=function\(\)', evaled_func)
                    cookie_c = execjs.compile(evaled_func)
                    try:
                        cookie = cookie_c.call(evaled_func_re[0]).split(";")[0].split("=")
                        U.Logging.info("当前种植cookie为: {}".format(cookie))
                        self.set_cookies(**{cookie[0]: cookie[1]})
                    except:
                        pass
                if response.status_code == 200 or response.status_code == 201:
                    if response.content:
                        if is_logger:
                            U.Logging.info(
                                "出参：{0}".format(response.content.decode()))
                        if urls["is_json"]:
                            return json.loads(response.content.decode())
                        elif urls.get("not_decode", ""):
                            return response.content
                        else:
                            return response.content.decode()
                    else:
                        U.Logging.info(
                            "url: {} 返回参数为空".format(urls["req_url"]))
                        error_data["data"] = "url: {} 返回参数为空".format(urls["req_url"])
                        return error_data
                elif response.status_code == 403:
                    U.Logging.error("ip 被封, 等待2秒")
                    sleep(2)
                else:
                    sleep(urls["re_time"])
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
            except socket.error:
                pass
        error_data["data"] = "接口返回异常，系统繁忙"
        return error_data


if __name__ == '__main__':
    pass



