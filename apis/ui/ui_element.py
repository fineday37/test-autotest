from fastapi import APIRouter

from services.ui.ui_element import UiElementService
from schemas.ui.ui_element import UiElementQuery, UiElementIn
from corelibs.http_response import partner_success

router = APIRouter()


@router.post("/list", description="获取元素列表")
async def get_element_list(params: UiElementQuery):
    data = await UiElementService.list(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存或更新元素")
async def save_or_update(params: UiElementIn):
    data = await UiElementService.save_or_update(params)
    return partner_success(data)
