import typing
from models.api_models import Env, EnvDataSource, EnvFunc
from schemas.api.env import EnvQuery, BindingDataSourceIn, EnvIn


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

    @staticmethod
    async def getEnvById(env_id: int) -> typing.Dict:
        """
        获取环境详情
        :param env_id:
        :return:
        """
        data = await Env.get_by_id(env_id)
        return data

    @staticmethod
    async def saveOrUpdate(params: EnvIn):
        data = await Env.create_or_update(params.model_dump())
        return data


class EnvDataSourceService:
    @staticmethod
    async def get_by_env_id(env_id: int) -> typing.Dict:
        """
        获取环境数据源
        :param env_id:
        :return:
        """
        data = await EnvDataSource.get_by_env_id(env_id)
        return data if data else []

    @staticmethod
    async def binding_data_source(params: BindingDataSourceIn):
        bind_list = await EnvDataSource.get_by_env_id(env_id=params.env_id)
        data_source_ids = [b.get("data_source_id") for b in bind_list if 'data_source_id' in b] if bind_list else []
        insert_data = [{"env_id": params.env_id, "data_source_id": source_id} \
                       for source_id in data_source_ids if source_id not in params.data_source_ids] if data_source_ids \
            else [{"env_id": params.env_id, "data_source_id": source_id} for source_id in params.data_source_ids]
        return await EnvDataSource.batch_create(insert_data)


class EnvFuncService:
    @staticmethod
    async def get_by_env_id(env_id: int) -> typing.Dict:
        """
        获取环境函数
        :param env_id:
        :return:
        """
        data = await EnvFunc.get_by_env_id(env_id)
        return data if data else []
