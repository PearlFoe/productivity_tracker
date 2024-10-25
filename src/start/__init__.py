from aiogram import Router

from src.settings import Settings
from .routers import router


def get_router(settings: Settings) -> Router:
    _router = Router()
    _router.include_router(router)
    return _router
