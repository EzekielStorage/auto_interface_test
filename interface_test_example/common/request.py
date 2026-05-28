# -*- coding: utf-8 -*-
__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'

import pytest_assume.plugin

"""
requests二次封装
"""
import typing as t
import pytest
from urllib.parse import urljoin

import allure
import urllib3
from requests import Session, Response

from common.cache import cache
from common.json_defind import json_loads, dumps
from common.regular import findalls, sub_var
from utils.change_request_data import change_request_data
from utils.logger import logger

urllib3.disable_warnings()
import json


class HttpRequest(Session):
    """requests方法二次封装"""

    def __init__(self, *args: t.Union[t.Set, t.List], **kwargs: t.Dict[t.Text, t.Any]):
        super(HttpRequest, self).__init__()
        self.exception = kwargs.get("exception", Exception)
        self.trust_env = False  # 可选：不信任环境变量中的代理设置

    def send_request(self, **kwargs: t.Dict[t.Text, t.Any]) -> Response:
        try:
            method = kwargs.get('method', 'GET').upper()
            # 统一使用 urljoin 进行 URL 拼接
            url = urljoin(cache.get('baseurl'), kwargs.get('route', ''))
            """ 就是一个JSON String，python数据类型才能够进行 kwargs.get('RequestData') 对象才会有属性，方法"""
            kwargs_str = dumps(kwargs)
            """ python3.8+ 的海象运算符
                使用海象运算符检查请求参数中是否包含需要替换的变量（如${variable}格式）
                findalls函数会查找所有变量并从缓存中获取对应的值
            """
            logger.info("Request Data 替换前 kwargs_str 内容: {}".format(kwargs_str))
            if is_sub := findalls(kwargs_str):
                try:
                    kwargs = change_request_data(json_loads(format_nested_json(sub_var(is_sub, kwargs_str))))
                    """更新url，之后如果还有遇到特定的传参，需要进行单独处理"""
                    url = urljoin(kwargs.get('baseurl', cache.get('baseurl')), kwargs.get('route', ''))
                    logger.info("Request Url: {}".format(url))
                    # 如果确定 headers 存在且为字典
                    cache.get('headers')['authorization'] = kwargs.get('authorization')
                    logger.info("Request Data json_loads后的数据: {}".format(kwargs))
                    # 判断如果调用的接口中包含update_requests_data.yaml文件中的接口，那么就将接口中的传参进行替换

                except json.JSONDecodeError as e:
                    logger.error(f"变量替换后JSON解析失败: {e}")
            logger.debug("获取kwargs中RequestData ：{}".format(kwargs.get('RequestData', {})))
            request_data = HttpRequest.mergedict(kwargs.get('RequestData', {}),
                                                 headers=cache.get('headers'),
                                                 timeout=cache.get('timeout'))
            # 添加禁用代理的配置
            request_data['proxies'] = {
                'http': None,
                'https': None
            }

            response = self.dispatch(method, url, **request_data, verify=False)

            # 确保传递给allure的参数不为None
            description_html = f"""
                        <font color=red>请求方法:</font>{method if method is not None else 'None'}<br/>
                        <font color=red>请求地址:</font>{url if url is not None else 'None'}<br/>
                        <font color=red>请求头:</font>{str(response.headers) if response.headers is not None else 'None'}<br/>
                        <font color=red>请求参数:</font>{json.dumps(kwargs.get('RequestData'), ensure_ascii=False) if kwargs is not None else 'None'}<br/>
                        <font color=red>响应状态码:</font>{str(response.status_code) if response.status_code is not None else 'None'}<br/>
                        <font color=red>响应时间:</font>{str(response.elapsed.total_seconds()) if response.elapsed is not None else 'None'}<br/>
                        """
            allure.dynamic.description_html(description_html)
            
            response_text = response.text if response.text is not None else ""
            logger.info("Request Result: {}{}".format(response, response_text))
            if ("error_id" in response_text):
                logger.debug("BMS自定义错误，报错接口:{}".format(url if url is not None else 'Unknown'))
                pytest.assume(False)

            return response
        except self.exception as e:
            logger.exception(format(e))
            raise e

    def dispatch(self, method, *args, **kwargs):
        """
        请求分发
        self 继承自 Session 类，具有 get, post, put, delete 等方法
        使用示例
            当 method='POST' 时：
            getattr(self, 'post') 获取 Session.post 方法
            handler(*args, **kwargs) 实际调用 self.post(*args, **kwargs)
            这种方式避免了使用多个 if-elif 语句来判断请求方法，提高了代码的灵活性和可维护性。
            getattr 是一个非常有用的内置函数，可以动态地访问对象的属性或方法。它在处理不确定的属性或方法时特别有用，可以提高代码的灵活性和通用性
        """
        handler = getattr(self, method.lower())
        return handler(*args, **kwargs)

    @staticmethod
    def mergedict(args, **kwargs):
        """
        合并字典，如果kwargs中存在args键，那么移除kwargs中的键，如果不存在将kwargs的键值合并，并且返回args
        """
        for k, v in args.items():
            if k in kwargs:
                kwargs[k] = {**args[k], **kwargs.pop(k)}
        args.update(kwargs)
        return args


def format_nested_json(text: str) -> str:
    """
    暴力字符串操作
    将文档中的 RequestData 里的两处格式进行修正：
    1. 将  {"json":"{"after_   修正为  {"json":{"after_
    2. 将  '"}"},"Validate"'  修正为 '"}}},"Validate"'
    """
    # 第一处替换
    out = text.replace('{"json":"{"after_', '{"json":{"after_')
    # 第二处替换
    out = out.replace('"}}"},"Validate"', '"}}},"Validate"')
    # 可能存在 第三处替换
    out = out.replace('"}"},"Validate"', '"}},"Validate"')
    return out
