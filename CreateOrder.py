import json
import re
import time
from json import JSONDecodeError

from urlConf import urls


def createOrder(session, cartMd5, token, addrId):
    """
    下单
    :return:
    """
    print("检测到有库存，阻塞下单，等待验证码中")
    while not session.VCode:  # 等待验证码识别成功
        time.sleep(0.01)
    print("账号:{} 验证码提交通过，下单中".format(session.userInfo.get("user", "")))
    createOrderUrls = urls.get("orderCreate", "")
    data = {
        "cart_md5":	"610cc344dad3a12bf2983af9933ee6bf",
        "addr_id":	addrId,
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
        "token": "138bd4305122c1cc9fda3a60a07aeff1",
    }
    createOrderRsp = session.httpClint.send(createOrderUrls, data)
    if createOrderRsp and createOrderRsp.get("success", "") == "订单提交成功":
        print("账号: {} {}".format(session.userInfo.get("user", ""), createOrderRsp.get("success", "")))
        session.orderDone = True
    elif createOrderRsp.get("error") == "验证码错误":
        session.VCode = ""


def joinCreateOrder(session):
    """
    进入下单页
    :return:
    """
    print("账号: {} cookie 已种植，正在下单".format(session.userInfo.get("user", "")))
    while not session.orderDone:
        joinCreateOrderUrls = urls.get("checkOrderFast", "")
        joinCreateOrderRsp = session.httpClint.send(joinCreateOrderUrls)
        cartMd5Re = re.compile(r'cart_md5:"(\S+)"')
        tokenRe = re.compile(r"'token':'(\S+)'")
        addrIdRe = re.compile(r'{"addr_id":"(\S+)"')
        try:
            cartMd5 = re.search(cartMd5Re, joinCreateOrderRsp).group(1)
            token = re.search(tokenRe, joinCreateOrderRsp).group(1)
            addrId = re.search(addrIdRe, joinCreateOrderRsp).group(1)
            print()
            createOrder(session, cartMd5, token, addrId)
        except (TypeError, AttributeError):
            try:
                jsonJoinCreateOrderRsp = json.loads(joinCreateOrderRsp)
                print(jsonJoinCreateOrderRsp.get("error"))
            except (JSONDecodeError, TypeError):
                print(joinCreateOrderRsp)


if __name__ == '__main__':
    print(joinCreateOrder(session=""))
