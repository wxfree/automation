from automation.common.log_service import LogService
import requests
log = LogService(__name__).log()


class Req:
    def __init__(self, token_key=None, token=None):
        self.session = requests.Session()
        if token_key and token:
            self.session.headers.update({token_key: token})

    def send_request(self, method, url, data=None, files=None, **kwargs):
        method = str(method).lower()
        resp = None
        if method == 'get':
            resp = self.session.get(url, params=data, **kwargs)
        else:
            resp = self.session.request(
                method, url, data=data, files=files, **kwargs)
        log.info(
            f'\n请求方法:{resp.request.method}\n请求地址:{resp.request.url}\n请求参数:{data}\n请求结果:{resp.text}\n请求头:{resp.request.headers}')
        if files:
            log.info(f"\n请求文件参数:{files}")
        return resp
