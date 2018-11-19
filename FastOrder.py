import argparse
import sys
import threading

from HttpUtils import HttpClient
from Login import login
import Utils as U


class fastOrderThread(threading.Thread):
    def __init__(self, userInfo, email, FastSnap, pid, WeiC, FastType):
        threading.Thread.__init__(self)
        U.Logging.info("线程{} 正在执行，登录账号为：{}".format(userInfo["user"], userInfo["user"]))

        self.userInfo = userInfo
        self.httpClint = HttpClient()
        self.email = email
        self.addrId = ""
        self.VCode = ""
        self.loginData = {}
        self.request_id = ""
        self.orderDone = False
        self.isStock = False
        self.pid = pid
        self.WeiC = WeiC
        self.orderType = 1
        self.checkVCodeTime = "10:59:55"
        self.isFastSnap = FastSnap  # 抢购时间点踩点打码，如果是测试，设置为False
        self.FastType = FastType  # 查单脚本，防止订单丢失

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
    parser.add_argument("--account", type=str, default="", required=True, help="账号，必填！")
    parser.add_argument("--FastType", type=int, default=0, required=True, help="0下单，1查单")
    parser.add_argument("--pwd", type=str, default="", required=True, help="密码，必填！")
    parser.add_argument("--email", type=str, default="931128603@qq.com", help="邮件通知人,多人用英文逗号隔开")
    parser.add_argument("--FastSnap", type=int, default=0, help="是否开启踩点打码, 0关闭，1开启")
    parser.add_argument("--pid", type=int, default=0, required=True, help="商品id")
    parser.add_argument("--WeiC", type=int, default=0, required=True, help="商品对打使用维C数量")
    return parser.parse_args(argv)


if __name__ == '__main__':
    args = parser_arguments(sys.argv[1:])
    account = args.account
    pwd = args.pwd
    email = args.email
    FastSnap = args.FastSnap
    FastType = args.FastType
    pid = args.pid
    WeiC = args.WeiC
    if account and pwd and pid:
        U.Logging.info(account)
        U.Logging.info(pwd)
        U.Logging.info(email)
        U.Logging.info(FastSnap)
        U.Logging.info(FastType)
        U.Logging.info(pid)
        U.Logging.info(WeiC)
        threadingPool = []
        accounts = account.split(",")
        pwds = pwd.split(",")
        for i in range(len(accounts)):
            userInfo = {"user": accounts[i], "pwd": pwds[i]}
            u = fastOrderThread(userInfo, email, FastSnap, pid, WeiC, FastType)
            threadingPool.append(u)
        for t in threadingPool:
            t.start()
    else:
        U.Logging.info("必填参数不能为空")