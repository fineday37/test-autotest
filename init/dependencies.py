from fastapi import Request
from corelibs import g
import uvicorn
from db import init_redis_pool
from exceptions.exceptions import AccessTokenFail
from corelibs.consts import TEST_USER_INFO, CACHE_DAY
from config import config
from fastapi import HTTPException
from utils.common import get_str_uuid
from exceptions.CustomHTTPException import CustomHTTPException


async def set_global_request(request: Request):
    """设置全局request 便与上下文的访问"""
    g.trace_id = get_str_uuid()
    g.request = request if request else None
    g.redis = await init_redis_pool()
    g.token = request.headers.get("token", None)


async def login_verification(request: Request):
    """
    登录校验
    :param request: 路径
    :return:
    """
    token = request.headers.get("token", None)
    router: str = request.scope.get('path', "")
    if router.startswith("/api") and not router.startswith("/api/file") and router not in config.WHITE_ROUTER:
        if not token:
            raise HTTPException(status_code=401, detail='未登录')
        user_info = await g.redis.get(TEST_USER_INFO.format(token))
        if not user_info:
            raise CustomHTTPException(status_code=200, error_message=11000)
            # raise AccessTokenFail()
        # 重置token时间
        await g.redis.set(TEST_USER_INFO.format(token), user_info, CACHE_DAY)


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8101, reload=True)
