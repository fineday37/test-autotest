import typing
from schemas.api.api_case import ApiCaseQuery, ApiCaseIdQuery, ApiCaseIn
from models.api_models import ApiCase
from fastapi import HTTPException


class ApiCaseService:
    @staticmethod
    async def list(params: ApiCaseQuery) -> typing.Dict:
        result = await ApiCase.get_list(params)
        return result

    @staticmethod
    async def get_case_by_ids(params: ApiCaseIdQuery) -> typing.Union[typing.Dict, typing.List]:
        result = await ApiCase.gey_case_by_ids(params)
        return result

    @staticmethod
    async def sava_or_update(params: ApiCaseIn):
        if not params.name:
            raise HTTPException(status_code=200, detail="用例名称不能为空")
        existing_data = await ApiCase.get_case_by_name(params.name)
        if params.id:
            api_case_info = await ApiCase.get(params.id)
            if not api_case_info:
                raise HTTPException(status_code=200, detail="接口不存在,禁止修改")
            if api_case_info.name != params.name and existing_data:
                raise HTTPException(status_code=200, detail="用例名称已存在")
        return await ApiCase.create_or_update(params.model_dump())
