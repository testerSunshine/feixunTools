import random
import threading

from HttpUtils import HttpClient
from Login import login


class fastOrderThread(threading.Thread):
    def __init__(self, userInfo,):
        threading.Thread.__init__(self)
        print("线程{} 正在执行，登录账号为：{}".format(userInfo["user"], userInfo["user"]))
        self.userInfo = userInfo
        self.cdn_list = ["113.107.238.206", "117.21.219.111", "117.21.219.76", "117.21.219.99", "117.21.219.73", "113.107.238.133", "122.228.238.92", "58.58.81.142", "112.90.216.63", "113.107.238.193", "106.42.25.225", "117.21.219.112", "112.90.216.104", "1.31.128.230", "1.31.128.140", "111.202.98.6", "1.31.128.153", "111.13.147.233", "111.47.226.25", "1.31.128.216", "1.31.128.231", "113.207.76.18",
                         "1.31.128.213", "1.31.128.139", "183.222.96.250", "1.31.128.217", "111.13.147.234", "112.90.216.82", "111.47.226.161", "183.222.96.234", "1.31.128.245", "1.31.128.203", "111.13.147.215"]
        self.httpClint = HttpClient()
        self.httpClint.cdn = self.cdn_list[random.randint(0, len(self.cdn_list)-1)]
        self.loginData = {}
        self.sku = ""
        self.orderDone = False
        self.stock = 0
        self.VCode = ""
        self.pid = 14
        self.WeiC = 0
        self.isFastSnap = False  # 抢购时间点踩点打码，如果是测试，设置为False

    def run(self):
        """
        执行下单脚本
        :return:
        """
        login(self)


if __name__ == '__main__':
    account = [
        # {"user": "13184689616", "pwd": "13184689616"},
        {"user": "13170858598", "pwd": "qaz123"},
        # {"user": "18019735400", "pwd": "a478478"},
        # {"user": "15205349005", "pwd": "xwg88888"},
        # {"user": "15323504956", "pwd": "848888"},
        # {"user": "17329929404", "pwd": "848888"},
        # {"user": "17753118752", "pwd": "848888"},
        # {"user": "13092446357", "pwd": "848888"},
        # {"user": "13287700977", "pwd": "wj848888"},
    ]
    threadingPool = []
    for userInfo in account:
        u = fastOrderThread(userInfo,)
        threadingPool.append(u)
    for t in threadingPool:
        t.start()
