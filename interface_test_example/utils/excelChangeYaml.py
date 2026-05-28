import os
import json
import re
from collections import OrderedDict

import pandas as pd
import yaml


# =========================
# YAML Dumper（强制块状 + 缩进）
# =========================
class MyDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def ordered_dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


yaml.add_representer(OrderedDict, ordered_dict_representer)
MyDumper.add_representer(OrderedDict, ordered_dict_representer)


# =========================
# JSON 安全解析（支持 ${var}）
# =========================
def safe_json_loads(json_str):
    if not isinstance(json_str, str):
        return json_str

    s = json_str.strip()

    # 去除 ```json 包裹
    if s.startswith('```json'):
        s = s[7:]
    if s.startswith('```'):
        s = s[3:]
    if s.endswith('```'):
        s = s[:-3]
    s = s.strip()

    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass

    # 给 ${var} 自动补引号
    temp = re.sub(r'(?<!")(\$\{[^\}]+\})(?!")', r'"\1"', s)

    try:
        data = json.loads(temp)
    except json.JSONDecodeError:
        return json_str

    def restore(obj):
        if isinstance(obj, dict):
            return OrderedDict((k, restore(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return [restore(i) for i in obj]
        return obj

    return restore(data)


# =========================
# Excel → YAML 主逻辑
# =========================
def excel_to_yaml(excel_file_path, yaml_file_path):
    try:
        df = pd.read_excel(excel_file_path, engine='openpyxl')
    except Exception as e:
        raise RuntimeError(f"无法读取 Excel 文件: {e}")

    # ---------- YAML 根结构 ----------
    result = OrderedDict()
    result['config'] = OrderedDict([
        ('skip', False),
        ('baseurl', '${BMS_URL}'),
        ('timeout', 30.0),
        ('verify_ssl', False),
        ('headers', OrderedDict([
            ('Accept', 'application/json, text/javascript, */*; q=0.01'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Accept-Language', 'zh-CN,zh;q=0.9'),
            ('Connection', 'keep-alive'),
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'),
            ('authorization', '${BMS_TOKEN}')
        ]))
    ])

    result['variable'] = OrderedDict()
    result['tests'] = OrderedDict()

    current_case = None

    # ---------- 逐行解析 Excel ----------
    for _, row in df.iterrows():
        case_name = row.get('testCaseName')

        # 新用例开始
        if pd.notna(case_name) and str(case_name).strip():
            current_case = str(case_name).strip()
            result['tests'][current_case] = OrderedDict([
                ('description', str(row.get('description', '')).strip()),
                ('method', str(row.get('method', '')).strip()),
                ('route', str(row.get('route', '')).strip()),
                ('RequestData', OrderedDict()),
                ('Validate', OrderedDict())
            ])

        if not current_case:
            continue

        case = result['tests'][current_case]

        # ---------- RequestData ----------
        req_type = row.get('RequestData_type')
        req_json = row.get('RequestData_json')

        if pd.notna(req_type) and pd.notna(req_json):
            case['RequestData'][str(req_type).strip()] = safe_json_loads(req_json)

        # ---------- Validate ----------
        if pd.notna(row.get('expectCode')):
            case['Validate']['expectCode'] = int(row['expectCode'])

        if pd.notna(row.get('checkResultsInNotIn')):
            case['Validate']['checkResultsInNotIn'] = row['checkResultsInNotIn']

        rk = row.get('resultCheckJsonpath_key')
        rv = row.get('resultCheckJsonpath_value')
        if pd.notna(rk) and pd.notna(rv):
            case['Validate'].setdefault(
                'resultCheckJsonpath', []
            ).append(f"{str(rk).strip()}:{str(rv).strip()}")

        # ---------- ResultData ----------
        if pd.notna(row.get('ResultData')):
            case['ResultData'] = str(row['ResultData']).strip()

        # ---------- Extract（最终版，推荐） ----------
        extract_key = row.get('Extract(list)')
        extract_jsonpath = row.get('Extract_jsonpath')

        if pd.notna(extract_key):
            key = str(extract_key).strip()

            if pd.notna(extract_jsonpath) and str(extract_jsonpath).strip():
                value = str(extract_jsonpath).strip()
                # ⭐ 关键：这里主动加一个空格
                extract_item = f"{key}: {value}"
            else:
                extract_item = key

            # ⭐ 强制字符串，防止 PyYAML 当成 dict
            extract_item = str(extract_item)

            result['tests'][current_case].setdefault('Extract', []).append(extract_item)

    # ---------- 清理空字段 ----------
    for case in result['tests'].values():
        if not case.get('RequestData'):
            case.pop('RequestData', None)
        if not case.get('Validate'):
            case.pop('Validate', None)

    # ---------- 写出 YAML ----------
    os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)

    with open(yaml_file_path, 'w', encoding='utf-8') as f:
        yaml.dump(
            result,
            f,
            allow_unicode=True,
            sort_keys=False,
            Dumper=MyDumper,
            default_flow_style=False,
            indent=2
        )

    print(f"YAML 生成成功：{yaml_file_path}")


# =========================
# 示例入口
# =========================
if __name__ == "__main__":
    excel_name = 'inbount_process_test01'

    project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    excel_path = os.path.join(project_root, 'caseFile', 'excel', 'BMS', f'{excel_name}.xlsx')
    yaml_path = os.path.join(project_root, 'caseFile', 'yaml', f'{excel_name}.yaml')

    excel_path = os.path.normpath(excel_path)
    yaml_path = os.path.normpath(yaml_path)

    if not os.path.exists(excel_path):
        print(f"[ERROR]  Excel 文件不存在: {excel_path}")
    else:
        excel_to_yaml(excel_path, yaml_path)
