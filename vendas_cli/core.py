from __future__ import annotations

from decimal import Decimal

import pandas as pd

from .schemas import (
    ProductTotal,
    ReportFilters,
    SalesSummary,
)


def compute_totals_by_product(
    df: pd.DataFrame,
) -> list[ProductTotal]:
    """Aggregate sales by product from the provided DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing produto, quantidade, preco_unitario
        and data columns as validated by parser.py.

    Returns
    -------
    list[ProductTotal]
        Structured list of aggregated totals per product, including total
        quantity sold and total sale value.

    """

    if df.empty:
        return []

    df = df.assign(_total_value=df["quantidade"] * df["preco_unitario"])

    aggregated = (
        df.groupby("produto", as_index=False)
        .agg(
            quantidade_total=("quantidade", "sum"),
            total_vendas=("_total_value", "sum"),
        )
        .sort_values(by="produto")
    )

    return [
        ProductTotal(
            produto=row["produto"],
            quantidade_total=int(row["quantidade_total"]),
            total_vendas=round(float(row["total_vendas"]), 2),
        )
        for _, row in aggregated.iterrows()
    ]


def compute_report(
    df: pd.DataFrame,
    start: str | None = None,
    end: str | None = None,
) -> SalesSummary:
    """Compute the final sales summary report for the dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Validated sales DataFrame containing at minimum the columns
        produto, quantidade, preco_unitario.
    start : str | None, optional
        Optional start date in ISO YYYY-MM-DD format.
    end : str | None, optional
        Optional end date in ISO YYYY-MM-DD format.

    Returns
    -------
    SalesSummary
        Pydantic model containing total sales, top-selling product, per-product
        breakdown, and filter metadata if applied.

    """

    if start and end:
        start_date = pd.to_datetime(start).date()
        end_date = pd.to_datetime(end).date()
        df = df[(df["data"] >= start_date) & (df["data"] <= end_date)]

    totals = compute_totals_by_product(df=df)

    total_sales_value = float(sum(Decimal(str(item.total_vendas)) for item in totals))
    top_product = (
        max(totals, key=lambda item: item.quantidade_total).produto if totals else ""
    )
    filters = (
        ReportFilters.model_validate({"start": start, "end": end})
        if start and end
        else None
    )

    return SalesSummary(
        valor_total=total_sales_value,
        produto_mais_vendido=top_product,
        totais_por_produto=totals,
        filtros=filters,
    )
