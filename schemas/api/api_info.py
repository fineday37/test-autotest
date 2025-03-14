from __future__ import annotations

import typing_extensions
from pydantic import BaseModel, Field, validator
import typing

from typing import Dict, Union
from typing_extensions import Literal
from schemas.step_data import TStepData
from typing import Optional

IncEx: typing_extensions.TypeAlias = 'set[int] | set[str] | dict[int, typing.Any] | dict[str, typing.Any] | None'


class BaseSchema(BaseModel):
    def model_dump(
            self,
            *,
            mode: Union[Literal['json', 'python'], str] = 'python',
            # mode: Literal['json', 'python'] | str = 'python',
            include: IncEx = None,
            exclude: IncEx = None,
            by_alias: bool = False,
            exclude_unset: bool = True,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool = True,
    ) -> Dict[str, typing.Any]:
        return self.__pydantic_serializer__.to_python(
            self,
            mode=mode,
            by_alias=by_alias,
            include=include,
            exclude=exclude,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
        )

    @validator('*', pre=True)
    def blank_strings(cls, v):
        if v == "":
            return None
        return v


class ApiQuery(BaseSchema):
    """查询参数序列化"""

    id: int = Field(None, description="id")
    ids: typing.List = Field(None, description="ids")
    name: Optional[str] = Field(None, description="接口名")
    api_status: int = Field(None, description="接口状态")
    api_type: int = Field(None, description="api 类型")
    code: str = Field(None, description="接口code")
    sort_type: str = Field(None, description="排序类型")
    priority: int = Field(None, description="优先级")
    project_id: int = Field(None, description="项目id")
    project_ids: typing.List[int] = Field(None, description="项目ids")
    module_id: Optional[typing.List[int]] = Field(None, description="模块id")
    module_ids: typing.List[int] = Field(None, description="ids")
    project_name: str = Field(None, description="项目名")
    order_field: str = Field(None, description="排序字段")
    created_by: Optional[int] = Field(None, description="创建人id")
    created_by_name: str = Field(None, description="创建人")


class ApiBaseSchema(BaseModel):
    key: str = Field(None, description="")
    value: str = Field(None, description="")
    remarks: str = Field(None, description="")


class ApiInfoIn(TStepData):
    """用例保存更新"""
    id: Optional[int] = Field(None, description="")
    project_id: int = Field(None, description="项目")
    module_id: int = Field(None, description="")
    status: Optional[int] = Field(None, description="状态")
    env_id: Optional[int] = Field(None, description="环境id")
    code_id: Optional[int] = Field(None, description="")
    code: str = Field(None, description="")
    priority: int = Field(None, description="优先级")
    method: str = Field(None, description="方法")
    url: str = Field(None, description="")
    tags: typing.List[str] = Field([], description="")
    remarks: str = Field(None, description="备注")
    headers: typing.List[ApiBaseSchema] = Field([], description="请求头")


class ApiId(BaseModel):
    id: int = Field(..., description="id")


class ApiRunSchema(BaseModel):
    """运行用例"""

    id: int = Field(None, description="id")
    ids: typing.List[int] = Field(None, description="ids")
    env_id: int = Field(None, description="环境id")
    name: str = Field(None, description="名称")
    run_type: int = Field(None, description="运行类型 10 同步， 20 异步")
    run_mode: str = Field(None, description="运行模式")
    number_of_run: int = Field(None, description="运行次数")
    exec_user_id: int = Field(None, description="执行人id")
    exec_user_name: str = Field(None, description="执行人")
