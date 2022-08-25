import requests
import asyncio
import aiohttp
import aiofiles
import tqdm
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def onefloat(num):
    return '{:.1f}'.format(num)


def calculate_time(fn):
    def wrapper(*args):
        start = time.time()
        fn(*args)
        end = time.time()
        print('消耗了:', end-start)
    return wrapper


@calculate_time
def run(url: str, name):
    if not url.startswith('http'):
        print('下载地址不存在 {url}')
        return
    with requests.get(url, stream=True) as r:
        with open(name, 'wb') as file:
            # 请求文件的大小 单位字节B
            total_size = int(r.headers['content-length'])
            print(total_size)
            # 已下载的字节数
            content_size = 0
            # 进度下载完成的百分比
            plan = 0
            # 请求开始的时间
            start_time = time.time()
            # 上一秒的下载大小
            temp_size = 0
            # 开始下载 每次请求1024字节
            for content in r.iter_content(chunk_size=1024):
                if content:
                    file.write(content)
                # 统计已下载的大小
                content_size += len(content)
                # 计算下载速度
                plan = (content_size / total_size) * 100
                # 每秒统计一次下载量
                if time.time() - start_time > 1:
                    # 重置开始时间
                    start_time = time.time()
                    # 每秒的下载量
                    speed = content_size - temp_size
                    # 我就按照MB/s当单位
                    print('\r', f"{onefloat(plan)}%", onefloat(speed/(1024**2)), 'MB/s', end='', flush=True)
                    # if 0 <= speed < 1024**2:
                    #     # 输出的数据会因为数据长短产生36.7% 3.0 MB/s/s问题
                    #     print('\r', f"{onefloat(plan)}%", onefloat(
                    #         speed/1024), 'KB/s', end='', flush=True)
                    # elif 1024**2 < speed <= 1024**3:
                    #     print('\r', f"{onefloat(plan)}%", onefloat(
                    #         speed/(1024**2)), 'MB/s', end='', flush=True)
                    # elif 1024**3 < speed <= 1024**4:
                    #     print('\r', f"{onefloat(plan)}%", onefloat(
                    #         speed/(1024**3)), 'GB/s', end='', flush=True)
                    # else:
                    #     print('\r', f"{onefloat(plan)}%", onefloat(
                    #         speed/(1024**4)), 'TB/s', end='', flush=True)
                    # 重置已下载大小
                    temp_size = content_size
            else:
                print('\r', '100%下载完成\n', end='', flush=True)


# async def run(url: str, name):
#     if not url.startswith('http'):
#         print('下载地址不存在 {url}')
#         return
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as r:
#             print(r.headers)
#             title = f"{name}.mp4"
#             async with aiofiles.open(title, 'wb') as file:
#                 # 请求文件的大小 单位字节B
#                 total_size = int(r.headers['Content-Length'])
#                 print(total_size)
#                 # 已下载的字节数
#                 content_size = 0
#                 # 进度下载完成的百分比
#                 plan = 0
#                 # 请求开始的时间
#                 start_time = time.time()
#                 # 上一秒的下载大小
#                 temp_size = 0
#                 while True:
#                     chunk = await r.content.read(1024)
#                     if not chunk:
#                         print('\r', f'{title} 100%下载完成\n', end='', flush=True)
#                         break
#                     await file.write(chunk)
#                     # 统计已下载的大小
#                     content_size += len(chunk)
#                     # 计算下载速度
#                     plan = (content_size / total_size) * 100
#                     # 每秒统计一次下载量
#                     if time.time() - start_time > 1:
#                         # 重置开始时间
#                         start_time = time.time()
#                         # 每秒的下载量
#                         speed = content_size - temp_size
#                         # 我就按照MB/s当单位
#                         print('\r', f"{onefloat(plan)}%", onefloat(
#                             speed/(1024**2)), 'MB/s', end='', flush=True)
#                         # if 0 <= speed < 1024**2:
#                         #     # 输出的数据会因为数据长短产生36.7% 3.0 MB/s/s问题
#                         #     print('\r', f"{onefloat(plan)}%", onefloat(
#                         #         speed/1024), 'KB/s', end='', flush=True)
#                         # elif 1024**2 < speed <= 1024**3:
#                         #     print('\r', f"{onefloat(plan)}%", onefloat(
#                         #         speed/(1024**2)), 'MB/s', end='', flush=True)
#                         # elif 1024**3 < speed <= 1024**4:
#                         #     print('\r', f"{onefloat(plan)}%", onefloat(
#                         #         speed/(1024**3)), 'GB/s', end='', flush=True)
#                         # else:
#                         #     print('\r', f"{onefloat(plan)}%", onefloat(
#                         #         speed/(1024**4)), 'TB/s', end='', flush=True)
#                         # 重置已下载大小
#                         temp_size = content_size


async def main():
    # download_urls = [
    #     f"https://ddys.tv/summer-time-render/?ep={i}" for i in range(16, 19)]
    download_urls = ['http://v26-default.ixigua.com/69e2a5d08b69a0cb0bb4ca3c41fbc8c4/63031d1d/video/tos/cn/tos-cn-v-0064/a6b51b1efdad44f580489f7dad223489/?filename=1080P.mp4',
                     'http://v3-default.ixigua.com/0c68f6d12a10d09a9a15a1152532707d/63031b75/video/tos/cn/tos-cn-v-0064/0b516149d452465386d441972b7fdc22/?filename=1080P.mp4',
                     'http://v26-default.ixigua.com/7b0dd3cfc6de4401a8e86bbd4fd19919/63031b28/video/tos/cn/tos-cn-v-0064/bb79a6412b7444d1a3243dd20b685c85/?filename=1080P.mp4'
                     ]
    tasks = []
    for index, url in enumerate(download_urls):
        tasks.append(asyncio.create_task(run(url, f'夏日重现{index+1}')))
    await asyncio.wait(tasks)


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def get_video_info(name, url):
    driver = get_driver()
    # comic = '夏日重现'
    driver.get(url)
    time.sleep(2)
    # 下面这步骤可能要多停留点时间
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located(
        (By.CSS_SELECTOR, '.vjs-big-play-button'))).click()
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    video = soup.select('#vjsp_html5_api')[0]
    video_src = video.get('src')
    print('video address', video_src)

    param = driver.current_url.split('?')[1]
    title = name + param.split('=')[1] + '.mp4'
    print('param=', param, 'title=', title)
    driver.quit()
    return video_src, title


if __name__ == '__main__':
    download_urls = [
        f"https://ddys.tv/summer-time-render/?ep={i}" for i in range(1, 19)]
    params = get_video_info('夏日重现', download_urls[6])
    run(*params)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
