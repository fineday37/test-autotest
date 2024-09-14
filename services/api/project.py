import typing

from corelibs.codes import CodeEnum
from exceptions.exceptions import ParameterError
from schemas.api.project import ProjectQuery, ProjectIn, ProjectId
from models.api_models import ProjectInfo, ModuleInfo


class ProjectService:
    @staticmethod
    async def get_project_list(params: ProjectQuery) -> typing.Dict:
        data = await ProjectInfo.project_list(params)
        return data

    @staticmethod
    async def save_or_update(params: ProjectIn) -> typing.Dict:
        if params.id:
            project_info = await ProjectInfo.get(params.id)
            if project_info.name != params.name:
                if await ProjectInfo.get_project_by_name(params.name):
                    raise ParameterError(CodeEnum.PROJECT_NAME_EXIST)
        else:
            if await ProjectInfo.get_project_by_name(params.name):
                raise ParameterError(CodeEnum.PROJECT_NAME_EXIST)
        return await ProjectInfo.create_or_update(params.model_dump())

    @staticmethod
    async def deleted(params: ProjectId) -> int:
        relation_module = await ModuleInfo.get_module_by_project_id(params.id)
        if relation_module:
            raise ParameterError(CodeEnum.PROJECT_HAS_MODULE_ASSOCIATION)
        return await ProjectInfo.delete(params.id)

    @staticmethod
    async def get_project_tree() -> typing.List:
        project_list = await ProjectInfo.get_all()
        module_list = await ModuleInfo.get_all()
        project_tree_list = []
        for project in project_list:
            project["children"] = []
            project['disabled'] = True
            for module in module_list:
                if module['project_id'] == project['id']:
                    project["children"].append(module)
                    project['disabled'] = False
            project_tree_list.append(project)
        return project_tree_list
