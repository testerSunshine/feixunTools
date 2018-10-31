# -*- coding: utf8 -*-
import json
import os
import socket
from collections import OrderedDict
from time import sleep
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
        self._cdn = "113.107.238.133"

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
        error_data = {"code": 99999, "message": "重试次数达到上限",}
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
            U.Logging.success(
                "url: {0}\n入参: {1}\n请求方式: {2}\n".format(urls["req_url"], data, method,))
        self.setHeadersHost(urls["Host"])
        for i in range(urls["re_try"]):
            try:
                sleep(urls.get("s_time", 0.001))
                requests.packages.urllib3.disable_warnings()
                response = self._s.request(method=method,
                                           timeout=20,
                                           url="https://" + self.cdn + urls["req_url"],
                                           data=data,
                                           allow_redirects=allow_redirects,
                                           verify=False,
                                           **kwargs)
                if response.status_code == 200 or response.status_code == 201:
                    if response.content:
                        if is_logger:
                            U.Logging.success(
                                "出参：{0}".format(response.content.decode()))
                        if urls["is_json"]:
                            return json.loads(response.content.decode())
                        elif urls.get("not_decode", ""):
                            return response.content
                        else:
                            return response.content.decode()
                    else:
                        U.Logging.success(
                            "url: {} 返回参数为空".format(urls["req_url"]))
                        error_data["data"] = "url: {} 返回参数为空".format(urls["req_url"])
                        return error_data
                elif response.status_code == 403:
                    U.Logging.success("ip 被封，{}".format(response.content))
                    sleep(4)
                else:
                    sleep(urls["re_time"])
            except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
                pass
            except socket.error:
                pass
        error_data["data"] = "接口返回异常，系统繁忙"
        return error_data
