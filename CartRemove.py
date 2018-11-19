from urlConf import urls
import Utils as U


def cartRemove(session, goods_id):
    """
    删除购物车中所有商品
    :param session:
    :return:
    """
    data = {
        "ident[]": goods_id
    }
    cartRemoveRps = session.httpClint.send(urls.get("cartRemove" ""), data)
    if cartRemoveRps.get("result", "") == "success":
        goods_id = cartRemoveRps["data"]["objects"]["goods"][0]["obj_ident"]
        U.Logging.info("当前删除购物车商品id为: {}".format(goods_id))
        cartRemove(session, goods_id)
    elif cartRemoveRps.get("error", "") == "购物车为空":
        U.Logging.error("购物车信息返回: {}".format(cartRemoveRps))
