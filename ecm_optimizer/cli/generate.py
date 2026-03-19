from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.config import DEFAULT_COFACTOR_DIGITS, DEFAULT_CONTROL_COUNT, DEFAULT_PREFIX, DEFAULT_SEED, DEFAULT_TRAIN_COUNT, NUMBERS_DIR
from ecm_optimizer.core.problem import generate_semiprime_samples, write_dataset, write_manifest


@click.command("generate")
@click.option("--target-digits", required=True, type=int, help="Digits of target prime factor p.")
@click.option("--cofactor-digits", default=DEFAULT_COFACTOR_DIGITS, show_default=True, type=int)
@click.option("--train-count", default=DEFAULT_TRAIN_COUNT, show_default=True, type=int)
@click.option("--control-count", default=DEFAULT_CONTROL_COUNT, show_default=True, type=int)
@click.option("--seed", default=DEFAULT_SEED, show_default=True, type=int)
@click.option("--output-dir", default=str(NUMBERS_DIR), show_default=True, type=click.Path(path_type=Path))
@click.option("--prefix", default=DEFAULT_PREFIX, show_default=True, type=str)
def generate_command(
    target_digits: int,
    cofactor_digits: int,
    train_count: int,
    control_count: int,
    seed: int,
    output_dir: Path,
    prefix: str,
) -> None:
    """Сгенерировать train/control-датасеты полупростых чисел."""
    total = train_count + control_count
    samples = generate_semiprime_samples(
        target_factor_digits=target_digits,
        cofactor_digits=cofactor_digits,
        count=total,
        seed=seed,
    )

    train = samples[:train_count]
    control = samples[train_count:]

    train_path = output_dir / f"{prefix}_train.txt"
    control_path = output_dir / f"{prefix}_control.txt"
    manifest_path = output_dir / f"{prefix}_manifest.csv"

    write_dataset(
        train_path,
        [s.n for s in train],
        header=f"train dataset: target_digits={target_digits}, cofactor_digits={cofactor_digits}, seed={seed}",
    )
    write_dataset(
        control_path,
        [s.n for s in control],
        header=f"control dataset: target_digits={target_digits}, cofactor_digits={cofactor_digits}, seed={seed}",
    )
    write_manifest(manifest_path, samples)

    click.echo(f"train_file={train_path}")
    click.echo(f"control_file={control_path}")
    click.echo(f"manifest_file={manifest_path}")
    click.echo(f"generated={total}")
