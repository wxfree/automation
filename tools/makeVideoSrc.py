import requests
import re
import json
import os
from icecream import ic
import time
"""
.*?惰性匹配,匹配结果尽可能短
.* 贪婪匹配,匹配结果尽可能长
"""

rootDir = r'/data/www/workspace/python-learn/data/tsdir'
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36'}
class MakeVideoSrc:
    def __init__(self, cont_id):
        self.contId = cont_id
        os.chdir(rootDir)
        # 获取m3u8路径的前缀
        playurl = self.download_m3u8()
        ic(playurl)
        self.prefix = self.get_prefix_path(playurl)

    def download_m3u8(self):
        url = 'http://h5.nty.tv189.com/api/portal/h5inter/auth-play'
        resp = requests.get(url, params={'contid': self.contId}, headers=headers)
        m3u8_url = ''
        if resp.status_code == 200:
            json_resp = json.loads(resp.text)
            m3u8_url = json_resp['info']['playurl']
            response = requests.get(m3u8_url, headers=headers)
            with open('./tysx.txt', 'wb') as f:
                f.write(response.content)
                f.close()
        return m3u8_url

    def download_ts(self):
        n = 1
        with open('./tysx.txt', 'r') as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue
                if line.startswith('http'):
                    ts_url = line.strip()
                else:
                    ts_url = self.prefix + line
                res = requests.get(ts_url, headers=headers)
                with open(f'{n}.ts', 'wb') as f2:
                    f2.write(res.content)
                    ic(f'正在下载{n}.ts')
                    f2.close()
                n = n + 1

    @classmethod
    def combine(cls):
        files = os.listdir()
        # 把同一个文件夹下的txt排除
        files.pop(files.index('tysx.txt'))
        files.pop(files.index('.DS_Store'))
        ic(files)
        for file in sorted(files, key=lambda x: int(x.split('.')[0])):
            if file.endswith('.txt'):
                continue
            ic(file)
            with open(file, 'rb') as f1:
                with open('tysx.mp4', 'ab') as f2:
                    f2.write(f1.read())
                    f2.close()
                f1.close()

    @classmethod
    def get_prefix_path(cls, route):
        reg = re.compile(r'.*?/\d{4}/\d{2}/\d{2}/')
        result = re.finditer(reg, route)
        for it in result:
            ic(it.group())
            url = it.group()
        return url


start = time.time()
mv = MakeVideoSrc('C42208006')
mv.download_ts()
mv.combine()
end = time.time()
ic(end - start)
