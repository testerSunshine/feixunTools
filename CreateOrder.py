import json
import re
import threading
import time
from json import JSONDecodeError
import Utils as U
from emailConf import sendEmail
from fateadm_api import fateadmJustice

from urlConf import urls


def createOrder(session, cartMd5, token, addrId):
    """
    下单
    :return:
    """
    U.Logging.info("检测到有库存，阻塞下单，等待验证码中")
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
    createOrderThreadPool = []
    for i in range(4):
        t = threading.Thread(target=createOrderThread, args=(data, session, i+1))
        t.setDaemon(True)
        createOrderThreadPool.append(t)
    for t in createOrderThreadPool:
        t.start()


def createOrderThread(data, session, ThreadId):
    """
    提交订单线程
    :param data:
    :param session:
    :return:
    """
    U.Logging.info("订单线程{}启动..".format(ThreadId))
    createOrderRsp = session.httpClint.send(urls.get("orderCreate", ""), data)
    if createOrderRsp and createOrderRsp.get("success", "") == "订单提交成功":
        U.Logging.info("账号: {} {}".format(session.userInfo.get("user", ""), createOrderRsp.get("success", "")))
        session.orderDone = True
        sendEmail("(接口返回成功，无订单号)", session.userInfo.get("user", ""), session.email)
    elif createOrderRsp.get("error") == "验证码错误":
        U.Logging.info("验证码错误")
        createOrderThread = threading.Thread(target=fateadmJustice, args=(session.request_id,))  # 打码错误调取退款接口
        createOrderThread.setDaemon(True)
        createOrderThread.start()
        session.VCode = ""


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
            createOrder(session, cartMd5, token, "")
        except (TypeError, AttributeError):
            try:
                jsonJoinCreateOrderRsp = json.loads(joinCreateOrderRsp)
                U.Logging.info(jsonJoinCreateOrderRsp.get("error"))
            except (JSONDecodeError, TypeError):
                U.Logging.info(joinCreateOrderRsp)


if __name__ == '__main__':
    a = '11111111111111111'
    addrIdRe = re.compile(r'{"addr_id":"(\S+)"')
    addrId = re.search(addrIdRe, a).group(1) or "11"
    print()