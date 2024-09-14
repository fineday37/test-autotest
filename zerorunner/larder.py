import csv
import os
import sys
import traceback
import types
import typing
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


def load_script_content(content: str, module_name: str, params: dict = None) -> types.ModuleType:
    mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
    if params:
        mod.__dict__.update(params)
    try:
        code = compile(content, module_name, 'exec')
        exec(code, mod.__dict__)
        return mod
    except IndentationError:
        raise IndentationError(f"脚本格式错误，请检查！\n {traceback.format_exc()}")


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