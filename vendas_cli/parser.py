from __future__ import annotations

import csv

import pandas as pd

from .helpers import validate_data
from .logger import get_logger
from .validators.validation import ProductsDFModel

logger = get_logger()


def load_csv(
    csv_path: str,
    encoding: str = "utf-8",
) -> pd.DataFrame:
    """Load and validate a CSV file into a pandas DataFrame.

    Parameters
    ----------
    csv_path : str
        Path to the CSV file.
    encoding : str, optional
        Encoding used to read the CSV. Defaults to 'utf-8', with fallback to 'latin1'.

    Returns
    -------
    pd.DataFrame
        Fully validated DataFrame, optionally filtered by date range.

    Raises
    ------
    ValueError
        If file decoding fails, numeric parsing fails, or schema validation fails.

    """

    logger.info(f"Reading CSV from path: {csv_path}")

    rows = None

    try:
        with open(csv_path, encoding=encoding, newline="") as file:
            reader = csv.DictReader(file, delimiter=",")
            rows = list(reader)
    except UnicodeDecodeError:
        logger.warning("UTF-8 decoding failed; falling back to latin1.")
        with open(csv_path, encoding="latin1", newline="") as file:
            reader = csv.DictReader(file, delimiter=",")
            rows = list(reader)

    logger.info(
        f"CSV successfully read using Python's 'csv' module. Total rows: {len(rows)}"
    )

    df = pd.DataFrame(rows)

    df.columns = [c.strip().lower() for c in df.columns]

    df = validate_data(df, ProductsDFModel)

    logger.info("Casting numeric fields with strict validation")

    try:
        df["quantidade"] = pd.to_numeric(
            df["quantidade"], errors="raise", downcast="integer"
        )
        df["preco_unitario"] = pd.to_numeric(df["preco_unitario"], errors="raise")
        df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date
    except Exception as exc:
        raise ValueError(f"Failed to parse fields: {exc}") from exc

    logger.info(
        f"CSV validated. Discarded {df.attrs.get('invalid_products', {}).get('total_invalid', 0)} invalid rows."
    )

    return df
