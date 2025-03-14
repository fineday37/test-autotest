from fastapi import APIRouter

from schemas.api.env import EnvQuery, BindingDataSourceIn, EnvIdQuery, EnvIn
from services.api.env import EnvService, EnvDataSourceService, EnvFuncService
from corelibs.http_response import partner_success, resp_200

router = APIRouter()


@router.post('/list', description="环境列表")
async def env_list(params: EnvQuery):
    data = await EnvService.list(params)
    return partner_success(data)


@router.post('/getEnvById', description="获取环境详情")
async def getEnvById(params: EnvQuery):
    data = await EnvService.getEnvById(params.id)
    return partner_success(data)


@router.post('/getDataSourceByEnvId', description="获取环境数据源")
async def getDataSourceByEnvId(params: EnvIdQuery):
    data = await EnvDataSourceService.get_by_env_id(params.env_id)
    return partner_success(data)


@router.post('/bindingDataSource', description="绑定数据源")
async def bindingDataSource(params: BindingDataSourceIn):
    data = await EnvDataSourceService.binding_data_source(params)
    return resp_200(data=data)


@router.post('/getFuncsByEnvId', description="获取环境函数")
async def getFuncsByEnv(params: EnvQuery):
    data = await EnvFuncService.get_by_env_id(params.id)
    return partner_success(data)


@router.post("/saveOrUpdate", description="保存或更新环境")
async def saveOrUpdate(params: EnvIn):
    data = await EnvService.saveOrUpdate(params)
    return resp_200(data=data)
