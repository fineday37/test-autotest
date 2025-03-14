from fastapi import APIRouter
from schemas.api.mock import MockQuery
from services.api.mock_api import MockService
from corelibs.http_response import partner_success

router = APIRouter()


@router.post('/list', description="获取mock列表")
async def get_mock_data(params: MockQuery):
    data = await MockService.get_mock_list(params)
    return partner_success(data)
