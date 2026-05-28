__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'
"""
    时间处理
"""
import math,time
from datetime import datetime


def getTimestamp():
    """获取时间戳"""
    return math.trunc(time.time())


def get_current_datetime_str():
    """返回当前时间 年月日时分秒格式"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')