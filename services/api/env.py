import typing

from models.api_models import Env
from schemas.api.env import EnvQuery


class EnvService:
    @staticmethod
    async def list(params: EnvQuery) -> typing.Dict:
        """
        获取环境列表
        :param params:
        :return:
        """
        data = await Env.get_list(params)
        return data
