from aiogram import Router, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from dependency_injector.wiring import inject, Provide

from .fsm import StartState
from .constants.messages import StartMessages
from .containers import StartContainer
from .services.users import UserService


router = Router()


@router.message(Command("start"))
@inject
async def start(
    message: types.Message,
    state: FSMContext,
    user_service: UserService = Provide[StartContainer.user_service],
) -> None:
    if not await user_service.user_exists(message.from_user):
        await user_service.create_new_user(message.from_user)

    await message.answer(text=StartMessages.START)
    await state.set_state(StartState.START)
