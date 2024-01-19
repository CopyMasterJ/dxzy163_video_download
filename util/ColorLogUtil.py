import logging
import os
import time
import colorlog
from logging.handlers import RotatingFileHandler

# 创建文件目录
cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个
# 修改log保存位置
timestamp = time.strftime("%Y-%m-%d", time.localtime())
logfile_name = '%s.log' % timestamp
logfile_path = os.path.join(log_path, logfile_name)
# 定义不同日志等级颜色
log_colors_config = {
    'DEBUG': 'bold_white',
    'INFO': 'bold_cyan',
    'WARNING': 'bold_yellow',
    'ERROR': 'bold_red',
    'CRITICAL': 'bold_red'
}

default_formats = {
    # 终端输出格式
    'color_format': '%(log_color)s%(asctime)s [%(filename)s:%(funcName)s: %(thread)d] L:%(lineno)d [%(levelname)s]: %(message)s',
    # 日志输出格式
    'log_format': '%(asctime)s [%(filename)s:%(funcName)s: %(thread)d] L:%(lineno)d [%(levelname)s]: %(message)s'
}


class Logger(logging.Logger):
    def __init__(self, name, level='INFO', file=None, encoding='utf-8'):
        super().__init__(name)
        self.encoding = encoding
        self.file = file
        self.level = level
        # 针对所需要的日志信息 手动调整颜色
        console_formatter = colorlog.ColoredFormatter(
            default_formats["color_format"],
            reset=True,
            log_colors=log_colors_config
        )  # 日志输出格式
        rotating_formatter = logging.Formatter(default_formats["log_format"])  #
        # 创建一个FileHandler，用于写到本地
        rotating_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=logfile_path,when='D',  backupCount=3, encoding='utf-8')
        rotating_file_handler.setFormatter(rotating_formatter)
        rotating_file_handler.setLevel(logging.DEBUG)
        self.addHandler(rotating_file_handler)
        # 创建一个StreamHandler,用于输出到控制台
        console = colorlog.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(console_formatter)
        self.addHandler(console)
        self.setLevel(logging.DEBUG)


logger = Logger(name=logfile_path, file=logfile_path)
