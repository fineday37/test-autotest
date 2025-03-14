from schemas.api.data_source import DataSourceQuery, SourceInfo, SourceIdIn, SourceTableIn, ExecuteParam
from models.api_models import DataSource
from db.db_connect import DBConfig, DB
from loguru import logger
import traceback


class DataSourceService:
    @staticmethod
    async def get_source_list(params: DataSourceQuery):
        return await DataSource.get_list(params)

    @staticmethod
    async def test_connect(params: SourceInfo) -> bool:
        try:
            db_config = DBConfig(
                host=params.host,
                port=params.port,
                user=params.user,
                password=params.password,
                read_timeout=3
            )
            db_engine = DB(db_config)
            db_engine.close()
        except Exception as e:
            logger.error(traceback.format_exc())
            return False
        return True

    @staticmethod
    async def get_db_connect(source_id: int, database: str = None) -> "DB":
        source_info = await DataSource.get(source_id)
        new_password = source_info.password
        if not source_info:
            raise ValueError("未找到数据源~")
        db_config = DBConfig(host=source_info.host,
                             port=source_info.port,
                             user=source_info.user,
                             password=new_password,
                             database=database,
                             read_timeout=3)
        db_engine = DB(db_config)
        return db_engine

    @staticmethod
    async def get_db_list(params: SourceIdIn):
        db_engine = await DataSourceService.get_db_connect(params.id)
        data = db_engine.execute("show databases")
        db_list = []
        for db in data:
            db_list.append({"name": db.get("Database", None), "hasChildren": True, "type": "database"})
        return db_list

    @staticmethod
    async def get_table_list(params: SourceTableIn):
        db_engine = await DataSourceService.get_db_connect(params.source_id)
        data = db_engine.execute(f"show tables from `{params.databases}`")
        table_list = []
        for table in data:
            table_list.append({"name": table.get(f"Tables_in_{params.databases}", None), "type": "table"})
        return table_list

    @staticmethod
    async def get_column_list(params: SourceTableIn):
        db_engine = await DataSourceService.get_db_connect(params.source_id)
        sql = f"""SELECT TABLE_NAME AS "table_name", COLUMN_NAME AS 'column_name', DATA_TYPE AS "data_type" FROM 
        information_schema.COLUMNS  WHERE TABLE_SCHEMA = '{params.databases}';"""
        data = db_engine.execute(sql)
        table_column_list = []
        table_info = {}
        for column in data:
            table_name = column.get("table_name")
            column_name = column.get("column_name")
            data_type = column.get("data_type")
            if table_name not in table_info:
                table_info[table_name] = []
            table_info[table_name].append({"columnName": column_name, "columnType": data_type})
        for key, value in table_info.items():
            table_column_list.append({"tblName": key, "tableColumns": value})
        return table_column_list

    @staticmethod
    async def execute_sql(params: ExecuteParam):
        db_engine = await DataSourceService.get_db_connect(params.source_id, params.database)
        return db_engine.execute(params.sql)

