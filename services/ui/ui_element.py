from models.ui_models import UiElement
from schemas.ui.ui_element import UiElementQuery, UiElementIn


class UiElementService:

    @staticmethod
    async def list(params: UiElementQuery):
        return await UiElement.get_list(params)

    @staticmethod
    async def save_or_update(params: UiElementIn):
        return await UiElement.create_or_update(params.model_dump())
