import typing

from pydantic import Field, BaseModel
from schemas.base import BaseSchema
from typing import Optional

OptionalInt = Optional[int]
OptionalStr = Optional[str]


class ModuleIn(BaseModel):
    id: int = Field(None, description="id")
    name: str = Field(..., description="模块名称")
    project_id: OptionalInt = Field(..., description="模块id")
    test_user: OptionalStr = Field(None, description="测试人员")
    leader_user: OptionalStr = Field(None, description="负责人")
    dev_user: OptionalStr = Field(None, description="开发人员")
    publish_app: OptionalStr = Field(None, description="发布应用")
    simple_desc: OptionalStr = Field(None, description="简要描述")
    remarks: OptionalStr = Field(None, description="其他信息'")
    config_id: OptionalInt = Field(None, description="关联配置id'")
    priority: OptionalInt = Field(None, description="优先级'")


class ModuleQuery(BaseSchema):
    """查询参数序列化"""

    id: int = Field(None, description="id")
    ids: typing.List = Field(None, description="id 列表")
    project_ids: typing.List = Field(None, description="project 列表")
    user_ids: typing.List = Field(None, description="user 列表")
    name: Optional[str] = Field(None, description="模块名称")
    project_name: str = Field(None, description="模块名称")
    project_id: OptionalInt = Field(None, description="模块id")
    order_field: str = Field(None, description="排序字段")
    sort_type: str = Field(None, description="排序类型")
    created_by_name: str = Field(None, description="创建人名称")


class ModuleId(BaseSchema):
    id: int = Field(..., description="id")
