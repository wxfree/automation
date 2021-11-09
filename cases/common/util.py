import yaml
import requests
import logging

class Util:
    host = 'http://106.14.40.137:8080'
    # host = 'https://www.coolarch.net'
    session = requests.session()

    @classmethod
    def read_yaml(cls, path):
        with open(path, encoding='utf-8') as f:
            res = yaml.load(f, Loader=yaml.FullLoader)
            return res

    @classmethod
    def clear_yaml(cls, path):
        with open(path, encoding='utf-8', mode='w') as f:
            f.truncate()

    @classmethod
    def write_yaml(cls, path, data):
        with open(path, encoding='utf-8', mode='a') as f:
            yaml.dump(data, stream=f, allow_unicode=True)

    @classmethod
    def send_request(cls, method, url, data=None, **kwargs):
        method = str(method).lower()
        resp = None
        if method == 'get':
            resp = Util.session.get(url, params=data, **kwargs)
        else:
            resp = Util.session.request(method, url, data=data, **kwargs)
        return resp

    @classmethod
    def get_real_path(cls, route):
        """拼接完整的接口地址"""
        return cls.host + route

    @staticmethod
    def set_log():
        logger = logging.getLogger()
        formatter = logging.Formatter('%(asctime)s  %(pathname)s[line:%(lineno)d]  %(levelname)s: %(message)s')
        sh = logging.StreamHandler()
        logger.addHandler(sh)
        sh.setFormatter(formatter)
        fh = logging.FileHandler('log.txt', encoding='utf-8')
        logger.addHandler(fh)
        fh.setFormatter(formatter)
        return logger


if __name__ == '__main__':
    util = Util()
    print(util.read_yaml('test.yaml')['token'])
