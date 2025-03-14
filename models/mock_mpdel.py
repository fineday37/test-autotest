from .base import Base
from sqlalchemy import Column, Integer, String, Select
from sqlalchemy.orm import aliased
from .api_models import User, ProjectInfo, ModuleInfo
from corelibs import g


class Mock(Base):
    __tablename__ = 'mock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False, comment='所属项目')
    module_id = Column(Integer, nullable=False, comment='所属模块')
    name = Column(String(255), nullable=False, comment='mock名称')
    path = Column(String(255), nullable=False, comment='mock路径')
    method = Column(String(255), nullable=False, comment='mock请求方式')
    content = Column(String(255), nullable=False, comment='mock内容')
    content_type = Column(String(255), nullable=False, comment='mock内容类型')
    http_code = Column(Integer, nullable=False, comment='http状态码')
    remark = Column(String(255), nullable=False, comment='备注')

    @classmethod
    async def get_mock_list(cls, params):
        q = [cls.enabled_flag == 1]
        if params.id and params.id != '':
            q.append(cls.id == params.id)
        if params.name and params.name != '':
            q.append(cls.name.like('%' + params.name + '%'))
        u = aliased(User)
        stmt = Select(cls.get_table_columns(),
                      u.nickname.label("created_by_name"),
                      User.nickname.label("updated_by_name"),
                      ProjectInfo.name.label("project_name"),
                      ModuleInfo.name.label("module_name"),
                      (g.request.url.scheme + "://" + g.request.headers.get('host') + cls.path).label("url")
                      ).where(*q) \
            .outerjoin(u, u.id == cls.created_by) \
            .outerjoin(User, User.id == cls.updated_by)\
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id)\
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id)
        return await cls.pagination(stmt)
