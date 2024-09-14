from schemas.ui.ui_case import UiCaseQuery
from schemas.ui.ui_element import UiElementQuery
from schemas.ui.ui_page import UiPageQuery
from .base import Base
from sqlalchemy import Column, String, Integer, JSON, select, func
from sqlalchemy.orm import aliased
from .systerm_models import User
from .api_models import ProjectInfo, ModuleInfo


class UiCase(Base):
    __tablename__ = "ui_case"
    name = Column(String(255), nullable=False, comment="用例名称", index=True)
    tags = Column(JSON, nullable=False, comment="用例标签")
    project_id = Column(Integer, nullable=False, comment="项目id")
    module_id = Column(Integer, nullable=False, comment="模块id")
    steps = Column(JSON, nullable=True, comment='运行步骤')
    setup_hooks = Column(JSON, nullable=True, comment='前置操作')
    teardown_hooks = Column(JSON, nullable=True, comment='后置操作')
    variables = Column(JSON, nullable=True, comment='变量')
    version = Column(String(255), nullable=False, comment='版本')
    remarks = Column(String(255), nullable=True, comment='备注')

    @classmethod
    async def get_list(cls, params: UiCaseQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('created_by_name'),
                      User.nickname.label('updated_by_name'),
                      ProjectInfo.name.label('project_name'),
                      ModuleInfo.name.label('module_name')).where(*q) \
            .outerjoin(u, cls.created_by == u.id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(ModuleInfo, cls.module_id == ModuleInfo.id) \
            .outerjoin(User, cls.updated_by == User.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_case_by_id(cls, pk: int):
        q = [cls.enabled_flag == 1, cls.id == pk]
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')
                      ) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())
        return await cls.get_result(stmt, first=True)


class UiElement(Base):
    __tablename__ = "ui_element"

    name = Column(String(255), nullable=False, comment='元素名称', index=True)
    location_method = Column(String(255), nullable=True, comment='定位类型')
    location_value = Column(String(255), nullable=True, comment='定位元素值')
    page_id = Column(Integer, nullable=False, comment='关联页面', index=True)
    remarks = Column(String(255), nullable=True, comment='备注')

    @classmethod
    async def get_list(cls, params: UiElementQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.page_id:
            q.append(cls.page_id == params.page_id)
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('created_by_name'),
                      User.nickname.label('updated_by_name')).where(*q).outerjoin(u, cls.created_by == u.id) \
            .outerjoin(User, cls.updated_by == User.id).order_by(cls.id.desc())
        return await cls.pagination(stmt)


class UiPage(Base):
    __tablename__ = "ui_page"
    name = Column(String(255), nullable=False, comment='页面名称', index=True)
    url = Column(String(255), nullable=False, comment='url')
    project_id = Column(Integer, nullable=True, comment='项目id')
    module_id = Column(Integer, nullable=True, comment='模块id')
    tags = Column(JSON, nullable=False, comment='标签')
    remarks = Column(String(255), nullable=True, comment='备注')

    @classmethod
    async def get_list(cls, params: UiPageQuery):
        q = [cls.enabled_flag == 1]
        if params.name:
            q.append(cls.name.like(f'%{params.name}%'))
        if params.url:
            q.append(cls.url.like(f'%{params.url}%'))
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      u.nickname.label('created_by_name'),
                      User.nickname.label('update_by_name'),
                      ProjectInfo.name.label('project_name'),
                      ModuleInfo.name.label('module_name'),
                      func.count(UiElement.id).label('element_count')).where(*q).outerjoin(u, cls.created_by == u.id) \
            .outerjoin(User, cls.updated_by == User.id) \
            .outerjoin(ProjectInfo, cls.project_id == ProjectInfo.id) \
            .outerjoin(ModuleInfo, cls.module_id == ModuleInfo.id) \
            .outerjoin(UiElement, UiElement.page_id == cls.id) \
            .group_by(cls.id) \
            .order_by(cls.id.desc())
        return await cls.pagination(stmt)

    @classmethod
    async def get_page_by_id(cls, pk):
        q = [cls.enabled_flag == 1, cls.id == pk]
        u = aliased(User)
        stmt = select(cls.get_table_columns(),
                      ModuleInfo.name.label('module_name'),
                      ProjectInfo.name.label('project_name'),
                      u.nickname.label('updated_by_name'),
                      User.nickname.label('created_by_name')) \
            .where(*q) \
            .outerjoin(u, u.id == cls.updated_by) \
            .outerjoin(ProjectInfo, ProjectInfo.id == cls.project_id) \
            .outerjoin(ModuleInfo, ModuleInfo.id == cls.module_id) \
            .outerjoin(User, User.id == cls.created_by) \
            .order_by(cls.id.desc())

        return await cls.get_result(stmt, first=True)
