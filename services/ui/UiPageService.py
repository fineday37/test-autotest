from schemas.ui.ui_page import UiPageQuery, UiPageIn, UiPageId
from models.ui_models import UiPage, UiElement


class UiPageService:
    @staticmethod
    async def list(params: UiPageQuery):
        return await UiPage.get_list(params)

    @staticmethod
    async def save_or_update(params: UiPageIn):
        page_info = await UiPage.create_or_update(params.model_dump())
        return page_info

    @staticmethod
    async def get_all_page_element():
        """获取页面元素信息"""
        all_element = await UiElement.get_all()
        all_page = await UiPage.get_all()
        page_element = []
        for page in all_page:
            page['elements'] = []
            page['disabled'] = True
            for element in all_element:
                if element['page_id'] == page['id']:
                    page['elements'].append(element)
                    page['disabled'] = False
            page_element.append(page)
        return page_element

    @staticmethod
    async def get_page_by_id(params: UiPageId):
        """根据id获取页面信息"""
        if not params.id:
            raise ValueError("id不能为空")
        page_info = await UiPage.get_page_by_id(params.id)
        if not page_info:
            raise ValueError("UI页面信息不存在")
        return page_info
