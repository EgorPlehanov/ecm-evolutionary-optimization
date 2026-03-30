from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.config import DEFAULT_COFACTOR_DIGITS, DEFAULT_CONTROL_COUNT, DEFAULT_PREFIX, DEFAULT_SEED, DEFAULT_TRAIN_COUNT, NUMBERS_DIR
from ecm_optimizer.core.problem import generate_semiprime_samples, write_dataset, write_generation_metadata, write_manifest
from ecm_optimizer.utils.io_utils import ensure_dir, utc_timestamp


@click.command("generate")
@click.option("--target-digits", required=True, type=int, help="Number of decimal digits in the target prime factor p.")
@click.option("--cofactor-digits", default=DEFAULT_COFACTOR_DIGITS, show_default=True, type=int, help="Number of decimal digits in the second prime factor q.")
@click.option("--train-count", default=DEFAULT_TRAIN_COUNT, show_default=True, type=int, help="How many samples to put into the training dataset.")
@click.option("--control-count", default=DEFAULT_CONTROL_COUNT, show_default=True, type=int, help="How many samples to put into the control dataset.")
@click.option("--seed", default=DEFAULT_SEED, show_default=True, type=int, help="Base random seed used for deterministic dataset generation.")
@click.option("--output-dir", default=str(NUMBERS_DIR), show_default=True, type=click.Path(path_type=Path), help="Directory where generated dataset files will be written.")
@click.option("--prefix", default=DEFAULT_PREFIX, show_default=True, type=str, help="Subdirectory prefix for generated files.")
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

    timestamp = utc_timestamp()
    folder_name = f"{target_digits}_{prefix}_{timestamp}" if prefix else f"{target_digits}_{timestamp}"
    artifact_dir = ensure_dir(output_dir / folder_name)

    generation_meta = {
        "target_digits": target_digits,
        "cofactor_digits": cofactor_digits,
        "seed": seed,
        "train_count": train_count,
        "control_count": control_count,
        "total_count": total,
        "prefix": prefix,
        "timestamp_utc": timestamp,
    }

    train_path = artifact_dir / "train.json"
    control_path = artifact_dir / "control.json"
    manifest_path = artifact_dir / "manifest.json"
    generation_path = artifact_dir / "generation.json"

    write_dataset(
        train_path,
        [s.n for s in train],
        role="train",
        generation=generation_meta,
    )
    write_dataset(
        control_path,
        [s.n for s in control],
        role="control",
        generation=generation_meta,
    )
    write_manifest(manifest_path, samples)
    write_generation_metadata(
        generation_path,
        {
            "format": "ecm_generation_v1",
            "generation": generation_meta,
            "files": {
                "train": str(train_path),
                "control": str(control_path),
                "manifest": str(manifest_path),
            },
        },
    )

    click.echo(f"dataset_dir: {artifact_dir}")
    click.echo(f"   train_file: {train_path}")
    click.echo(f"   control_file: {control_path}")
    click.echo(f"   manifest_file: {manifest_path}")
    click.echo(f"   generation_file: {generation_path}")
    click.echo(f"generated={total}")
