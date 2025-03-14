from fastapi import APIRouter
from schemas.api.data_source import DataSourceQuery, SourceInfo, SourceIdIn, SourceTableIn, ExecuteParam
from services.api.data_source import DataSourceService
from corelibs.http_response import partner_success, resp_200

router = APIRouter()


@router.post("/sourceList", description="数据源列表")
async def data_source_list(params: DataSourceQuery):
    data = await DataSourceService.get_source_list(params)
    return partner_success(data)


@router.post("/testConnect", description="测试连接")
async def test_connect(params: SourceInfo):
    data = await DataSourceService.test_connect(params)
    return resp_200(data=data)


@router.post("/dbList", description="获取数据库列表")
async def db_list(params: SourceIdIn):
    data = await DataSourceService.get_db_list(params)
    return partner_success(data)


@router.post("/tableList", description="获取表列表")
async def table_list(params: SourceTableIn):
    data = await DataSourceService.get_table_list(params)
    return partner_success(data)


@router.post("/columnList", description="获取表字段列表")
async def column_list(params: SourceTableIn):
    data = await DataSourceService.get_column_list(params)
    return partner_success(data)


@router.post("/mysql/execute", description="执行sql")
async def execute(params: ExecuteParam):
    data = await DataSourceService.execute_sql(params)
    return partner_success(data)
