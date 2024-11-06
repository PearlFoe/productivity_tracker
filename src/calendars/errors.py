class BaseCalendarError(Exception):
    def __init__(self, *args: object, message: str) -> None:
        super().__init__(*args)
        self._message = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self._message}"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self._message}"


class CalendarDuplicateError(BaseCalendarError):
    def __init__(self, *args: object, calendar_id: str, message: str = None) -> None:
        super().__init__(*args, message=message or "Calendar with id {calendar_id} already exists")


class InvalidCalendarIDError(BaseCalendarError):
    def __init__(self, *args: object, calendar_id: str, message: str = None) -> None:
        super().__init__(
            *args, message=message or "Calendar with id {calendar_id} not found or access was not granted"
        )
