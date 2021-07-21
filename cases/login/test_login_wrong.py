import time
from selenium import webdriver
import pytest


# 此处测试登录不触发登录请求，测试登录错误检测
# 测试所有用例    python -m pytest cases -sv
# 单独测试某个用例  python -m pytest cases/login/test_login_wrong.py::TestWrongPwd::test_c0006 -sv
# setup_class前置条件中写driver可以使跑脚本时间降低N多。每次重新打开被控浏览器跑一个用例要将近一分钟
# pytest产生测试报告 python -m pytest cases/login --html=report.html --self-contained-html
# @pytest.mark.xxx 如果不在pytest.ini中配置的，会有warning，mark可以配在class上

@pytest.mark.interface
class TestWrongPwd:
    @classmethod
    def setup_class(cls):
        # cls.driver = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe')
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        # 正式环境
        # self.driver.get('http://www.coolarch.net/html/home/home.html')
        # 测试环境
        cls.driver.get('http://106.14.40.137:8080/home/home.html')

    @classmethod
    def teardown_class(cls):
        """等待3s退出浏览器"""
        time.sleep(3)
        cls.driver.quit()

    def setup_method(self):
        """每个用例开始前点击登录"""
        self.driver.find_element_by_xpath('//nav/div/ul/li/a[text()="登录"]').click()

    def teardown_method(self):
        """每个用例结束前等待3s，关闭登录弹框，达到清空输入数据的目的"""
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="cardLR"]/div[2]/div/button').click()

    def test_c0001(self):
        """输入正确账号，只含有英文"""
        res = self.login_and_check('13761401814', 'aaaaaaaa')
        assert res == '密码至少8位，且必须包含字母和数字'

    def test_c0002(self):
        """输入正确账号，不输入密码"""
        res = self.login_and_check('13761401814', None)
        assert res == '不能为空'

    def test_c0003(self):
        """输入正确账号，只含有数字"""
        res = self.login_and_check('13761401814', '11111111')
        assert res == '密码至少8位，且必须包含字母和数字'

    def test_c0004(self):
        """不输入账号，输入正确密码"""
        res = self.login_and_check(None, 'aacd2020')
        assert res == '不能为空,请输入有效的手机号码或邮箱地址'

    def test_c0005(self):
        """输入非手机号非邮箱，输入正确密码"""
        res = self.login_and_check('1376140', 'aacd2020')
        assert res == '请输入有效的手机号码或邮箱地址'

    def test_c0006(self):
        """输入非手机号，输入正确密码"""
        res = self.login_and_check('1376140', 'aacd2020')
        assert res == '请输入有效的手机号码或邮箱地址'

    def test_c0007(self):
        """输入非手机号，输入错误密码"""
        res = self.login_and_check('1376140', 'aacd202')
        # <br>换行符可以用\n代替
        assert res == '请输入有效的手机号码或邮箱地址\n密码至少8位，且必须包含字母和数字'

    def test_c0008(self):
        """不输入账号，不输入密码"""
        res = self.login_and_check(None, None)
        assert res == '不能为空,请输入有效的手机号码或邮箱地址\n不能为空'

    # def test_c0009(self):
    #     """正确账号密码成功登录"""
    #     res = self.login_and_check('13761401814', 'ccad2020')
    # 这个没有返回会验证错误

    def login_and_check(self, username, password):
        account = self.driver.find_element_by_id('loginTel')
        if username is not None:
            account.send_keys(username)

        pwd = self.driver.find_element_by_id('loginPass')
        if password is not None:
            pwd.send_keys(password)

        login_btn = self.driver.find_element_by_xpath('//div/button[text()=" 登录 "]')
        login_btn.click()

        error_msg = self.driver.find_element_by_css_selector('#loginForm .text-danger')
        # 此处必须将报错信息内容提前存好，不然会报错
        alert_msg = error_msg.text
        time.sleep(2)
        return alert_msg
