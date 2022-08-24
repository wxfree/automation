import os


class Configuration:
    PROJECT_NAME = 'automation'
    # 正式环境
    PROD_HOST = 'http://www.coolarch.net/html'
    # 测试环境
    DEV_HOST = 'http://106.14.40.137:8080'
    # 配置当前环境
    HOST = DEV_HOST
    # 配置移动端还是PC端
    MOBILE = False
    # 配置是否无头浏览器
    HEADLESS = False
    # 获取文件目录
    cur_path = os.path.abspath(os.path.dirname(__file__))
    # 获取项目根路径，内容为当前项目的名字
    root_path = cur_path[:cur_path.find(PROJECT_NAME)+len(PROJECT_NAME)]
    # extract.yaml路径
    extract_path = root_path + '/extract.yaml'
    db_config = {
        'host': 'rm-uf6a335vgas97gum8ko.mysql.rds.aliyuncs.com',
        'user': 'wangxin',
        'password': 'wangxin',
        # 'database': 'mzkj_dev',
        'database': 'mzkj_extend'
    }
