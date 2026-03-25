from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.config import NUMBERS_DIR
from ecm_optimizer.core.problem import read_dataset_metadata


def resolve_dataset_path(dataset_ref: str | None, *, expected_file: str) -> Path:
    """Resolve dataset reference from file path, directory path, or latest generated dataset."""
    if dataset_ref is None:
        latest_dir = _latest_generated_dataset_dir(expected_file=expected_file)
        if latest_dir is None:
            raise click.UsageError(
                f"No generated datasets found in {NUMBERS_DIR}. Generate one first or pass --dataset explicitly."
            )
        return latest_dir / expected_file

    ref = Path(dataset_ref)

    if ref.exists() and ref.is_file():
        return ref

    if ref.exists() and ref.is_dir():
        candidate = ref / expected_file
        if candidate.exists() and candidate.is_file():
            return candidate
        raise click.UsageError(f"Expected dataset file '{expected_file}' inside directory: {ref}")

    if ref.suffix:
        raise click.UsageError(f"Dataset file not found: {ref}")

    candidate = NUMBERS_DIR / ref / expected_file
    if candidate.exists() and candidate.is_file():
        return candidate

    raise click.UsageError(
        f"Cannot resolve dataset '{dataset_ref}'. Pass full file path or generated folder name under {NUMBERS_DIR}."
    )


def dataset_generation_seed(dataset_path: Path, *, fallback: int) -> int:
    """Read generation seed from dataset metadata and return fallback on missing/invalid value."""
    meta = read_dataset_metadata(dataset_path)
    raw = meta.get("seed")
    if raw is None:
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback


def _latest_generated_dataset_dir(*, expected_file: str) -> Path | None:
    if not NUMBERS_DIR.exists():
        return None

    candidates = [
        d for d in NUMBERS_DIR.iterdir()
        if d.is_dir() and (d / expected_file).exists() and (d / 'generation.json').exists()
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda d: d.stat().st_mtime)
