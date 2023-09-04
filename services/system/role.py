import traceback
import typing
from loguru import logger
from models.systerm_models import Roles, User
from schemas.system.roles import RoleIn, RoleDel, RoleQuery
from fastapi import HTTPException


class RolesService:
    """
    角色类
    """

    @staticmethod
    async def list(params: RoleQuery):
        data = await Roles.get_list(params)
        for row in data.get("rows", []):
            row["menus"] = list(map(int, (row["menus"].split(',')))) if row["menus"] else []
        return data

    @staticmethod
    async def save_or_update(params: RoleIn):
        if params.id:
            role_info = await Roles.get(params.id)
            if role_info.name != params.name:
                if await Roles.get_roles_by_name(params.name):
                    raise HTTPException(status_code=200, detail="角色名已存在")
        else:
            if await Roles.get_roles_by_name(params.name):
                raise HTTPException(status_code=200, detail="角色名已存在")
        result = await Roles.create_or_update(params.model_dump())
        return result

    @staticmethod
    async def deleted(params: RoleDel):
        try:
            relation_data = await User.get_user_by_roles(params.id)
            if relation_data:
                raise HTTPException(status_code=200, detail="该角色存在用户关联，禁止删除")
            return await Roles.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())




