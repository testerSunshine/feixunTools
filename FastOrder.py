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
        self.WeiC = 23900
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
        # {"user": "15624288288", "pwd": "xwg888888"},
        # {"user": "18765580967", "pwd": "xwg88888"},
        # {"user": "13078526201", "pwd": "feixun666"},
        # {"user": "13078561905", "pwd": "feixun666"},
        # {"user": "13027868397", "pwd": "feixun666"},

        {"user": "13027807823", "pwd": "cy940407"},
        {"user": "13064018566", "pwd": "wj848888"},
        {"user": "13869179286", "pwd": "848888"},
        {"user": "13092446357", "pwd": "848888"},
        {"user": "15579435155", "pwd": "848888"},
    ]
    threadingPool = []
    for userInfo in account:
        u = fastOrderThread(userInfo,)
        threadingPool.append(u)
    for t in threadingPool:
        t.start()
