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
_SUPPORTED_OPERATION_TYPES = {"generate", "optimize", "validate", "analyze"}


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
        if "$map_ref" in value and len(value) == 1:
            map_ref = value["$map_ref"]
            if not isinstance(map_ref, dict):
                raise click.UsageError("$map_ref value must be an object")
            template = map_ref.get("template")
            items_spec = map_ref.get("items")
            if not isinstance(template, str):
                raise click.UsageError("$map_ref.template must be a string")
            if items_spec is None:
                raise click.UsageError("$map_ref.items is required")

            items = _resolve_refs(items_spec, context, allow_unresolved=allow_unresolved)
            if not isinstance(items, list):
                raise click.UsageError("$map_ref.items must resolve to a list")

            mapped: list[Any] = []
            for idx, item in enumerate(items):
                local_context: dict[str, Any] = {**context, "item": item, "index": idx}
                ref_expr = _REF_PATTERN.sub(
                    lambda match: str(
                        _get_ref_value(match.group(1), local_context, allow_unresolved=allow_unresolved)
                    ),
                    template,
                )
                mapped.append(_get_ref_value(ref_expr, context, allow_unresolved=allow_unresolved))
            return mapped

        if "$ref" in value and len(value) == 1:
            ref = value["$ref"]
            if not isinstance(ref, str):
                raise click.UsageError("$ref value must be a string")
            resolved_ref = _REF_PATTERN.sub(
                lambda match: str(_get_ref_value(match.group(1), context, allow_unresolved=allow_unresolved)),
                ref,
            )
            return _get_ref_value(resolved_ref, context, allow_unresolved=allow_unresolved)
        return {k: _resolve_refs(v, context, allow_unresolved=allow_unresolved) for k, v in value.items()}

    if isinstance(value, list):
        return [_resolve_refs(v, context, allow_unresolved=allow_unresolved) for v in value]

    if isinstance(value, str):
        if value.startswith("$ref:"):
            ref_expr = value[len("$ref:") :]
            resolved_ref = _REF_PATTERN.sub(
                lambda match: str(_get_ref_value(match.group(1), context, allow_unresolved=allow_unresolved)),
                ref_expr,
            )
            return _get_ref_value(resolved_ref, context, allow_unresolved=allow_unresolved)

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


def _to_positive_int(value: Any, *, field: str) -> int:
    if not isinstance(value, int) or value <= 0:
        raise click.UsageError(f"Repeat field '{field}' must be a positive integer.")
    return value


def _build_repeat_iterations(
    repeat_spec: Any,
    context: dict[str, dict[str, Any]],
    *,
    dry_run: bool,
) -> tuple[str, list[dict[str, Any]]]:
    if isinstance(repeat_spec, int):
        count = _to_positive_int(repeat_spec, field="repeat")
        return "iter", [{"index": idx} for idx in range(count)]

    if not isinstance(repeat_spec, dict):
        raise click.UsageError("Repeat block must have integer or object field 'repeat'.")

    alias = repeat_spec.get("as", "iter")
    if not isinstance(alias, str) or not alias:
        raise click.UsageError("Repeat field 'as' must be a non-empty string.")
    if alias == "params":
        raise click.UsageError("Repeat alias 'params' is reserved.")

    count_raw = repeat_spec.get("count")
    values_raw = repeat_spec.get("values")

    if values_raw is not None and not isinstance(values_raw, dict):
        raise click.UsageError("Repeat field 'values' must be an object when provided.")
    resolved_values = _resolve_refs(values_raw or {}, context, allow_unresolved=dry_run)
    normalized_values: dict[str, list[Any]] = {}
    for key, value in resolved_values.items():
        if not isinstance(key, str) or not key:
            raise click.UsageError("Repeat 'values' keys must be non-empty strings.")
        if not isinstance(value, list):
            raise click.UsageError(f"Repeat values '{key}' must be a list.")
        normalized_values[key] = value

    inferred_count: int | None = None
    if normalized_values:
        lengths = {len(items) for items in normalized_values.values()}
        if len(lengths) != 1:
            raise click.UsageError("All repeat 'values' lists must have the same length.")
        inferred_count = lengths.pop()

    if count_raw is None:
        if inferred_count is None:
            raise click.UsageError("Repeat object must provide 'count' or non-empty 'values'.")
        count = inferred_count
    else:
        count = _to_positive_int(count_raw, field="count")
        if inferred_count is not None and inferred_count != count:
            raise click.UsageError(
                f"Repeat 'count' ({count}) does not match values length ({inferred_count})."
            )

    iterations: list[dict[str, Any]] = []
    for idx in range(count):
        payload: dict[str, Any] = {"index": idx}
        for key, items in normalized_values.items():
            payload[key] = items[idx]
        iterations.append(payload)
    return alias, iterations


def _execute_operations(
    operations: list[Any],
    *,
    context: dict[str, dict[str, Any]],
    dry_run: bool,
    step_counter: list[int],
) -> None:
    for raw_op in operations:
        if not isinstance(raw_op, dict):
            raise click.UsageError(f"Operation #{step_counter[0] + 1} must be an object.")

        if "repeat" in raw_op:
            nested_operations = raw_op.get("operations")
            if not isinstance(nested_operations, list) or not nested_operations:
                raise click.UsageError("Repeat block must contain non-empty 'operations' list.")
            repeat_label = raw_op.get("label")
            if repeat_label is not None and not isinstance(repeat_label, str):
                raise click.UsageError("Repeat block label must be a string.")
            if repeat_label == "params":
                raise click.UsageError("Operation label 'params' is reserved for top-level plan parameters.")

            alias, iterations = _build_repeat_iterations(raw_op["repeat"], context, dry_run=dry_run)
            previous_alias = context.get(alias)
            for iteration in iterations:
                context[alias] = iteration
                _execute_operations(
                    nested_operations,
                    context=context,
                    dry_run=dry_run,
                    step_counter=step_counter,
                )
            if previous_alias is None:
                context.pop(alias, None)
            else:
                context[alias] = previous_alias

            if repeat_label:
                if repeat_label in context:
                    raise click.UsageError(
                        f"Repeat block produced duplicate label '{repeat_label}'. "
                        "Use unique labels."
                    )
                values: dict[str, list[Any]] = {}
                if iterations:
                    for key in iterations[0]:
                        if key == "index":
                            continue
                        values[key] = [iteration.get(key) for iteration in iterations]
                context[repeat_label] = {
                    "type": "repeat",
                    "alias": alias,
                    "count": len(iterations),
                    "iterations": iterations,
                    "values": values,
                }
            continue

        step_counter[0] += 1
        idx = step_counter[0]
        op_type = raw_op.get("type")
        label = raw_op.get("label")
        args = raw_op.get("args", {})

        if op_type not in _SUPPORTED_OPERATION_TYPES:
            raise click.UsageError(f"Unsupported operation type '{op_type}' in #{idx}")
        if label is not None and not isinstance(label, str):
            raise click.UsageError(f"Operation #{idx} label must be a string.")
        if label == "params":
            raise click.UsageError("Operation label 'params' is reserved for top-level plan parameters.")
        if not isinstance(args, dict):
            raise click.UsageError(f"Operation #{idx} args must be an object.")

        resolved_label = _resolve_refs(label, context, allow_unresolved=dry_run) if label else None
        if resolved_label is not None and not isinstance(resolved_label, str):
            raise click.UsageError(f"Operation #{idx} resolved label must be a string.")

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
        if resolved_label:
            if resolved_label in context:
                raise click.UsageError(
                    f"Operation #{idx} produced duplicate label '{resolved_label}'. "
                    "Use unique labels, e.g. with '{{iter.index}}'."
                )
            context[resolved_label] = {
                "type": op_type,
                "args": resolved_args,
                "output": parsed,
                **parsed,
            }


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
    _execute_operations(operations, context=context, dry_run=dry_run, step_counter=[0])

    click.echo("plan_status: completed" if not dry_run else "plan_status: dry_run")
