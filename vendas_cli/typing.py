from __future__ import annotations

from typing import Literal, TypedDict

OutputFormat = Literal["text", "json"]


class CLIArgs(TypedDict):
    """Typed contract representing validated CLI arguments.

    Attributes
    ----------
    csv_path : str
        Path to the CSV file, already validated for existence and extension.
    format : OutputFormat
        Output formatting style (`text` or `json`).
    start : str | None
        Start date filter in `YYYY-MM-DD` format, if provided.
    end : str | None
        End date filter in `YYYY-MM-DD` format, if provided.

    """

    csv_path: str
    format: OutputFormat
    start: str | None
    end: str | None
