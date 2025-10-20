from __future__ import annotations

import pandera as pa
from pandera.typing import Series


class ProductsDFModel(pa.DataFrameModel):
    """Pandera validation schema for the sales CSV dataset.

    This schema ensures that the input CSV contains the required columns
    with the correct data types before being processed by the core logic
    (`core.py`) or loaded via the parsing layer (`parser.py`).

    Expected Columns
    ----------------
    produto : str
        Product name.
    quantidade : int
        Units sold per record row.
    preco_unitario : float
        Unit price of the product.
    data : datetime
        Sale date, automatically coerced to `datetime.date`.

    Notes
    -----
    The `coerce=True` option enables automatic type coercion during validation,
    ensuring that numeric and date fields are converted properly or raise
    structured errors when incompatible.

    """

    produto: Series[str]
    quantidade: Series[int] = pa.Field(
        ge=0, description="Quantity must be zero or positive."
    )
    preco_unitario: Series[float] = pa.Field(
        ge=0.0, description="Unit price must be zero or positive."
    )
    data: Series[pa.DateTime]

    class Config:
        coerce = True
