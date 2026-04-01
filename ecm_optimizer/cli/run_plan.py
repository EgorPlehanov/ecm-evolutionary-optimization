from __future__ import annotations

import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any

import click

from ecm_optimizer.config import DATA_DIR, EXPERIMENTS_DIR
from ecm_optimizer.utils.io_utils import read_json

PLANS_DIR = DATA_DIR / "plans"

_REF_PATTERN = re.compile(r"\{\{\s*([a-zA-Z0-9_.-]+)\s*\}\}")


def _resolve_plan_path(plan: str) -> Path:
    candidate = Path(plan)
    if candidate.exists():
        return candidate

    plan_name = plan if plan.endswith(".json") else f"{plan}.json"
    path = PLANS_DIR / plan_name
    if path.exists():
        return path

    raise click.UsageError(
        f"Plan not found: '{plan}'. Use file path or file name inside {PLANS_DIR}."
    )


def _parse_stdout(stdout: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if "=" in stripped:
            key, value = stripped.split("=", 1)
            parsed[key.strip()] = value.strip()
        elif ":" in stripped:
            key, value = stripped.split(":", 1)
            parsed[key.strip()] = value.strip()
    return parsed


def _get_ref_value(ref: str, context: dict[str, dict[str, Any]], *, allow_unresolved: bool = False) -> Any:
    parts = ref.split(".")
    if not parts:
        raise click.UsageError(f"Empty ref expression: '{ref}'")
    label = parts[0]
    if label not in context:
        if allow_unresolved:
            return f"<unresolved:{ref}>"
        raise click.UsageError(f"Unknown ref label: '{label}'")

    value: Any = context[label]
    for part in parts[1:]:
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            if allow_unresolved:
                return f"<unresolved:{ref}>"
            raise click.UsageError(f"Cannot resolve ref '{ref}': missing field '{part}'")
    return value


def _resolve_refs(value: Any, context: dict[str, dict[str, Any]], *, allow_unresolved: bool = False) -> Any:
    if isinstance(value, dict):
        if "$ref" in value and len(value) == 1:
            ref = value["$ref"]
            if not isinstance(ref, str):
                raise click.UsageError("$ref value must be a string")
            return _get_ref_value(ref, context, allow_unresolved=allow_unresolved)
        return {k: _resolve_refs(v, context, allow_unresolved=allow_unresolved) for k, v in value.items()}

    if isinstance(value, list):
        return [_resolve_refs(v, context, allow_unresolved=allow_unresolved) for v in value]

    if isinstance(value, str):
        if value.startswith("$ref:"):
            return _get_ref_value(value[len("$ref:") :], context, allow_unresolved=allow_unresolved)

        def replacer(match: re.Match[str]) -> str:
            return str(_get_ref_value(match.group(1), context, allow_unresolved=allow_unresolved))

        return _REF_PATTERN.sub(replacer, value)

    return value


def _operation_to_args(operation_type: str, args: dict[str, Any]) -> list[str]:
    cli_args = [operation_type]
    for key, value in args.items():
        option = f"--{key}"
        if isinstance(value, bool):
            if value:
                cli_args.append(option)
            continue
        if value is None:
            continue
        if isinstance(value, list):
            for item in value:
                cli_args.extend([option, str(item)])
            continue
        cli_args.extend([option, str(value)])
    return cli_args


def _dataset_to_experiments_input(dataset_value: Any) -> str:
    if not isinstance(dataset_value, str):
        raise click.UsageError("Analyze arg 'dataset' must resolve to a string path or dataset name.")
    if dataset_value.startswith("<unresolved:"):
        return dataset_value

    dataset_path = Path(dataset_value)
    if dataset_path.suffix:
        dataset_name = dataset_path.parent.name
    else:
        dataset_name = dataset_path.name

    if not dataset_name:
        raise click.UsageError(f"Cannot resolve dataset name from analyze dataset arg: '{dataset_value}'.")

    return str(EXPERIMENTS_DIR / dataset_name)


def _apply_analyze_shortcuts(args: dict[str, Any]) -> dict[str, Any]:
    resolved = dict(args)
    if "dataset" not in resolved:
        return resolved

    dataset_entry = resolved.pop("dataset")
    dataset_inputs: list[str]
    if isinstance(dataset_entry, list):
        dataset_inputs = [_dataset_to_experiments_input(item) for item in dataset_entry]
    else:
        dataset_inputs = [_dataset_to_experiments_input(dataset_entry)]

    if "input" not in resolved:
        resolved["input"] = dataset_inputs if len(dataset_inputs) > 1 else dataset_inputs[0]
        return resolved

    existing_input = resolved["input"]
    if isinstance(existing_input, list):
        resolved["input"] = [*existing_input, *dataset_inputs]
    else:
        resolved["input"] = [existing_input, *dataset_inputs]
    return resolved


@click.command("run-plan")
@click.option(
    "--plan",
    required=True,
    type=str,
    help="Path to JSON plan file OR file name inside data/plans.",
)
@click.option("--dry-run", is_flag=True, help="Print resolved operations without executing them.")
def run_plan_command(plan: str, dry_run: bool) -> None:
    """Выполнить JSON-план автоматизированного запуска generate/optimize/validate."""
    plan_path = _resolve_plan_path(plan)
    plan_payload = read_json(plan_path)

    operations = plan_payload.get("operations")
    if not isinstance(operations, list) or not operations:
        raise click.UsageError("Plan must contain a non-empty 'operations' list.")

    params = plan_payload.get("params", {})
    if not isinstance(params, dict):
        raise click.UsageError("Plan field 'params' must be an object when provided.")

    context: dict[str, dict[str, Any]] = {"params": _resolve_refs(params, {})}

    click.echo(f"plan_file: {plan_path}")
    for idx, op in enumerate(operations, start=1):
        if not isinstance(op, dict):
            raise click.UsageError(f"Operation #{idx} must be an object.")

        op_type = op.get("type")
        label = op.get("label")
        args = op.get("args", {})

        if op_type not in {"generate", "optimize", "validate", "analyze"}:
            raise click.UsageError(f"Unsupported operation type '{op_type}' in #{idx}")
        if label is not None and not isinstance(label, str):
            raise click.UsageError(f"Operation #{idx} label must be a string.")
        if label == "params":
            raise click.UsageError("Operation label 'params' is reserved for top-level plan parameters.")
        if not isinstance(args, dict):
            raise click.UsageError(f"Operation #{idx} args must be an object.")

        resolved_args = _resolve_refs(args, context, allow_unresolved=dry_run)
        if op_type == "analyze":
            resolved_args = _apply_analyze_shortcuts(resolved_args)
        command_tail = _operation_to_args(op_type, resolved_args)
        cmd = [sys.executable, "-m", "ecm_optimizer.cli.main", *command_tail]
        click.echo(f"\nSTEP_{idx}: {' '.join(shlex.quote(token) for token in cmd)}")

        if dry_run:
            continue

        stdout_lines: list[str] = []
        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        ) as process:
            assert process.stdout is not None
            for line in process.stdout:
                stdout_lines.append(line)
                click.echo(line.rstrip())
            return_code = process.wait()

        if return_code != 0:
            raise click.ClickException(f"Operation #{idx} failed with exit code {return_code}.")

        parsed = _parse_stdout("".join(stdout_lines))
        if label:
            context[label] = {
                "type": op_type,
                "args": resolved_args,
                "output": parsed,
                **parsed,
            }

    click.echo("plan_status: completed" if not dry_run else "plan_status: dry_run")
