from fastapi import APIRouter

from corelibs.http_response import partner_success
from schemas.api.module import ModuleQuery, ModuleIn, ModuleId
from services.api.module import ModuleService

router = APIRouter()


@router.post('/list', description="模块列表")
async def module_list(params: ModuleQuery):
    data = await ModuleService.list(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description="保存或更新模块")
async def save_or_update(params: ModuleIn):
    data = await ModuleService.save_or_update(params)
    return partner_success(data)
