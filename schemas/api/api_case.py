from pydantic import root_validator, BaseModel, Field
import typing
from schemas.step_data import TStepData

from zerorunner.models import BaseSchema

OptionalStr = typing.Optional[str]
OptionalInt = typing.Optional[int]


class ApiCaseQuery(BaseModel):
    id: int = Field(None, description='')
    ids: typing.List[int] = Field(None, description='')
    name: str = Field(None, description="")
    module_name: str = Field(None, description="")
    project_name: str = Field(None, description="")
    project_id: int = Field(None, description="项目id")
    project_ids: typing.List[int] = Field(None, description="项目ids")
    order_field: str = Field(None, description="")
    created_by: int = Field(None, description="")
    created_by_name: str = Field(None, description="")
    suite_type: int = Field(None, description="")
    user_ids: typing.List[int] = Field(None, description="user ids")


class ApiCaseIdQuery(BaseModel):
    ids: typing.List[int] = Field(None, description='')


class ApiBaseSchema(BaseModel):
    key: str = Field(None, description="")
    value: str = Field(None, description="")
    remarks: str = Field(None, description="")


class TCaseRequestData(BaseModel):
    """用例请求数据 前端保存的 api id"""
    api_id: typing.Union[str, int] = Field(None, description="api id")
    name: str = Field(None, description="用例名称")
    method: str = Field(None, description="请求方法")


class TCaseStepData(TStepData):
    """测试用例数据"""
    sub_steps: typing.List['TCaseStepData'] = Field([], description="子步骤， 当前字段只对 if  loop 类型有效")
    request: typing.Optional[TCaseRequestData] = Field(None, description="引用用例")


class ApiCaseIn(BaseModel):
    """用例保存"""
    id: int = Field(None, description="")
    name: str = Field(None, description="")
    env_id: OptionalStr = Field(None, description="")
    project_id: int = Field(None, description="")
    remarks: str = Field(None, description="")
    step_rely: int = Field(1, description="")
    step_data: typing.Optional[typing.List[TCaseStepData]] = Field(None, description="步骤内容")
    headers: typing.List[ApiBaseSchema] = Field(None, description="请求头参数")
    variables: typing.List[ApiBaseSchema] = Field(None, description="变量参数")


class ApiTestCaseRun(BaseSchema):
    id: int = Field(..., description="用例id")
    env_id: typing.Optional[typing.Optional[int]] = Field(None, description="环境id")


class TestCaseRun(BaseModel):
    id: int = Field(None, description="")
    name: OptionalStr = Field(None, description="")
    env_id: typing.Optional[typing.Union[int, str]] = Field(None, description="")
    project_id: OptionalInt = Field(None, description="")
    module_id: OptionalInt = Field(None, description="")
    remarks: OptionalStr = Field(None, description="")
    step_data: typing.Optional[typing.List[TCaseStepData]] = Field([], description="步骤数据")
    step_rely: bool = Field(True, description="步骤依赖 True依赖，False 不依赖")
    headers: typing.Optional[typing.List[ApiBaseSchema]] = Field(None, description="请求头参数")
    variables: typing.Optional[typing.List[ApiBaseSchema]] = Field(None, description="变量参数")
