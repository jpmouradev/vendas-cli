from __future__ import annotations

import os

os.environ.setdefault("DISABLE_PANDERA_IMPORT_WARNING", "True")

import argparse
import sys

from .core import compute_report
from .helpers import validate_csv_path, validate_filter_date
from .logger import get_logger
from .output import render_output
from .parser import load_csv
from .typing import CLIArgs

logger = get_logger()


def map_parsed_args(args: argparse.Namespace) -> CLIArgs:
    """Convert parsed CLI namespace into a typed CLIArgs mapping.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed arguments received from the CLI parser (argparse.ArgumentParser).

    Returns
    -------
    CLIArgs
        Typed dictionary containing only the validated fields required by the
        processing pipeline (csv_path, format, start, end).

    """

    return CLIArgs(
        csv_path=args.csv_path,
        format=args.format,
        start=args.start,
        end=args.end,
    )


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for the CLI.

    Returns
    -------
    argparse.ArgumentParser
        Configured parser with expected arguments.

    """

    parser = argparse.ArgumentParser(
        prog="vendas-cli",
        description=(
            "Generate advanced sales reports from a CSV file using "
            "Python standard libraries for ingestion and validated aggregation."
        ),
        epilog=(
            "Examples:\n"
            "  vendas-cli data.csv --format text\n"
            "  vendas-cli data.csv --format json\n"
            "  vendas-cli data.csv --start 2025-01-01 --end 2025-01-31\n"
            "  vendas-cli data.csv --format json --start 2025-01-01 --end 2025-01-31\n"
            "\n"
            "Exit codes:\n"
            "  0  Success\n"
            "  1  Error during validation or processing"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=(
            "vendas-cli <csv_path> --format {text,json} "
            "[--start YYYY-MM-DD --end YYYY-MM-DD]"
        ),
    )

    parser.add_argument(
        "csv_path",
        type=validate_csv_path,
        help="Path to the CSV file containing sales data.",
    )
    parser.add_argument(
        "--format",
        dest="format",
        choices=["text", "json"],
        default="text",
        help="Output format: 'text' for CLI display or 'json' for structured output.",
    )
    parser.add_argument(
        "--start",
        dest="start",
        type=validate_filter_date,
        default=None,
        help="Start date filter (YYYY-MM-DD). Must be used together with --end.",
    )
    parser.add_argument(
        "--end",
        dest="end",
        type=validate_filter_date,
        default=None,
        help="End date filter (YYYY-MM-DD). Must be used together with --start.",
    )
    return parser


def main() -> None:
    """Run the main entrypoint for vendas-cli.

    Parses arguments, triggers the processing pipeline, and prints the final
    output. Handles exceptions and ensures appropriate exit codes.
    """

    parser = _build_parser()
    args = parser.parse_args()

    if bool(args.start) ^ bool(args.end):
        parser.error(
            "Both --start and --end must be provided together "
            "(e.g., --start 2025-01-01 --end 2025-03-31)."
        )

    if args.start and args.end and args.start > args.end:
        parser.error(
            f"--start date ({args.start}) cannot be greater than --end date ({args.end}). "
            "Please provide a valid date range in YYYY-MM-DD format."
        )

    try:
        typed_args: CLIArgs = map_parsed_args(args)

        logger.info("Loading DataFrame...")
        df = load_csv(csv_path=typed_args["csv_path"])

        logger.info("Computing sales report...")
        summary = compute_report(
            df=df,
            start=typed_args["start"],
            end=typed_args["end"],
        )

        logger.info("Rendering output...")
        output = render_output(
            summary=summary,
            output_format=typed_args["format"],
        )

        print(output)
        sys.exit(0)

    except Exception as exc:
        logger.error(f"Error: {exc}")
        sys.exit(1)
