from aiogram import Router

from src.settings import Settings
from .routers import router
from .containers import CalendarContainer


async def _get_container(settings: Settings) -> CalendarContainer:
    container = CalendarContainer()
    container.env.from_dict(settings.model_dump())
    # await container.init_resources()

    return container


async def get_router(settings: Settings) -> Router:
    _router = Router()
    _router.container = await _get_container(settings)
    _router.include_router(router)
    return _router
