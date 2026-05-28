# -*- coding: utf-8 -*-
__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'
"""
    正则处理
"""
import json
import re
from string import Template

from common.cache import cache
from common.json_defind import is_json_str
from utils.logger import logger

"""
    目的：通过json数据中的名称获取名称中对应的值 
    栗子：{"username":"admin"}
    get_var(username, A),获取到admin的信息。
"""


def get_var(key, raw_str):
    """
    获取变量，优先使用JSON解析，回退到正则表达式
    """
    logger.info("jsonpath数据格式key {}".format(key))
    if is_json_str(raw_str):
        try:
            logger.info("json数据格式raw_str {}".format(raw_str))
            # 优先使用JSON解析
            data = json.loads(raw_str)

            def find_key(obj, target_key):
                if isinstance(obj, dict):
                    if target_key in obj:
                        return obj[target_key]
                    for v in obj.values():
                        result = find_key(v, target_key)
                        if result is not None:
                            return result
                elif isinstance(obj, list):
                    for item in obj:
                        result = find_key(item, target_key)
                        if result is not None:
                            return result
                return None

            result = find_key(data, key)
            logger.debug("json数据格式result {}".format(result))
            if result is not None:
                return str(result)
        except:
            pass  # JSON解析失败则回退到正则

    # 回退到正则表达式方法
    patterns = [
        r'"%s":(\d+(?:\.\d+)?)' % key,
        r'"%s":"(.*?)"' % key,
        r'"%s":([^,\}]+)' % key
    ]

    for pattern in patterns:
        match = re.compile(pattern).findall(raw_str)
        if match:
            return match[0]

    # 最后的回退方案
    return re.compile(r'%s' % key).findall(raw_str)[0]


def findalls(string):
    """查找所有需要替换的变量
    输入字符串："Hello, ${name}! Your ID is ${id}."
    假设 cache 中有 name="Alice", id="123"
    返回结果：{'name': 'Alice', 'id': '123'}
    """
    '''
        添加特殊判断，如果获取到的是TOKEN、URL，直接更新缓存中的数据
    '''
    key = re.compile(r"\${(.*?)\}").findall(string)
    res = {k: cache.get(k) for k in key}
    logger.debug("需要替换的变量：{}".format(res))

    return res


def sub_var(keys, string):
    """替换变量，keys 变量字典，将字典的值替换到模板中"""
    s = Template(string)
    res = s.safe_substitute(keys)
    logger.debug("替换结果：{}".format(res))
    return res


if __name__ == '__main__':
    id = 69
    cache.set("id", id)
    print(findalls("Hello, ${name}! Your ID is ${id}."))
