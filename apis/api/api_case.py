from fastapi import APIRouter
from schemas.api.api_case import ApiCaseQuery, ApiCaseIdQuery, ApiCaseIn, ApiTestCaseRun, ApiCaseId
from services.api.api_case import ApiCaseService
from corelibs.http_response import partner_success
from utils.current_user import current_user
from celery_worker.tasks.test_case import async_run_testcase

router = APIRouter()


@router.post('/list', description="获取用例列表")
async def api_case_list(params: ApiCaseQuery):
    data = await ApiCaseService.list(params)
    return partner_success(data)


@router.post("/getCaseByIds", description="根据id获取用例")
async def get_case_by_ids(params: ApiCaseIdQuery):
    data = await ApiCaseService.get_case_by_ids(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="更新或新增用例")
async def sava_or_update(params: ApiCaseIn):
    exist_case_info = await ApiCaseService.sava_or_update(params)
    return partner_success(exist_case_info)


@router.post("/runTestCase", description="运行用例")
async def run_test_case(params: ApiTestCaseRun):
    if not params.id:
        raise ValueError("id 不能为空")
    current_user_info = await current_user()
    exec_user_id = current_user_info.get("id", None)
    exec_user_name = current_user_info.get("nickname", None)
    kwargs = dict(case_id=params.id,
                  case_env_id=params.env_id,
                  exec_user_id=exec_user_id,
                  exec_user_name=exec_user_name)
    # async_run_testcase.apply_async(kwargs=kwargs, __business_id=params.id)
    await async_run_testcase(**kwargs)
    return partner_success(msg="用例异步运行， 请稍后再测试报告列表查看 😊")


@router.post("/getCaseInfo", description="获取用例详情")
async def get_case_info(params: ApiCaseId):
    data = await ApiCaseService.get_case_info(params)
    return partner_success(data)
