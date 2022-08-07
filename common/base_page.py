from automation.common.util import log
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import traceback


class BasePage:
    def __init__(self, driver: webdriver.Chrome):
        log.info(f'开始初始化浏览器')
        self.driver = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def locate_elements(self, name, value):
        elements = self.driver.find_elements(name, value)
        return elements

    def locate_element(self, name, value):
        log.info(f'正在定位元素 {name} 元素值 {value}')
        element = self.driver.find_element(name, value)
        return element

    def open(self, url):
        try:
            log.info(f'正在打开 {url}')
            self.driver.get(url)
        except Exception as e:
            log.error(f"打开页面异常: \n {traceback.format_exc()}")

    def on_input(self, name, value, text):
        try:
            log.info(f'正在定位 {name} 元素,元素值 {value},输入的内容 {text}')
            element = self.locate_elements(name, value)[0]
            if element:
                element.send_keys(text)
        except Exception as e:
            log.error(f'输入内容失败 {traceback.format_exc()}')

    def on_click(self, name, value):
        try:
            log.info(f'正在定位 {name} 元素,元素值 {value},点击')
            element = self.locate_elements(name, value)[0]
            log.info(f"is_displayed: {element.is_displayed()}")
            if element:
                element.click()
        except Exception as e:
            log.error(f"点击元素异常: \n {traceback.format_exc()}")

    @staticmethod
    def wait(t, info=""):
        log.info(f'正在等待 {t} 秒, {info}')
        time.sleep(t)

    def open_new_page(self, url):
        try:
            log.info(f'正在打开新标签页 {url}')
            script = 'window.open("' + url + '")'
            self.driver.execute_script(script)
        except Exception as e:
            log.error(f"打开新页面异常: \n {traceback.format_exc()}")

    def switch_page(self, page_index):
        handles = self.driver.window_handles
        log.info(f'切换当前页面句柄到handles[{page_index}]')
        self.driver.switch_to.window(handles[page_index])

    def quit(self):
        log.info('正在关闭整个浏览器')
        self.driver.quit()

    def close(self):
        log.info('正在关闭某个标签页')
        self.driver.close()

    def refresh(self):
        log.info('正在刷新当前页')
        self.driver.refresh()

    @staticmethod
    def inner_locator(el, name, value):
        log.info(f"正在定位 {name} 元素,元素值为 {value}")
        element = el.find_element(name, value)
        return element

    def inner_click(self, el, name, value):
        element = self.inner_locator(el, name, value)
        log.info(f"正在点击 {value}")
        element.click()

    def save_screen_shot(self, path):
        log.info(f"正在截屏 图片存放在 {path}")
        self.driver.save_screenshot(path)

    def execute_script(self, script):
        log.info('正在执行JS')
        self.driver.execute_script(script)

    def move_to_element(self, name, value):
        log.info(f"鼠标正在移到 {name} 元素,元素值为 {value}")
        ActionChains(self.driver).move_to_element(self.locate_element(name, value)).perform()

    def mouse_click(self, name, value):
        el = self.locate_element(name, value)
        log.info(f"鼠标正在点击 {name} 元素,元素值为 {value}")
        ActionChains(self.driver).click(el).perform()

    def wait_element_visibility(self, name, value, timeout=15, poll_frequency=0.5):
        log.info(f"等待 {name} 元素, 元素值为 {value} 存在")
        WebDriverWait(self.driver, timeout=timeout, poll_frequency=poll_frequency).until(expected_conditions.presence_of_all_elements_located(name, value))
    