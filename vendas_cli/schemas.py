from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class ReportFilters(BaseModel):
    """Represents an optional date range filter applied to the dataset.

    Attributes
    ----------
    start : date
        Inclusive start date for the range.
    end : date
        Inclusive end date for the range.

    """

    start: date
    end: date


class ProductTotal(BaseModel):
    """Aggregated sales data for a single product.

    Attributes
    ----------
    produto : str
        Name of the product.
    quantidade_total : int
        Total units sold across all matching entries.
    total_vendas : float
        Monetary total of (quantity * unit_price) for this product.

    """

    produto: str
    quantidade_total: int
    total_vendas: float


class SalesSummary(BaseModel):
    """Final structured sales summary, ready for output rendering.

    Attributes
    ----------
    valor_total : float
        Total value of all sales.
    produto_mais_vendido : str
        Product with the highest total quantity sold.
    totais_por_produto : list[ProductTotal]
        Per-product breakdown including quantity and sales totals.
    filtros : ReportFilters | None
        Filter metadata if a date range was applied, otherwise `None`.

    """

    valor_total: float
    produto_mais_vendido: str
    totais_por_produto: list[ProductTotal]
    filtros: ReportFilters | None = None
