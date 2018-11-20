# -*- coding: utf8 -*-
__author__ = 'MR.wen'
import time
from email.header import Header
from email.mime.text import MIMEText
import smtplib
import Utils as U


def sendEmail(msg, account, email):
    """
    邮件通知
    :param str: email content
    :return:
    """
    sender = "931128603@qq.com"
    receiver = email
    subject = '恭喜，账号: {} 在{}已抢购成功, 请登录官网立即付款！！！'.format(account, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),)
    username = "931128603@qq.com"
    password = "xrvenridfpnnbehh"
    host = "smtp.qq.com"
    s = "订单编号: {}, 付款地址: https://mall.phicomm.com/my-vclist.html, 如果重复发送请忽略。".format(msg)

    msg = MIMEText(s, 'plain', 'utf-8')  # 中文需参数‘utf-8’，单字节字符不需要
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    smtp = smtplib.SMTP_SSL()
    for i in range(3):  # 邮件发送失败重试三次
        try:
            smtp.connect(host)
            smtp.login(username, password)
            smtp.sendmail(sender, receiver.split(","), msg.as_string())
            smtp.quit()
            U.Logging.success("email send success.")
            break
        except (smtplib.SMTPServerDisconnected, smtplib.SMTPAuthenticationError):
            time.sleep(1)


if __name__ == '__main__':
    sendEmail(1)