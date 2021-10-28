import pytest
from automation.cases.common.util import Util


# @pytest.fixture(scope='session', name='login-fixture', autouse=True)
# def login():
#     """客户账号登录在extract.yaml中记录token"""
#     data = {'account': '13761401814', 'password': 'ccad2020'}
#     resp = Util().send_request('post', Util().get_real_path('/customer/user/login'), data=data)
#     print(resp.text)
#     Util().write_yaml('extract.yaml', {'token': resp.json()['result']['token'], 'id': resp.json()['result']['id']})