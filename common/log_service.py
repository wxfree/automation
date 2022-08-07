import logging
from automation.common.configuration import Configuration
import time


class LogService:
    def __init__(self, logger_name=None) -> None:
        """错误等级debug,info,warning,error,critical"""
        self.logger = logging.getLogger(logger_name)
        formatter = logging.Formatter(
            '%(asctime)s  %(filename)s[line:%(lineno)d]  %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        self.logger.addHandler(sh)
        sh.setFormatter(formatter)
        # 文件日志输出到年月日.log文件下
        fh = logging.FileHandler(Configuration.root_path + f'/log/{time.strftime("%Y%m%d")}.log', encoding='utf-8')
        self.logger.addHandler(fh)
        fh.setFormatter(formatter)

    def log(self):
        return self.logger