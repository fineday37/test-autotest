from pydantic import BaseModel, Field
import typing


class MockQuery(BaseModel):
    id: typing.Optional[int] = Field(None, description='mock id')
    name: typing.Optional[str] = Field(None, description='mock名称')
