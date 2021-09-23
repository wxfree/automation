import sys
import requests
import json
from icecream import ic
import os
import re
"""
判断当前系统：
import sys
sys.platform
win32
import platform
platform.platform()
Windows-10-10.0.18362-SP0
"""

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36'
}


class MakeMp4:
    def __init__(self, cont_id):
        self.contId = cont_id
        self.rootPath = r'D:\wangxin\video'
        os.chdir(self.rootPath)
        # self.url = 'https://h5v1.nty.tv189.com/6/ol/st02/2021/09/06/Q4M_6c49dec8-ab6c-4593-a6ec-ae0e1cdb0c1a.mp4.m3u8?sign=7e53dd72685409db53691d20707ab8ad&qualityCode=1945&version=1&guid=545c2422-bb6f-4cac-d94d-7fb981b016a0&app=115010310149&cookie=9b91551bafc49dd084bfe302be3a4ca1&session=9b91551bafc49dd084bfe302be3a4ca1&uid=0&uname=10000000000&time=20210922151019&videotype=2&cid=C43579896&cname=&cateid=&dev=000001&ep=1&os=30&ps=0099&clienttype=android&appver=11.0.0.0&res=&channelid=01833310&pid=1000000432&orderid=SUCC&nid=&cp=00000020&sp=00000020&ip=58.33.171.234&ipSign=1d1fa130e3d7ce0f73e9b13fc338c8cb&cdntoken=api_614ad6dbf2c75&a=Zxx5enr6Ca317sjhnH5eHR7K5sWV91Ho&pvv=&t=614b0f1c&cf=tx&s2=647bba344396e7c8170902bcf2e15551'

        self.url = self.get_m3u8()
        # 获取m3u8路径
        self.prefix_path = self.get_url_path(self.url)

    def get_m3u8(self):
        m3u8_url = ''
        response = requests.get('https://h5.nty.tv189.com/api/portal/h5inter/auth-play', params={'contid': self.contId}, headers=headers)
        if response.status_code == 200:
            json_resp = json.loads(response.text)
            m3u8_url = json_resp['info']['playurl']
            ic(json_resp)
            resp = requests.get(m3u8_url, headers=headers)
            with open(r'D:\wangxin\video\tysx.txt', 'wb') as f:
                f.write(resp.content)
                f.close()
        return m3u8_url

    def get_ts_list(self):
        with open(r'D:\wangxin\video\tysx.txt', 'r') as f:
            for line in f.readlines():
                if line.startswith('#') or line == '\n':
                    continue
                if line.startswith('http'):
                    ts_url = line.strip()
                else:
                    ts_url = self.prefix_path + line.strip()
                ic(ts_url)
                r = re.finditer(r'/seg-(?P<num>\d+)-', ts_url)
                for it in r:
                    n = it.group('num')
                res = requests.get(ts_url, headers=headers)
                with open(f'./{n}.ts', 'wb') as f2:
                    f2.write(res.content)
                    f2.close()
            f.close()

    @classmethod
    def make_mp4(cls):
        files = os.listdir()
        files.pop(files.index('tysx.txt'))
        files = sorted(files, key=lambda x: int(x.split('.')[0]))
        # if sys.platform != 'win32':
        #     files.pop(files.index('.DS_Store'))
        ic(files)
        # os.system(r'copy /b D:\wangxin\video\*.ts D:\wangxin\video\tysx.mp4')
        for file in files:
            ic(file)
            if file.endswith('.ts'):
                with open(file, 'rb') as f1:
                    with open('test.mp4', 'ab') as f2:
                        f2.write(f1.read())

    @classmethod
    def get_url_path(cls, url_path):
        reg = re.compile(r'.*?\d{4}/\d{2}/\d{2}/')
        resp = re.finditer(reg, url_path)
        path = ''
        for it in resp:
            ic(it.group())
            path = it.group()
        return path


contentId = input('请输入需要下载的视频id：')
mu = MakeMp4(contentId)
mu.get_ts_list()
mu.make_mp4()
