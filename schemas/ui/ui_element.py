from pydantic import BaseModel, Field


class UiElementQuery(BaseModel):
    name: str = Field(None, title="用例名称", description='用例名称')
    page_id: int = Field(None, title="页面id", description='页面id')


class UiElementIn(BaseModel):
    name: str = Field(None, title="元素名称", description='元素名称')
    location_method: str = Field(..., title="定位方式")
    location_value: str = Field(..., title="定位值")
    page_id: int = Field(..., title="页面id")
    remarks: str = Field(None, title="备注")