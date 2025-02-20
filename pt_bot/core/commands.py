from aiogram.types import BotCommand

COMMANDS = (
    BotCommand(
        command="/start",
        description="Start dialog with bot",
    ),
    BotCommand(
        command="/calendar",
        description="Add new or change connected calendars",
    ),
    BotCommand(
        command="/notification",
        description="Modify notifications settings",
    ),
    BotCommand(
        command="/statistics",
        description="Show calendar statistics",
    ),
)
