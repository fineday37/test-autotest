import copy

from loguru import logger
from pydantic import BaseModel, Field
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from zerorunner.model.base import CheckModeEnum

from zerorunner.exceptions import ParamsError, ValidationFailure
from zerorunner.models import Validators, VariablesMapping, ExtractData
from zerorunner.parse import Parser, parse_string_value


class DriverSetting(BaseModel):
    """driver设置"""
    command_executor: str = Field("http://127.0.0.1:4444/wb/hub", description="远程地址")
    browser_name: str = Field("chrome", description="浏览器名称")
    headless: bool = Field(True, description="是否无头模式")
    executable_path: str = Field(None, description="浏览器驱动路径")
    chrome_driver: str = Field(None, description="chrome驱动路径")
    snapshot: bool = Field(True, description="截图路径")
    page_flash_timeout: int = Field(90, description="页面闪烁超时")
    element_wait_timeout: int = Field(10, description="元素等待超时")


class ZeroDriver:
    def __init__(self, setting: DriverSetting):
        self.setting = setting
        self._session_variables = {}
        if setting.browser_name.lower() == "chrome":
            options = Options()
            # options.add_argument('--disable-gpu')
            # options.add_argument("--no-sandbox")
            # options.add_argument('--ignore-certificate-errors')
            # options.add_experimental_option("excludeSwitches",
            #                                 ['load-extension', 'enable-automation', 'enable-logging'])
            if setting.headless:
                options.add_argument("--headless")
            if setting.executable_path:
                """本地执行"""
                self.driver = webdriver.Chrome(executable_path=setting.executable_path, options=options)
            else:
                """远程执行"""
                # 默认vnc密码：secret
                """http://chromedriver.storage.googleapis.com/index.htm 驱动下载"""
                desired_capabilities = {
                    "browserName": "chrome",  # 浏览器名称
                    "version": "",  # 操作系统版本
                    "platform": "ANY",  # 平台，这里可以是windows、linux、andriod等等
                    "javascriptEnabled": True,  # 是否启用js
                }
                self.driver = webdriver.Remote(command_executor=setting.command_executor,
                                               options=options,
                                               desired_capabilities=desired_capabilities)
        else:
            raise Exception(f"暂不支持其他浏览器: {setting.browser_name}")
        # 元素等待超时时间
        self.driver.implicitly_wait(setting.element_wait_timeout)  # seconds
        # 页面刷新超时时间
        self.driver.set_page_load_timeout(setting.page_flash_timeout)  # seconds
        self.driver.maximize_window()

    def get_session_variables(self):
        """获取session变量"""
        return self._session_variables

    def quit(self):
        """退出"""
        self.driver.quit()

    def get_driver_session_id(self):
        """获取session_id"""
        return self.driver.session_id

    def get_screenshot(self, screenshot_type="base64", file_path=None):
        """截图"""
        if screenshot_type == "base64":
            """方法得到图片的base64编码"""
            return self.driver.get_screenshot_as_base64()
        elif screenshot_type == "png":
            """方法得到图片的二进制数据"""
            return self.driver.get_screenshot_as_png()
        elif screenshot_type == "file":
            """方法得到图片的二进制数据"""
            if not file_path:
                raise Exception("截图路径不能为空")
            return self.driver.get_screenshot_as_file(file_path)
        else:
            raise Exception(f"不支持的截图类型: {screenshot_type}")

    @staticmethod
    def get_uniform_comparator(comparator: str):
        """统一比较器"""
        if comparator in ["eq", "equals", "equal"]:
            return "equal"
        elif comparator in ["lt", "less_than"]:
            return "less_than"
        elif comparator in ["le", "less_or_equals"]:
            return "less_or_equals"
        elif comparator in ["gt", "greater_than"]:
            return "greater_than"
        elif comparator in ["ge", "greater_or_equals"]:
            return "greater_or_equals"
        elif comparator in ["ne", "not_equal"]:
            return "not_equal"
        elif comparator in ["str_eq", "string_equals"]:
            return "string_equals"
        elif comparator in ["len_eq", "length_equal"]:
            return "length_equal"
        elif comparator in [
            "len_gt",
            "length_greater_than",
        ]:
            return "length_greater_than"
        elif comparator in [
            "len_ge",
            "length_greater_or_equals",
        ]:
            return "length_greater_or_equals"
        elif comparator in ["len_lt", "length_less_than"]:
            return "length_less_than"
        elif comparator in [
            "len_le",
            "length_less_or_equals",
        ]:
            return "length_less_or_equals"
        else:
            return comparator

    @staticmethod
    def uniform_validator(validator):
        """ 统一校验器

        Args:
            validator (dict): validator maybe in two formats:

                format1: this is kept for compatibility with the previous versions.
                    {"check": "status_code", "comparator": "eq", "expect": 201}
                    {"check": "$resp_body_success", "comparator": "eq", "expect": True}
                format2: recommended new version, {assert: [check_item, expected_value]}
                    {'eq': ['status_code', 201, 'mode']}
                    {'eq': ['$resp_body_success', True, 'mode']}

        Returns
            dict: validator info

                {
                    "check": "status_code",
                    "expect": 201,
                    "assert": "equals"
                }

        """
        if not isinstance(validator, dict):
            raise ParamsError(f"invalid validator: {validator}")

        if "check" in validator and "expect" in validator:
            # format1
            check_item = validator["check"]
            expect_value = validator["expect"]
            message = validator.get("message", "")
            check_mode = validator.get("mode", None)
            continue_extract = validator.get("continue_extract", False)
            continue_index = validator.get("continue_index", 0)
            comparator = validator.get("comparator", "eq")

        else:
            raise ParamsError(f"invalid validator: {validator}")

        # uniform comparator, e.g. lt => less_than, eq => equals
        assert_method = ZeroDriver.get_uniform_comparator(comparator)

        return {
            "mode": check_mode,
            "check": check_item,
            "expect": expect_value,
            "assert": assert_method,
            "message": message,
            "continue_extract": continue_extract,
            "continue_index": continue_index,
        }
