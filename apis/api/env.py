from fastapi import APIRouter
from schemas.api.env import EnvQuery
from services.api.env import EnvService
from corelibs.http_response import partner_success

router = APIRouter()


@router.post('/list', description="环境列表")
async def env_list(params: EnvQuery):
    data = await EnvService.list(params)
    return partner_success(data)
