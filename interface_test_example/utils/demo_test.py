import random

from common import common_method
from common import variable_parameter as vp
from common.cache import cache
from common.json_defind import json_loads, dumps

# 故障信息
str = '''{"code":200,"message":"Success","data":{"new_base_info":{"last":"","next":"new_repair","file_required":false,"fault_list":[{"id":224,"code":"MPFA00224","cn_name":"\u7535\u6c60\u635f\u574f\u8fdb\u6c34","en_name":"Battery water damage","short_desc":"","created_at":"2023-12-26 13:23:07","updated_at":"2024-09-19 16:18:32","category_id":9,"de_name":null,"fault_code":""},{"id":-2,"code":"MPFA00001","cn_name":"\u5176\u4ed6","en_name":"Other","short_desc":"","created_at":"2021-06-15 11:17:23","updated_at":"2021-07-21 21:11:47","category_id":0,"de_name":null,"fault_code":""},{"id":243,"code":"MPFA00243","cn_name":"\u6bdb\u8c46Y\u6362\u7535\u6c60","en_name":"ModelY-changeBattery","short_desc":"","created_at":"2024-09-02 16:06:28","updated_at":"2024-09-20 13:59:40","category_id":9,"de_name":null,"fault_code":""},{"id":263,"code":"MPFA00263","cn_name":"\u6bdb\u8c46Y\u6362\u8f6e\u80ce","en_name":"changeTyre","short_desc":"","created_at":"2024-09-11 17:46:13","updated_at":"2024-09-13 15:24:51","category_id":9,"de_name":null,"fault_code":""},{"id":278,"code":"MPFA00278","cn_name":"\u6bdb\u8c46\u7cfb","en_name":"Tesla-repair","short_desc":"","created_at":"2024-10-30 11:18:06","updated_at":"2024-11-18 17:04:02","category_id":9,"de_name":"Mao Dou Serie","fault_code":""}],"field_list":[]},"new_repair":{"last":"new_base_info","next":"","file_required":false,"defective_reasons":[{"id":1,"code":"ASRR0001","type":2,"cn_name":"\u4e3b\u677f\u7834\u635f","en_name":"The main board is damaged","short_desc":"","created_at":"2021-06-15 20:45:27","updated_at":"2021-06-15 20:47:23"},{"id":13,"code":"ASRR0013","type":2,"cn_name":"\u6545\u969c\u95ee\u9898\u65e0\u6cd5\u4fee\u590d","en_name":"The fault cannot be repaired","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":12,"code":"ASRR0012","type":2,"cn_name":"\u673a\u8eab\u87ba\u4e1d\u751f\u9508\u8150\u8680\/\u6ed1\u7259","en_name":"Body screws are rusty and corroded\/sliding teeth","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":4,"code":"ASRR0004","type":2,"cn_name":"\u4ee5\u6362\u4ee3\u4fee","en_name":"Replace instead of repair","short_desc":"","created_at":"2021-06-23 16:23:42","updated_at":"2025-11-11 15:06:43"},{"id":14,"code":"ASRR0014","type":2,"cn_name":"\u6d4b\u8bd5\u4e00\u4e0b","en_name":"The fault cannot be repaired","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":11,"code":"ASRR0011","type":2,"cn_name":"\u4e25\u91cd\u810f\u6c61\/\u5f02\u5473","en_name":"Severely dirty\/smell","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":10,"code":"ASRR0010","type":2,"cn_name":"\u5916\u89c2\u4ef6\u7834\u635f\/\u65ad\u88c2","en_name":"Damaged\/fractured appearance","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":9,"code":"ASRR0009","type":2,"cn_name":"\u7f3a\u6599","en_name":"Lake of material","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":8,"code":"ASRR0008","type":2,"cn_name":"\u5176\u4ed6","en_name":"Other","short_desc":"","created_at":"2021-06-25 19:17:13","updated_at":"2021-06-25 19:17:13"},{"id":3,"code":"ASRR0003","type":2,"cn_name":"\u7535\u6c60\u81a8\u80c0","en_name":"The xxx","short_desc":"","created_at":"2021-06-23 16:23:33","updated_at":"2021-06-23 16:23:33"}],"field_list":[]}}}'''
# 选择故障标签
str3 = '''{"code":200,"message":"Success","data":[{"id":2,"company":"test999","cn_company":"\u6d4b\u8bd5\u4e3b\u8d26\u53f7","tag_count":5,"is_config":1,"fault_tag_list":[{"id":87,"user_id":2,"fault_tag":"\u6d78\u6db2","en_fault_tag":"immersion","ge_fault_tag":"eintauchen","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"},{"id":88,"user_id":2,"fault_tag":"\u7834\u635f","en_fault_tag":"demaged","ge_fault_tag":"besch\u00e4digt","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"},{"id":89,"user_id":2,"fault_tag":"\u5176\u4ed6","en_fault_tag":"other","ge_fault_tag":"andere","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"},{"id":90,"user_id":2,"fault_tag":"\u70e7\u6bc1","en_fault_tag":"burnt","ge_fault_tag":"brennen","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"},{"id":91,"user_id":2,"fault_tag":"\u8fdb\u6db2","en_fault_tag":"liquid inlet","ge_fault_tag":"In der fl\u00fcssigkeit","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"}]}]}'''
# 选择维修材料
str4 = '''{"code":200,"message":"Success","data":[{"id":2470,"sku":"MR_301remote","type":6,"sku_name":"301\u9065\u63a7\u5668","en_sku_name":"301remote","materiel_type":1,"is_key_parts":0,"sku_info":{"sku":"MR_301remote","sku_name":"301\u9065\u63a7\u5668","en_sku_name":"301remote","materiel_type":1,"is_key_parts":0},"is_relevance":1},{"id":5964,"sku":"MR_mtr_003","type":6,"sku_name":"new mtr","en_sku_name":"new mtr","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_mtr_003","sku_name":"new mtr","en_sku_name":"new mtr","materiel_type":1,"is_key_parts":1},"is_relevance":1},{"id":5150,"sku":"MR_1109","type":6,"sku_name":"\u7535\u6c60","en_sku_name":"Battary","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_1109","sku_name":"\u7535\u6c60","en_sku_name":"Battary","materiel_type":1,"is_key_parts":1},"is_relevance":1},{"id":7679,"sku":"MR_ANJT_ATX_830","type":6,"sku_name":"\u6377\u5b89\u7279ATX830","en_sku_name":"ANJT_ATX_830","materiel_type":2,"is_key_parts":0,"sku_info":{"sku":"MR_ANJT_ATX_830","sku_name":"\u6377\u5b89\u7279ATX830","en_sku_name":"ANJT_ATX_830","materiel_type":2,"is_key_parts":0},"is_relevance":1},{"id":2136,"sku":"MR_0401BCP808","type":6,"sku_name":"\u524d\u6444\u50cf\u5934\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":0,"sku_info":{"sku":"MR_0401BCP808","sku_name":"\u524d\u6444\u50cf\u5934\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":0},"is_relevance":0},{"id":2137,"sku":"MR_0401BCP809","type":6,"sku_name":"\u540e\u6444\u50cf\u5934\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":0,"sku_info":{"sku":"MR_0401BCP809","sku_name":"\u540e\u6444\u50cf\u5934\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":0},"is_relevance":0},{"id":3701,"sku":"MR_bi_bi","type":6,"sku_name":"MR_bi_bi","en_sku_name":"BI\u6d4b\u8bd5","materiel_type":1,"is_key_parts":0,"sku_info":{"sku":"MR_bi_bi","sku_name":"MR_bi_bi","en_sku_name":"BI\u6d4b\u8bd5","materiel_type":1,"is_key_parts":0},"is_relevance":0},{"id":2151,"sku":"MR_B0401BCP817","type":6,"sku_name":"\u6309\u952e\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":0,"sku_info":{"sku":"MR_B0401BCP817","sku_name":"\u6309\u952e\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":0},"is_relevance":0},{"id":4444,"sku":"MR_1111","type":6,"sku_name":"11111","en_sku_name":"54","materiel_type":1,"is_key_parts":0,"sku_info":{"sku":"MR_1111","sku_name":"11111","en_sku_name":"54","materiel_type":1,"is_key_parts":0},"is_relevance":0},{"id":7726,"sku":"MR_GIANT_ATX830_TYRE","type":6,"sku_name":"\u6377\u5b89\u7279ATX830_TYRE","en_sku_name":"GIANT_ATX830_TYRE","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_GIANT_ATX830_TYRE","sku_name":"\u6377\u5b89\u7279ATX830_TYRE","en_sku_name":"GIANT_ATX830_TYRE","materiel_type":1,"is_key_parts":1},"is_relevance":0}]}'''
# 故障信息详情
repair_fault_data = '''{"code":200,"message":"Success","data":[{"id":7279,"order_id":4694,"fault_id":224,"engineer_id":10389,"engineer_name":"chris_eng","repair_method_checked":[],"note":"test","file_path":"https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/161939_\u5fae\u4fe1\u56fe\u7247_2025-12-26_175118_646.jpg","created_at":"2026-01-04 08:23:15","updated_at":"2026-01-04 08:23:15","part_list":[{"id":7187,"order_id":4694,"sku":"RP_ModelY","fault_id":224,"num":2,"materiel_sku":"MR_1109","type":1,"level":0,"error_desc":"test","file_path":"https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162203_ANJT-jtb.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162246_ModelYMaterial.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162254_Rivet.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162304_\u4e00\u5b57\u87ba\u4e1d\u5200.png","sku_type":2,"relation_id":0,"created_at":"2026-01-04 16:23:15","updated_at":"2026-01-04 16:23:15","new_sn":null,"old_sn":"123444;5555","fault_tag":[{"text":"\u6d78\u6db2","value":87,"id":87,"user_id":2,"fault_tag":"\u6d78\u6db2","en_fault_tag":"immersion","ge_fault_tag":"eintauchen","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"}],"service_type":1,"fault_reason":null,"product_info":{"sku":"MR_1109","sku_name":"\u7535\u6c60","en_sku_name":"Battary","materiel_type":1,"is_key_parts":1}},{"id":7188,"order_id":4694,"sku":"RP_ModelY","fault_id":224,"num":1,"materiel_sku":"MR_301remote","type":1,"level":0,"error_desc":null,"file_path":null,"sku_type":2,"relation_id":0,"created_at":"2026-01-04 16:23:15","updated_at":"2026-01-04 16:23:15","new_sn":null,"old_sn":null,"fault_tag":[{"text":"\u5176\u4ed6","value":89,"id":89,"user_id":2,"fault_tag":"\u5176\u4ed6","en_fault_tag":"other","ge_fault_tag":"andere","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"}],"service_type":1,"fault_reason":null,"product_info":{"sku":"MR_301remote","sku_name":"301\u9065\u63a7\u5668","en_sku_name":"301remote","materiel_type":1,"is_key_parts":0}}],"fault_info":{"id":224,"code":"MPFA00224","cn_name":"\u7535\u6c60\u635f\u574f\u8fdb\u6c34","en_name":"Battery water damage","short_desc":"","created_at":"2023-12-26 13:23:07","updated_at":"2024-09-19 16:18:32","category_id":9,"de_name":null}}]}'''

''' 
    提交完成Submit数据，根据故障信息动态添加故障部位
    @material_list 故障信息对应的故障部位，需要从缓存中获取
    @fault_part_num 选择几个故障部位
    @fault_details 故障信息详情
    @tags_data 故障标签
    @num_sku 物料的数量
'''


def add_summit_data(material_list, fault_details, tags_data, fault_part_num, num_sku):
    # Parse the input data
    material = json_loads(material_list)['data']
    # 只是获取第一个故障部位的fault_info
    fault_info = json_loads(fault_details)['data'][0]['fault_info']
    fault_id = json_loads(fault_details)['data'][0]['id']
    # Randomly select unique faults 先写死，去一个物料
    selected_material = random.sample(material, min(fault_part_num, len(material)))[0]['sku_info']
    # 故障信息的附件，可以有视频
    fault_detail_file = vp.FILE_PATH
    format_file_data = process_file_video_image(fault_detail_file)
    # 维修部件的附件，只能是图片
    material_detail_file = vp.REPAIR_FILE_PATH
    format_material_file_data = process_file_video_image(material_detail_file)

    part_list = {
        "service_type": 1,
        "materiel_sku": "MR_1109",
        "type": 1,  # 默认给1，需要进行动态更新
        "num": 2,
        "order_id": 4694,
        # "old_sn": "123444;5555",
        # "new_sn": "",
        "error_desc": "故障部件信息对应的部件描述",
        "fault_tag": [],
        "materiel_sku_obj": {},
        "file_path": material_detail_file,
        # "old_sn_list": [],
        # "new_sn_list": [],
        "product_info": selected_material,
        "fault_id": fault_id,
        "id": 7213,
        "pathArr": format_material_file_data,
        # "sku": "RP_ModelY",
        # "sku_type": 2,
        # "relation_id": 0,
        # "updated_at": "2026-01-04 09:57:57" # 这三个字段主要是为了记录，多次修改保存故障部件
    }
    # 故障信息描述的部件
    fault = {
        "created_at": "2026-01-04 09:57:57",
        "engineer_id": 10389,
        "engineer_name": "chris_eng",
        "fault_id": 224,
        "fault_info": fault_info,
        "file_path": fault_detail_file,
        "id": 0,
        "note": "自动化测试维修备注",
        "order_id": 123,
        "part_list": [part_list],
        "pathArr": format_file_data,
        "repair_method_checked": [],  # 弃用
        "updated_at": "2026-01-04 09:57:57"
    }
    # TODO 存在风险，每次都会把fault_list清空重新添加
    fault_list = []
    fault_list.append(fault)

    # Construct the checked_data dictionary
    checked_data = {
        "checked": [],
        "data": [],
        "fault_list": fault_list,
        "file_path": "",  # 弃用字段
        "is_inventory": "true",
        "note": "",  # 弃用字段
        "order_id": 123,
        "step_code": "new_repair",
        "type": vp.REPAIR_TYPE_REJECTS
    }

    add_sn_method_tags_to_submit_data(checked_data, tags_data, num_sku)
    return checked_data


# 动态添加SN方法、维修方法、故障标签
def add_sn_method_tags_to_submit_data(submit_data, tags_data, num_sku):
    part_list_per = submit_data['fault_list'][0]['part_list'][0]
    fault_tag = json_loads(tags_data)['data'][0]['fault_tag_list']
    fault_tags = random.sample(fault_tag, random.randint(1, 2))
    for i in fault_tags:
        i.setdefault('value', i['id'])
        i.setdefault('user_id', cache.get("user_id"))  # 公司主账号的用户id test999就是2
        i.setdefault('text', i['fault_tag'])
    # 给部件添加故障标签
    part_list_per['fault_tag'] = fault_tags
    method_data = random.choice(vp.REPAIR_METHOD)
    print("选择的维修方法为：", method_data)
    part_list_per['type'] = method_data
    is_key_parts = part_list_per["product_info"]["is_key_parts"] == 1
    if method_data == 1 or method_data == 5:
        # Check if the material is a key part and generate SNs accordingly
        if is_key_parts:
            old_sn_list = []
            for _ in range(num_sku):
                random_str = common_method.get_random_data_number(10)
                old_sn_list.append(random_str)

            # Join the SNs with ';' but ensure the last one does not have a trailing ';'
            old_sn = ";".join(old_sn_list)

            # Add the generated SNs to the submit_data
            part_list_per.setdefault('old_sn', old_sn)
            part_list_per.setdefault('old_sn_list', old_sn_list)
    elif method_data == 2:
        # Check if the material is a key part and generate SNs accordingly
        if is_key_parts:
            old_sn_list = []
            new_sn_list = []
            for _ in range(num_sku):
                random_str_old = common_method.get_random_data_number(10)
                random_str_new = common_method.get_random_data_number(10)
                if random_str_new == random_str_old:
                    random_str_new = common_method.get_random_data_number(10)
                new_sn_list.append(random_str_new)
                old_sn_list.append(random_str_old)

            # Join the SNs with ';' but ensure the last one does not have a trailing ';'
            old_sn = ";".join(old_sn_list)
            new_sn = ";".join(new_sn_list)

            # Add the generated SNs to the submit_data
            part_list_per['old_sn'] = old_sn
            part_list_per['old_sn_list'] = old_sn_list
            part_list_per['new_sn'] = new_sn
            part_list_per['new_sn_list'] = new_sn_list
    elif method_data == 3:
        # Check if the material is a key part and generate SNs accordingly
        if is_key_parts:
            new_sn_list = []
            for _ in range(num_sku):
                random_str_new = common_method.get_random_data_number(10)
                new_sn_list.append(random_str_new)

            # Join the SNs with ';' but ensure the last one does not have a trailing ';'
            new_sn = ";".join(new_sn_list)

            # Add the generated SNs to the submit_data
            part_list_per['new_sn'] = new_sn
            part_list_per['new_sn_list'] = new_sn_list
    return submit_data


# 选择故障信息
def add_repair_check_data(submit_data, check_num):
    # Parse the input data
    data = json_loads(submit_data)
    fault_list = data['data']['new_base_info']['fault_list']

    # Filter out faults with id < 0
    valid_faults = [fault for fault in fault_list if fault['id'] >= 0]

    # Randomly select unique faults
    selected_faults = random.sample(valid_faults, min(check_num, len(valid_faults)))

    # Map fields to the required structure
    fault_checked = []
    field_map = {
        'id': 'fault_id',
        'cn_name': 'cn_name',
        'en_name': 'en_name'
    }
    # TODO service_type 暂时考虑保内维修，写死为1
    for fault in selected_faults:
        new_fault = {new_key: fault[old_key] for old_key, new_key in field_map.items()}
        new_fault.setdefault('service_type', vp.SERVICE_TYPE)
        fault_checked.append(new_fault)

    # Construct the checked_data dictionary
    checked_data = {
        "checked": fault_checked,
        "file_path": vp.FILE_PATH_TWO,
        "note": vp.REPAIR_CHECK_NOTE,
        "old_sn": 123,
        "new_sn": None,
        "order_id": 123,
        "step_code": vp.STEP_CODE
    }
    return checked_data


# 处理文件视频图片方法生成对应的pathArr格式
def process_file_video_image(input_string):
    # Initialize the result collection
    pathArr = []

    # Split the input string by ','
    parts = input_string.split(',')

    # Iterate over each part
    for part in parts:
        part = part.strip()  # Remove any leading/trailing whitespace
        if part.endswith('.mp4'):
            pathArr.append({
                "type": "video",
                "url": part,
                "poster": ""
            })
        elif part.endswith('.jpg') or part.endswith('.png'):
            pathArr.append({
                "type": "image",
                "url": part,
                "poster": part
            })

    return pathArr


# 测试数据
if __name__ == '__main__':
    # # 故障信息
    # str1 = '''{"code":200,"message":"Success","data":{"new_base_info":{"last":"","next":"new_repair","file_required":false,"fault_list":[{"id":224,"code":"MPFA00224","cn_name":"\u7535\u6c60\u635f\u574f\u8fdb\u6c34","en_name":"Battery water damage","short_desc":"","created_at":"2023-12-26 13:23:07","updated_at":"2024-09-19 16:18:32","category_id":9,"de_name":null,"fault_code":""},{"id":-2,"code":"MPFA00001","cn_name":"\u5176\u4ed6","en_name":"Other","short_desc":"","created_at":"2021-06-15 11:17:23","updated_at":"2021-07-21 21:11:47","category_id":0,"de_name":null,"fault_code":""},{"id":243,"code":"MPFA00243","cn_name":"\u6bdb\u8c46Y\u6362\u7535\u6c60","en_name":"ModelY-changeBattery","short_desc":"","created_at":"2024-09-02 16:06:28","updated_at":"2024-09-20 13:59:40","category_id":9,"de_name":null,"fault_code":""},{"id":263,"code":"MPFA00263","cn_name":"\u6bdb\u8c46Y\u6362\u8f6e\u80ce","en_name":"changeTyre","short_desc":"","created_at":"2024-09-11 17:46:13","updated_at":"2024-09-13 15:24:51","category_id":9,"de_name":null,"fault_code":""},{"id":278,"code":"MPFA00278","cn_name":"\u6bdb\u8c46\u7cfb","en_name":"Tesla-repair","short_desc":"","created_at":"2024-10-30 11:18:06","updated_at":"2024-11-18 17:04:02","category_id":9,"de_name":"Mao Dou Serie","fault_code":""}],"field_list":[]},"new_repair":{"last":"new_base_info","next":"","file_required":false,"defective_reasons":[{"id":1,"code":"ASRR0001","type":2,"cn_name":"\u4e3b\u677f\u7834\u635f","en_name":"The main board is damaged","short_desc":"","created_at":"2021-06-15 20:45:27","updated_at":"2021-06-15 20:47:23"},{"id":13,"code":"ASRR0013","type":2,"cn_name":"\u6545\u969c\u95ee\u9898\u65e0\u6cd5\u4fee\u590d","en_name":"The fault cannot be repaired","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":12,"code":"ASRR0012","type":2,"cn_name":"\u673a\u8eab\u87ba\u4e1d\u751f\u9508\u8150\u8680\/\u6ed1\u7259","en_name":"Body screws are rusty and corroded\/sliding teeth","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":4,"code":"ASRR0004","type":2,"cn_name":"\u4ee5\u6362\u4ee3\u4fee","en_name":"Replace instead of repair","short_desc":"","created_at":"2021-06-23 16:23:42","updated_at":"2025-11-11 15:06:43"},{"id":14,"code":"ASRR0014","type":2,"cn_name":"\u6d4b\u8bd5\u4e00\u4e0b","en_name":"The fault cannot be repaired","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":11,"code":"ASRR0011","type":2,"cn_name":"\u4e25\u91cd\u810f\u6c61\/\u5f02\u5473","en_name":"Severely dirty\/smell","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":10,"code":"ASRR0010","type":2,"cn_name":"\u5916\u89c2\u4ef6\u7834\u635f\/\u65ad\u88c2","en_name":"Damaged\/fractured appearance","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":9,"code":"ASRR0009","type":2,"cn_name":"\u7f3a\u6599","en_name":"Lake of material","short_desc":"","created_at":"2022-02-16 21:11:47","updated_at":"2022-02-16 21:11:47"},{"id":8,"code":"ASRR0008","type":2,"cn_name":"\u5176\u4ed6","en_name":"Other","short_desc":"","created_at":"2021-06-25 19:17:13","updated_at":"2021-06-25 19:17:13"},{"id":3,"code":"ASRR0003","type":2,"cn_name":"\u7535\u6c60\u81a8\u80c0","en_name":"The xxx","short_desc":"","created_at":"2021-06-23 16:23:33","updated_at":"2021-06-23 16:23:33"}],"field_list":[]}}}'''
    # # 选择故障标签
    # str2 = '''{"code":200,"message":"Success","data":[{"id":2,"company":"test999","cn_company":"\u6d4b\u8bd5\u4e3b\u8d26\u53f7","tag_count":5,"is_config":1,"fault_tag_list":[{"id":87,"user_id":2,"fault_tag":"\u6d78\u6db2","en_fault_tag":"immersion","ge_fault_tag":"eintauchen","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"},{"id":88,"user_id":2,"fault_tag":"\u7834\u635f","en_fault_tag":"demaged","ge_fault_tag":"besch\u00e4digt","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"},{"id":89,"user_id":2,"fault_tag":"\u5176\u4ed6","en_fault_tag":"other","ge_fault_tag":"andere","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"},{"id":90,"user_id":2,"fault_tag":"\u70e7\u6bc1","en_fault_tag":"burnt","ge_fault_tag":"brennen","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"},{"id":91,"user_id":2,"fault_tag":"\u8fdb\u6db2","en_fault_tag":"liquid inlet","ge_fault_tag":"In der fl\u00fcssigkeit","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"}]}]}'''
    # # material
    # str3 = '''{"code":200,"message":"Success","data":[{"id":2470,"sku":"MR_301remote","type":6,"sku_name":"301\u9065\u63a7\u5668","en_sku_name":"301remote","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_301remote","sku_name":"301\u9065\u63a7\u5668","en_sku_name":"301remote","materiel_type":1,"is_key_parts":1},"is_relevance":1},{"id":5964,"sku":"MR_mtr_003","type":6,"sku_name":"new mtr","en_sku_name":"new mtr","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_mtr_003","sku_name":"new mtr","en_sku_name":"new mtr","materiel_type":1,"is_key_parts":1},"is_relevance":1},{"id":5150,"sku":"MR_1109","type":6,"sku_name":"\u7535\u6c60","en_sku_name":"Battary","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_1109","sku_name":"\u7535\u6c60","en_sku_name":"Battary","materiel_type":1,"is_key_parts":1},"is_relevance":1},{"id":7679,"sku":"MR_ANJT_ATX_830","type":6,"sku_name":"\u6377\u5b89\u7279ATX830","en_sku_name":"ANJT_ATX_830","materiel_type":2,"is_key_parts":1,"sku_info":{"sku":"MR_ANJT_ATX_830","sku_name":"\u6377\u5b89\u7279ATX830","en_sku_name":"ANJT_ATX_830","materiel_type":2,"is_key_parts":1},"is_relevance":1},{"id":2136,"sku":"MR_0401BCP808","type":6,"sku_name":"\u524d\u6444\u50cf\u5934\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_0401BCP808","sku_name":"\u524d\u6444\u50cf\u5934\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":1},"is_relevance":0},{"id":2137,"sku":"MR_0401BCP809","type":6,"sku_name":"\u540e\u6444\u50cf\u5934\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_0401BCP809","sku_name":"\u540e\u6444\u50cf\u5934\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":1},"is_relevance":0},{"id":3701,"sku":"MR_bi_bi","type":6,"sku_name":"MR_bi_bi","en_sku_name":"BI\u6d4b\u8bd5","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_bi_bi","sku_name":"MR_bi_bi","en_sku_name":"BI\u6d4b\u8bd5","materiel_type":1,"is_key_parts":1},"is_relevance":0},{"id":2151,"sku":"MR_B0401BCP817","type":6,"sku_name":"\u6309\u952e\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_B0401BCP817","sku_name":"\u6309\u952e\u7ec4\u4ef6","en_sku_name":"1","materiel_type":1,"is_key_parts":1},"is_relevance":0},{"id":4444,"sku":"MR_1111","type":6,"sku_name":"11111","en_sku_name":"54","materiel_type":1,"is_key_parts":0,"sku_info":{"sku":"MR_1111","sku_name":"11111","en_sku_name":"54","materiel_type":1,"is_key_parts":0},"is_relevance":0},{"id":7726,"sku":"MR_GIANT_ATX830_TYRE","type":6,"sku_name":"\u6377\u5b89\u7279ATX830_TYRE","en_sku_name":"GIANT_ATX830_TYRE","materiel_type":1,"is_key_parts":1,"sku_info":{"sku":"MR_GIANT_ATX830_TYRE","sku_name":"\u6377\u5b89\u7279ATX830_TYRE","en_sku_name":"GIANT_ATX830_TYRE","materiel_type":1,"is_key_parts":1},"is_relevance":0}]}'''
    # # 故障信息详情
    # str4 = '''{"code":200,"message":"Success","data":[{"id":7279,"order_id":4694,"fault_id":224,"engineer_id":10389,"engineer_name":"chris_eng","repair_method_checked":[],"note":"test","file_path":"https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/161939_\u5fae\u4fe1\u56fe\u7247_2025-12-26_175118_646.jpg","created_at":"2026-01-04 08:23:15","updated_at":"2026-01-04 08:23:15","part_list":[{"id":7187,"order_id":4694,"sku":"RP_ModelY","fault_id":224,"num":2,"materiel_sku":"MR_1109","type":1,"level":0,"error_desc":"test","file_path":"https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162203_ANJT-jtb.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162246_ModelYMaterial.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162254_Rivet.png,https://d2msipxqnvj5w6.cloudfront.net/test/files/20260104/162304_\u4e00\u5b57\u87ba\u4e1d\u5200.png","sku_type":2,"relation_id":0,"created_at":"2026-01-04 16:23:15","updated_at":"2026-01-04 16:23:15","new_sn":null,"old_sn":"123444;5555","fault_tag":[{"text":"\u6d78\u6db2","value":87,"id":87,"user_id":2,"fault_tag":"\u6d78\u6db2","en_fault_tag":"immersion","ge_fault_tag":"eintauchen","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"}],"service_type":1,"fault_reason":null,"product_info":{"sku":"MR_1109","sku_name":"\u7535\u6c60","en_sku_name":"Battary","materiel_type":1,"is_key_parts":1}},{"id":7188,"order_id":4694,"sku":"RP_ModelY","fault_id":224,"num":1,"materiel_sku":"MR_301remote","type":1,"level":0,"error_desc":null,"file_path":null,"sku_type":2,"relation_id":0,"created_at":"2026-01-04 16:23:15","updated_at":"2026-01-04 16:23:15","new_sn":null,"old_sn":null,"fault_tag":[{"text":"\u5176\u4ed6","value":89,"id":89,"user_id":2,"fault_tag":"\u5176\u4ed6","en_fault_tag":"other","ge_fault_tag":"andere","created_at":"2024-10-09 09:44:03","updated_at":"2024-10-09 09:44:03"}],"service_type":1,"fault_reason":null,"product_info":{"sku":"MR_301remote","sku_name":"301\u9065\u63a7\u5668","en_sku_name":"301remote","materiel_type":1,"is_key_parts":0}}],"fault_info":{"id":224,"code":"MPFA00224","cn_name":"\u7535\u6c60\u635f\u574f\u8fdb\u6c34","en_name":"Battery water damage","short_desc":"","created_at":"2023-12-26 13:23:07","updated_at":"2024-09-19 16:18:32","category_id":9,"de_name":null}}]}'''
    #
    # fault_part_num = 1
    # num_sku = 2
    # check_num = 1
    # # 选择故障信息,需要将这个故障信息id传到另外衣柜接口获取到对应的material_list
    # check_fault_data = add_repair_check_data(str1, check_num)
    # print("选择的故障信息：{}".format(check_fault_data))
    # submit_data = add_summit_data(str3, str4, str2, fault_part_num, num_sku)
    # print(dumps(submit_data))
    #
    # test01 = {
    #     "tags_list": []
    # }
    #
    # test01.setdefault('tags_list', ['a', 'b'])
    # print(test01)

    str1 = '''[
    {
        "name": "20260117-225113.jpg",
        "url": "https:\/\/d2msipxqnvj5w6.cloudfront.net\/prod\/files\/20260117\/225121_20260117-225113.jpg"
    }
]'''
    print(json_loads(str1))
