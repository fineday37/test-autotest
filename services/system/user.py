import logging
import typing
import uuid
from schemas.system.user import UserLogin, UserIn, UserLoginRecordIn, UserQuery, UserResetPwd, UserDel
from models.systerm_models import User, UserLoginRecord, Menu, Roles
from corelibs.codes import CodeEnum
from fastapi import HTTPException
import typing
from corelibs.serialize import default_serialize
from utils.des import encrypt_rsa_password, decrypt_rsa_password
import datetime
from corelibs import g
from corelibs.consts import TEST_USER_INFO, CACHE_DAY
from loguru import logger
from utils import current_user
from db import init_redis_pool
import traceback
from services.system.menu import MenuService


class UserService:
    # 新增用户

    # 登录
    @staticmethod
    async def login(params: UserLogin) -> typing.Dict[typing.Text, typing.Any]:
        username = params.username
        password = params.password
        if not username and not password:
            raise HTTPException(status_code=200, detail=CodeEnum.PARTNER_CODE_PARAMS_FAIL.msg)
        user_info = await User.get_user_by_name(username)
        if not user_info:
            raise HTTPException(status_code=200, detail=CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
        u_password = decrypt_rsa_password(user_info["password"])
        if u_password != password:
            raise HTTPException(status_code=200, detail=CodeEnum.WRONG_USER_NAME_OR_PASSWORD.msg)
            # raise ValueError(CodeEnum.WRONG_USER_NAME_OR_PASSWORD.mag)
        token = str(uuid.uuid4())
        login_time = default_serialize(datetime.datetime.now())
        tag = user_info.get("tag", None)
        roles = user_info.get("roles", None)
        token_user_info = {
            "id": user_info["id"],
            "token": token,
            "login_time": login_time,
            "username": user_info["username"],
            "nickname": user_info["nickname"],
            "roles": roles if roles else [],
            "tag": tag if tag else []
        }
        # g.redis = await init_redis_pool()
        await g.redis.set(TEST_USER_INFO.format(token), token_user_info, CACHE_DAY)
        logging.info(f'用户 {user_info["username"]} 登录了系统')
        try:
            login_ip = g.request.headers.get("X-Real-IP", None)
            if not login_ip:
                login_ip = g.request.client.host
            params = UserLoginRecordIn(
                token=token,
                code=user_info["username"],
                user_id=user_info["id"],
                user_name=user_info["nickname"],
                login_type="password",
                login_time=login_time,
                login_ip=login_ip,
            )
            await UserService.user_login_record(params)
        except Exception as err:
            logger.error(f"登录日志记录错误\n{err}")
        return token_user_info

    # 登录日志
    @staticmethod
    async def user_login_record(params: UserLoginRecordIn):
        result = await UserLoginRecord.create_or_update(params.model_dump())
        return result

    # 登出
    @staticmethod
    async def logout():
        token = g.request.headers.get("token", None)
        try:
            await g.redis.delete(TEST_USER_INFO.format(token))
        except Exception as err:
            logger.error(traceback.format_exc())

    # 查看用户列表
    @staticmethod
    async def list(params: UserQuery):
        data = await User.get_list(params)
        for row in data["rows"]:
            roles = row.get("roles", None)
            tags = row.get("tags", None)
            row["roles"] = roles if roles else []
            row["tags"] = tags if tags else []
        return data

    # 修改密码
    @staticmethod
    async def reset_password(params: UserResetPwd):
        if params.new_pwd != params.re_new_pwd:
            raise HTTPException(status_code=200, detail="二次密码确认错误")
        user_info = await User.get(params.id)
        if params.old_pwd != decrypt_rsa_password(user_info.password):
            raise HTTPException(status_code=200, detail=CodeEnum.OLD_PASSWORD_ERROR.msg)
        if params.new_pwd == decrypt_rsa_password(user_info.password):
            raise HTTPException(status_code=200, detail=CodeEnum.NEW_PWD_NO_OLD_PWD_EQUAL.msg)
        password = encrypt_rsa_password(params.new_pwd)
        await User.update(params.id, {"password": password})

    @staticmethod
    async def deleted(params: UserDel):
        try:
            return await User.delete(params.id)
        except Exception as err:
            logger.error(traceback.format_exc())

    # 编辑保存用户信息
    @staticmethod
    async def sava_or_update(params: UserIn) -> typing.Dict[typing.Text, typing.Any]:
        if params.password:
            del params.password
        if not params.id:
            raise HTTPException(status_code=400, detail="id不能为空")
        username = params.username
        userinfo = await User.get(params.id, to_dict=True)
        other_users = await User.get_filter_all([User.id != params.id])
        other_user = [user["username"] for user in other_users]
        if username != userinfo["username"] and username in other_user:
            raise HTTPException(status_code=400, detail="用户名重复")
        result = await User.create_or_update(params.model_dump())
        return result

    # 根据token获取用户信息
    @staticmethod
    async def get_user_info_by_token(token: str) -> typing.Union[typing.Dict[typing.Text, typing.Any], None]:
        # g.redis = await init_redis_pool()
        token_user_info = await g.redis.get(TEST_USER_INFO.format(token))
        if not token_user_info:
            raise HTTPException(status_code=401, detail=CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        user_info = await User.get(token_user_info["id"])
        if not user_info:
            raise HTTPException(status_code=401, detail=CodeEnum.PARTNER_CODE_TOKEN_EXPIRED_FAIL.msg)
        return {
            "id": user_info.id,
            "avatar": user_info.avatar,
            "username": user_info.username,
            "nickname": user_info.nickname,
            "roles": user_info.roles,
            "tags": user_info.tags,
            "login_time": token_user_info.get("login_time", None)
        }

    # 根据token获取菜单权限
    @staticmethod
    async def get_menu_by_token(token: str) -> typing.List[typing.Dict[typing.Text, typing.Any]]:
        current_user_info = await current_user.current_user(token)
        if not current_user_info:
            return []
        user_info = await User.get(current_user_info["id"])
        if not user_info:
            return []
        menu_ids = []
        if user_info.user_type == 10:
            all_menu = await Menu.get_menu_all()
            menu_ids += [i["id"] for i in all_menu]
        else:
            roles = await Roles.get_roles_by_ids(user_info.roles if user_info.roles else [])
            for i in roles:
                menu_ids += list(map(int, i["menus"].split(',')))
            if not menu_ids:
                return []
            parent_menus = await Menu.get_parent_id_by_ids(list(set(menu_ids)))
            menu_ids += [i["parent_id"] for i in parent_menus]
            all_menu = await Menu.get_menu_by_ids(list(set(menu_ids)))
        parent_menu = [menu for menu in all_menu if menu['parent_id'] == 0]
        return MenuService.menu_assembly(parent_menu, all_menu) if menu_ids else []


async def user_register(user_params: UserIn) -> "User":
    """用户注册"""
    id_info = await User.get_user_by_id(user_params.id)
    if id_info:
        raise HTTPException(status_code=200, detail="用户id已存在")
    user_info = await User.get_user_by_name(user_params.username)
    if user_info:
        raise HTTPException(status_code=200, detail="用户名已被注册")
    user = await User.create(user_params.model_dump())
    return user





