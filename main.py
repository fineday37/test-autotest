import os.path

from fastapi import FastAPI, Depends
from config import config
from init.dependencies import set_global_request
import uvicorn
from config import config
from corelibs.logger import init_logger, logger
from init.cors import init_cors
from init.dependencies import set_global_request, login_verification
from init.exception import init_exception
from init.middleware import init_middleware, my_middleware
from init.mount import init_mount
from init.routers import init_router
from fastapi.middleware.cors import CORSMiddleware
from db import init_redis_pool
from exceptions.CustomHTTPException import CustomHTTPException
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI(title="zerorunner",
              description=config.PROJECT_DESC,
              version=config.PROJECT_VERSION,
              # dependencies=[Depends(set_global_request), Depends(login_verification)]
              )


@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.error_message},
    )


origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def init_app():
    """ 注册中心 """
    init_mount(app)  # 挂载静态文件

    # init_middleware(app)  # 注册请求响应拦截

    init_exception(app)  # 注册捕获全局异常

    init_router(app)  # 注册路由

    # init_cors(app)  # 初始化跨域

    init_logger()

    logger.info("日志初始化成功！！!")  # 初始化日志


@app.on_event("startup")
async def startup():
    # app.state.redis = await init_redis_pool()
    await init_app()  # 加载注册中心


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="127.0.0.1", port=8103, reload=True)
