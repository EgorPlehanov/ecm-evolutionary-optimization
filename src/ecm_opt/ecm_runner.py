from __future__ import annotations

import re
import subprocess
import time
from dataclasses import dataclass

SUCCESS_RE = re.compile(r"Factor found")


@dataclass(frozen=True)
class CurveRun:
    """Результат одного запуска кривой ECM."""

    success: bool
    seconds: float
    stdout: str
    stderr: str


def run_single_curve(ecm_bin: str, n: int, b1: int, b2: int, timeout_sec: float | None = None) -> CurveRun:
    """Запустить одну кривую ECM для числа `n` и вернуть флаг успеха и время.

    Args:
        ecm_bin: Путь к бинарнику `ecm`.
        n: Составное число, которое нужно факторизовать.
        b1: Первая граница ECM.
        b2: Вторая граница ECM.
        timeout_sec: Ограничение по времени на один запуск.

    Returns:
        Объект `CurveRun` со статусом, временем выполнения и выводом процесса.
    """
    cmd = [ecm_bin, str(b1), str(b2)]
    started = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            input=f"{n}\n",
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - started
        return CurveRun(success=False, seconds=elapsed, stdout=exc.stdout or "", stderr=(exc.stderr or "") + "\nTIMEOUT")

    elapsed = time.perf_counter() - started
    output = (proc.stdout or "") + "\n" + (proc.stderr or "")

    success = bool(SUCCESS_RE.search(output))
    return CurveRun(success=success, seconds=elapsed, stdout=proc.stdout, stderr=proc.stderr)
