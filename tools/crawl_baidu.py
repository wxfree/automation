import re
import json
import traceback
import aiohttp
import asyncio
import requests
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from automation.common.base_page import BasePage
from automation.common.database import Database
from automation.common.configuration import Configuration
from automation.common.log_service import LogService
from automation.common.util import Util
from fake_useragent import UserAgent
log = LogService(__name__).log()
util = Util()


class BaiduSpider(BasePage):
    def __init__(self, designer="邢同和", keyword="上海", page_num=1) -> None:
        self.bp = self.get_browser()
        self.designer = designer
        self.keyword = keyword
        self.page_num = page_num
        self.emails, self.phones, self.results, self.detail, total_urls = [], [], [], [], []
        # self.origin_urls = self.main()
        # self.origin_urls = ['http://www.baidu.com/link?url=7oU33D4vAnC7u_wD_g6d1yVnXH5MEji6xb9bFqZA8Ghhjlb1SfRXbW3cUvsu8q5QqK1v7IegCEBQBLLyeaDOpPmeqMW8NQ_iDiTMCHujDjC', 'http://www.baidu.com/link?url=5KkDCDPBTmxIfceLQfMa8G-bud2z72Q3uNb0atDbDlQOoKtwh3vIhU6p2nfnVGp3z1rN1QVU9EQDjPkkdGemWgM9gQ4l-GiGwwkGxbWAv2m', 'http://www.baidu.com/link?url=0LXE9nMGVS8orHKTPs_XCGWQVHE9lZ6s615F2u9Sc1g4Bbdnp4TJKYH4H1_hWLc6QEWfnLKzNYxCJ394w1FHU_', 'http://www.baidu.com/link?url=GNxAuB_JlwfEejzD5v-gQzyUySiCt7mBvuIPj0NRw8b19K_JLXT94yH0ccJe5Tae', 'http://www.baidu.com/link?url=Hwhjp85LGL4JEEieZTQpzuom43RW3LfpZFCMZOdchbDaRZ-1F2jsc7V8I8_iZA4X2SgJ1glLLNDc1VohA35l4EdqOAaklxwB-PtpfFEnvlMss9cIk1_0piGvlUMMiA_QdjGVXeEOVdiWjStgnxpvtntjZ7EuSYkxGSmSlpFdDmS46FrsQ3YdCe70fPVXxCr0l2w-5Qpe3LCt3l6Hav1b2NwiGoyCNNvOJR_kFcV8DbGEIDB_Rr6oENr9wbRs98OW_lvBjnHDJcBUPlLMcHFROK', 'http://www.baidu.com/link?url=nQvRAH_DVHTXnOYiy1bBJFQadGmiPvLQw5YySC-cB3kccmOhYJ36uG5YqqOfoeXVxlfE7d3Hm5sdG70UrpmGq_', 'http://www.baidu.com/link?url=8r60dHggZg9DPbuxCeSyL3V7E6ohTEmXMRY0yU3KTbIagZaKatRHOJH_uSarljKU1lHFgsSKrYzAMt6AlwTDNU9iKSWpiA3AeFp6xkxuv2v-Un8I4J9CKUsOKX1PnMfh', 'http://www.baidu.com/link?url=CLzEC9Tgc6fO7bVbLv3nvRvAVedrps0cpKzt4rJnQbl9fh5PmpAvDoUPeEYMiY5EDbm3jECA2vra7qmCQkhZDli6N0BmkHnQrhXHGoDf2Ma', 'http://www.baidu.com/link?url=01QRi84pTUkb_T5IpWht4ayKJkT2UJGBco2ZV160W90fjqjqRCbtnfx1Fme4FEIiV0K7n4REQ_1EXpLN1-ZVv2scOBwwXrkJShWgVhavqGMZA0xCaLcScI3tPezYm2wd', 'http://www.baidu.com/link?url=S-BfBsIz9b1SY5izqMAV6MAL4ES1P1fY5TG8CIudVSqB6QjLokGtN-S0bFWa6MRjiYxdxZsvlhwcImtUqy8IZvYSMRhNfmDcW8rPXj5rf5mlJyFv-KFNQZhoGBQvtxjEGN8KKIL61n_L1glhgC3gia']
        # self.direct_urls = self.parse_redirect_urls(self.origin_urls)
        self.direct_urls = ['http://baijiahao.baidu.com/s?id=1725915995850368990&wfr=spider&for=pc', 'http://baijiahao.baidu.com/s?id=1725926810972388933&wfr=spider&for=pc', 'https://book.douban.com/subject/1727942/', 'http://www.hw-mp.com/nd.jsp?id=78', 'https://mp.weixin.qq.com/s?__biz=MjM5MjQ3NDIwMQ==&mid=2649553727&idx=2&sn=224c68eed71e64f7852e1db51dbbf224&chksm=bebdee0989ca671f86fb9b7585bc3b221cabdd4e588aa8490e2423a3ef8a57bd92ebc2b07aba&scene=27', 'https://j.eastday.com/p/1645952935043483', 'https://baike.baidu.com/item/%E9%82%A2%E5%90%8C%E5%92%8C/10766305?fr=aladdin', 'https://haokan.baidu.com/v?pd=wisenatural&vid=4558941328731173432', 'https://view.inews.qq.com/a/20220227A084AY00?startextras=undefined&from=amptj', 'https://easylearn.baidu.com/edu-page/tiangong/questiondetail?id=1724941258258161402&fr=search']
        print(self.direct_urls)
    
    def get_browser(self):
        # 反反爬虫 https://blog.51cto.com/u_15127500/4748564
        chrome_options = Options()
        # 不加载图片提升速度, 碰到安全检查看不到图片有点麻烦
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')
        # 取消显示Chrome正在受到自动测试软件控制 enable-automation
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging', 'enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # 手机 ua
        # chrome_options.add_argument('User-Agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36')
        # PC ua
        chrome_options.add_argument(
            'User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
        chrome_options.add_argument('--disable-blink-features')
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-browser-side-navigation')
        # 使用headless 状态会导致窗口默认大小为0x0,并且处于Minimized状态,启动后可能会造成部分元素无法被点击等异常,使用headless容易被反爬
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('window-size=1920x1080')
        # chrome_options.add_argument('--start-maximized')
        bp = BasePage(webdriver.Chrome(options=chrome_options))
        bp.driver.implicitly_wait(10)
        bp.driver.maximize_window()
        bp.driver.set_page_load_timeout(15)
        return bp

    # 设置百度登录信息
    def set_baidu_cookie(self):
        content = util.read_yaml(Configuration.root_path + '/extract.yaml')
        if content and 'bduss' in content:
            bduss_cookie = content['bduss']
            # 删除页面所有cookie
            self.bp.driver.delete_all_cookies()
            self.bp.driver.add_cookie({
                'name': 'BDUSS',
                'value': bduss_cookie
            })
            self.bp.driver.add_cookie({
                'name': 'BDUSS_BFESS',
                'value': bduss_cookie
            })
            # script = f"document.cookie+='BDUSS={bduss_cookie};BDUSS_BFESS={bduss_cookie}'"
            # bp.execute_script(script)
            # # 刷新页面获取登录信息
            self.bp.refresh()

    def collect_urls(self, items):
        # return ['http://www.super-sh.com/super-sh/pc/index.html']
        result = []
        for index, item in enumerate(items):
            url = item.get_attribute('href')
            # title = item.text
            if url:
                result.append(url)
        return result

    # 获取百度搜索结果
    def main(self):
        # total_urls = []
        self.bp.open('https://www.baidu.com')
        self.set_baidu_cookie()
        # 百度搜索+"",搜索结果没有广告
        self.bp.on_input(By.ID, 'kw', f'{self.designer} {self.keyword}\n')
        real_page_total = self.bp.locate_elements(By.CSS_SELECTOR, '.page-inner_2jZi2 a')
        log.info(f"总共页码:{len(real_page_total)}")

        for i in range(1, int(self.page_num)+1):
            items = self.bp.locate_elements(By.CSS_SELECTOR, '#content_left .c-title.t a')
            log.info(f'当前正在爬取第{i}页: {self.bp.driver.current_url}')
            log.info(f'当前爬取页面共有{len(items)}条')
            resp = self.collect_urls(items)
            self.total_urls.extend(resp)
            try:
                self.bp.mouse_click(By.XPATH, "//a[contains(text( ), '下一页')]")
                self.bp.wait(3)
            except Exception as e:
                log.error(f"翻页问题, {traceback.format_exc()}")
                # 划到最下面能看到分页再截图
                self.bp.execute_script(
                    "window.scrollTo(0, document.documentElement.scrollHeight-document.documentElement.clientHeight)")
                self.bp.save_screen_shot(f'./screenshot/{self.designer}_{self.keyword}_翻页问题.png')
                break
        self.bp.quit()
        log.info(f"{len(self.total_urls)} {self.total_urls}")
        # 翻页卡顿会导致重复爬取同一页的搜索结果,去重下
        self.total_urls = list(set(self.total_urls))
        return self.total_urls

    # 获取数据redirect后的地址
    def parse_redirect_urls(self, urls):
        final_urls = []
        for url in urls:
            resp = requests.get(url, headers={'User-Agent': UserAgent().random}, allow_redirects=False)
            if resp.status_code == 302:
                final_urls.append(resp.headers['Location'])
        return final_urls


    # 搜索11位长度的手机号
    @staticmethod
    def get_phoneno(string):
        result = []
        # 获取数字列表集合
        number_list = re.findall('\d+', string)
        # 筛选11位数字
        number11 = list(filter(lambda x: len(x) == 11, number_list))
        for num in number11:
            if re.match('1[35789]\d{9}', num):
                result.append(num)
        return result

    async def download(self, url):
        # emails, phones, results, detail = [], [], [], []
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'User-Agent': UserAgent().random}) as r:
                html = await r.text()
                soup = BeautifulSoup(html, 'html.parser')
                content = soup.body.get_text()
                resp = self.get_phoneno(content)
                # 一堆字符串中匹配,不能使用'^$',这个正则只能匹配xxx@xxx.xxx
                email = re.findall('[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+', content)
                # 座机正则https://www.cnblogs.com/songqiaoli/p/3896794.html '0\d{2,3}-\d{7,8}|\(?0\d{2,3}[)-]?\d{7,8}|\(?0\d{2,3}[)-]*\d{7,8}'
                # 只留下有-的座机匹配
                tel_resp = re.findall('0\d{2,3}-\d{7,8}|\(?0\d{2,3}[)-]\d{7,8}', content)
                # 邮箱手机座机在这里先去重
                email_temp = list(set(email))
                tel_resp.extend(resp)
                phone_temp = list(set(tel_resp))
                email_temp_str = ','.join(email_temp)
                phone_temp_str = ','.join(phone_temp)
                log.info(f"{resp} {email} {tel_resp}")
                if len(resp)+len(email)+len(tel_resp) > 0:
                    self.emails.extend(email)
                    self.phones.extend(resp)
                    self.phones.extend(tel_resp)
                    self.results.append({
                        'url': url,
                        'email': email_temp_str,
                        'phoneNumber': phone_temp_str
                    })
                # 没有搜到结果的url
                else:
                    self.detail.append({
                        'url': url,
                        'email': '',
                        'phoneNumber': ''
                    })
    
    async def mainmain(self):
        tasks = []
        for url in self.direct_urls:
            tasks.append(asyncio.create_task(self.download(url)))
        await asyncio.wait(tasks)

    # 抓取邮件、手机、座机信息
    def parse_html(self,url, html):
        detail = []
        phones = []
        emails = []
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        # 获取页面文字内容,soup包含js、css,时间戳会影响手机号码正则匹配
        # content = soup.getText()
        content = soup.body.get_text()
        resp = self.get_phoneno(content)
        # 一堆字符串中匹配,不能使用'^$',这个正则只能匹配xxx@xxx.xxx
        email = re.findall('[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+\.[a-zA-Z]+', content)
        # 座机正则https://www.cnblogs.com/songqiaoli/p/3896794.html '0\d{2,3}-\d{7,8}|\(?0\d{2,3}[)-]?\d{7,8}|\(?0\d{2,3}[)-]*\d{7,8}'
        # 只留下有-的座机匹配
        tel_resp = re.findall('0\d{2,3}-\d{7,8}|\(?0\d{2,3}[)-]\d{7,8}', content)
        # 邮箱手机座机在这里先去重
        email_temp = list(set(email))
        tel_resp.extend(resp)
        phone_temp = list(set(tel_resp))
        email_temp_str = ','.join(email_temp)
        phone_temp_str = ','.join(phone_temp)
        log.info(f"{resp} {email} {tel_resp}")
        if len(resp)+len(email)+len(tel_resp) > 0:
            emails.extend(email)
            phones.extend(resp)
            phones.extend(tel_resp)
            results.append({
                'url': url,
                'email': email_temp_str,
                'phoneNumber': phone_temp_str
            })
        # 没有搜到结果的url
        else:
            detail.append({
                'url': url,
                'email': '',
                'phoneNumber': ''
            })
        return phones, emails, results, detail

    def excute_sql(self):
        db = Database(**Configuration.db_config)
        url_detail = {'total': 0, 'detail': []}
        emails = list(set(emails))
        phones = list(set(phones))
        email_str = ','.join(emails)
        phone_str = ','.join(phones)
        log.info(f"去重后的邮件: {email_str}")
        log.info(f"去重后的号码: {phone_str}")
        url_detail['total'] = len(self.total_urls)
        url_detail['detail'].extend(self.results)
        log.info(f"全部url数据:\n{url_detail}")
        db.execute_query(f"insert into `tb_designer_data` (designer, keyword, url, email, phone_number, url_detail) values ('{self.designer}', '{self.keyword}', '{json.dumps(self.results)}', '{email_str}', '{phone_str}', '{json.dumps(url_detail)}')")


if __name__ == '__main__':
    # designer = input('请输入设计师姓名:')
    # keyword = input('请输入搜索关键字:')
    # page_num = int(input('请输入需要爬取多少页:'))
    spider = BaiduSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.mainmain())
    print(spider.total_urls)
    # spider.bp.open('https://www.baidu.com')
    # spider.set_baidu_cookie()
    # spider.bp.wait(2)
    # spider.bp.quit()
    # async def parse(url):
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url, headers={'User-Agent': UserAgent().random}) as r:
    #             await print(r.headers)
    
    # parse('http://www.baidu.com/link?url=7oU33D4vAnC7u_wD_g6d1yVnXH5MEji6xb9bFqZA8Ghhjlb1SfRXbW3cUvsu8q5QqK1v7IegCEBQBLLyeaDOpPmeqMW8NQ_iDiTMCHujDjC')