import typing
from utils.current_user import current_user
from fastapi import APIRouter, HTTPException
from loguru import logger
from schemas.api.api_info import ApiQuery, ApiInfoIn, ApiId, ApiRunSchema
from services.api.api_info import ApiInfoService
from corelibs.http_response import partner_success, resp_200
from corelibs import g

router = APIRouter()


@router.post("/list", description="获取接口列表")
async def api_list(params: ApiQuery):
    data = await ApiInfoService.list(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="更新保存接口")
async def save_or_update(params: ApiInfoIn):
    data = await ApiInfoService.save_or_update(params)
    return partner_success(data)


@router.post('/getApiInfo', description="获取接口详情")
async def get_api_info(params: ApiId):
    api_info = await ApiInfoService.detail(params)
    return partner_success(api_info)


@router.post("/setApiStatus", description='接口失效生效')
async def set_api_status(params: typing.List[str]):
    count = await ApiInfoService.set_status(params)
    return resp_200(data={"生效数量": count})


@router.post('/deleted', description="删除接口")
async def deleted(params: ApiId):
    data = await ApiInfoService.deleted(params.id)
    return resp_200(data=data)


@router.post("/runApi", description="运行接口")
async def run_api(params: ApiRunSchema):
    current_user_info = await current_user()
    params.exec_user_id = current_user_info.get("id", None)
    params.exec_user_name = current_user_info.get("nickname", None)
    summary = await ApiInfoService.run(params)
    return partner_success(summary)


@router.post("/debugApi", description="调试接口")
async def debug_api(params: ApiInfoIn):
    data = await ApiInfoService.debug(params)
    return partner_success(data)

