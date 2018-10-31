import re
import time

from urlConf import urls


def createOrder(session, ):
    """
    下单
    :return:
    """
    cartMd5, token, addrId = joinCreateOrder(session)
    print("阻塞下单，等待验证码中")
    while not session.VCode:  # 等待验证码识别成功
        time.sleep(0.01)
    print("验证码提交通过，下单中")
    createOrderUrls = urls.get("orderCreate", "")
    data = {
        "cart_md5":	cartMd5,
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
        "token": token,
    }
    createOrderRsp = session.httpClint.send(createOrderUrls, data)
    if createOrderRsp and createOrderRsp.get("success", "") == "订单提交成功":
        print(createOrderRsp.get("success", ""))
        session.orderDone = True
    elif createOrderRsp.get("error") == "验证码错误":
        session.VCode = ""


def joinCreateOrder(session):
    """
    进入下单页
    :return:
    """
    joinCreateOrderUrls = urls.get("checkOrderFast", "")
    joinCreateOrderRsp = session.httpClint.send(joinCreateOrderUrls)
    cartMd5Re = re.compile(r'cart_md5:"(\S+)"')
    tokenRe = re.compile(r"'token':'(\S+)'")
    addrIdRe = re.compile(r'{"addr_id":"(\S+)"')
    try:
        cartMd5 = re.search(cartMd5Re, joinCreateOrderRsp).group(1)
        token = re.search(tokenRe, joinCreateOrderRsp).group(1)
        addrId = re.search(addrIdRe, joinCreateOrderRsp).group(1)
        return cartMd5, token, addrId
    except (TypeError, AttributeError):
        print(joinCreateOrderRsp)
        return "", "", ""


if __name__ == '__main__':
    print(joinCreateOrder(session=""))
