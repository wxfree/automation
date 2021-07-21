from selenium import webdriver
import time
# 下面这块可以加快webdriver打开网页的速度，但是会增加结果的反复变化
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# desired_capabilities = DesiredCapabilities.CHROME
# desired_capabilities["pageLoadStrategy"] = "none"


def login_and_check(username, password):
    wd = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe')
    wd.maximize_window()
    wd.implicitly_wait(10)
    # 正式环境
    # wd.get('http://www.coolarch.net/html/home/home.html')
    # 测试环境
    wd.get('http://106.14.40.137:8080/home/home.html')
    login = wd.find_element_by_xpath('//nav/div/ul/li/a[text()="登录"]')
    login.click()

    account = wd.find_element_by_id('loginTel')
    if username is not None:
        account.send_keys(username)

    pwd = wd.find_element_by_id('loginPass')
    if password is not None:
        pwd.send_keys(password)

    login_btn = wd.find_element_by_xpath('//div/button[text()=" 登录 "]')
    login_btn.click()

    error_msg = wd.find_element_by_css_selector('#loginForm .text-danger')
    # 此处必须将报错信息内容提前存好，不然会报错
    alert_msg = error_msg.text
    time.sleep(2)
    wd.quit()
    return alert_msg


def login_success(username, password):
    wd = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe')
    wd.maximize_window()
    wd.implicitly_wait(10)
    wd.get('http://www.coolarch.net/html/home/home.html')
    login = wd.find_element_by_xpath('//nav/div/ul/li/a[text()="登录"]')
    login.click()

    account = wd.find_element_by_id('loginTel')
    if username is not None:
        account.send_keys(username)

    pwd = wd.find_element_by_id('loginPass')
    if password is not None:
        pwd.send_keys(password)

    login_btn = wd.find_element_by_xpath('//div/button[text()=" 登录 "]')
    login_btn.click()
    # 登录成功就能获取accessToken和accountInfo 登录信息
    access_token = wd.execute_script('return localStorage.getItem("accessToken")')
    account_info = wd.execute_script('return localStorage.getItem("accountInfo")')
    # 将该信息存入文件中，以便下次获取登录信息
    with open('./data/logininfo.txt', 'w') as f:
        f.write(f'{access_token}\n{account_info}')
        f.close()
