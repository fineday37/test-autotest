import inspect
import logging
import os
import types

from config import config
from schemas.api.functions import FunctionQuery, FuncIn, FuncListQuery, FuncDebug
from models.api_models import Functions
import typing
import sys
import uuid
import importlib
from corelibs.logger import logger
from zerorunner.parse import get_mapping_function, parse_string_value


class FunctionsService:
    @staticmethod
    async def list(params: FunctionQuery) -> typing.Dict:
        return await Functions.get_list(params)

    @staticmethod
    async def get_function_info(params: FunctionQuery) -> typing.Dict:
        return await Functions.get_function_by_id(params.id)

    @staticmethod
    async def update_or_create(params: FuncIn) -> typing.Dict:
        module_name = uuid.uuid4().hex
        mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
        code = compile(params.content, module_name, "exec")
        exec(code, mod.__dict__)
        imported_module = importlib.import_module(module_name)
        module_functions = {}

        for name, item in vars(imported_module).items():
            if isinstance(item, types.FunctionType):
                module_functions[name] = item
        logger.info(module_functions)
        return await Functions.create_or_update(params.model_dump())

    @staticmethod
    async def handle_func_content(func_id: typing.Union[int, str, None]) -> typing.Dict:
        common_func_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                        'utils', 'basic_function.py')
        common_content = ""
        if os.path.exists(common_func_path):
            w = open(common_func_path, encoding='utf8')
            common_content = w.read()
        content = ""
        if func_id:
            func_info = await Functions.get(func_id)
            if func_info:
                content = func_info.content
        data = {
            "common_content": common_content,
            "content": content
        }
        return data

    @staticmethod
    def handle_func_info(func):
        func_info = inspect.signature(func)
        parameters = func_info.parameters
        args_dict = dict()
        for name, param_info in parameters.items():
            args_dict.setdefault(name, param_info.default if not isinstance(param_info.default, type) else '')

        return dict(
            func_name=func.__name__,
            func_args=str(func_info),
            args_info=args_dict,
            func_doc=func.__doc__,
        )

    @staticmethod
    async def get_function_by_id(params: FuncListQuery) -> typing.Dict:
        file_info = await FunctionsService.handle_func_content(params.id)
        content = file_info.get("content")
        common_content = file_info.get("common_content")
        module_name = f"{params.id}_{uuid.uuid4().__hash__()}"
        mod = sys.modules.setdefault(module_name, types.ModuleType(module_name))
        code = compile(f"{common_content}\n{content}", module_name, "exec")
        exec(code, mod.__dict__)
        imported_module = importlib.import_module(module_name)
        functions_mapping = {}
        func_list = []
        for name, item in vars(imported_module).items():
            if isinstance(item, types.FunctionType):
                functions_mapping[name] = item
        for func_name, func in functions_mapping.items():
            if not params.id:
                file_contents = common_content
            else:
                file_contents = content
            if file_contents.find(f"def {func_name}(") == -1:
                continue
            if params.func_name:
                if params.func_name in func.__name__ or params.func_name in func.__doc__ if func.__doc__ else '':
                    func_list.append(FunctionsService.handle_func_info(func))
            else:
                func_list.append(FunctionsService.handle_func_info(func))
        func_data = {
            'func_list': func_list,
            'functions_mapping': functions_mapping,
        }
        return func_data

    @staticmethod
    async def debug_func(params: FuncDebug):
        try:
            data = await FunctionsService.get_function_by_id(FuncListQuery(id=params.id))
            functions_mapping = data.get('functions_mapping')
            func = get_mapping_function(params.func_name, functions_mapping)
            if not func:
                raise ValueError('未匹配到函数！')
            args_info = {key: parse_string_value(value) for key, value in params.args_info.items()}
            result = func(**args_info)
            return result
        except Exception as err:
            raise ValueError(f"函数调试错误：{str(err)}")


