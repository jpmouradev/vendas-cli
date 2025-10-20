from __future__ import annotations

import json

from .helpers import format_currency
from .schemas import ProductTotal, ReportFilters, SalesSummary
from .typing import OutputFormat


def render_text_table(
    totals: list[ProductTotal],
    total_value: float,
    top_product: str,
    filters: ReportFilters | None,
) -> str:
    """Render the sales summary as a formatted text table.

    Parameters
    ----------
    totals : List[ProductTotal]
        List of per-product aggregated totals.
    total_value : float
        Total sales value across all products.
    top_product : str
        Product with the highest quantity sold.
    filters : ReportFilters | None
        Filter metadata if applied.

    Returns
    -------
    str
        Readable, aligned CLI output.

    """

    lines: list[str] = []

    if not totals:
        lines.append("NO ITEMS FOUND IN THIS PERIOD")
    else:
        lines.append(f"TOTAL SALES: { format_currency(total_value) }")
        lines.append(f"TOP PRODUCT: { top_product }")
        lines.append("")
        lines.append("PRODUCT                        QTY     TOTAL VALUE")
        lines.append("--------------------------------------------------")

        for entry in totals:
            lines.append(
                f"{entry.produto:<30}  {entry.quantidade_total:>4}  { format_currency(entry.total_vendas):>12}"
            )

    if filters:
        lines.append("")
        lines.append(f"FILTER APPLIED: {filters.start} : {filters.end}")

    return "\n".join(lines)


def render_output(
    summary: SalesSummary,
    output_format: OutputFormat,
) -> str:
    """Render the sales summary in the requested output format.

    Parameters
    ----------
    summary : SalesSummary
        The fully computed summary model.
    output_format : OutputFormat
        Either "text" or "json".

    Returns
    -------
    str
        JSON string or formatted table string.

    """

    if output_format == "json":
        return json.dumps(
            summary.model_dump(mode="json", exclude_none=True),
            ensure_ascii=False,
            indent=2,
        )

    return render_text_table(
        totals=summary.totais_por_produto,
        total_value=summary.valor_total,
        top_product=summary.produto_mais_vendido,
        filters=summary.filtros,
    )
