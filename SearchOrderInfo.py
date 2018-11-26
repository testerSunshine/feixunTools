import copy
import re
import time

from emailConf import sendEmail
from urlConf import urls
import Utils as U


def searchOrderInfo(session):
    """
    查询账号订单状态, 查询间隔十秒
    :param session:
    :return:
    """
    U.Logging.info("账号：{} 查询线程开始启动...".format(session.userInfo.get("user", "")))
    while not session.orderDone:
        searchOrderInfoRsp = session.httpClint.send(urls.get("myOrder", ""))
        if searchOrderInfoRsp:
            if searchOrderInfoRsp.find("您还没有相关订单哦") != -1:
                if session.FastType is 1:  # 如果是查订单的话，就只查一次
                    U.Logging.info("账号：{} 无待付款订单".format(session.userInfo.get("user", "")))
                    break
                else:
                    time.sleep(5)
            elif searchOrderInfoRsp.find("订单号：") != -1:
                orderRe = re.compile(r'order:\[{"order_id":"(\S+)","uid":')
                orderId = re.search(orderRe, searchOrderInfoRsp).group(1)
                orderDetail(session, orderId,)
            else:
                U.Logging.error("账号：{}订单查询失败".format(session.userInfo.get("user", "")))


def orderDetail(session, orderID):
    """
    检查支付状态
    :param session:
    :param orderID:
    :return:
    """
    if orderID:
        orderDetailUrls = copy.copy(urls["orderDetail"])
        orderDetailUrls["req_url"] = orderDetailUrls["req_url"].format(orderID)
        session.httpClint.send(orderDetailUrls)

        checkPaymentUrls = copy.copy(urls["checkPayment"])
        checkPaymentUrls["req_url"] = checkPaymentUrls["req_url"].format(orderID)
        session.httpClint.send(checkPaymentUrls)
        doPayment(session, orderID)


def doPayment(session, orderID):
    """
    组装跳转支付宝参数
    :param session:
    :param orderID:
    :return:
    """
    if orderID:
        doPaymentUrls = copy.copy(urls["doPayment"])
        doPaymentUrls["req_url"] = doPaymentUrls["req_url"].format(orderID)
        doPaymentRsp = session.httpClint.send(doPaymentUrls)
        if doPaymentRsp:
            _input_charset_re = re.compile('name="_input_charset" value="(\S+)" />')
            it_b_pay_re = re.compile('name="it_b_pay" value="(\S+)" />')
            notify_url_re = re.compile('name="notify_url" value="(\S+)" />')
            out_trade_no_re = re.compile('name="out_trade_no" value="(\S+)" />')
            partner_re = re.compile('name="partner" value="(\S+)" />')
            payment_type_re = re.compile('name="payment_type" value="(\S+)" />')
            return_url_re = re.compile('name="return_url" value="(\S+)" />')
            seller_id_re = re.compile(' name="seller_id" value="(\S+)" />')
            service_re = re.compile('name="service" value="(\S+)" />')
            subject_re = re.compile('name="subject" value="(\S+)" />')
            total_fee_re = re.compile('name="total_fee" value="(\S+)" />')
            sign_re = re.compile('name="sign" value="(\S+)" />')
            sign_type_re = re.compile(' name="sign_type" value="(\S+)" />')

            _input_charset = re.search(_input_charset_re, doPaymentRsp).group(1)
            it_b_pay = re.search(it_b_pay_re, doPaymentRsp).group(1)
            notify_url = re.search(notify_url_re, doPaymentRsp).group(1)
            out_trade_no = re.search(out_trade_no_re, doPaymentRsp).group(1)
            partner = re.search(partner_re, doPaymentRsp).group(1)
            payment_type = re.search(payment_type_re, doPaymentRsp).group(1)
            return_url = re.search(return_url_re, doPaymentRsp).group(1)
            seller_id = re.search(seller_id_re, doPaymentRsp).group(1)
            service_re = re.search(service_re, doPaymentRsp).group(1)
            subject = re.search(subject_re, doPaymentRsp).group(1)
            total_fee = re.search(total_fee_re, doPaymentRsp).group(1)
            sign = re.search(sign_re, doPaymentRsp).group(1)
            sign_type = re.search(sign_type_re, doPaymentRsp).group(1)

            print("_input_charset", _input_charset)
            print("it_b_pay", it_b_pay)
            print("notify_url", notify_url)
            print("out_trade_no", out_trade_no)
            print("partner", partner)
            print("payment_type", payment_type)
            print("return_url", return_url)
            print("seller_id", seller_id)
            print("service_re", service_re)
            print("subject", subject)
            print("total_fee", total_fee)
            print("sign", sign)
            print("sign_type", sign_type)

            url = "https://mapi.alipay.com/gateway.do?_input_charset={0}&it_b_pay={1}&notify_url={2}&out_trade_no={3}&" \
                  "partner={4}&payment_type={5}&return_url={6}&seller_id={7}&service={8}&subject={9}&total_fee={10}&sign={11}&sign_type={12}"\
                .format(_input_charset,
                        it_b_pay,
                        notify_url,
                        out_trade_no,
                        partner,
                        payment_type,
                        return_url,
                        seller_id,
                        service_re,
                        subject,
                        total_fee,
                        sign,
                        sign_type,)
            print(url)
            U.Logging.info("账号: {} 查询到待付款订单，订单号: {} ".format(session.userInfo.get("user", ""), orderID, ))
            sendEmail(orderID, session.userInfo.get("user", ""), session.email, url)
            session.orderDone = True


if __name__ == '__main__':
    pass