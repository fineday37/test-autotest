import typing

from pydantic import Field, BaseModel

from schemas.base import BaseSchema
from typing import Optional

OptionalInt = Optional[int]
OptionalStr = Optional[str]


class EnvQuery(BaseSchema):
    """查询参数序列化"""

    id: OptionalInt = Field(None, description="id")
    ids: Optional[typing.List[typing.Union[int, str]]] = Field(None, description="ids")
    name: OptionalStr = Field(None, description="环境名")
    created_by_name: OptionalStr = Field(None, description="创建人")


class EnvIdQuery(BaseModel):
    env_id: int = Field(None, description="env_id")


class BindingDataSourceIn(BaseModel):
    env_id: int = Field(..., description="")
    data_source_ids: Optional[typing.List[int]] = Field(..., description="")


class BindingFuncIn(BaseModel):
    env_id: int = Field(..., description="")
    func_ids: typing.List[int] = Field(..., description="")


class EnvIn(BaseModel):
    id: OptionalInt = Field(None, description="")
    name: str = Field(..., description="环境名")
    headers: typing.List[typing.Dict] = Field(..., description="请求头")
    domain_name: str = Field(..., description="域名")
    remarks: str = Field(None, description="备注")
    variables: typing.List[typing.Dict] = Field(..., description="变量")
