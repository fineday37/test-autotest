# -*- coding: utf-8 -*-
# @author: xiaobai


from fastapi import APIRouter
from apis.system import user, roles, file
app_router = APIRouter()

# system
app_router.include_router(user.router, prefix="/user", tags=["user"])
app_router.include_router(roles.router, prefix="/role", tags=["role"])
app_router.include_router(file.router, prefix='/file', tags=["file"])

