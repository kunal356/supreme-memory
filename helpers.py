"""Helper utilities (profiling, etc.) used by the scripts."""
import time
import logging

from typing import Callable, Any, Sequence, Tuple

logger = logging.getLogger("trackbase.helpers")


def profile_call(func: Callable[..., Any], args: Sequence[Any]) -> Tuple[list, int]:
    """Time the execution of a function with the given positional arguments.

    Args:
        func: The callable to profile.
        args: A sequence of positional arguments to pass to the function.

    Returns:
        A 2-tuple of (result, duration_ms) where:
            - result is whatever the function returns,
            - duration_ms is an integer duration in milliseconds.
    """
    start = time.monotonic()
    try:
        result = func(*args)
        duration_ms = int((time.monotonic() - start) * 1000)
        return result, duration_ms
    except Exception:
        duration_ms = int((time.monotonic() - start) * 1000)
        logger.exception("profile_call: function %r failed after %d ms", getattr(
            func, "__name__", func), duration_ms)
        raise
