# Postavljanje logiranja. Dekoratori pisu kroz isti ovaj logger.

from __future__ import annotations

import logging

from .config import LOG_DIR, LOG_FILE

_LOGGER_NAME = "text_classifier"


def setup_logging(console_level: int = logging.INFO) -> logging.Logger:
    """Slozi logger tako da pise i u konzolu i u datoteku."""
    logger = logging.getLogger(_LOGGER_NAME)
    if logger.handlers:
        # vec je postavljeno, inace bi se svaka poruka ispisala dvaput
        return logger

    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s")

    console = logging.StreamHandler()
    console.setLevel(console_level)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # U datoteku ide sve, u konzolu samo ono bitnije.
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    return logger
