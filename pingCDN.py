import re

import requests

url = "http://ping.chinaz.com/iframe.ashx?t=ping&callback=jQuery111304361832209485905_1541601608329"
data = {
    "guid": "b1499d95-7e3c-472a-9682-e58e1b362633",
    "host":	 "mall.phicomm.com",
    "ishost": "0",
    "encode": "3mljLh3urdaycd2i8R2vRwQhYFsnPQ6A",
    "checktype": "0",
}
cdn_list = []
num = 0
while True:
    try:
        result = requests.post(url, data, timeout=60)
        ipRe = re.compile(r"ip:'(\S+)',ipaddress:")
        ip = re.search(ipRe, result.content.decode()).group(1)
        if ip not in cdn_list:
            cdn_list.append(ip)
            num += 1
            print("发现当前cdn {} 为新的cdn，加入cdn列表, 总共发现{}个cdn".format(ip, num))
    except:
        pass
