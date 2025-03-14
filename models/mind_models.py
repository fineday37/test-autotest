from sqlalchemy import Column, String, Integer, select, JSON

from models.base import Base

from schemas.mindmap.mind import MindMapQuery


class MindMapModel(Base):
    __tablename__ = "mind_map"
    mind_data = Column(JSON, nullable=False, comment='脑图数据')
    module_case = Column(Integer, nullable=False, comment='模块id')
    api_case = Column(Integer, nullable=False, comment='用例id')

    @classmethod
    async def get_list(cls, mind_id: int, params: MindMapQuery):
        q = [cls.enabled_flag == 1, cls.api_case == mind_id]
        if params.id:
            q.append(cls.id == params.id)
        if params.api_case:
            q.append(cls.api_case == params.api_case)
        if params.module_case:
            q.append(cls.module_case == params.module_case)
        stmt = select(cls.mind_data).where(*q)
        return await cls.get_result(stmt)
