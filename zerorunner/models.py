from enum import Enum
from pydantic import BaseModel, Field, HttpUrl, validator
import typing


Name = str
Url = str
BaseUrl = typing.Union[HttpUrl, str]
VariablesMapping = typing.Dict[str, typing.Any]
ParametersMapping = typing.Dict[str, typing.Any]
FunctionsMapping = typing.Dict[str, typing.Callable]
Headers = typing.Dict[str, str]
Cookies = typing.Dict[str, str]
Verify = bool
# Hooks = typing.List[Union[Text, Dict[Text, Text]]]
Hooks = typing.List[typing.Any]
Export = typing.List[str]
Env = typing.Dict[str, typing.Any]


class MethodEnum(str, Enum):
    """请求方法枚举"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    NA = "N/A"


class TStepLogType(str, Enum):
    """步骤日志类型"""
    start = "开始"
    end = "结束"
    success = "成功"
    fail = "失败"
    skip = "跳过"
    err = "错误"
    wait = "等待"
    loop = "循环"
    condition = "条件"


class TStepTypeEnum(str, Enum):
    """步骤类型枚举"""
    api = "api"
    case = "case"
    wait = "wait"
    script = "db_script"
    sql = "sql"
    extract = "extract"
    loop = "loop"
    IF = "IF"
    ui = "ui"


TStepControllerDict = {
    "api": "接口",
    "case": "用例",
    "wait": "等待控制器",
    "db_script": "脚本控制器",
    "sql": "sql控制器",
    "extract": "提取控制器",
    "loop": "循环控制器",
    "if": "条件控制器",
    "ui": "ui用例"
}


class LoopTypeEnum(str, Enum):
    """循环类型枚举"""
    For = "for"
    Count = "count"
    While = "while"


class ComparatorEnum(str, Enum):
    """比较方法枚举， 条件控制器， 循环控制 使用"""
    equals = "equals"
    not_equals = "not_equals"
    contains = "contains"
    not_contains = "not_contains"
    gt = "gt"
    lt = "lt"
    none = "none"
    not_none = "not_none"


class TStepResultStatusEnum(str, Enum):
    """步骤数据状态"""
    success = "SUCCESS"
    fail = "FAILURE"
    skip = "SKIP"
    err = "ERROR"


class CheckModeEnum(str, Enum):
    """校验模式枚举"""
    JsonPath = "JsonPath"
    jmespath = "jmespath"
    variable_or_func = "variable_or_func"
    RequestHeaders = "request_headers"
    ResponseHeaders = "response_headers"


class RequestData(BaseModel):
    """请求数据"""
    method: typing.Optional[MethodEnum] = Field(MethodEnum.GET, description="请求方法")
    url: Url = Field(..., description="url")
    headers: Headers = Field({}, description="请求头")
    cookies: Cookies = Field({}, description="cookies")
    body: typing.Union[str, bytes, typing.List, typing.Dict, None] = Field({}, description="body")


class ResponseData(BaseModel):
    """响应数据"""
    status_code: int = Field(..., description="状态码")
    headers: typing.Dict = Field(..., description="响应头")
    cookies: typing.Optional[Cookies] = Field(..., description="cookies")
    encoding: typing.Union[str, None] = Field(None, description="encoding")
    content_type: str = Field(..., description="类型")
    body: typing.Union[str, bytes, typing.List, typing.Dict, None] = Field(..., description="body")


class ReqRespData(BaseModel):
    """请求响应数据"""
    request: RequestData = Field(..., description="请求数据")
    response: ResponseData = Field(..., description="响应数据")


class AddressData(BaseModel):
    """地址信息"""
    client_ip: str = Field("N/A", description="客户端ip")
    client_port: int = Field(0, description="客户端端口")
    server_ip: str = Field("N/A", description="服务端ip")
    server_port: int = Field(0, description="服务端端口")


class RequestStat(BaseModel):
    """请求统计"""
    content_size: float = Field(0, description="响应内容大小")
    response_time_ms: float = Field(0, description="响应时间 毫秒")
    elapsed_ms: float = Field(0, description="过程时间")


class SessionData(BaseModel):
    """请求会话数据，包括请求、响应、验证器和stat数据"""

    success: bool = Field(False, description="是否成功")
    req_resp: ReqRespData = Field({}, description="请求，响应数据")
    stat: RequestStat = Field(RequestStat(), description="时间")
    address: AddressData = Field(AddressData(), description="地址")
    validators: typing.Dict = Field({}, description="校验")


class UiSessionData(BaseModel):
    """ui会话数据"""
    action: str = Field(None, description="动作")
    data: str = Field(None, description="输入数据")
    location_method: str = Field(None, description="定位方法")
    location_value: str = Field(None, description="定位值")
    cookie: typing.Dict = Field(None, description="cookie")
    locator_data: typing.Dict = Field({}, description="定位器数据")
    validators: typing.Dict = Field({}, description="校验")
    screenshot_file_base64: str = Field(None, description="截图base64")


class StepResult(BaseModel):
    """测试步骤数据"""

    name: str = Field("", description="步骤名称")
    case_id: str = Field("", description="case_id")
    index: int = Field(0, description="index")
    start_time: float = Field(0, description="开始时间")
    duration: float = Field(0, description="执行耗时")
    success: bool = Field(False, description="是否成功")
    status: str = Field("", description="步骤状态  success 成功  fail 失败  skip 跳过  err 错误")
    step_type: str = Field("", description="步骤类型")
    step_tag: typing.Union[str, None] = Field(None, description="步骤标签")
    message: str = Field("", description="错误信息等")
    env_variables: VariablesMapping = Field({}, description="环境变量")
    variables: VariablesMapping = Field({}, description="变量")
    case_variables: VariablesMapping = Field({}, description="用例变量")
    step_result: typing.List['StepResult'] = Field([], description="步骤结果")
    session_data: SessionData = Field(None, description="请求信息")
    ui_session_data: UiSessionData = Field(None, description="ui请求数据")
    # pre_hook_data: typing.List['StepResult'] = Field([], description="前置")
    # post_hook_data: typing.List['StepResult'] = Field([], description="后置")
    setup_hook_results: typing.List['StepResult'] = Field([], description="前置hook")
    teardown_hook_results: typing.List['StepResult'] = Field([], description="后置hook")
    export_vars: VariablesMapping = Field({}, description="提取变量数据")
    log: str = Field("", description="执行log")
    attachment: str = Field("", description="附件")

    def dict(self, *args, **kwargs):
        """获取报告时去除 请求信息 避免报告数据太大"""
        kwargs["exclude"] = {"request", "response"}
        return super(StepResult, self).dict(*args, **kwargs)


class TRequest(BaseModel):
    """请求模型"""
    method: MethodEnum
    url: Url
    params: typing.Dict[str, str] = {}
    headers: Headers = {}
    req_json: typing.Union[typing.Dict, typing.List, str] = Field(None, alias="json")
    data: typing.Union[str, typing.Dict[str, typing.Any]] = None
    cookies: Cookies = {}
    timeout: float = 120
    allow_redirects: bool = True
    verify: Verify = False
    upload: typing.Dict = {}  # used for upload files


class RequestData(BaseModel):
    method: typing.Optional[MethodEnum] = MethodEnum.GET
    url: Url
    headers: Headers = {}
    cookies: Cookies = {}
    body: typing.Union[str, bytes, typing.List, typing.Dict, None] = {}


class ResponseData(BaseModel):
    status_code: int
    headers: typing.Dict
    cookies: typing.Optional[Cookies]
    encoding: typing.Union[str, None] = None
    content_type: str
    body: typing.Union[str, bytes, typing.List, typing.Dict, None]


class ReqRespData(BaseModel):
    request: RequestData
    response: ResponseData


class RequestStat(BaseModel):
    content_size: float = 0
    response_time_ms: float = 0
    elapsed_ms: float = 0


class AddressData(BaseModel):
    client_ip: str = "N/A"
    client_port: int = 0
    server_ip: str = "N/A"
    server_port: int = 0


class SessionData(BaseModel):
    """请求会话数据，包括请求、响应、验证器和stat数据"""

    success: bool = False
    req_resp: ReqRespData = {}
    stat: RequestStat = RequestStat()
    address: AddressData = AddressData()
    validators: typing.Dict = {}


class BaseSchema(BaseModel):
    def dict(self, *args, **kwargs):
        if "exclude_none" not in kwargs:
            kwargs["exclude_none"] = True
        return super(BaseSchema, self).model_dump(*args, **kwargs)

    @validator('*', pre=True)
    def blank_strings(cls, v):
        if v == "":
            return None
        return v


class ApiBodyFileValueSchema(BaseSchema):
    id: str = Field("", description="文件id")
    name: str = Field("", description="文件名称")


class ApiBodyFileDataSchema(BaseSchema):
    key: str = Field("", description="form表单名称")
    value: typing.Union[str, ApiBodyFileValueSchema] = Field("", description="文件数据")
    type: str = Field("", description="类型 file text")


class TRequestData(TRequest):
    mode: str = Field("", description="模式 raw  form-data 等")
    # data: typing.Union[str, typing.List[ApiBodyFileDataSchema]] = Field(None, description="数据json 数据 或者form-data数据等")
    language: str = Field("", description="raw 中包含json text 等")
    upload: typing.Dict = Field({}, description="上传文件的数据")
    headers: typing.List[typing.Any] = Field([], description="请求头")


class TSqlRequest(BaseModel):
    """sql请求模型"""
    sql: str = Field("", description="sql")
    host: str = Field(None, description="host")
    port: typing.Optional[int] = Field(None, description="端口")
    user: typing.Optional[str] = Field(None, description="用户名")
    password: typing.Optional[str] = Field(None, description="密码")
    database: typing.Optional[str] = Field("", description="数据库")
    timeout: typing.Optional[int] = Field(None, description="超时时间")  # 超时时间
    variable_name: typing.Optional[str] = Field(None, description="变量赋值名称")  # 变量赋值名称


class TUiRequest(BaseModel):
    """ui请求模型"""
    action: str = Field(None, description="动作")
    data: str = Field(None, description="输入数据")
    location_method: typing.Optional[str] = Field(None, description="定位方法")
    location_value: typing.Optional[str] = Field(None, description="定位值")
    cookie: typing.Optional[typing.Union[typing.Dict, str]] = Field(None, description="cookie")
    output: typing.Optional[str] = Field(None, description="输出")


class TIFRequest(BaseModel):
    """if请求模型"""
    check: str = Field("", description="校验变量")
    comparator: str = Field("", description="对比规则")
    expect: str = Field("", description="对比值")
    remarks: str = Field("", description="备注")
    teststeps: typing.List[object] = Field([], description="步骤")


class ValidatorData(BaseModel):
    """验证模式"""
    mode: str = Field(None, description="校验方法")
    check: typing.Any = Field(None, description="校验值")
    comparator: str = Field(None, description="比较器")
    expect: typing.Any = Field(None, description="预期值")
    continue_extract: bool = Field(False, description="继续提取 针对 mode = JsonPath 才有效")
    continue_index: int = Field(0, description="提取index")


class TLoopRequest(BaseModel):
    """循环请求"""
    loop_type: str = Field("", description="count 次数循环  for 循环  while 循环")
    # loop_type == "count"
    count_number: int = Field(0, description="循环次数")
    count_sleep_time: int = Field(0, description="休眠时间")  # 休眠时间

    # loop_type == "for"
    for_variable_name: str = Field(None, description="循环变量名")  # 循环变量名
    for_variable: typing.Any = Field(None, description="循环变量")  # 循环变量
    for_sleep_time: int = Field(0, description="休眠时间")  # 休眠时间

    # loop_type == "while"
    while_comparator: str = Field(None, description="比对条件")  # 比对条件
    while_variable: typing.Any = Field(None, description="循环变量")  # 循环变量
    while_value: str = Field(None, description="循环值")  # 循环值
    while_sleep_time: int = Field(0, description="")
    while_timeout: int = Field(0, description="超时时间")  # 超时时间

    teststeps: typing.List[object] = Field([], description="步骤")


class TStepBase(BaseModel):
    """步骤基类"""
    case_id: typing.Optional[typing.Union[str, int]] = Field(None, description="用例id")
    step_type: str = Field("", description="步骤类型 api if loop sql wait 等")
    name: Name = Field("", description="步骤名称")
    index: int = Field(0, description="排序")
    step_id: str = Field("", description="步骤id")
    retry_times: int = Field(0, description="重试次数")
    retry_interval: int = Field(0, description="重试间隔")
    parent_step_id: str = Field("", description="父级步骤id")


class ExtractData(BaseModel):
    """提取模型"""
    name: str = Field("", description="提取变量名称")
    path: str = Field("", description="提取路径")
    continue_extract: bool = Field(False, description="是否继续提取")
    continue_index: int = Field(0, description="继续提取下标")
    extract_type: str = Field("", description="提取类型 jmespath jsonpath")


class TWaitRequest(BaseModel):
    """等待请求"""
    wait_time: int = Field(0, description="等待时间")


class TScriptRequest(BaseModel):
    """脚本请求"""
    script_content: str = Field(None, description="脚本类容")


class TStep(TStepBase):
    """步骤模型"""
    testcase: typing.Union[str, typing.Callable, None] = Field(None, description="测试用例")
    variables: VariablesMapping = Field({}, description="步骤变量")
    # pre_steps: "TStep" = Field([], description="前置步骤")
    # post_steps: "TStep" = Field([], description="后置步骤")
    # parameters 加入步骤 参数
    parameters: ParametersMapping = Field({}, description="步骤参数")
    setup_hooks: typing.List[typing.Union[str, dict, object]] = Field([], description="前置钩子")
    teardown_hooks: typing.List[typing.Union[str, dict, object]] = Field([], description="后置钩子")
    setup_code: typing.Optional[typing.Union[str, typing.Dict]] = Field(None, description="前置code")
    teardown_code: typing.Optional[typing.Union[str, typing.Dict]] = Field(None, description="后置code")
    # used to extract request's response field
    extracts: typing.List[ExtractData] = Field([], description="提取")
    # used to export session variables from referenced testcase
    export: Export = Field([], description="导出")
    validators: typing.List[ValidatorData] = Field([], alias="validate")
    request: TRequest = Field(None, description="api请求")
    sql_request: typing.Optional[TSqlRequest] = Field(None, description="sql请求")
    if_request: typing.Optional[TIFRequest] = Field(None, description="if请求")
    wait_request: typing.Optional[TWaitRequest] = Field(None, description="wait请求")
    loop_request: typing.Optional[TLoopRequest] = Field(None, description="loop请求")
    script_request: typing.Optional[TScriptRequest] = Field(None, description="script请求")
    ui_request: typing.Optional[TUiRequest] = Field(None, description="ui请求")


class TConfig(BaseModel):
    """配置模型"""
    name: Name = Field(..., description="名称")
    case_id: typing.Union[str, int, None] = Field(None, description="用例id")
    verify: Verify = Field(False, description="是否校验")
    base_url: BaseUrl = Field("", description="base_url")
    functions: FunctionsMapping = Field({}, description="函数mapping")
    step_rely: bool = Field(False, description="步骤依赖")
    # Text: prepare variables in debugtalk.py, ${gen_variables()}
    variables: typing.Union[VariablesMapping, str] = Field({}, description="变量")
    env_variables: typing.Union[VariablesMapping, str] = Field({}, description="环境变量")
    parameters: typing.Union[VariablesMapping, str] = Field({}, description="参数")
    # 请求头
    headers: VariablesMapping = {}
    # teardown_hooks: Hooks = []
    export: Export = Field([], description="导出数据")


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
    step_type: str = Field(..., description="步骤类型")
    setup_hooks: typing.List[typing.Union["TStepData", str]] = []
    teardown_hooks: typing.List[typing.Union["TStepData", str]] = []
    variables: typing.List[typing.Any] = Field([], description="变量")
    validators: typing.List[ValidatorData] = Field([], alias="validators")
    request: typing.Optional[TRequestData] = Field(None, description="api请求参数")
    sql_request: typing.Optional[TSqlData] = Field(None, description="sql请求参数")
    if_request: typing.Optional[TIFStepData] = Field(None, description="if请求参数")
    loop_request: typing.Optional[TLoopStepData] = Field(None, description="loop请求参数")


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


class TestCaseInOut(BaseModel):
    """用例输入输出"""
    config_vars: VariablesMapping = Field({}, description="配置参数")
    export_vars: typing.Dict = Field({}, description="导出参数")


class TestCaseSummary(BaseModel):
    """用例汇总数据"""
    name: str = Field(..., description="报告名称")
    success: bool = Field(..., description="是否成功")
    case_id: typing.Optional[typing.Union[str, int]] = Field(None, description="用例id")
    start_time: typing.Union[float, str] = Field(0, description="开始时间")
    response_time: float = Field(0, description="请求时间")
    duration: float = Field(0, description="耗时")
    run_count: int = Field(0, description="运行数量")
    actual_run_count: int = Field(0, description="实际执行数量")
    run_success_count: int = Field(0, description="运行成功数")
    run_fail_count: int = Field(0, description="运行错误数")
    run_skip_count: int = Field(0, description="运行跳过数")
    run_err_count: int = Field(0, description="运行错误数")
    start_time_iso_format: str = Field("", description="运行时间系统时间")
    in_out: TestCaseInOut = Field({}, description="输出")
    # message 记录错误信息
    message: str = Field("", description="信息")
    log: str = Field("", description="日志")
    step_results: typing.List[StepResult] = Field([], description="步骤结果")


Validators = typing.List[ValidatorData]
