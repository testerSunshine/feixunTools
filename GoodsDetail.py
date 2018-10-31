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

    goodsDetailRsp = session.httpClint.send(getGoodsDetailUrls)

    data = goodsDetailRsp.get("data", {})
    session.sku = data["product"]["bn"]
    product_id = data["product"]["product_id"]
    goodsProducts(session, product_id)


if __name__ == '__main__':
    httpClint = HttpClient()
    getGoodsDetailUrls = copy.copy(urls["getGoodsDetail"])
    getGoodsDetailUrls["req_url"] = getGoodsDetailUrls["req_url"].format(5)
    goodsDetailRsp = httpClint.send(getGoodsDetailUrls)
    print(goodsDetailRsp["data"]["product"])
