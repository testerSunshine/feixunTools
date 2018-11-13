import re
import time

from emailConf import sendEmail
from urlConf import urls
import Utils as U


def searchOrderInfo(session):
    """
    查询账号订单状态, 查询间隔十秒
    :param session:
    :return:
    """
    U.Logging.info("账号：{} 查询线程开始启动...".format(session.userInfo.get("user", "")))
    while not session.orderDone:
        searchOrderInfoRsp = session.httpClint.send(urls.get("myOrder", ""))
        if searchOrderInfoRsp:
            if searchOrderInfoRsp.find("您还没有相关订单哦") != -1:
                time.sleep(5)
            elif searchOrderInfoRsp.find("订单号：") != -1:
                orderRe = re.compile(r'order:\[{"order_id":"(\S+)","uid":')
                orderId = re.search(orderRe, searchOrderInfoRsp).group(1)
                U.Logging.info("账号: {} 查询到待付款订单，订单号: {}".format(session.userInfo.get("user", ""), orderId,))
                sendEmail(orderId, session.userInfo.get("user", ""), session.email)
                session.orderDone = True
            else:
                U.Logging.error("账号：{}订单查询失败".format(session.userInfo.get("user", "")))


if __name__ == '__main__':
    pass