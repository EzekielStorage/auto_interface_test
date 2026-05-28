# -*- coding: utf-8 -*-
__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'
"""
序列化和反序列化类
"""
import json
import logging

import jsonpath


def json_loads(content):
    """
    反序列化
        json对象 -> python数据类型
    """
    try:
        if content.strip().startswith('{') or content.strip().startswith('['):
            content = content.replace("'", '"')
        return json.loads(content)
    except json.JSONDecodeError as e:
        # 记录错误信息，便于调试
        logging.error(f"JSON解析失败: {e}")
        logging.error(f"错误内容: {content}")
        raise


def dumps(content, ensure_ascii=True):
    """
    序列化
        python数据类型 -> json对象
    """
    # return json.dumps(content, ensure_ascii=ensure_ascii)
    return json.dumps(content, ensure_ascii=ensure_ascii, separators=(',', ':'))

def is_json_str(string):
    """验证是否为json字符串"""
    try:
        json.loads(string)
        return True
    except:
        return False


def get_json_value(key, string):
    """
    读取jsonpath格式的测试用例
    """
    try:
        json_data = json_loads(string)
        # 移除单引号、双引号、空格
        result = jsonpath.jsonpath(json_data, key)
        logging.debug("jsonpath结果值：{}={}".format(key, result))
        return result[0] if result else None
    except:
        logging.exception("Error: testCase Invalid JSON string")
        return None
