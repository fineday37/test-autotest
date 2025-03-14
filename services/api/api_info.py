import typing
from schemas.api.api_info import ApiQuery, ApiInfoIn, ApiId, ApiRunSchema
from models.api_models import ApiInfo
from fastapi import HTTPException
from corelibs.serialize import default_serialize
from services.api.run_handle_new import HandelRunApiStep
from zerorunner.testcase_new import ZeroRunner
from services.api.api_report import ReportService


class ApiInfoService:
    @staticmethod
    async def list(params: ApiQuery) -> typing.Dict:
        data = await ApiInfo.get_list(params)
        return data

    @staticmethod
    async def save_or_update(params: ApiInfoIn):
        if not params.name:
            raise HTTPException(status_code=200, detail="接口名称不能为空")
        existing_data = await ApiInfo.get_api_by_name(params.name)
        if params.id:
            api_info = await ApiInfo.get(params.id)
            if not api_info:
                raise HTTPException(status_code=200, detail="该接口不存在,禁止修改")
            if api_info.name != params.name and existing_data:
                raise HTTPException(status_code=200, detail="修改的接口名存在重复")
        return await ApiInfo.create_or_update(params.model_dump())

    @staticmethod
    async def detail(params: ApiId) -> typing.Dict:
        api_info = await ApiInfo.get_api_by_id(params.id)
        if not api_info:
            raise HTTPException(status_code=200, detail="接口不存在")
        return api_info

    @staticmethod
    async def set_status(params: typing.List[str]):
        api_info = await ApiInfo.set_status(params)
        return api_info

    @staticmethod
    async def deleted(pk: int):
        return await ApiInfo.delete(id=pk)

    @staticmethod
    async def run(params: ApiRunSchema):
        case_info = await ApiInfo.get(params.id)
        run_params = ApiInfoIn(**default_serialize(case_info), env_id=params.id)
        case_info = await HandelRunApiStep().init(run_params)
        runner = ZeroRunner()
        summary = runner.run_tests(case_info.get_testcase())
        report_info = await ReportService.save_report(summary=summary,
                                                      run_mode='api',
                                                      run_type=params.run_type,
                                                      project_id=case_info.api_info.project_id,
                                                      module_id=case_info.api_info.module_id,
                                                      env_id=case_info.api_info.env_id,
                                                      exec_user_id=params.exec_user_id,
                                                      exec_user_name=params.exec_user_name,
                                                      )
        return report_info

    @staticmethod
    async def debug(params: ApiInfoIn):
        case_info = await HandelRunApiStep().init(params)
        runner = ZeroRunner()
        summary = runner.run_tests(case_info.get_testcase())
        return summary
