import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import json
from urllib import parse
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB


# requests获得的数据，resp.text是str, resp.content是bytes
# 优化措施1.根据第一条歌曲名是否包含Live，往后顺延
# 孙燕姿 我怀念的 会报错

class KuWoMusic:
    def __init__(self, keyword, need_download=0):
        """
            @rid:音乐的id
            @keyword:音乐搜索关键字
            @params:查询音乐下载地址的接口参数
            @headers：模拟爬虫ua
            @items：搜索列表页结果
            @need_download:是否需要进行下载，默认为0
        """
        self.driver = webdriver.Chrome()
        self.keyword = keyword
        self.params = {
            'br': '320kmp3',
            'type': 'convert_url3'
        }
        self.need_download = need_download
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
        self.items = self.get_search_result()
        self.info = self.get_data()

    # 根据搜索关键字查询并返回音乐列表
    def get_search_result(self):
        url = 'https://kuwo.cn/search/list?key=' + parse.quote(self.keyword)
        self.driver.maximize_window()
        # 此处search_list是用js加载进来的，使用显式等待更好，否则无法获取完整页面代码
        # self.driver.implicitly_wait(10)
        self.driver.get(url)
        # print("等待网页响应...")
        # wait = WebDriverWait(self.driver, 10)
        # wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "search_list")))
        # print("正在获取网页数据...")
        time.sleep(1)
        d = self.driver.page_source
        soup = BeautifulSoup(d, 'html.parser')
        # self.driver.close()
        # 返回整个大区块，可以获得歌名、歌手、专辑、封面、时长
        return soup.select('.song_item')

    # 返回歌曲数据
    def get_data(self):
        song_info = []
        for item in self.items:
            song = item.select('.name')[0]
            song_name = song.string
            href = song.get('href')
            rid = href.split('/')[2]
            song_artist = item.select('.song_artist')[0].string
            song_album = item.select('.song_album')[0].string
            print(song_name, song_artist, song_album, href)
            if 'Live' not in song_name:
                song_info.append({
                    'name': song_name,
                    'artist': song_artist,
                    'album': song_album,
                    'rid': rid
                })
        print('song_info', song_info)
        return song_info

    def get_download_url(self):
        url = 'https://kuwo.cn/url'
        self.params['rid'] = self.info[0]['rid']
        print('info', self.info)
        print('rid', self.info[0]['rid'])
        resp = requests.get(url, params=self.params, headers=self.headers)
        print('code', resp.status_code)
        if resp.status_code == 200 and resp.text != 'failed':
            print(resp.text)
            res = json.loads(resp.text)
            print(res['url'])
            if self.need_download == 0:
                self.driver.get(res['url'])
            else:
                self.get_file(res['url'])
                self.driver.close()
        else:
            print('没有找到下载链接')

    def get_file(self, url):
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            print(resp.headers['Content-Type'])
            suffix = resp.headers['Content-Type']
            # 该地址内容是否为音频
            if 'audio' in suffix:
                with open(self.keyword + '.mp3', 'wb') as f:
                    f.write(resp.content)
                    f.close()
                print('下载完成')
                self.set_mp3_info()
            else:
                print('非音频文件')
        else:
            print('无法获得文件内容', resp.status_code)

    def set_mp3_info(self):
        """修改mp3中的元信息"""
        print(self.keyword)
        music = ID3('./' + self.keyword + '.mp3')
        # music.add(APIC(  # 插入封面
        #     encoding=3,
        #     mime='image/jpeg',
        #     type=3,
        #     desc=u'Cover',
        #     data=self.info['picData']))
        music.add(TIT2(encoding=3, text=self.info[0]['name']))  # 插入歌名
        music.add(TPE1(encoding=3, text=self.info[0]['artist']))  # 插入作者
        music.add(TALB(encoding=3, text=self.info[0]['album']))
        music.save()


musicName = input('请输入要下载的音乐:')
kuwo = KuWoMusic(musicName, 1)
kuwo.get_download_url()
