import argparse

import pytest

from vendas_cli.helpers import (
    format_currency,
    validate_csv_path,
    validate_filter_date,
)


def test_validate_csv_path_valid(tmp_path):
    file_path = tmp_path / "test.csv"
    file_path.write_text("dummy,data")

    result = validate_csv_path(str(file_path))

    assert result == str(file_path)


def test_validate_csv_path_invalid_extension(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("dummy,data")

    with pytest.raises(argparse.ArgumentTypeError) as exc:
        validate_csv_path(str(file_path))

    assert "File must have .csv extension" in str(exc.value)


def test_validate_csv_path_file_not_found():
    with pytest.raises(argparse.ArgumentTypeError) as exc:
        validate_csv_path("non_existing.csv")

    assert "File 'non_existing.csv' not found" in str(exc.value)


def test_validate_filter_date_valid():
    result = validate_filter_date("2025-01-15")
    assert result == "2025-01-15"


def test_validate_filter_date_invalid():
    with pytest.raises(argparse.ArgumentTypeError) as exc:
        validate_filter_date("15-01-2025")

    assert "Invalid date" in str(exc.value)


def test_format_currency():
    assert format_currency(199.9) == "199.90"
    assert format_currency(10) == "10.00"
    assert format_currency(0) == "0.00"
