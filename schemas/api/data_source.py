from pydantic import BaseModel, Field
import typing


class DataSourceQuery(BaseModel):
    id: typing.Optional[int] = Field(None, description="数据源id")
    source_type: str = Field(None, description="数据源类型")
    name: str = Field(None, description="数据源名称")
    source_ids: typing.List[int] = Field(None, description="数据源id列表")


class SourceInfo(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str = None


class SourceIdIn(BaseModel):
    id: int = Field(None, description="数据源id")


class SourceTableIn(BaseModel):
    source_id: int = Field(None, description="数据源id")
    databases: str = Field(None, description="数据库名称")


class ExecuteParam(BaseModel):
    source_id: int
    database: str = ""
    sql: str
