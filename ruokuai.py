# coding:utf-8
import requests
from hashlib import md5


class RClient(object):

    def __init__(self, username, password):
        self.username = username
        self.password = md5(password.encode()).hexdigest()
        self.soft_id = '96061'
        self.soft_key = '6facb9da7bb645ad9c4a229464b2cf89'
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def rk_create(self, im, im_type, timeout=60):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        try:
            r = requests.post('http://api.ruokuai.com/create.json', timeout=10, data=params, files=files,
                              headers=self.headers)
            return r.json()
        except:
            pass

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        return r.json()

    def get_info(self):
        parms = {
            "username": self.username,
            "password": self.password
        }
        r = requests.post("http://api.ruokuai.com/info.json", data=parms, headers=self.headers).json()
        if r.get("Score", ""):
            return "当前余额 {}".format(r.get("Score", ""))
        else:
            return r.get("Error", "若快发生未知错误")


if __name__ == '__main__':
    rc = RClient('931128603', 'wen1995', )
    print(rc.get_info())
