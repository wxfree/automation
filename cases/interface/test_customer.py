from automation.cases.common.util import Util
import pytest
import allure
import os
# python -m pytest cases/inter/test_customer.py::TestCustomerInterface::test_interface0003 -sv


@pytest.mark.usefixtures('command_sql')
class TestCustomerInterface(Util):
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)

    @allure.feature('客户相关接口')
    @pytest.mark.usefixtures('获取登录token')
    @pytest.mark.parametrize('args', Util.read_yaml(current_path+'/customer.yaml'))
    def test_customer_interface(self, args):
        allure.dynamic.title(args['name'])
        method = args['request']['method']
        route = args['request']['url']
        data = args['request']['params']
        resp = self.send_request(method=method, url=self.get_real_path(route), data=data, headers=self.get_header())
        print(resp.text)
        assert resp.json()['code'] == 200

    def get_header(self):
        return {'X-Access-Token': self.read_yaml(self.parent_path+'/extract.yaml')['token']}

    @allure.epic('数学法则')
    @allure.feature('加法法则')
    @allure.story('两数相加')
    def test_plus(self):
        allure.dynamic.title('测试加法')
        with allure.step('first step:获取第一个加数'):
            a = 2
        with allure.step('second step：获取第二个加数'):
            b = 3
        with allure.step('third step：获取加法的和'):
            answer = a + b
        # allure.attach(body, name)
        allure.attach(f'a={a},b={b},结果为{answer}', '参数', allure.attachment_type.TEXT)
        assert answer == 4


if __name__ == '__main__':
    pytest.main(['-sv'])
