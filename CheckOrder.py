import copy

from CreateOrder import *
from urlConf import urls


def goodsProducts(session, product_id):
    """
    拉起订单
    :param session:
    :param product_id:
    :return:
    """
    checkOrderUrls = copy.copy(urls["goodsProducts"])
    checkOrderUrls["req_url"] = checkOrderUrls["req_url"].format(product_id)

    session.httpClint.send(checkOrderUrls)

    ajPriceProducts(session, product_id)


def ajPriceProducts(session, product_id):
    """
    拉起订单2
    :param session:
    :param product_id:
    :return:
    """
    ajPriceProductsUrls = copy.copy(urls["ajPriceProducts"])
    ajPriceProductsUrls["req_url"] = ajPriceProductsUrls["req_url"].format(product_id)

    session.httpClint.send(ajPriceProductsUrls)

    checkOrderUrls = copy.copy(urls["cartFastBuy"])

    checkOrderUrls["req_url"] = checkOrderUrls["req_url"].format(session.pid)
    session.httpClint.send(checkOrderUrls)
    if session.orderType is 0:  # 常规下单
        U.Logging.info("下单接口1")
        joinCreateOrder(session)
    else:
        U.Logging.info("下单接口2")
        addCart(session)


def addCart(session):
    """
    将商品加入购物车
    :param session:
    :return:
    """
    addCartUrls = copy.copy(urls["cartAdd"])
    addCartUrls["req_url"] = addCartUrls["req_url"].format(session.pid)
    addCartRsp = session.httpClint.send(addCartUrls)
    for _ in range(2):  # 防止没有加入购物车
        if addCartRsp.get("success", "") == "操作成功":
            break
    joinCreateOrder2(session)





