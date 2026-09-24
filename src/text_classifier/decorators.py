# Dekoratori za logiranje i mjerenje vremena.
# `timed` mi je ujedno i primjer closurea.

from __future__ import annotations

import functools
import logging
import time
from typing import Callable, Optional, TypeVar

# Dekorator ne dira tip rezultata, pa ga provlacim kroz TypeVar.
T = TypeVar("T")

logger = logging.getLogger("text_classifier")


def log_calls(func: Callable[..., T]) -> Callable[..., T]:
    """Zapise svaki poziv funkcije, s argumentima i s onim sto je vratila.

    >>> @log_calls
    ... def zbroji(a: int, b: int) -> int:
    ...     return a + b
    >>> zbroji(2, 3)
    5
    >>> zbroji.__name__
    'zbroji'
    """
    @functools.wraps(func)  # bez ovoga funkcija izgubi svoje ime i docstring
    def wrapper(*args: object, **kwargs: object) -> T:
        logger.debug("poziv %s(args=%s, kwargs=%s)", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logger.debug("%s -> %r", func.__name__, result)
        return result

    return wrapper


def timed(label: Optional[str] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Izmjeri koliko je funkcija trajala i zapise to u log.

    Posto prima argument, ima jedan sloj vise nego obicni dekorator: `timed`
    vraca dekorator, a dekorator vraca wrapper. I jedan i drugi vide `label`
    iz vanjske funkcije, i to je taj closure.

    >>> @timed("test")
    ... def spora() -> int:
    ...     return sum(range(1_000))
    >>> spora()
    499500
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        name: str = label or func.__name__

        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> T:
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                # finally da izmjerim vrijeme i kad funkcija pukne
                elapsed_ms = (time.perf_counter() - start) * 1000.0
                logger.info("%s trajalo %.1f ms", name, elapsed_ms)

        return wrapper

    return decorator
