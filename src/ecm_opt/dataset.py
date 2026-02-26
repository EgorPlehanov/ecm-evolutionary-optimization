from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GeneratedSample:
    n: int
    p: int
    q: int


def _is_probable_prime(n: int, rounds: int = 16, rng: random.Random | None = None) -> bool:
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
    if count <= 0:
        raise ValueError("count must be positive")
    if cofactor_digits <= 0 or target_factor_digits <= 0:
        raise ValueError("digit sizes must be positive")

    rng = random.Random(seed)
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


def write_dataset(path: str, numbers: list[int], header: str) -> None:
    lines = [f"# {header}", "# one decimal composite N per line"]
    lines.extend(str(n) for n in numbers)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(path: str, samples: list[GeneratedSample]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rows = ["n,p,q"]
    rows.extend(f"{s.n},{s.p},{s.q}" for s in samples)
    Path(path).write_text("\n".join(rows) + "\n", encoding="utf-8")
