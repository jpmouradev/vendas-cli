import argparse
import os
from datetime import datetime

import pandas as pd
import pandera as pa

from .logger import get_logger
from .validators.validation import ProductsDFModel

logger = get_logger()


def validate_csv_path(path: str) -> str:
    """Validate that the provided path exists and points to a valid CSV file.

    Parameters
    ----------
    path : str
        File path provided via CLI.

    Returns
    -------
    str
        The same path if it is valid.

    Raises
    ------
    argparse.ArgumentTypeError
        Raised if the file does not exist or does not have a `.csv` extension.
    """

    if not path.lower().endswith(".csv"):
        raise argparse.ArgumentTypeError("File must have .csv extension")

    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File '{path}' not found")

    return path


def validate_filter_date(date_str: str) -> str:
    """Validate that the date string follows the `YYYY-MM-DD` pattern.

    Parameters
    ----------
    date_str : str
        Date string provided via CLI.

    Returns
    -------
    str
        The same date string if it is valid.

    Raises
    ------
    argparse.ArgumentTypeError
        Raised if the string is not in a valid `YYYY-MM-DD` format.
    """

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError as err:
        raise argparse.ArgumentTypeError(
            f"Invalid date '{date_str}'. Use format YYYY-MM-DD."
        ) from err


def format_currency(value: float) -> str:
    """Format a numeric value as currency with two decimal places.

    Parameters
    ----------
    value : float
        The numeric value to format.

    Returns
    -------
    str
        String formatted as a currency value, e.g., "199.90".

    """

    return f"{value:.2f}"


def validate_data(df: pd.DataFrame, model: type[ProductsDFModel]) -> pd.DataFrame:
    """Validate a DataFrame using a Pandera schema and reformat raw Pandera errors into
    clear, user-friendly CLI messages.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be validated. It is assumed that columns exist as expected
        by the Pandera schema.
    model : type[pa.DataFrameModel]
        The Pandera model class used for validation (e.g. `ProductsDFModel`).

    Returns
    -------
    pd.DataFrame
        The validated DataFrame (unchanged) if no validation errors are found.

    Raises
    ------
    SystemExit
        Exits the CLI with a friendly formatted error message summarizing validation
        issues when data does not conform to the schema. Displays up to 10 error lines,
        and appends `...` if more errors were detected.

    """

    try:
        return model.validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        expected_columns = set(model.to_schema().columns.keys())
        received_columns = set(df.columns)

        missing_columns = expected_columns - received_columns

        if missing_columns:
            missing_list = ", ".join(sorted(missing_columns))
            raise SystemExit(
                f"[ERROR] Missing required column(s): {missing_list}. "
                "Ensure the CSV headers match the expected schema."
            ) from None

        failures = err.failure_cases
        messages = []

        error_buffer = []

        for _, failure in failures.iterrows():
            idx = failure.get("index", None)
            column = failure.get("column", "?")
            failure_case = failure.get("failure_case", "<empty>")
            check = failure.get("check", "")

            if idx is None:
                continue

            row = int(idx) + 1

            if "null" in check or "nullable" in check:
                text = f"Row {row}: required field '{column}' is missing or empty."
            elif "type" in check or "coerce" in check:
                text = f"Row {row}: invalid value '{failure_case}' in column '{column}' — incorrect type."
            elif "greater_than" in check:
                text = f"Row {row}: invalid value '{failure_case}' in column '{column}' — negative."
            else:
                text = (
                    f"Row {row}: validation error in column '{column}': {failure_case}"
                )

            error_buffer.append((row, column, text))

        sorted_errors = sorted(error_buffer, key=lambda x: (x[0], x[1]))

        messages = [text for _, _, text in sorted_errors]

        if not messages:
            raise SystemExit(
                "[ERROR] Validation failed, but all errors were internal Pandera-level and ignored."
            ) from None

        formatted = "\n".join(messages[:10])
        raise SystemExit(f"[ERROR] Data validation failed:\n{formatted}\n...") from None
