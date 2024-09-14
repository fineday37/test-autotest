import typing

from corelibs.codes import CodeEnum
from exceptions.exceptions import ParameterError
from models.api_models import ModuleInfo
from schemas.api.module import ModuleQuery, ModuleIn


class ModuleService:
    @staticmethod
    async def list(params: ModuleQuery) -> typing.Dict:
        data = await ModuleInfo.get_list(params)
        return data

    @staticmethod
    async def save_or_update(params: ModuleIn):
        if params.id:
            module_info = await ModuleInfo.get(params.id)
            if module_info.name != params.name:
                if await ModuleInfo.get_module_by_name(params.name):
                    raise ParameterError(CodeEnum.PROJECT_NAME_EXIST)
        else:
            if await ModuleInfo.get_module_by_name(params.name):
                raise ParameterError(CodeEnum.PROJECT_NAME_EXIST)
        return await ModuleInfo.create_or_update(params.model_dump())
