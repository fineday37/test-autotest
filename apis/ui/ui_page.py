from fastapi import APIRouter
from schemas.ui.ui_page import UiPageQuery, UiPageIn, UiPageId
from services.ui.UiPageService import UiPageService
from corelibs.http_response import partner_success


router = APIRouter()


@router.post("/list", description="获取页面列表")
async def get_page_list(params: UiPageQuery):
    data = await UiPageService.list(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存或更新页面信息")
async def save_or_update(params: UiPageIn):
    data = await UiPageService.save_or_update(params)
    return partner_success(data)


@router.post("/getAllPageElement")
async def get_all_page_element():
    """获取页面元素信息"""
    data = await UiPageService.get_all_page_element()
    return partner_success(data)


@router.post("/getPageById")
async def get_ui_case_by_id(params: UiPageId):
    """根据id获取页面信息"""
    data = await UiPageService.get_page_by_id(params)
    return partner_success(data)

