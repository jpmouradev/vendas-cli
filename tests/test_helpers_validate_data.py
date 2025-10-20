import pandas as pd
import pytest

from tests.mocks.fake_pandera_model import FakePanderaModel
from vendas_cli.helpers import validate_data


def test_validate_data_raises_systemexit_and_formats_errors():
    df = pd.DataFrame(
        {
            "produto": ["", "Item", "Item"],
            "quantidade": ["1", "abc", "3"],
            "preco_unitario": ["10.0", "5.0", ""],
            "data": ["2025-01-01", "2025-01-02", ""],
        }
    )

    with pytest.raises(SystemExit) as exc:
        validate_data(df, FakePanderaModel)

    message = str(exc.value)

    assert "[ERROR] Data validation failed:" in message
    assert "Row 1: required field 'produto' is missing or empty." in message
    assert "Row 2: invalid value 'abc' in column 'quantidade'" in message
    assert "Row 3: required field 'preco_unitario' is missing or empty." in message
    assert "Row 4: required field 'data' is missing or empty." in message


def test_validate_data_raises_missing_column_error():
    df = pd.DataFrame(
        {
            "produto": ["", "Item", "Item"],
            "quantidade": ["1", "abc", "3"],
            "preco_unitario": ["10.0", "5.0", ""],
        }
    )

    with pytest.raises(SystemExit) as exc:
        validate_data(df, FakePanderaModel)

    message = str(exc.value)

    assert "[ERROR] Missing required column(s): data" in message
