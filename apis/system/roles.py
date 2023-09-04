from fastapi import APIRouter
from schemas.system.roles import RoleIn, RoleQuery, RoleDel
from services.system.role import RolesService
from corelibs.http_response import partner_success, resp_200

router = APIRouter()


@router.post('/list', description='获取角色列表')
async def all_roles(params: RoleQuery):
    data = await RolesService.list(params)
    return resp_200(data=data)


@router.post('/saveOrUpdate', description="新增或更新角色")
async def save_or_update(params: RoleIn):
    data = await RolesService.save_or_update(params)
    return resp_200(data=data)


@router.post('/deleted', description="删除角色")
async def deleted(params: RoleDel):
    data = await RolesService.deleted(params)
    return resp_200(data=data)