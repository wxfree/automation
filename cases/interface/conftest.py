import pytest
from automation.cases.common.util import Util
import os

current_path = os.path.dirname(__file__)
parent_path = os.path.dirname(current_path)
util = Util()


@pytest.fixture(scope='function', name='获取登录token', autouse=False)
def login():
    """客户账号登录在extract.yaml中记录token"""
    if util.read_yaml(parent_path + '/extract.yaml'):
        return
    data = {'account': '13761401814', 'password': 'ccad2020'}
    resp = util.send_request('post', util.get_real_path('/customer/user/login'), data=data)
    print(resp.text, resp.json())
    util.write_yaml(parent_path + '/extract.yaml', {'token': resp.json()['result']['token']})


@pytest.fixture(scope='session', name='command_sql')
def execute_sql():
    print('所有用例前执行一次')
    yield
    print('所有用例后执行一次')
