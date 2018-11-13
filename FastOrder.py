import argparse
import sys
import threading

from HttpUtils import HttpClient
from Login import login
import Utils as U


class fastOrderThread(threading.Thread):
    def __init__(self, userInfo, email, FastSnap, pid, WeiC):
        threading.Thread.__init__(self)
        U.Logging.info("线程{} 正在执行，登录账号为：{}".format(userInfo["user"], userInfo["user"]))
        self.userInfo = userInfo
        self.httpClint = HttpClient()
        self.email = email
        self.loginData = {}
        self.request_id = ""
        self.orderDone = False
        self.pid = pid
        self.WeiC = WeiC
        self.checkVCodeTime = "10:59:55"
        self.isFastSnap = FastSnap  # 抢购时间点踩点打码，如果是测试，设置为False

    def run(self):
        """
        执行下单脚本
        :return:
        """
        login(self)


def parser_arguments(argv):
    """
    不应该在这里定义，先放在这里
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=str, default="", help="账号，必填！")
    parser.add_argument("--email", type=int, default="931128603@qq.com", help="邮件通知人,多人用英文逗号隔开")
    parser.add_argument("--FastSnap", type=bool, default=False, help="是否开启踩点打码")
    parser.add_argument("--pid", type=int, default=0, help="商品id")
    parser.add_argument("--WeiC", type=int, default=0, help="商品对打使用维C数量")
    return parser.parse_args(argv)


if __name__ == '__main__':
    args = parser_arguments(sys.argv[1:])
    account = args.account
    email = args.email
    FastSnap = args.FastSnap
    pid = args.pid
    WeiC = args.WeiC
    if account and email and pid and WeiC:
        U.Logging.info(account)
        U.Logging.info(email)
        U.Logging.info(FastSnap)
        U.Logging.info(pid)
        U.Logging.info(WeiC)
    # account = [
    #     {"user": "18983788725", "pwd": "880418"},
    #     {"user": "15330501819", "pwd": "880418"},
    #     {"user": "17783082325", "pwd": "880418"},
    #     {"user": "17783082725", "pwd": "880418"},
    #     {"user": "18723129757", "pwd": "880418"},
    # ]
        threadingPool = []
        for userInfo in eval(account):
            u = fastOrderThread(userInfo, email, FastSnap, pid, WeiC)
            threadingPool.append(u)
        for t in threadingPool:
            t.start()
