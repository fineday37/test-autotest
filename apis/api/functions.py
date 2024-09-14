from fastapi import APIRouter
from schemas.api.functions import FunctionQuery, FuncIn, FuncListQuery, FuncDebug
from services.api.functions import FunctionsService
from corelibs.http_response import partner_success

router = APIRouter()


@router.post("/list", description="获取函数列表")
async def get_function_list(params: FunctionQuery):
    data = await FunctionsService.list(params)
    return partner_success(data)


@router.post("/getFuncInfo", description="获取函数详情")
async def get_function_info(params: FunctionQuery):
    data = await FunctionsService.get_function_info(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="更新或创建函数")
async def update_or_create(params: FuncIn):
    data = await FunctionsService.update_or_create(params)
    return partner_success(data)


@router.post("/getFuncList", description="获取函数列表")
async def get_func_list(params: FuncListQuery):
    try:
        data = await FunctionsService.get_function_by_id(params)
        func_list = data.get('func_list')
        return partner_success(func_list)
    except Exception as err:
        raise ValueError(f"查询函数名称失败:{err}")


@router.post('/debugFunc', description="脚本调试")
async def debug_func(params: FuncDebug):
    result = await FunctionsService.debug_func(params)
    return partner_success({'result': result})
