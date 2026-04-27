from __future__ import annotations

import json
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ecm_optimizer.config import PACKAGE_VERSION


def utc_timestamp() -> str:
    """Вернуть текущий UTC-moment в компактном формате для имен файлов."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_dir(path: str | Path) -> Path:
    """Гарантировать существование директории и вернуть объект `Path`."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def current_command_line() -> str:
    """Вернуть команду запуска в shell-safe виде с нормализованным CLI-алиасом."""
    normalized_args = ["ecm-optimizer", *sys.argv[1:]]
    return " ".join(shlex.quote(arg) for arg in normalized_args)


def enrich_with_metadata(
    payload: dict[str, Any],
    *,
    command: str | None = None,
    command_line: str | None = None,
) -> dict[str, Any]:
    """Добавить к payload стандартные метаданные проекта."""
    metadata = {
        "timestamp_utc": utc_timestamp(),
        "package_version": PACKAGE_VERSION,
    }
    if command is not None:
        metadata["command"] = command
    if command_line is not None:
        metadata["command_line"] = command_line
    return {**metadata, **payload}


def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    """Сериализовать словарь в JSON-файл с красивым форматированием."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def write_json_atomic(path: str | Path, payload: dict[str, Any], *, tmp_suffix: str = ".tmp") -> None:
    """
    Атомарно записать JSON через временный файл и replace.

    Это снижает риск получить битый JSON при аварийной остановке процесса во время записи.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = p.with_name(f"{p.name}{tmp_suffix}")
    tmp_path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp_path.replace(p)


def write_json_with_meta(
    path: str | Path,
    payload: dict[str, Any],
    *,
    command: str | None = None,
    command_line: str | None = None,
) -> None:
    """Сохранить JSON-файл и автоматически дополнить его метаданными."""
    write_json(path, enrich_with_metadata(payload, command=command, command_line=command_line))


def read_json(path: str | Path) -> dict[str, Any]:
    """Прочитать JSON-файл и вернуть его содержимое как словарь."""
    return json.loads(Path(path).read_text(encoding="utf-8"))
