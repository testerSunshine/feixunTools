from urlConf import urls


def searchOrderInfo(session):
    """
    查询账号订单状态
    :param session:
    :return:
    """
    searchOrderInfoRsp = session.httpClint.send(urls.get("myOrder", ""))
    if searchOrderInfoRsp:
        print(searchOrderInfoRsp)

