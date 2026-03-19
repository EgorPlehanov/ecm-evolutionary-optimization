from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(verbose: bool = False, log_file: str | Path | None = None) -> logging.Logger:
    """Настроить логирование в консоль и при необходимости в файл."""
    level = logging.DEBUG if verbose else logging.INFO
    logger = logging.getLogger("ecm_optimizer")
    logger.setLevel(level)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    if log_file is not None:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(path, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
