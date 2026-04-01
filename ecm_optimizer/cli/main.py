from __future__ import annotations

import click

from ecm_optimizer.cli.analyze import analyze_command
from ecm_optimizer.cli.generate import generate_command
from ecm_optimizer.cli.optimize import optimize_command
from ecm_optimizer.cli.run_plan import run_plan_command
from ecm_optimizer.cli.validate import validate_command
from ecm_optimizer.utils.logging_utils import configure_logging


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--verbose", is_flag=True, help="Enable verbose logging.")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """CLI для генерации датасетов, оптимизации и валидации ECM-параметров."""
    ctx.ensure_object(dict)
    ctx.obj["logger"] = configure_logging(verbose=verbose)


main.add_command(generate_command)
main.add_command(optimize_command)
main.add_command(validate_command)
main.add_command(run_plan_command)
main.add_command(analyze_command)


if __name__ == "__main__":
    main()
