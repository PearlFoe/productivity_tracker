from collections.abc import Callable
from functools import wraps
from typing import Any


def wrap_injected(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args: tuple, **kwargs: dict) -> Any:
        return f(*args, **kwargs)

    return wrapper
