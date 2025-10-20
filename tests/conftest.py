from datetime import date

import pandas as pd
import pytest


@pytest.fixture
def df_sample():
    """DataFrame genérico para ser reutilizado nos testes do core."""
    return pd.DataFrame(
        {
            "produto": ["A", "A", "B"],
            "quantidade": [2, 3, 1],
            "preco_unitario": [10.0, 10.0, 5.0],
            "data": [
                date(2025, 1, 10),
                date(2025, 1, 15),
                date(2025, 1, 20),
            ],
        }
    )
