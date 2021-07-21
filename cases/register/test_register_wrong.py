from selenium import webdriver
import time
import pytest
# 注册 最先判定是否点选已阅读并接受《用户协议》
# 错误提示在每一行<div class="invalid-feedback"></div>中显示，如果里面有提示就是有问题，从上到下排列
# python -m pytest cases/register/test_register_wrong.py::TestWrongRegister::test_r0014 -sv
# 2021-07-12更新了classmethod前置后置方法，只打开一次浏览器，会造成数据未清空，断言失效问题。解决方式：提取注册条件的属性
# 注意：脚本错误很可能是元素没有找到造成的。要注意同样的注册有多个地方存在


class TestWrongRegister:
    @classmethod
    def setup_class(cls):
        # cls.driver = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe')
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        # 正式环境
        # self.driver.get('http://www.coolarch.net/html/home/home.html')
        # 测试环境
        cls.driver.get('http://106.14.40.137:8080/home/home.html')

    @classmethod
    def teardown_class(cls):
        time.sleep(3)
        cls.driver.quit()

    def setup_method(self):
        register_btn = self.driver.find_element_by_xpath('//div/ul/li/a[text()="注册"]')    # 这是调出注册弹框的按钮
        register_btn.click()

    def teardown_method(self):
        time.sleep(3)
        close_btn = self.driver.find_element_by_xpath('//*[@id="cardLR"]/div[2]/div/button')
        close_btn.click()

    @pytest.mark.ui
    def test_r0001(self):
        """没有点选用户协议"""
        dic = {'phone': '13761401814', 'password': '', 'confirmPassword': '', 'identity': ' 我是建筑师    '}
        res = self.register(**dic)
        assert res == '请先阅读并接受《用户协议》'

    @pytest.mark.ui
    def test_r0002(self):
        """手机号/邮箱号错误"""
        dic = {'phone': '1376140181', 'validateCode': '', 'password': '', 'confirmPassword': '', 'identity': ' 我是客户    '}
        self.read()
        res = self.register(**dic)
        assert res == '请输入有效的手机号码或邮箱地址'

    def test_r0003(self):
        """手机号/邮箱号为空"""
        dic = {'phone': '1376140181', 'validateCode': '', 'password': '', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '请输入有效的手机号码或邮箱地址'

    def test_r0004(self):
        """验证码为空"""
        dic = {'phone': '13761401814', 'validateCode': '', 'password': '', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '不能为空'

    def test_r0005(self):
        """验证码小于6位"""
        dic = {'phone': '13761401814', 'validateCode': '1234', 'password': '', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '验证码是6位数字'

    def test_r0006(self):
        """验证码小于6位"""
        dic = {'phone': '13761401814', 'validateCode': '1234aa', 'password': '', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '验证码是6位数字'

    def test_r0007(self):
        """密码为空"""
        dic = {'phone': '13761401814', 'validateCode': '123456', 'password': '', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '不能为空'

    def test_r0008(self):
        """密码小于8位"""
        dic = {'phone': '13761401814', 'validateCode': '123456', 'password': 'aacd202', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '密码至少8位，且必须包含字母和数字'

    def test_r0009(self):
        """密码大于8位，都是数字"""
        dic = {'phone': '13761401814', 'validateCode': '123456', 'password': '111111112', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '密码至少8位，且必须包含字母和数字'

    def test_r0010(self):
        """密码大于8位，都是字母"""
        # 密码可以有特殊字符
        dic = {'phone': '13761401814', 'validateCode': '123456', 'password': 'asdssaddsd', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '密码至少8位，且必须包含字母和数字'

    def test_r0011(self):
        """密码正确，确认密码为空"""
        # 密码可以有特殊字符
        dic = {'phone': '13761401814', 'validateCode': '123456', 'password': 'aacd()121', 'confirmPassword': ''}
        self.read()
        res = self.register(**dic)
        assert res == '不能为空'

    def test_r0012(self):
        """密码正确，确认密码符合有数字有字母大于8位，但是跟密码不一样"""
        # 密码可以有特殊字符
        dic = {'phone': '13761401814', 'validateCode': '123456', 'password': 'aacd()121', 'confirmPassword': 'aacd()1213'}
        self.read()
        res = self.register(**dic)
        assert res == '两次密码输入不一致'

    def test_r0013(self):
        """密码正确，确认密码符合有数字有字母大于8位，但是跟密码不一样"""
        # 密码可以有特殊字符
        dic = {'phone': '13761401814', 'validateCode': '123456', 'password': 'aacd()121', 'confirmPassword': 'aaaa'}
        self.read()
        res = self.register(**dic)
        assert res == '密码至少8位，且必须包含字母和数字,两次密码输入不一致'

    def test_r0014(self):
        """密码正确，确认密码符合有数字有字母大于8位，但是跟密码不一样"""
        # 密码可以有特殊字符
        dic = {'phone': '13761401814', 'validateCode': '123456', 'password': 'aacd()121', 'confirmPassword': '11111aa'}
        self.read()
        res = self.register(**dic)
        assert res == '密码至少8位，且必须包含字母和数字,两次密码输入不一致'

    def register(self, *args, **kwargs):
        """需要这些字段phone, validateCode, password, confirmPassword, identity"""
        if 'phone' in kwargs:
            self.driver.find_element_by_id('signupTel').send_keys(kwargs['phone'])
        if 'validateCode' in kwargs:
            self.driver.find_element_by_id('signupCode').send_keys(kwargs['validateCode'])
        if 'password' in kwargs:
            self.driver.find_element_by_id('signupPass').send_keys(kwargs['password'])
        if 'confirmPassword' in kwargs:
            self.driver.find_element_by_id('signupConfirmPass').send_keys(kwargs['confirmPassword'])
        if 'identity' in kwargs:
            # 此处无法直接点击input的xpath，所以选择使用js点击方法选中
            self.driver.execute_script('document.querySelectorAll("#signupForm > div:nth-child(5) > div > div.select-wrapper.mdb-select.colorful-select.dropdown-primary > input")[0].click()')
            time.sleep(1)
            # wd.find_element_by_xpath('//span[text()=" 我是客户    "]').click()
            choice = kwargs['identity']
            self.driver.find_element_by_xpath(f'//span[text()="{choice}"]').click()

        self.driver.find_element_by_xpath('//div/button[text()=" 注册 "]').click()
        msg = ''
        # display:none的东西selenium扒不出来
        # feedbacks = self.driver.find_elements_by_css_selector('#signupForm .invalid-feedback')
        # print(feedbacks)
        # for feedback in feedbacks:
        #     print('feedback', feedback.text)
        #     if feedback.text:
        #         msg = feedback.text.strip()
        self.driver.execute_script('msg="";feedbacks = document.querySelectorAll("#signupForm .invalid-feedback");'
                                   'for (i=0;i<feedbacks.length;i++){'
                                   'if (feedbacks[i].innerText){'
                                   'msg = feedbacks[i].innerText;break}'
                                   '}')
        msg = self.driver.execute_script('return msg')
        error_msg = self.driver.find_element_by_css_selector('#signupForm .text-danger').text.strip()
        # print('hello python', error_msg, msg)
        # 默认先返回没看用户协议的错误，如果点了，返回其他乱七八糟的错误
        return error_msg if error_msg else msg

    def read(self):
        """点选已阅读用户协议"""
        self.driver.find_element_by_css_selector('#signupForm .form-check-label').click()


