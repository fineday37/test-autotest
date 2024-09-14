import typing
from pydantic import BaseModel, Field
from zerorunner.models import TIFRequest, TSqlRequest, TLoopRequest, ValidatorData, TRequestData, TStep


class TSqlData(TSqlRequest):
    env_id: typing.Optional[int] = None
    source_id: typing.Optional[int] = None


class TIFStepData(TIFRequest):
    teststeps: typing.List["TStepData"] = Field([], description='步骤')


class TLoopStepData(TLoopRequest):
    teststeps: typing.List["TStepData"] = Field([], description='步骤')


class TStepData(TStep):
    """继承步骤类，方便入库存储"""
    enable: bool = True  # 是否有效
    # step_type: str = Field(..., description="步骤类型")
    setup_hooks: typing.List[typing.Union["TStepData", str]] = []
    teardown_hooks: typing.List[typing.Union["TStepData", str]] = []
    variables: typing.List[typing.Any] = Field([], description="变量")
    validators: typing.List[ValidatorData] = Field([], alias="validators")
    request: typing.Optional[TRequestData] = Field(None, description="api请求参数")
    sql_request: typing.Optional[typing.Optional[TSqlData]] = Field(None, description="sql请求参数")
    if_request: typing.Optional[TIFStepData] = Field(None, description="if请求参数")
    loop_request: typing.Optional[TLoopStepData] = Field(None, description="loop请求参数")
