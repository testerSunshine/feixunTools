import copy
import threading
import time
from CheckOrder import goodsProducts
from CheckVcode import getVcode
from HttpUtils import HttpClient
from urlConf import urls
import random


def goodsDetail(session,):
    """
    进入商详
    :param session:
    :return:
    """
    getGoodsDetailUrls = copy.copy(urls["getGoodsDetail"])
    getGoodsDetailUrls["req_url"] = getGoodsDetailUrls["req_url"].format(session.pid)
    t = threading.Thread(target=getVcode, args=(session,))
    t.setDaemon(True)
    t.start()
    req_num = 0
    while not session.orderDone:
        _cdn = session.cdn_list[random.randint(0, len(session.cdn_list)-1)]
        session.httpClint.cdn = _cdn
        print("当前请求的cdn为: {}".format(_cdn))
        if session.orderDone:
            break
        req_num += 1
        if req_num == 5:  # 设置请求频率，防止被403
            print("管控心跳频率")
            time.sleep(req_num)
            req_num = 0
        goodsDetailRsp = session.httpClint.send(getGoodsDetailUrls)
        if goodsDetailRsp and goodsDetailRsp.get("result") == "success":
            data = goodsDetailRsp.get("data", {})
            stock = data["stock"]
            if int(stock) > 0:
                print("商品: {}，当前库存为: {}, 尝试下单".format(data["name"], stock))
                session.sku = data["product"]["bn"]
                product_id = data["product"]["product_id"]
                goodsProducts(session, product_id)
            else:
                print("商品: {}，当前库存为: {}, 判定为无库存".format(data["name"], stock))
    print("验证码线程执行完成")


if __name__ == '__main__':
    httpClint = HttpClient()
    getGoodsDetailUrls = copy.copy(urls["getGoodsDetail"])
    getGoodsDetailUrls["req_url"] = getGoodsDetailUrls["req_url"].format(5)
    goodsDetailRsp = httpClint.send(getGoodsDetailUrls)
    print(goodsDetailRsp["data"]["product"])
