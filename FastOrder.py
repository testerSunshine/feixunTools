import threading

from HttpUtils import HttpClient
from Login import login
import Utils as U


class fastOrderThread(threading.Thread):
    def __init__(self, userInfo,):
        threading.Thread.__init__(self)
        U.Logging.info("线程{} 正在执行，登录账号为：{}".format(userInfo["user"], userInfo["user"]))
        self.userInfo = userInfo
        self.httpClint = HttpClient()
        self.loginData = {}
        self.request_id = ""
        self.orderDone = False
        self.pid = 13
        self.WeiC = 29900
        self.checkVCodeTime = "10:59:55"
        self.isFastSnap = True  # 抢购时间点踩点打码，如果是测试，设置为False

    def run(self):
        """
        执行下单脚本
        :return:
        """
        login(self)


if __name__ == '__main__':
    account = [
        {"user": "18983788725", "pwd": "880418"},
        {"user": "15330501819", "pwd": "880418"},
        {"user": "17783082325", "pwd": "880418"},
        {"user": "17783082725", "pwd": "880418"},
        {"user": "18723129757", "pwd": "880418"},
    ]
    threadingPool = []
    for userInfo in account:
        u = fastOrderThread(userInfo,)
        threadingPool.append(u)
    for t in threadingPool:
        t.start()
