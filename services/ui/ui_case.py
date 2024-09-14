from schemas.api.api_case import TCaseStepData, TestCaseRun
from schemas.ui.ui_case import UiCaseQuery, UiCaseIn, UiCaseId
from models.ui_models import UiCase
from services.api.run_handle_new import HandelTestCase
from zerorunner.models import TUiRequest


class UiCaseServer:
    @staticmethod
    async def list(params: UiCaseQuery):
        return await UiCase.get_list(params)

    @staticmethod
    async def get_case_by_id(params: UiCaseId):
        """根据id获取用例信息"""
        if not params.id:
            raise ValueError("id参数不能为空")
        page_info = await UiCase.get_case_by_id(params.id)
        if not page_info:
            raise ValueError("用例不存在")
        return page_info

    @staticmethod
    async def save_or_update(params: UiCaseIn):
        """保存或更新用例信息"""
        page_info = await UiCase.create_or_update(params.model_dump())
        return await UiCaseServer.get_case_by_id(UiCaseId(id=page_info['id']))

    @staticmethod
    async def handel_ui_case2run_schemas(ui_case: UiCaseIn):
        """处理用例信息"""
        step_data = []
        if ui_case.steps:
            for step in ui_case.steps:
                case_step = TCaseStepData(
                    case_id=ui_case.id,
                    name=step.name,
                    index=step.index,
                    step_type='ui',
                    enable=step.enable,
                    variables=step.variables,
                    ui_request=TUiRequest(
                        action=step.action,
                        data=step.data,
                        location_value=step.location_value,
                        location_method=step.location_method,
                        cookie=step.cookie,
                        output=step.output,
                    ),
                )
                step_data.append(case_step)
        run_params = TestCaseRun(id=ui_case.id,
                                 name=ui_case.name,
                                 env_id=None,
                                 project_id=ui_case.project_id,
                                 module_id=ui_case.module_id,
                                 remarks=ui_case.remarks,
                                 variables=ui_case.variables,
                                 step_data=step_data)
        api_case_info = await HandelTestCase().init(run_params)
        return api_case_info
