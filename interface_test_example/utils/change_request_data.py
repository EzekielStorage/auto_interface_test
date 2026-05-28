# -*- coding: utf-8 -*-
__author__ = 'Chris'
__email__ = 'ezekieli0451@gmail.com'

import random
import string
from jsonpath_ng import parse
from common.json_defind import json_loads,dumps
from common.handle_request_data import yaml_to_json
from common import variable_parameter
import os
from utils.logger import logger
from common import common_method

def change_request_data(kwargs):
    # 直接写死，只要是入库订单接口，那么就进这个方法进行入库，并且自动填写SN
    url = variable_parameter.API['inbound']
    if url in kwargs['route']:
        # 读取 yaml 文件，通过jsonpath动态更新请求参数
        update_name = 'update_requests_data'
        # 获取当前文件所在目录的上级目录（项目根目录）
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        excel_path = os.path.join(project_root, 'tests', "BMS", 'update_request_data', f'{update_name}.yaml')
        logger.info("jsondata 更新前数据: {} ".format(dumps(kwargs) if kwargs is not None else "None"))
        # 增加None值检查
        if not kwargs:
            logger.warning("kwargs为空，跳过数据更新")
            return kwargs

        jsonpath_data = yaml_to_json(excel_path)  # dict
        logger.info(
            "读取update_requests_data.yaml 数据: {} ".format(jsonpath_data if jsonpath_data is not None else "None"))
        for item_name, item_data in jsonpath_data['replace_data'].items():
            print(f"处理项目: {item_name}")
            # 获取 URL
            url = item_data.get('url', 'N/A')
            print(f"  URL: {url}")
            if url in kwargs['route']:
                logger.info(" url 匹配成功")
                # 遍历 json_path_update 列表
                json_path_updates = item_data.get('json_path_update', []) # list
                for key,value in enumerate(json_path_updates):
                    k,v = next(iter(dict(value).items()))
                    if(k == '$.order_info[0].sn_list'):
                        # 生成一个长10位字母+数字的随机数，并将其放入集合中
                        random_str = common_method.get_random_data_alphanumeric(10)
                        v = [random_str]  # 将v改为包含随机字符串的列表（集合形式）
                        logger.info("生成随机数SN: {}".format(v))
                    # 提取request_data
                    if 'RequestData' in kwargs and 'json' in kwargs['RequestData']:
                        request_kwargs = json_loads(dumps(kwargs['RequestData']['json']))
                        logger.info("遍历出来的更新value值: {}".format(v if v is not None else "None"))
                        # 增加None值检查
                        if request_kwargs is not None and k is not None:
                            expr = parse(k).update(request_kwargs, v if v is not None else "")
                            kwargs['RequestData']['json'] = request_kwargs
                logger.info("kwargs 更新后的数据: {} ".format(dumps(kwargs) if kwargs is not None else "None"))
                return kwargs
            else:
                return kwargs

    # 维修接口：根据type判断是检测不愁还是维修步骤


    return kwargs if kwargs is not None else {}

if __name__ == '__main__':
    update_name = 'update_requests_data'
    # 获取当前文件所在目录的上级目录（项目根目录）
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    excel_path = os.path.join(project_root, 'tests', "BMS", 'update_request_data', f'{update_name}.yaml')
    print(excel_path)