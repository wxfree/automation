import yaml
import os


class YamlUtil:
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file

    def read_yaml(self):
        with open(self.yaml_file, encoding='utf-8') as f:
            value = yaml.load(f, Loader=yaml.FullLoader)
            return value


if __name__ == '__main__':
    res = YamlUtil('./test.yaml').read_yaml()
    print(res, res['result'][0]['name'])
    print(os.getcwd())
    print(os.path.abspath(__file__))
    print(os.path.dirname(__file__))
    print(os.path.dirname)
    print(__file__)
