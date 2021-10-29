from automation.cases.common.util import Util
import pytest
import allure
import os
# python -m pytest cases/inter/test_customer.py::TestCustomerInterface::test_interface0003 -sv


class TestCustomerInterface(Util):
    current_path = os.path.dirname(__file__)
    parent_path = os.path.dirname(current_path)

    @pytest.mark.parametrize('args', Util.read_yaml(current_path+'/customer.yaml'))
    def test_customer_interface(self, args):
        print(os.path.dirname(__file__))
        allure.dynamic.title(args['name'])
        method = args['request']['method']
        route = args['request']['url']
        data = args['request']['params']
        resp = self.send_request(method=method, url=self.get_real_path(route), data=data, headers=self.get_header())
        print(resp.text)
        assert resp.json()['code'] == 200

    def get_header(self):
        return {'X-Access-Token': self.read_yaml(TestCustomerInterface.parent_path+'/extract.yaml')['token']}
    #
    # def test_path(self):
    #     print(os.path.dirname(__file__))


if __name__ == '__main__':
    pytest.main(['-sv'])
