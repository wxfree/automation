import requests
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
import re
import json

# 'Referer': 'https://pearvideo.com/video_1739658',
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Cookie': 'acw_tc=781bad2516303936369067693e6338f1a327aa90cb29b2098dd38c17576123'
}


def get_contid(string: str) -> list:
    result = []
    reg = '<a href="(.*?)" class="popularembd actplay">'
    conts = re.findall(reg, string)
    for cont in conts:
        print(cont.split('_')[1])
        result.append(cont.split('_')[1])
    return result


def download(contid):
    download_url = 'https://pearvideo.com/videoStatus.jsp'
    headers['Referer'] = 'https://pearvideo.com/video_' + contid
    download_resp = requests.get(download_url, headers=headers, params={'contId': contid})
    if download_resp.status_code == 200:
        download_resp_json = json.loads(download_resp.text)
        src_url = download_resp_json['videoInfo']['videos']['srcUrl']
        # https://video.pearvideo.com/mp4/third/20210823/1630477888440-10008579-103556-hd.mp4
        # https://video.pearvideo.com/mp4/third/20210823/cont-1739658-10008579-103556-hd.mp4
        # res = src_url.split('/')
        # need_replace_string = res[-1].split('-')[0]
        res = re.findall('/(\d*?)-', src_url)
        need_replace_string = res[0]
        play_url = src_url.replace(need_replace_string, 'cont-' + contid)
        print('最终下载地址', play_url)
    else:
        print('视频播放接口获取失败')


origin_url = 'https://pearvideo.com/popular_loading.jsp?reqType=1&categoryId=10&start=10&sort=9'

resp = requests.get(origin_url, headers=headers)
print(resp.status_code)
print(resp.text)
if resp.status_code == 200:
    resp.encoding = resp.apparent_encoding
    print(resp.text)
    contids = get_contid(resp.text)
    print(contids)
    for cc in contids:
        download(cc)
