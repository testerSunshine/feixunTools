import copy
import time

from fateadm_api import TestFunc, fateadm_code
from ruokuai import RClient
from urlConf import urls


def getVcode(session):
    """
    获取验证码
    :return:
    """
    print("识别验证码线程启动...")
    if session.isFastSnap:
        while time.strftime('%H:%M:%S', time.localtime(time.time())) < session.checkVCodeTime:
            pass
        print("抢购时间点，开始自动打码")
    vcodeUrls = copy.copy(urls.get("vcode", ""))
    vcodeUrls["req_url"] = vcodeUrls["req_url"].format(session.loginData.get("member_id"))
    # R = RClient(931128603, "wen1995")
    while True:
        if session.orderDone:
            break
        print("正在下载验证码")
        VcodeRsp = session.httpClint.send(vcodeUrls)
        codeRsp = fateadm_code(VcodeRsp)
        # codeRsp = R.rk_create(VcodeRsp, 4030)
        if codeRsp:
            _VCode = codeRsp
            session.VCode = _VCode
            print("验证码识别成功，识别为: {}".format(_VCode))
        # for i in range(2):
        #     print("验证码第{}次识别".format(i+1))
        #     VcodeRsp = session.httpClint.send(vcodeUrls)
        #     codeRsp = R.rk_create(VcodeRsp, 4030)
        #     if codeRsp and codeRsp.get("Result", ""):
        #         _VCode = codeRsp.get("Result", "")
        #         checkVCodeStatus = checkVCode(session, _VCode)
        #         if checkVCodeStatus:
        #             print("验证码识别成功，识别为: {}".format(_VCode))
        #             session.VCode = _VCode
        #             break
        #         else:
        #             session.VCode = ""
        for _ in range(400):
            if session.VCode == "":   # 如果检测到验证码识别失败了，立即重新识别验证码
                break
            else:
                time.sleep(0.1)
        session.VCode = ""  # 设置验证码
        print("验证码识别有效期超过45秒，正在重新识别")


def checkVCode(session, vCode):
    """
    校验验证码
    :param session:
    :return:
    """
    checkVCodeUrls = urls.get("checkVcode", '')
    data = {
        "vcode": vCode,
        "member_id": session.loginData["member_id"]
    }
    checkVCodeRsp = session.httpClint.send(checkVCodeUrls, data)
    if checkVCodeRsp and checkVCodeRsp.get("result", "") == "success":
        return vCode


if __name__ == '__main__':
    pass