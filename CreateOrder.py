import datetime
import json
import re
import threading
import time
from json import JSONDecodeError
import Utils as U
from emailConf import sendEmail
from urlConf import urls


def createOrder(session, cartMd5, token):
    """
    下单
    :return:
    """
    session.isStock = True
    U.Logging.info("账号:{} 检测到有库存，阻塞下单，等待验证码中".format(session.userInfo.get("user", "")))
    while not session.VCode:  # 等待验证码识别成功
        time.sleep(0.01)
    U.Logging.info("账号:{} 验证码提交通过，下单中".format(session.userInfo.get("user", "")))
    data = {
        "cart_md5":	cartMd5,
        "addr_id":	session.addrId,
        "dlytype_id": 1,
        "payapp_id": "alipay",
        "need_invoice":	"true",
        "invoice_title": "",
        "invoice_type":	3,
        "memo": "",
        "vcode": session.VCode,
        "yougouma": "",
        "useVcNum": session.WeiC,
        "useDdwNum": 0,
        "token": token,
    }
    createOrderThread(data, session,)
    # createOrderThreadPool = []
    # for i in range(3):
    #     t = threading.Thread(target=createOrderThread, args=(data, session, i+1))
    #     t.setDaemon(True)
    #     createOrderThreadPool.append(t)
    # for t in createOrderThreadPool:
    #     t.start()


def createOrderThread(data, session):
    """
    提交订单线程
    :param data:
    :param session:
    :return:
    """
    U.Logging.info("订单线程{}启动..".format(session.userInfo.get("user", "")))
    orderCreateUrls = urls.get("orderCreate", "") if session.orderType is 0 else urls.get("orderCreate2", "")  # 如果是下单接口2，就要用对应2的下单接口
    createOrderRsp = session.httpClint.send(orderCreateUrls, data)
    if createOrderRsp and createOrderRsp.get("success", "") == "订单提交成功":
        U.Logging.info("账号: {} {}".format(session.userInfo.get("user", ""), createOrderRsp.get("success", "")))
        sendEmail("(接口返回成功，无订单号)", session.userInfo.get("user", ""), session.email)
        session.orderDone = True
    else:
        U.Logging.info("账号: {} {}".format(session.userInfo.get("user", ""), createOrderRsp))
    # elif createOrderRsp.get("error") == "验证码错误":
    #     U.Logging.info("验证码错误")
    #     createOrderT = threading.Thread(target=fateadmJustice, args=(session.request_id,))  # 打码错误调取退款接口
    #     createOrderT.setDaemon(True)
    #     createOrderT.start()
    #     session.VCode = ""


def joinCreateOrder(session):
    """
    进入下单页
    :return:
    """
    U.Logging.info("账号: {} cookie 已种植，正在下单".format(session.userInfo.get("user", "")))
    while not session.orderDone:
        joinCreateOrderUrls = urls.get("checkOrderFast", "")
        joinCreateOrderRsp = session.httpClint.send(joinCreateOrderUrls)
        cartMd5Re = re.compile(r'cart_md5:"(\S+)"')
        tokenRe = re.compile(r"'token':'(\S+)'")
        try:
            cartMd5 = re.search(cartMd5Re, joinCreateOrderRsp).group(1)
            token = re.search(tokenRe, joinCreateOrderRsp).group(1)
            session.httpClint.get_cookies()
            createOrder(session, cartMd5, token)
        except (TypeError, AttributeError):
            try:
                jsonJoinCreateOrderRsp = json.loads(joinCreateOrderRsp)
                U.Logging.info(jsonJoinCreateOrderRsp.get("error"))
            except (JSONDecodeError, TypeError):
                U.Logging.info(joinCreateOrderRsp)


def joinCreateOrder2(session):
    """
    进入下单页
    :return:
    """
    U.Logging.info("账号: {} cookie 已种植，正在下单".format(session.userInfo.get("user", "")))
    while not session.orderDone:
        joinCreateOrderUrls = urls.get("checkOrderFast2", "")
        joinCreateOrderRsp = session.httpClint.send(joinCreateOrderUrls)
        cartMd5Re = re.compile(r'cart_md5:"(\S+)"')
        tokenRe = re.compile(r"'token':'(\S+)'")
        try:
            cartMd5 = re.search(cartMd5Re, joinCreateOrderRsp).group(1)
            token = re.search(tokenRe, joinCreateOrderRsp).group(1)
            session.httpClint.get_cookies()
            createOrder(session, cartMd5, token)
        except (TypeError, AttributeError):
            try:
                jsonJoinCreateOrderRsp = json.loads(joinCreateOrderRsp)
                U.Logging.info(jsonJoinCreateOrderRsp.get("error", ""))
            except (JSONDecodeError, TypeError):
                U.Logging.info(joinCreateOrderRsp)


if __name__ == '__main__':
    pass