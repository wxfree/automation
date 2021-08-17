import requests
import json
import logging
# python -m pytest cases/interface/test_customer.py::TestCustomerInterface::test_interface0003 -sv


class TestCustomerInterface:
    def setup_class(self):
        print('\n类开始了')
        # logging.basicConfig(filename=r'D:\wangxin\automation\spider\data\log.txt', filemode='a', level=logging.DEBUG,
        #                     format='%(asctime)s | %(filename)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        # -------------------------------------------------调用登录接口获取登录信息-------------------------------------------------------
        # data = {'account': '13761401822', 'password': 'ccad2020'}
        # resp = requests.post('http://106.14.40.137:8080/customer/user/login', data=data)
        # json_resp = json.loads(resp.text)
        # self.token = json_resp['result']['token']
        # self.headers = {
        #     'X-Access-Token': self.token
        # }
        # print(self.token)
        # ----------------------------------------------------------------------------------------------------------------------------
        self.headers = {
            'X-Access-Token': 'eyJhbGciOiJIUzUxMiIsInppcCI6IkdaSVAifQ.H4sIAAAAAAAAAKtWKi5NUrJSMjQxMjE1MzK0MDGxMLY0MjMwNFPSUUqtKFCyMjQzsjS3sDA0MNFRKi1OLQqpLEhVsjKuBQBf1GkoOwAAAA.gl6WNuea8MGBdU81jcP35rG7n-1_qnwMq-FJDsC1B9LQKC5bnH8hX19SJlDc4z6BOoD3NzgO9g6wKvRmEdw2Ig'
        }


    @classmethod
    def teardown_class(cls):
        print('\n类结束了')

    def setup_method(self):
        print('\n方法开始了')

    def teardown_method(self):
        print('\n方法结束了')

    def req(self, method, path, data={}):
        url = 'http://106.14.40.137:8080' + path
        if method == 'get':
            resp = requests.request(method, url, params=data, headers=self.headers)
        else:
            resp = requests.request(method, url, data=data, headers=self.headers)
        logging.info(resp.text)
        if resp.status_code == 200:
            json_resp = json.loads(resp.text)
            return json_resp
        else:
            return {'code': -1, 'msg': '请求失败'}

    def test_interface0001(self):
        """关注建筑师作品"""
        resp = self.req('get', '/customer/boss/personal/designerCases/list')
        assert resp['code'] == 200

    def test_interface0002(self):
        """关注的文章"""
        resp = self.req('get', '/customer/boss/personal/article/list')
        assert resp['code'] == 200

    def test_interface0003(self):
        """关注的建筑师"""
        resp = self.req('get', '/customer/boss/personal/designer/list')
        assert resp['code'] == 200

    def test_interface0004(self):
        """进行中的项目"""
        resp = self.req('get', '/customer/boss/personal/project/proceeding')
        assert resp['code'] == 500

    def test_interface0005(self):
        """已完结的项目"""
        resp = self.req('get', '/customer/boss/personal/project/finished')
        assert resp['code'] == 500

    # def test_interface0006(self):
    #     """查看任务书"""
    #     resp = self.req('get', '/customer/boss/personal/project/taskFile/catTask')
    #     assert resp['code'] == 500
    #
    # def test_interface0007(self):
    #     """签署确认客户设计任务书"""
    #     resp = self.req('put', '/customer/boss/personal/project/taskFile/signBossRequiredTaskFile')
    #     assert resp['code'] == 500
    #
    # def test_interface0008(self):
    #     """查看代理合同"""
    #     resp = self.req('get', '/customer/boss/personal/project/contract/agencyContract')
    #     assert resp['code'] == 500
