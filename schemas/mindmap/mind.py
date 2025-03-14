import typing

from pydantic import BaseModel


class MindMapIn(BaseModel):
    api_case: int
    module_case: int
    mind_data: str


class MindMapOut(BaseModel):
    id: int
    mind_data: str


class MindMapQuery(BaseModel):
    id: typing.Optional[int] = None
    type: typing.Optional[str] = None
    module_case: typing.Optional[int] = None
    api_case: typing.Optional[int] = None
