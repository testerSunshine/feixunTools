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
        self.pid = 5
        self.WeiC = 0
        self.checkVCodeTime = "11:40:00"
        self.isFastSnap = False  # 抢购时间点踩点打码，如果是测试，设置为False

    def run(self):
        """
        执行下单脚本
        :return:
        """
        login(self)


if __name__ == '__main__':
    account = [
        # {"user": "18329363861", "pwd": "18329363861"},
        # {"user": "18019735400", "pwd": "a478478"},
        # {"user": "15216609313", "pwd": "a478478"},
        # {"user": "17721369494", "pwd": "a478478"},
        {"user": "15624288288", "pwd": "xwg888888"},
        # {"user": "13184689616", "pwd": "qaz123"},
        # {"user": "13170858598", "pwd": "qaz123"},
    ]
    threadingPool = []
    for userInfo in account:
        u = fastOrderThread(userInfo,)
        threadingPool.append(u)
    for t in threadingPool:
        t.start()
