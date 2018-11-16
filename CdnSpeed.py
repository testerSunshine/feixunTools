import datetime

from HttpUtils import HttpClient
from urlConf import urls


cdn = ["113.107.238.206", "117.21.219.111", "117.21.219.76", "117.21.219.99", "117.21.219.73",
         "113.107.238.133", "122.228.238.92", "58.58.81.142", "112.90.216.63", "113.107.238.193",
         "106.42.25.225", "117.21.219.112", "112.90.216.104", "1.31.128.230", "1.31.128.140",
         "111.202.98.6", "1.31.128.153", "111.13.147.233", "111.47.226.25", "1.31.128.216",
         "1.31.128.231", "113.207.76.18", "1.31.128.213", "1.31.128.139", "183.222.96.250",
         "1.31.128.217", "111.13.147.234", "112.90.216.82", "111.47.226.161", "183.222.96.234",
         "1.31.128.245", "1.31.128.203", "111.13.147.215", "111.13.147.204", "112.90.216.81",
         "1.31.128.244", "1.31.128.202"
         ]


class cdnSpeed:
    def __init__(self):
        self.httpClint = HttpClient()
        self.httpClint._cdn = [cdn[0]]

    def speed(self):
        print("cdn测试开始")
        self.httpClint.send(urls.get("m", ""))
        for c in cdn:
            self.httpClint._cdn = [c]
            startTime = datetime.datetime.now()
            result = self.httpClint.send(urls.get("m", ""))
            if result.find("斐讯商城") != -1:
                print("测试cdn: {}，速度为: {}ms".format(c, (datetime.datetime.now() - startTime).microseconds / 1000))
            else:
                print("测试cdn: {} 有问题".format(c))


if __name__ == '__main__':
    cdnSpeed().speed()