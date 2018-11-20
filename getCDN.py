#!/usr/bin/python
# --*-- coding:utf-8 --*--
import os
import time
cdn = []

for _ in range(1000):
    print("当前cdn: {}".format(cdn))
    str = "ping -c 1 mall.phicomm.com"
    try:
        result = os.popen(str).readlines()[1].split(" ")
        _cdn = result[3].replace(":", "")
        _timeOut = result[6].split("=")[1]
        if _cdn not in cdn:
            cdn.append(_cdn)
        print("cdn节点: {}, 延时: {}ms".format(_cdn, _timeOut))
        time.sleep(0.1)
    except:
        pass