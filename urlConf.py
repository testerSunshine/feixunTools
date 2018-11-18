# coding=utf-8
import random

import time

urls = {
    "login": {  # 登录接口
        "req_url": "/m/passport-post_login.html",
        "req_type": "post",
        "Referer": "https://mall.phicomm.com/m/passport-login.html",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 2,
        "s_time": 2,
        "is_logger": True,
        "is_json": True,
    },
    "passportLogin": {  # 登录页
        "req_url": "/m/passport-login.html",
        "req_type": "get",
        "Referer": "https://mall.phicomm.com/m/passport-login.html",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 100,
        "re_time": 2,
        "s_time": 2,
        "is_logger": False,
        "is_json": False,
    },
    "getGoodsDetail": {  # 商详
        "req_url": "/m/item-getGoodsDetail.html?pid={}",
        "req_type": "get",
        "Referer": "https://mall.phicomm.com/m/passport-login.html",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 1,
        "s_time": 1,
        "is_logger": True,
        "is_json": True,
    },
    "vcode": {  # 获取验证码
        "req_url": "/m/vcode-index-passport{}.html",
        "req_type": "get",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": False,
        "is_json": False,
        "not_decode": True,
    },
    "checkVcode": {  # 检查验证码
        "req_url": "/index.php/openapi/vcodeapi/checkVcode",
        "req_type": "post",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": True,
        "is_json": True,
    },
    "orderCreate": {  # 下单
        "req_url": "/m/order-create-is_fastbuy.html",
        "req_type": "post",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 0.1,
        "re_try": 10,
        "re_time": 2,
        "s_time": 0.1,
        "is_logger": True,
        "is_json": True,
    },
    "checkOrderFast": {  # 进入订单页
        "req_url": "/m/checkout-fastbuy.html",
        "req_type": "post",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 1,
        "s_time": 1,
        "is_logger": False,
        "is_json": False,
    },
    "goodsProducts": {  # 拉起订单页1
        "req_url": "/index.php/openapi/goods/products/product_id/{}",
        "req_type": "post",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": True,
        "is_json": True,
    },
    "ajPriceProducts": {  # 拉起订单页2
        "req_url": "/index.php/openapi/ajprice/products?product_id={}",
        "req_type": "post",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": True,
        "is_json": True,
    },
    "selectSku": {  # 选择订单类型
        "req_url": "/index.php/openapi/restrict/get_restrict",
        "req_type": "post",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": True,
        "is_json": True,
    },
    "cartFastBuy": {  # 购物车
        "req_url": "/index.php/m/cart-fastbuy-{}-1.html?",
        "req_type": "get",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": False,
        "is_json": False,
    },
    "item-5": {  # 商详
        "req_url": "/m/item-5.html",
        "req_type": "get",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 0.1,
        "s_time": 0.1,
        "is_logger": False,
        "is_json": False,
    },
    "myOrder": {  # 订单列表
        "req_url": "/m/my-orders-s1.html",
        "req_type": "get",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 5,
        "s_time": 5,
        "is_logger": False,
        "is_json": False,
    },
    "receiver": {  # 收货地址
        "req_url": "/m/my-receiver.html",
        "req_type": "get",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 5,
        "s_time": 5,
        "is_logger": False,
        "is_json": False,
    },
    "m": {  # 主页
        "req_url": "/m/",
        "req_type": "get",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 1,
        "s_time": 1,
        "is_logger": False,
        "is_json": False,
    },
    "checkOrderFast2": {  # 下单接口2
        "req_url": "/m/checkout.html",
        "req_type": "get",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 1,
        "s_time": 1,
        "is_logger": False,
        "is_json": False,
    },
    "cartAdd": {  # 加入购物车
        "req_url": "/index.php/m/cart-add-{}-1.html",
        "req_type": "get",
        "Referer": "",
        "Host": "mall.phicomm.com",
        "Content-Type": 1,
        "re_try": 10,
        "re_time": 1,
        "s_time": 1,
        "is_logger": True,
        "is_json": True,
    },
}