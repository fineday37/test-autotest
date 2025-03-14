import contextlib
import csv
import os
import sys
import traceback
import types
import typing
from io import StringIO

from loguru import logger

from zerorunner import exceptions


def load_module_functions(module) -> typing.Dict[str, typing.Callable]:
    """ 加载python模块函数
    Args:
        module: python 模块
    Returns:
        dict: python函数字典

            {
                "func1_name": func1,
                "func2_name": func2
            }

    """
    module_functions = {}

    for name, item in vars(module).items():
        if isinstance(item, types.FunctionType):
            module_functions[name] = item

    return module_functions


class CapturingLogHandler:
    def __init__(self, output_buffer):
        self.output_buffer = output_buffer

    def write(self, message):
        self.output_buffer.write(message)


def load_script_content(content: str, module_name: str, params: dict = None) -> [types.ModuleType, StringIO]:
    mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
    output_buffer = StringIO()
    log_handler = CapturingLogHandler(output_buffer)
    fmt = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <" \
          "level>{level: <8}</level> | <cyan>{line}</cyan> | <level>{message}</level>"
    temp_logger = logger.add(log_handler, format=fmt)
    if not params:
        params = {}
    if "request" not in params:
        import requests
        params["requests"] = requests
    params["logger"] = temp_logger
    # if content:
    #     content = f'print({content}, end="")'
    if params:
        mod.__dict__.update(params)
    try:
        code = compile(content, module_name, "exec")
        with contextlib.redirect_stdout(output_buffer):
            exec(code, mod.__dict__)
        captured_output = output_buffer.getvalue()
        return mod, captured_output
    except IndentationError:
        raise IndentationError(f"格式错误，请检查！\n {traceback.format_exc()}")
    finally:
        logger.remove(temp_logger)
        output_buffer.close()


def load_csv_file(csv_file: str) -> typing.List[typing.Dict]:
    """ 加载csv文件

    Args:
        csv_file (str): csv file path, csv file content is like below:

    Returns:
        list: list of parameters, each parameter is in dict format

    Examples:
        >>> cat csv_file
        username,password
        test1,111111
        test2,222222
        test3,333333

        >>> load_csv_file(csv_file)
        [
            {'username': 'test1', 'password': '111111'},
            {'username': 'test2', 'password': '222222'},
            {'username': 'test3', 'password': '333333'}
        ]

    """

    if not os.path.isfile(csv_file):
        # file path not exist
        raise exceptions.CSVNotFound(csv_file)

    csv_content_list = []

    with open(csv_file, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_content_list.append(row)

    return csv_content_list
