from pydantic import BaseModel, Field
import typing


class UiCaseQuery(BaseModel):
    """用例查询条件"""
    name: str = Field(None, description="页面名称")


class UiCaseId(BaseModel):
    id: int = Field(..., description="id")


class UiCaseStepIn(BaseModel):
    """用例步骤入参"""
    id: typing.Optional[int] = Field(None, description="id")
    index: int = Field(True, description="步骤顺序")
    enable: bool = Field(True, description="是否启用")
    name: str = Field(None, description="步骤名称")
    page_id: typing.Optional[typing.Union[str, int]] = Field(None, description="页面id")
    element_id: typing.Optional[typing.Union[str, int]] = Field(None, description="页面元素id")
    page_element_id: typing.Optional[typing.Union[str, typing.List]] = Field(None, description="页面元素id")
    location_method: str = Field(None, description="元素类型")
    location_value: str = Field(None, description="元素值")
    action: str = Field(None, description="操作")
    action_value: typing.List = Field(None, description="操作")
    data: str = Field(None, description="数据")
    script: str = Field(None, description="脚本")
    remarks: typing.Optional[str] = Field(None, description="备注")
    cookie: str = Field(None, description="cookie")
    output: str = Field(None, description="输出")
    variables: typing.List = Field([], description="变量")
    breakpoint: bool = Field(False, description="断点")


class UiCaseIn(BaseModel):
    """用例入参"""
    id: int = Field(None, description="id")
    name: str = Field(None, description="用例名称")
    executeNode: typing.Union[str, int] = Field(None, description="执行节点")
    browser: typing.Union[str, int] = Field(None, description="浏览器")
    project_id: int = Field(None, description="项目id")
    module_id: int = Field(None, description="模块id")
    tags: typing.List = Field(None, description="标签")
    setup_hooks: typing.Optional[str] = Field(None, description="前置条件")
    teardown_hooks: typing.Optional[str] = Field(None, description="后置条件")
    variables: typing.Optional[typing.Dict] = Field(None, description="变量")
    steps: typing.Optional[typing.List[UiCaseStepIn]] = Field([], description="步骤")
    remarks: str = Field(None, description="备注")


class UiTestCaseRun(BaseModel):
    id: int = Field(..., description="用例id")
    env_id: int = Field(None, description="环境id")