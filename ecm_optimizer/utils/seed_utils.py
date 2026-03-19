from __future__ import annotations

import hashlib


def make_deterministic_seed(seed: int | None, salt: str) -> int:
    """Построить детерминированный seed на основе базового seed и salt."""
    base = 0 if seed is None else int(seed)
    digest = hashlib.sha256(f"{base}:{salt}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % (2**32)


def get_seed(seed: int | None, salt: str) -> int:
    """Получить независимый детерминированный seed для отдельной задачи."""
    return make_deterministic_seed(seed, salt)
