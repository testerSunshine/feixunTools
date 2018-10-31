import random
import threading

from HttpUtils import HttpClient
from Login import login


class fastOrderThread(threading.Thread):
    def __init__(self, userInfo,):
        threading.Thread.__init__(self)
        print("线程{} 正在执行，登录账号为：{}".format(userInfo["user"], userInfo["user"]))
        self.userInfo = userInfo
        self.httpClint = HttpClient()
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
        {"user": "18019735400", "pwd": "a478478"},
        {"user": "15205349005", "pwd": "xwg88888"},
        {"user": "15323504956", "pwd": "848888"},
        {"user": "17329929404", "pwd": "848888"},
        {"user": "17753118752", "pwd": "848888"},
        {"user": "13092446357", "pwd": "848888"},
        {"user": "13287700977", "pwd": "wj848888"},
    ]
    threadingPool = []
    for userInfo in account:
        u = fastOrderThread(userInfo,)
        threadingPool.append(u)
    for t in threadingPool:
        t.start()
