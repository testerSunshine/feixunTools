from GoodsDetail import goodsDetail
from urlConf import urls


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
            print("账号: {}已登录".format(session.userInfo.get("user", "")))
            session.loginData = loginRsp.get("data", "")
            goodsDetail(session)
            break
        else:
            print(loginRsp.get("error", ""))
