import copy

from CreateOrder import createOrder
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
    createOrder(session, )
