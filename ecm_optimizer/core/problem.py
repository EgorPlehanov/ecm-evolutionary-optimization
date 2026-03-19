from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

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


def write_dataset(path: str | Path, numbers: list[int], header: str) -> None:
    """Сохранить список чисел в текстовый файл датасета."""
    lines = [f"# {header}", "# one decimal composite N per line"]
    lines.extend(str(n) for n in numbers)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(path: str | Path, samples: list[GeneratedSample]) -> None:
    """Сохранить полный manifest с `n`, `p` и `q` для всех образцов."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rows = ["n,p,q"]
    rows.extend(f"{s.n},{s.p},{s.q}" for s in samples)
    Path(path).write_text("\n".join(rows) + "\n", encoding="utf-8")


def read_dataset_metadata(path: str | Path) -> dict[str, str]:
    """Прочитать метаданные из первых строк датасета с комментариями."""
    metadata: dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines()[:10]:
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
    """Прочитать текстовый датасет и извлечь из него числа `N`."""
    values: list[int] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(int(line))
    return values
