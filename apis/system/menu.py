from fastapi import APIRouter
from services.system.menu import MenuService
from corelibs.http_response import partner_success, resp_200
from schemas.system.menu import MenuIn, MenuDel, MenuViews

router = APIRouter()


@router.post('/allMenu', description="获取所有菜单权限")
async def all_menu():
    data = await MenuService.all_menu()
    return partner_success(data)


@router.post('/getAllMenus', description="获取菜单嵌套结构")
async def get_all_menus():
    data = await MenuService.all_menu_nesting()
    return partner_success(data)


@router.post('/saveOrUpdate', description="新增或修改菜单")
async def sava_or_update(params: MenuIn):
    data = await MenuService.save_or_update(params)
    return partner_success(data)


@router.post("/deleted", description="删除菜单")
async def deleted(params: MenuDel):
    data = await MenuService.deleted(params)


@router.post("/setMenuViews", description="设置菜单访问量")
async def set_menu_views(params: MenuViews):
    data = await MenuService.set_menu_views(params)
    return resp_200(data=data)
