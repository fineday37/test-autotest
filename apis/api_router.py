
from fastapi import APIRouter
from apis.system import user, roles, file, menu
from apis.api import api_case, api_info, project, module, env, api_report, functions
from apis.ui import ui_case, ui_page, ui_element
from apis.mindmap import mind

app_router = APIRouter()

# system
app_router.include_router(user.router, prefix="/user", tags=["user"])
app_router.include_router(roles.router, prefix="/role", tags=["role"])
app_router.include_router(file.router, prefix='/file', tags=["file"])
app_router.include_router(menu.router, prefix='/menu', tags=["menu"])

# api
app_router.include_router(api_info.router, prefix='/apiInfo', tags=["api_info"])
app_router.include_router(api_case.router, prefix="/apiCase", tags=["api_case"])
app_router.include_router(project.router, prefix="/project", tags=["project"])
app_router.include_router(module.router, prefix="/module", tags=["module"])
app_router.include_router(env.router, prefix="/env", tags=["env"])
app_router.include_router(api_report.router, prefix="/report", tags=["report"])
app_router.include_router(functions.router, prefix="/functions", tags=["functions"])
app_router.include_router(ui_case.router, prefix="/uiCase", tags=["ui_case"])
app_router.include_router(ui_page.router, prefix="/uiPage", tags=["ui_page"])
app_router.include_router(ui_element.router, prefix="/uiElement", tags=["ui_element"])
app_router.include_router(mind.router, prefix="/mind", tags=["mind"])

