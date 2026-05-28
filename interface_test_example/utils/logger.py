__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'
"""
    日志
"""
import os,logging
from logging.handlers import RotatingFileHandler
from utils.time import getTimestamp

def init_logger():
    """初始化日志"""
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    now_date = getTimestamp()
    debug_file = os.path.join(basedir, 'logs', f'{now_date}.log')

    logger_formatter = logging.Formatter(
        '%(levelname)s %(asctime)s [%(filename)s:%(lineno)s] %(thread)d %(message)s')

    # debug
    logger_debug = logging.getLogger('apitest')
    handler_debug = RotatingFileHandler(debug_file,
                                        encoding='utf-8',
                                        maxBytes=20 * 1024 * 1024,
                                        backupCount=10)
    handler_debug.setFormatter(logger_formatter)
    logger_debug.setLevel(logging.DEBUG)
    logger_debug.addHandler(handler_debug)
    # 在控制台输出
    return logger_debug


logger = init_logger()

if __name__ == '__main__':
    logger.debug("debug")
    logger.info("info")
    logger.warning('warning')
    logger.error("error")
    logger.critical('critical')