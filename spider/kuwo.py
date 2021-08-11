import time
import requests
import json
from urllib import parse
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB


class KuWoMusic:
    def __init__(self, keyword, need_download=0):
        """
            @rid:音乐的id
            @keyword:音乐搜索关键字
            @params:查询音乐下载地址的接口参数
            @headers：模拟爬虫ua
            @items：搜索列表页结果
            @need_download:是否需要进行下载，默认为0
            @index: 默认下载第一首，如果第一首下载链接获取不到，自动+1拿下一首
        """
        self.keyword = keyword
        self.params = {
            'br': '320kmp3',
            'type': 'convert_url3'
        }
        self.need_download = need_download
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/91.0.4472.164 Safari/537.36',
            'Referer': 'https://kuwo.cn/search/list?key=' + parse.quote(self.keyword),
            'csrf': '2M93WAUL0L1',
            'Cookie': 'kw_token=2M93WAUL0L1'
        }
        self.items = self.get_search_result()
        self.info = self.get_data()
        self.index = 0

    # 一下两方法使用直接获取接口信息的方法获取音乐参数
    def get_search_result(self):
        params = {
            'key': self.keyword,    # 此处不需要编码，自动会搞
            'pn': 1,
            'rn': 5,
            'httpStatus': 1,
            'reqId': 'bf6d4fd1-fa4d-11eb-9620-fbd4984981ba'
        }
        url = 'https://kuwo.cn/api/www/search/searchMusicBykeyWord'
        resp = requests.get(url, params=params, headers=self.headers)
        print(resp.request.url)
        print('status_code', resp.status_code)
        print('text', resp.text)
        if resp.status_code == 200:
            json_resp = json.loads(resp.text)
            return json_resp['data']['list']

    def get_data(self):
        song_info = []
        for item in self.items:
            song_name = item['name']
            rid = item['rid']
            song_album = item['album']
            song_artist = item['artist']
            song_poster = item['pic']
            song_duration = item['duration']
            print(song_name, song_artist, song_album, rid, song_duration)
            if 'Live' not in song_name:
                song_info.append({
                    'name': song_name,
                    'artist': song_artist,
                    'rid': rid,
                    'duration': song_duration,
                    'album': song_album,
                    'poster': song_poster
                })
        return song_info

    def get_download_url(self):
        """@index 默认下载选项第一首"""
        url = 'https://kuwo.cn/url'
        self.params['rid'] = self.info[self.index]['rid']
        print('info', self.info)
        print('rid', self.info[self.index]['rid'])
        resp = requests.get(url, params=self.params, headers=self.headers)
        print('code', resp.status_code)
        print('request URL', resp.request.url)
        if resp.status_code == 200 and resp.text != 'failed':
            print(resp.text)
            res = json.loads(resp.text)
            print(res['url'])
            self.get_file(res['url'])
        else:
            print('没有找到下载链接')
            self.index += 1
            print('new index', self.index)
            self.get_download_url()

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
        result = self.check_mp3_info()
        # music.add(APIC(  # 插入封面
        #     encoding=3,
        #     mime='image/jpeg',
        #     type=3,
        #     desc=u'Cover',
        #     data=result['poster']))
        music.add(TIT2(encoding=3, text=result['name']))  # 插入歌名
        music.add(TPE1(encoding=3, text=result['artist']))  # 插入作者
        music.add(TALB(encoding=3, text=result['album']))
        music.save()

    def check_mp3_info(self):
        result = self.info[self.index]
        for item in result.keys():
            if result[item] is None:
                result[item] = ''
        return result


musicName = input('请输入要下载的音乐:')
begin = time.time()
ku_wo = KuWoMusic(musicName, 1)
ku_wo.get_download_url()
end = time.time()
print(f'本次下载消耗了{end - begin}')
