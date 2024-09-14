import typing

from pydantic import Field

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
