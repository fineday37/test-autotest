from pydantic import BaseModel, Field
import typing
from ..models import TConfig, TStep
from zerorunner.step.step import Step
from zerorunner.model.base import MethodEnum, Url, Headers, Cookies, Verify


class TestCase(BaseModel):
    """用例模型"""

    class Config:
        arbitrary_types_allowed = True
    config: TConfig = Field(..., description="配置")
    teststeps: typing.List[typing.Union[Step, object]] = Field(..., description="用例步骤")


class TRequest(BaseModel):
    """api 请求模型"""
    method: MethodEnum = Field(..., description="请求方法")
    url: Url = Field(..., description="请求url")
    params: typing.Dict[str, str] = Field({}, description="参数")
    headers: Headers = Field({}, description="请求头")
    req_json: typing.Union[typing.Dict, typing.List, str] = Field(None, alias="json")
    data: typing.Union[str, typing.Dict[str, typing.Any]] = Field(None, description="data数据")
    cookies: Cookies = Field({}, description="cookies")
    timeout: float = Field(120, description="超时时间")
    allow_redirects: bool = Field(True, description="允许重定向")
    verify: Verify = Field(False, description="开启验证")
    upload: typing.Dict = Field({}, description="上传文件")
