import re

import Utils as U
from urlConf import urls


def receiver(session):
    """
    获取收货地址
    :param session:
    :return:
    """
    U.Logging.info("账号：{} 查询线程开始启动...".format(session.userInfo.get("user", "")))
    receiverRsp = session.httpClint.send(urls.get("receiver", ""))
    if receiverRsp:
        receiverRe = re.compile(r'lists:\[{"addr_id":"(\S+)","uid":')
        session.addrId = re.search(receiverRe, receiverRsp).group(1)
    else:
        U.Logging.info("查询收货地址失败")

