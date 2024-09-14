from pydantic import BaseModel, Field
import typing


class FunctionQuery(BaseModel):
    id: int = Field(None, description="id")
    ids: typing.List[int] = Field(None, description="ids")
    project_name: str = Field(None, description="项目名称")
    name: str = Field(None, description="脚本名称")
    common: str = Field(None, description="")


class FuncIn(BaseModel):
    id: int = Field(None, description="id")
    content: str = Field(None, description="")
    project_id: str = Field(None, description="")
    name: str = Field(None, description="")
    remarks: str = Field(None, description="")


class FuncListQuery(BaseModel):
    id: typing.Optional[int] = Field(None, description="id")
    func_name: str = Field(None, description="函数名称")


class FuncId(BaseModel):
    id: int = Field(..., description="id")


class FuncDebug(BaseModel):
    id: typing.Optional[int] = Field(None, description="id")
    func_parse_str: str = Field(None, description="")
    func_name: str = Field(None, description="")
    args_info: typing.Dict[typing.Text, typing.Any] = Field({}, description="")
