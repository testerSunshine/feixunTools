from GoodsDetail import goodsDetail
from SearchOrderInfo import searchOrderInfo
from urlConf import urls
import Utils as U


def login(session):
    """
    登录 获取cookie 和 必要的member_id
    :return: {"member_lv_id":"1","experience":null,"order_num":1,"member_id":"6527184"}}
    """
    loginUrls = urls.get("login")
    data = {
        "uname": session.userInfo.get("user", ""),
        "password": session.userInfo.get("pwd", ""),
        "forward": "",
    }
    session.httpClint.send(urls.get("passportLogin"))
    while True:
        loginRsp = session.httpClint.send(loginUrls, data)
        if loginRsp and loginRsp.get("success", "") == "登录成功":
            U.Logging.info("账号: {}已登录".format(session.userInfo.get("user", "")))
            session.loginData = loginRsp.get("data", "")
            if session.FastType is 0:  # 下单
                goodsDetail(session)
                break
            elif session.FastType is 1:  # 查单
                searchOrderInfo(session)
                break
        else:
            U.Logging.error("账号: {} 错误信息: {}".format(session.userInfo.get("user", ""), loginRsp.get("error", "")))
