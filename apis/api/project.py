from fastapi import APIRouter
from schemas.api.project import ProjectQuery, ProjectIn, ProjectId
from services.api.project import ProjectService
from corelibs.http_response import partner_success, resp_200

router = APIRouter()


@router.post('/list', description='项目列表')
async def project_list(params: ProjectQuery):
    data = await ProjectService.get_project_list(params)
    return partner_success(data)


@router.post('/saveOrUpdate', description='更新保存项目')
async def save_or_update(params: ProjectIn):
    data = await ProjectService.save_or_update(params)
    return partner_success(data)


@router.post('/deleted', description='删除项目')
async def deleted(params: ProjectId):
    data = await ProjectService.deleted(params)
    return resp_200(data=data, msg='删除成功')


@router.post('/getProjectTree', description='获取项目树')
async def get_project_tree():
    data = await ProjectService.get_project_tree()
    return partner_success(data)
