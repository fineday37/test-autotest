import json

from starlette.responses import JSONResponse

from schemas.api.mock import MockQuery
from models.mock_mpdel import Mock
from fastapi import FastAPI


class MockService:
    @staticmethod
    async def get_mock_list(params: MockQuery):
        data = await Mock.get_mock_list(params)
        return data

    @staticmethod
    async def run_mock(app: FastAPI):
        @app.on_event("startup")
        async def load_mock_apis():
            data = await Mock.get_all()
            for item in data:
                app.add_route(item["path"],
                              lambda response=item["content"]: JSONResponse(
                                  content=json.loads(item["content"])),
                              methods=[item["method"]])
