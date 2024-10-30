class UserAlreadyExistsError(Exception):
    def __init__(self, *args: object, tg_id: int) -> None:
        super().__init__(*args)
        self._tg_id = tg_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: user with id {self._tg_id} already exists in database"
