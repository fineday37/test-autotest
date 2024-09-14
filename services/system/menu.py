import traceback
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from loguru import logger
import typing
from corelibs import g
from corelibs.codes import CodeEnum
from models.systerm_models import Menu
from schemas.system.menu import MenuIn, MenuDel, MenuViews
from utils import current_user


class MenuService:
    """菜单类"""

    @staticmethod
    async def all_menu() -> typing.List[typing.Any]:
        """平铺菜单"""
        return await Menu.get_menu_all()

    @staticmethod
    async def all_menu_nesting() -> typing.List[typing.Any]:
        """嵌套菜单"""
        all_menu = jsonable_encoder(await MenuService.all_menu())
        parent_menu = [menu for menu in all_menu if menu["parent_id"] == 0]
        result = MenuService.menu_assembly(parent_menu, all_menu)
        return result

    @staticmethod
    async def save_or_update(params: MenuIn) -> typing.Dict[typing.Text, typing.Any]:
        existing_menu = await Menu.get_menu_by_name(params.name)
        # 新增
        if not params.id:
            if existing_menu:
                raise HTTPException(status_code=200, detail='路由名称已存在！')
        # 编辑新名称不等于其他名称
        else:
            menu_info = await Menu.get(params.id)
            if menu_info.name != params.name and existing_menu:
                raise HTTPException(status_code=200, detail='路由名称已存在！')

        result = await Menu.create_or_update(params.model_dump())
        return result

    @staticmethod
    async def deleted(params: MenuDel) -> int:
        parent_menus = await Menu.get_menu_by_parent(params.id)
        if parent_menus:
            raise ValueError(CodeEnum.MENU_HAS_MODULE_ASSOCIATION.msg)

        result = await Menu.delete(params.id)
        return result

    @staticmethod
    async def set_menu_views(params: MenuViews):
        current_user_info = await current_user.current_user()
        current_user_id = current_user_info.get("id", None)
        remote_addr = g.request.headers.get("X-Real-Ip", None)
        # remote_ip = g.request.remote_addr
        if not params.menu_id:
            raise HTTPException(status_code=200, detail="未选择菜单")
        try:
            await Menu.add_menu_views(params.menu_id)
            data = await Menu.get_menu_views(params.menu_id)
            logger.info(f"[{current_user_id}] IP {remote_addr} 访问了[{params.menu_id}]菜单")
            return data
        except Exception as err:
            logger.error(traceback.format_exc())

    @staticmethod
    def assemble_menu_data(menu: typing.Dict[typing.Text, typing.Any]) -> typing.Dict[typing.Text, typing.Any]:
        """
        菜单组装
        :param menu:
        :return:
        """
        if not menu.get('meta', None):
            menu['meta'] = {
                'title': menu.get('title', None),
                'isLink': menu.pop('isLink', None),
                'isHide': menu.pop('isHide', None),
                'isKeepAlive': menu.pop('isKeepAlive', None),
                'isAffix': menu.pop('isAffix', None),
                'isIframe': menu.pop('isIframe', None),
                'icon': menu.pop('icon', None),
                'roles': ['all']
            }
        return menu

    @staticmethod
    def menu_assembly(parent_menu: typing.List[typing.Any], all_menu: typing.List[typing.Any]) -> typing.List[
        typing.Any]:
        """
        递归遍历菜单
        :param parent_menu: 一级菜单列表
        :param all_menu: 所有菜单
        :return:
        """
        for parent in parent_menu:
            MenuService.assemble_menu_data(parent)
            for menu in all_menu:
                if menu['parent_id'] == parent['id']:
                    parent['children'] = [] if not parent.get('children', None) else parent['children']
                    MenuService.assemble_menu_data(menu)
                    parent['children'].append(menu)
            MenuService.menu_assembly(parent['children'], all_menu) if parent.get('children', None) else ...
        return parent_menu
