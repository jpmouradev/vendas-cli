import json
from datetime import date

from vendas_cli.output import render_output
from vendas_cli.schemas import ProductTotal, ReportFilters, SalesSummary


def make_summary():
    return SalesSummary(
        valor_total=55.0,
        produto_mais_vendido="A",
        totais_por_produto=[
            ProductTotal(produto="A", quantidade_total=5, total_vendas=50.0),
            ProductTotal(produto="B", quantidade_total=1, total_vendas=5.0),
        ],
        filtros=ReportFilters(start=date(2025, 1, 1), end=date(2025, 12, 31)),
    )


def test_render_output_json():
    summary = make_summary()
    output = render_output(summary, output_format="json")

    data = json.loads(output)
    assert data["valor_total"] == 55.0
    assert data["produto_mais_vendido"] == "A"
    assert len(data["totais_por_produto"]) == 2


def test_render_output_text_format():
    summary = make_summary()
    output = render_output(summary, output_format="text")

    assert "TOTAL SALES:" in output
    assert "A" in output
    assert "FILTER APPLIED:" in output


def test_render_output_empty_list():
    summary = SalesSummary(
        valor_total=0, produto_mais_vendido="", totais_por_produto=[], filtros=None
    )

    output = render_output(summary, output_format="text")
    assert "NO ITEMS FOUND IN THIS PERIOD" in output
