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
        self.VCode = ""
        self.pid = 14
        self.WeiC = 23900
        self.checkVCodeTime = "10:59:30"
        self.isFastSnap = True  # 抢购时间点踩点打码，如果是测试，设置为False

    def run(self):
        """
        执行下单脚本
        :return:
        """
        login(self)


if __name__ == '__main__':
    account = [
        {"user": "18329363861", "pwd": "18329363861"},
        {"user": "18019735400", "pwd": "a478478"},
        # {"user": "15216609313", "pwd": "a478478"},
        # {"user": "17721369494", "pwd": "a478478"},
    ]
    threadingPool = []
    for userInfo in account:
        u = fastOrderThread(userInfo,)
        threadingPool.append(u)
    for t in threadingPool:
        t.start()
