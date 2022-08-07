import os


class Configuration:
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
    # extract.yaml路径
    extract_path = os.getcwd() + '/extract.yaml'
    # root_path项目根目录
    root_path = os.getcwd()
    db_config = {
        'host': 'rm-uf6a335vgas97gum8ko.mysql.rds.aliyuncs.com',
        'user': 'wangxin',
        'password': 'wangxin',
        # 'database': 'mzkj_dev',
        'database': 'mzkj_extend'
    }
