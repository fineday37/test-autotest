from fastapi import APIRouter, Request
from schemas.system.user import UserLogin, UserIn, UserQuery, UserResetPwd, UserDel
from services.system.user import UserService
from corelibs.http_response import partner_success, resp_200
from fastapi import HTTPException
from corelibs import g

router = APIRouter()


@router.post('/userRegister', description="新增用户")
async def user_register(user_info: UserIn):
    data = await UserService.user_register(user_info)
    return partner_success(data)


@router.post("/login", description='登录')
async def login(params: UserLogin):
    data = await UserService.login(params)
    return partner_success(data, msg="登录成功！")


@router.post("/logout", description="登出")
async def logout():
    await UserService.logout()
    return {"success": "退出账号成功"}


@router.post("/list", description="用户列表")
async def user_list(params: UserQuery):
    data = await UserService.list(params)
    return partner_success(data)


@router.post("/saveOrUpdate", description="更新用户")
async def save_or_update(params: UserIn):
    await UserService.sava_or_update(params)
    return partner_success()


@router.post("getUserInfoByToken", description="根据token获取用户信息")
async def gey_user_info(request: Request):
    token = request.headers.get("token")
    user_info = await UserService.get_user_info_by_token(token)
    return partner_success(user_info)


@router.post("/resetPassword", description="修改密码")
async def reset_password(params: UserResetPwd):
    await UserService.reset_password(params)
    return {"success": "密码修改成功"}


@router.post("/deleted", description="删除用户")
async def deleted(params: UserDel):
    data = await UserService.deleted(params)
    if data == 0:
        raise HTTPException(status_code=200, detail="数据删除成功")
    return {"success": "状态删除成功", "total": data}


@router.post('/getMenuByToken', description="根据token获取菜单权限")
async def get_menu_by_token():
    user_info = await UserService.get_menu_by_token(g.token)
    return partner_success(user_info)
