import time
from typing import Callable


def profile_call(func: Callable, args: list):
    start = time.monotonic()
    result = func(*args)
    duration = (time.monotonic() - start) * 1000

    return result, int(duration)
