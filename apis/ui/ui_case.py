from fastapi import APIRouter

from celery_worker.tasks.ui_case import async_run_ui
from schemas.ui.ui_case import UiCaseQuery, UiTestCaseRun, UiCaseIn, UiCaseId
from services.ui.ui_case import UiCaseServer
from corelibs.http_response import partner_success
from utils.current_user import current_user

router = APIRouter()


@router.post("/list", description="获取用例列表")
async def get_case_list(params: UiCaseQuery):
    data = await UiCaseServer.list(params)
    return partner_success(data)


@router.post("/getUiCaseById")
async def get_ui_case_by_id(params: UiCaseId):
    """根据id获取用例信息"""
    data = await UiCaseServer.get_case_by_id(params)
    return partner_success(data)


@router.post("/saveOrUpdate")
async def save_or_update(params: UiCaseIn):
    """保存或更新用例信息"""
    data = await UiCaseServer.save_or_update(params)
    return partner_success(data)


@router.post("/runUiCaseById", description="运行测试用例")
async def run_ui_case_by_id(params: UiTestCaseRun):
    if not params.id:
        raise ValueError("id不能为空")
    current_user_info = await current_user()
    exec_user_id = current_user_info.get("id", None)
    exec_user_name = current_user_info.get("nickname", None)
    kwargs = dict(ui_id=params.id,
                  env_id=params.env_id,
                  exec_user_id=exec_user_id,
                  exec_user_name=exec_user_name)
    await async_run_ui(**kwargs, __business_id=params.id)
    # async_run_ui.apply_async(kwargs=kwargs, __business_id=params.id)
