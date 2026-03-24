from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ecm_optimizer.utils.seed_utils import get_seed


@dataclass(frozen=True)
class GeneratedSample:
    """Один сгенерированный полупростой пример и его множители."""

    n: int
    p: int
    q: int


def _is_probable_prime(n: int, rounds: int = 16, rng: random.Random | None = None) -> bool:
    """Проверить число на вероятную простоту тестом Миллера — Рабина."""
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2

    rng = rng or random.Random()
    for _ in range(rounds):
        a = rng.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _random_odd_with_digits(digits: int, rng: random.Random) -> int:
    """Сгенерировать случайное нечетное число с заданным количеством цифр."""
    if digits <= 0:
        raise ValueError("digits must be positive")
    low = 10 ** (digits - 1)
    high = 10**digits - 1
    x = rng.randrange(low, high + 1)

    if x % 2 == 0:
        x += 1
        if x > high:
            x -= 2
    return x


def _generate_prime(digits: int, rng: random.Random) -> int:
    """Итеративно искать простое число заданной длины."""
    while True:
        candidate = _random_odd_with_digits(digits=digits, rng=rng)
        if _is_probable_prime(candidate, rng=rng):
            return candidate


def generate_semiprime_samples(
    target_factor_digits: int,
    cofactor_digits: int,
    count: int,
    seed: int,
) -> list[GeneratedSample]:
    """Сгенерировать набор уникальных полупростых чисел `n = p * q`."""
    if count <= 0:
        raise ValueError("count must be positive")
    if cofactor_digits <= 0 or target_factor_digits <= 0:
        raise ValueError("digit sizes must be positive")

    rng = random.Random(get_seed(seed, "dataset-generation"))
    samples: list[GeneratedSample] = []
    seen_n: set[int] = set()

    while len(samples) < count:
        p = _generate_prime(target_factor_digits, rng)
        q = _generate_prime(cofactor_digits, rng)
        if p == q:
            continue
        n = p * q
        if n in seen_n:
            continue
        seen_n.add(n)
        samples.append(GeneratedSample(n=n, p=p, q=q))

    return samples


def _write_json(path: str | Path, payload: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_dataset(
    path: str | Path,
    numbers: list[int],
    role: str,
    generation: dict[str, Any] | None = None,
) -> None:
    """Сохранить список чисел в JSON-файл датасета."""
    payload: dict[str, Any] = {"format": "ecm_dataset_v1", "role": role, "numbers": numbers}
    if generation is not None:
        payload["generation"] = generation
    _write_json(path, payload)


def write_manifest(path: str | Path, samples: list[GeneratedSample]) -> None:
    """Сохранить полный manifest с `n`, `p` и `q` для всех образцов в JSON."""
    _write_json(path, {"format": "ecm_manifest_v1", "samples": [s.__dict__ for s in samples]})


def write_generation_metadata(path: str | Path, payload: dict[str, Any]) -> None:
    """Сохранить JSON с параметрами генерации и путями к артефактам."""
    _write_json(path, payload)


def read_dataset_metadata(path: str | Path) -> dict[str, str]:
    """Прочитать метаданные датасета (JSON или старый text/csv формат)."""
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        metadata: dict[str, str] = {}
        generation = data.get("generation") if isinstance(data, dict) else None
        if isinstance(generation, dict):
            for key, value in generation.items():
                metadata[str(key)] = str(value)
        return metadata

    metadata: dict[str, str] = {}
    for line in p.read_text(encoding="utf-8").splitlines()[:10]:
        line = line.strip()
        if not line.startswith("#"):
            continue
        body = line.lstrip("#").strip()
        for part in body.split(","):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                metadata[k.strip()] = v.strip()
    return metadata


def load_numbers(path: str | Path) -> list[int]:
    """Прочитать датасет и извлечь из него числа `N` (JSON или старый text/csv)."""
    p = Path(path)
    if p.suffix.lower() == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("numbers"), list):
            return [int(v) for v in data["numbers"]]
        if isinstance(data, list):
            return [int(v) for v in data]
        raise ValueError(f"Unsupported dataset JSON format: {p}")

    values: list[int] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(int(line))
    return values
