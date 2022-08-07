from mzkj_automation.common.configuration import Configuration
from mzkj_automation.api.common_api import CommonApi
from mzkj_automation.api.backfront_api import BackfrontApi
from selenium.webdriver.chrome.options import Options
from mzkj_automation.common.log_service import LogService
import yaml
import time
log = LogService(__name__).log()


class Util:
    # current_path = os.path.dirname(__file__)
    # parent_path = os.path.dirname(current_path)

    @staticmethod
    def read_yaml(path):
        # log.info(f"当前yaml路径是 {path}")
        with open(path, encoding='utf-8', mode='r') as f:
            value = yaml.load(f, Loader=yaml.FullLoader)
            return value

    def read_key(self, path, key):
        resp = self.read_yaml(path)
        return resp[key]

    def del_key(self, path, *args):
        resp = self.read_yaml(path)
        if len(args):
            log.info(f'删除extract.yaml中的 {args}')
            for item in args:
                # 确保yaml中有这个字段
                if item in resp:
                    del resp[item]
        self.write_yaml(path, resp, 'w')

    @staticmethod
    def clear_yaml(path):
        with open(path, encoding='utf-8', mode='w') as f:
            f.truncate()

    @staticmethod
    def write_yaml(path, data, mode='a'):
        log.info(f"当前yaml路径是 {path}")
        with open(path, encoding='utf-8', mode=mode) as f:
            yaml.dump(data, f, allow_unicode=True)

    @staticmethod
    def config_navigator(is_headless, is_mobile=False):
        """配置chromedriver的无头属性和移动端属性"""
        chrome_options = Options()
        chrome_options.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--disable-gpu')
        if is_headless:
            chrome_options.add_argument('--headless')
        if is_mobile:
            mobile_emulation = {'deviceName': 'iPhone 6/7/8'}
            chrome_options.add_experimental_option(
                'mobileEmulation', mobile_emulation)
        return chrome_options

    @staticmethod
    def is_expire(target_time):
        """True:过期,False:没过期 """
        now_time = int(time.time())
        return True if now_time > int(target_time) else False

    @staticmethod
    def to_struct_time(timestamp):
        """将时间戳转换成具体格式"""
        t = int(timestamp)
        local_time = time.localtime(t)
        str_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
        return str_time
 
    def user_login(self, username, password, cont='customer'):
        identity = cont if cont == 'customer' else 'architect'
        access_token = ''
        account_info = ''
        try:
            expire_time = self.read_key(Configuration.extract_path, identity+'_expire_time')
            if self.is_expire(expire_time):
                log.info(f"{cont} token已过期,请重新获取")
                self.del_key(Configuration.extract_path, identity+'_expire_time', identity+'_expire_date', identity+'_result', identity+'_token')
            access_token = self.read_key(Configuration.extract_path, identity+'_token')
            account_info = self.read_key(Configuration.extract_path, identity+'_result')
        except Exception as e:
            resp = CommonApi().login(username, password)
            result = resp['result']
            token = result['token']
            access_token = '"' + token + '"'
            account_info = f"{result}"
            expire = int(time.time()) + 7*24*3600
            expire_date = self.to_struct_time(expire)
            self.write_yaml(Configuration.extract_path, {
                            identity+'_token': access_token, identity+'_result': result, identity+'_expire_time': expire, identity+'_expire_date': expire_date})
        finally:
                # script = f"""
                #     accountInfo = {account_info}
                #     accessToken = '{access_token}'
                #     console.log(accountInfo, accessToken)
                #     localStorage.setItem('accountInfo', JSON.stringify(accountInfo))
                #     localStorage.setItem('accessToken', accessToken)
                # """
                # self.driver.execute_script(script)
            return access_token, account_info
        
    def admin_login(self, username, password):
        """
        @description: 管理员账号,只要记录个Authorization
        """
        access_token = ''
        try:
            expire_time = self.read_key(Configuration.extract_path, 'admin_expire_time')
            if self.is_expire(expire_time):
                log.info(f"admin token已过期,请重新获取")
                self.del_key(Configuration.extract_path, 'admin_token', 'admin_expire_date', 'admin_expire_time')
            access_token = self.read_key(Configuration.extract_path, 'admin_token')
        except Exception as e:
            resp = BackfrontApi().login(username, password)
            access_token = resp['result']['accessToken']['token']
            expire = int(time.time()) + 7*24*3600
            expire_date = self.to_struct_time(expire)
            self.write_yaml(Configuration.extract_path, {
                            'admin_token': access_token, 'admin_expire_time': expire, 'admin_expire_date': expire_date})
        finally:
            return access_token
