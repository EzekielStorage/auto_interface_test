import os
import pytest
import yaml
from dotenv import dotenv_values
from requests import Response
from requests.exceptions import RequestException
import allure

# 假设这些模块是您项目的一部分
from common.cache import cache
from common.request import HttpRequest
from common.result import check_results, get_result, get_result_data
from utils.logger import logger


def pytest_addoption(parser):
    parser.addoption(
        "--test_example_name",
        action="store",
        default=None,
        help="指定要执行的 update yaml 文件名（不含 .yaml 后缀）"
    )


def pytest_configure(config):
    if not hasattr(config, '_execution_plan_built'):
        logger.info("=" * 20 + " Pytest Configure: Initializing Session " + "=" * 20)

        env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
        if os.path.exists(env_file):
            env_vars = dotenv_values(env_file)
            for k, v in env_vars.items():
                cache.set(k, v)
            logger.info(f"Loaded {len(env_vars)} variables from .env file into cache.")

        # 从命令行参数获取 update_name，如果没有则使用默认值
        test_example_name = config.getoption("--test_example_name") or config.getini("test_example_name")
        sequence_config = load_sequence_config(test_example_name)
        plan, flow_vars = build_execution_plan(sequence_config)
        logger.info(f"Execution plan built: {plan}")
        logger.info(f"Flow variables built: {flow_vars}")

        config.execution_plan = plan
        config.flow_variables = flow_vars
        config._execution_plan_built = True


def pytest_collect_file(parent, path):
    if path.ext not in (".yml", ".yaml"):
        return None
    execution_plan = getattr(parent.config, 'execution_plan', [])
    filename = path.basename
    for flow_name, yaml_name in execution_plan:
        if filename == yaml_name:
            return YamlFile.from_parent(parent, fspath=path, flow_name=flow_name)
    return None


def pytest_runtest_setup(item):
    if not hasattr(item.session, '_executed_flows'):
        item.session._executed_flows = set()
    flow_name = getattr(item.parent, "flow_name", None)
    if not flow_name:
        return
    if flow_name not in item.session._executed_flows:
        logger.info(f"Entering new flow [{flow_name}]. Injecting flow variables.")
        flow_variables = getattr(item.config, 'flow_variables', {})
        flow_vars_to_inject = flow_variables.get(flow_name, {})
        if flow_vars_to_inject:
            for k, v in flow_vars_to_inject.items():
                logger.info(f"  -> Set flow variable: {k}={v}")
                cache.set(k, v)
        item.session._executed_flows.add(flow_name)


def pytest_collection_modifyitems(config, items):
    execution_plan = getattr(config, 'execution_plan', None)
    if not execution_plan:
        return

    def get_sort_key(item):
        item_flow = getattr(item.parent, "flow_name", None)
        item_yaml = os.path.basename(str(item.fspath))

        flow_index = len(execution_plan)
        for i, (plan_flow, plan_yaml) in enumerate(execution_plan):
            if item_flow == plan_flow and item_yaml == plan_yaml:
                flow_index = i
                break

        try:
            # 使用 item 在原始列表中的位置作为次要排序键，以保证文件内部顺序
            original_index = items.index(item)
        except ValueError:
            original_index = -1
        return (flow_index, original_index)

    items.sort(key=get_sort_key)
    logger.info(
        "Final execution order determined:\n%s",
        "\n".join(
            f"  - Flow: {getattr(i.parent, 'flow_name', 'N/A')}, File: {i.fspath.basename}, Test: {i.name}" for i in
            items)
    )


# =========================
# 辅助函数和自定义类
# =========================

def load_sequence_config(test_example_name='test_example_name'):
    project_root = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(project_root, 'tests', "BMS", "batch_run_testexample", f'{test_example_name}.yaml')
    
    logger.info(f"Loading sequence config from: {yaml_path}")
    
    if not os.path.exists(yaml_path):
        raise FileNotFoundError(f"Sequence config file not found: {yaml_path}")
    
    try:
        with open(yaml_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode {yaml_path}: {e}")
        # 尝试使用其他编码（如 gb18030）读取中文 Windows 系统上的文件
        with open(yaml_path, encoding="gb18030") as f:
            return yaml.safe_load(f)


def build_execution_plan(sequence_config: dict):
    plan = []
    flow_vars = {}
    for flow_name, items in sequence_config.items():
        flow_vars[flow_name] = {}
        for key, value in items.items():
            if value is None:
                if key.startswith("test"):
                    plan.append((flow_name, f"{key}.yaml"))
            else:
                flow_vars[flow_name][key] = value
    return plan, flow_vars


class YamlFile(pytest.File):
    def __init__(self, *args, flow_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.flow_name = flow_name

    def collect(self):
        raw = yaml.safe_load(self.fspath.open(encoding="utf-8"))
        if raw.get('config', {}).get('skip'):
            pytest.skip(f"YAML file '{self.fspath.basename}' skipped via config")
        if variable := raw.get('variable'):
            for k, v in variable.items():
                cache.set(k, v)
        if config := raw.get('config'):
            for k, v in config.items():
                cache.set(k, v)
        if tests := raw.get('tests'):
            for name, spec in tests.items():
                if 'config' in raw:
                    spec['baseurl'] = raw['config'].get('baseurl', '')
                    if 'headers' in raw['config']:
                        spec['authorization'] = raw['config']['headers'].get('authorization', '')
                yield YamlTest.from_parent(self, name=spec.get('description') or name, spec=spec)


class YamlTest(pytest.Item):
    def __init__(self, name, parent, spec):
        super().__init__(name, parent)
        self.spec = spec
        self.request = HttpRequest(exception=(RequestException, Exception))

    def runtest(self):
        with allure.step(f"执行测试：{self.name}"):
            r = self.request.send_request(**self.spec)
            self.response_handle(r, self.spec.get('Validate'), self.spec.get('Extract'), self.spec.get('ResultData'))

    def response_handle(self, r: Response, validate, extract, resultData):
        if validate:
            check_results(r, validate)
        if extract:
            get_result(r, extract)
        if resultData:
            get_result_data(r, resultData)

    def repr_failure(self, excinfo):
        """
        【核心修正】健壮的失败报告钩子。
        确保将异常信息转换为字符串再进行日志记录。
        """
        # 将异常对象转换为字符串，避免底层日志记录器处理复杂对象时出错
        error_str = str(excinfo.value)
        logger.critical(f"Caught failure in repr_failure: {error_str}")
        # 原始的 pytest 报告仍然可以正确显示
        return super().repr_failure(excinfo)

    def reportinfo(self):
        return self.fspath, 0, f"usecase: {self.name}"
