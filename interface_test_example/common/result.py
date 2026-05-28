# -*- coding: utf-8 -*-
__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'
"""
response响应处理
"""
import allure
import pytest

from common.cache import cache
from common.regular import re, get_var
from utils.logger import logger
from .json_defind import get_json_value


def check_results(r, validate):
    """检查运行结果
        1. 验证接口是否正常: expectCode
        2. 验证测试数据在返回结果中: checkResultsIn
        3. 验证测试数据不在返回结果中: checkResultsInNotIn
        4. 正则校验指定字段：regularCheck，例子：regularCheck: '"author_id":\s*9'
        5. 通过jsonpath格式断言相关字段：resultCheckJsonpath
    """
    from common.cache import cache
    cached_validate = cache.get('last_validate') or {}

    # 如果缓存中有数据，则优先使用缓存数据
    expectCode = validate.get('expectCode', cached_validate.get('expectCode'))
    checkResultsIn = validate.get('checkResultsIn', cached_validate.get('checkResultsIn'))
    checkResultsInNotIn = validate.get('checkResultsInNotIn', cached_validate.get('checkResultsInNotIn'))
    regularCheck = validate.get('regularCheck', cached_validate.get('regularCheck'))
    accountCheck = validate.get('accountCheck', cached_validate.get('accountCheck'))
    resultCheckJsonpath = validate.get('resultCheckJsonpath', cached_validate.get('resultCheckJsonpath'))
    if expectCode:
        with allure.step("校验返回响应码"):
            allure.attach(name='预期响应码', body=str(expectCode))
            allure.attach(name='实际响应码', body=str(r.status_code))
        """判断响应结果是否为200"""
        pytest.assume(expectCode == r.status_code)
    if checkResultsIn:
        with allure.step("校验响应预期值"):
            allure.attach(name='预期值%s' % checkResultsIn, body=str(checkResultsIn))
            allure.attach(name='实际值', body=r.text)
        logger.info("checkResultsIn的数据为：{}".format(checkResultsIn))
        # 多个断言用逗号隔开
        if ',' in checkResultsIn:
            checks = [check.strip() for check in checkResultsIn.split(',')]
            for check in checks:
                pytest.assume(check in r.text)
        else:
            pytest.assume(checkResultsIn in r.text)
    if checkResultsInNotIn:
        with allure.step("校验响应预期值"):
            allure.attach(name='预期值%s' % checkResultsInNotIn, body=str(checkResultsInNotIn))
            allure.attach(name='实际值', body=r.text)
        logger.info("checkResultsInNotIn的数据为：{}".format(checkResultsInNotIn))
        # 多个断言用逗号隔开
        if ',' in checkResultsInNotIn:
            checks = [check.strip() for check in checkResultsInNotIn.split(',')]
            for check in checks:
                pytest.assume(check not in r.text)
        else:
            pytest.assume(checkResultsInNotIn not in r.text)
    if regularCheck:
        with allure.step("正则校验返回结果"):
            allure.attach(name='预期正则', body=regularCheck)
            allure.attach(name='响应值', body=str(
                re.findall(regularCheck, r.text)))
        pytest.assume(re.findall(regularCheck, r.text))
    if accountCheck and checkResultsIn:
        count = r.text.count(checkResultsIn)
        expected_count = int(accountCheck)  # 假设accountCheck是一个整数字符串
        with allure.step("校验响应中关键字出现次数"):
            allure.attach(name='关键字%s' % checkResultsIn, body=checkResultsIn)
            allure.attach(name='预期出现次数%s' % expected_count, body=str(expected_count))
            allure.attach(name='实际出现次数', body=str(count))
        logger.info("关键字 '{}' 在响应中出现了 {} 次".format(checkResultsIn, count))
        pytest.assume(count == expected_count)
    if resultCheckJsonpath:
        with allure.step("JSONPath校验返回结果"):
            # 处理数组情况
            if isinstance(resultCheckJsonpath, list):
                for item in resultCheckJsonpath:
                    if item:  # 跳过空项
                        _validate_jsonpath_item(r, item)
            else:
                _validate_jsonpath_item(r, resultCheckJsonpath)


def get_result(r, extract):
    logger.debug("response test：{}".format(r.text))

    """
        获取值，只是获取接口返回的值，如果缓存中存在改key了就不会再更新，对其他的cache更新没有影响的
        只要不调用这个方法，所以能够完美的跳过${order}这类冲上下文获取值的清空，传一个固定值就是运行指定流程
    """

    for item in extract:
        try:
            logger.debug("正则格式的Extract项：{}".format(item))
            # 判断是否为字典格式的Extract项，如 {"order_no: $.data.order_no"}
            if ":" in item and "$" in item:
                # 处理字典格式的Extract项
                logger.debug("JSONPath格式的Extract项：{}".format(item))
                key = item.split(":")[0].strip()
                jsonpath = item.split(":")[1].strip()
                value = get_json_value(jsonpath, r.text)
                logger.debug("JSONPath格式的value：{},{},{}".format(key,jsonpath,value))
                # 增加None值检查
                if value is not None:
                    cache.set(key, value)
                    pytest.assume(key in cache)
                else:
                    logger.warning(f"未能从响应中提取到值: {key}")
            elif isinstance(item, dict):
                key = list(item.keys())[0]  # 字典格式，取key
                jsonpath = item[key]  # 字典格式，取value
                value = get_json_value(jsonpath, r.text)
                # 增加None值检查
                if value is not None:
                    cache.set(key, value)
                    pytest.assume(key in cache)
                else:
                    logger.warning(f"未能从响应中提取到值: {key}")
            # 调整，Extract传参只能通过jsonpath进行唯一定位，防止先cache中的key命名与responseDate中的字段名重复
            # else:
            #     # 处理字符串格式的Extract项
            #     key = item
            #     value = get_var(key, r.text)
            #     logger.debug("正则提取结果值：{}={}".format(key, value))
            #     cache.set(key, value)
            #     # 断言key是否存在缓存中，如果不存在提示错误
            #     pytest.assume(key in cache)
        except IndexError:
            logger.error(f"提取变量 {item} 时发生索引越界错误")
            pytest.assume(False)
        except Exception as e:
            logger.error(f"提取变量 {item} 时发生错误: {e}")
            pytest.assume(False)
    with allure.step("提取返回结果中的值"):
        for item in extract:
            # 根据Extract项的类型来确定key
            if isinstance(item, dict):
                key = list(item.keys())[0]  # 字典格式，取key
            else:
                key = item.split(":")[0].strip() if ":" in item else item  # 字符串格式，直接使用
            
            # 获取缓存中的值，如果为None则使用默认值
            cached_value = cache.get(key)
            display_value = str(cached_value) if cached_value is not None else "未提取到值"
            
            allure.attach(name="提取%s" % key, body=display_value)


def get_result_data(r, resultData):
    """将接口请求结果存入缓存，key为resultData"""
    import json
    logger.debug("保存接口返回结果：{}".format(r.text))
    with allure.step("保存接口返回结果"):
        allure.attach(name="resultData", body=r.text)

    # 如果resultData为真且响应内容是JSON格式，则处理data字段
    if resultData and r.text:
        try:
            # 解析JSON响应
            response_json = json.loads(r.text)
            # 检查是否存在data字段且为非空数组
            if 'data' in response_json and isinstance(response_json['data'], list) and len(response_json['data']) > 0:
                # 提取data中的第一个元素并存入缓存
                logger.debug("获取data中的第一个元素：{}".format(response_json['data'][0]))

                resultData = response_json['data'][0]
                cache.set('resultData', json.dumps(resultData, ensure_ascii=False))
                logger.debug("保存data中第一个元素：{}".format(cache.get('resultData')))
                with allure.step("保存data中第一个元素"):
                    allure.attach(name="firstDataElement", body=json.dumps(resultData, ensure_ascii=False, indent=2))
        except Exception as e:
            logger.error(f"处理resultData时发生错误: {e}")


def _validate_jsonpath_item(r, item):
    """验证单个JSONPath项"""
    try:
        # 如果item是dict类型，例如 {"$.data[0].status": "1"}
        if isinstance(item, dict):
            key = list(item.keys())[0]
            expected_value = str(item[key])
        else:
            # 清理引号并分割key和value
            clean_item = item.strip().strip('"').strip("'")
            if ':' in clean_item:
                key, expected_value = clean_item.split(':', 1)
                key = key.strip().strip('"').strip("'")
                expected_value = expected_value.strip().strip('"').strip("'")
            else:
                # 如果没有':'分隔符，无法处理
                logger.warning(f"无效的JSONPath格式: {item}")
                pytest.assume(False)
                return
        
        # 解析预期值中的变量
        if expected_value.startswith('${') and expected_value.endswith('}'):
            var_name = expected_value[2:-1]
            cached_value = cache.get(var_name)
            if cached_value is not None:
                expected_value = cached_value
        actual_value = get_json_value(key, r.text)

        allure.attach(name=f'JSONPath表达式', body=key)
        allure.attach(name=f'预期值%s' % key, body=expected_value)
        allure.attach(name=f'实际值%s' % key, body=str(actual_value))
        logger.debug("JSONPath预期结果值：{}={}".format(key, expected_value))
        logger.debug("JSONPath实际结果值：{}={}".format(key, actual_value))
        # 断言：转化为相同类型再比较
        pytest.assume(_compare_values(actual_value, expected_value))

    except Exception as e:
        logger.error(f"JSONPath校验失败: {e}")
        pytest.assume(False)


# 修改为类型转换后比较
def _compare_values(actual, expected):
    # 尝试转换为相同类型再比较
    if isinstance(actual, (int, float)) and isinstance(expected, str):
        try:
            # 尝试将expected转换为数字
            if '.' in expected:
                expected_converted = float(expected)
            else:
                expected_converted = int(expected)
            return actual == expected_converted
        except ValueError:
            pass
    return actual == expected
