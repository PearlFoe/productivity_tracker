from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

from dependency_injector.wiring import inject as di_inject

F = TypeVar("F", bound=Callable[..., Any])


def inject(f: F) -> F:
    @wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        injected = di_inject(f)
        return injected(*args, **kwargs)

    return cast(F, wrapper)
