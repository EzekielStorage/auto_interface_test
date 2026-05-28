import json
import os
import yaml
from common.json_defind import json_loads



def yaml_to_json(yaml_path: str):

    # 读取 YAML，返回的是字典
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_data = yaml.safe_load(f)
    return yaml_data


# def update_requests_data(yaml_to_json, request_data):


if __name__ == "__main__":
    update_name = 'update_requests_data'
    project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    excel_path = os.path.join(project_root, 'tests', "BMS", 'service', 'updateRequestData', f'{update_name}.yaml')

    json = yaml_to_json(excel_path, False)
    print(json)
