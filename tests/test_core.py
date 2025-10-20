from datetime import date

from vendas_cli.core import compute_report, compute_totals_by_product


def test_compute_totals_by_product(df_sample):
    result = compute_totals_by_product(df_sample)

    assert len(result) == 2
    assert result[0].produto == "A"
    assert result[0].quantidade_total == 5
    assert result[0].total_vendas == 50.0


def test_compute_report_full_range(df_sample):
    summary = compute_report(df_sample, start="2025-01-01", end="2025-12-31")

    assert summary.valor_total == 55.0
    assert summary.produto_mais_vendido == "A"
    assert summary.filtros.start == date(2025, 1, 1)
    assert summary.filtros.end == date(2025, 12, 31)


def test_compute_report_filtered(df_sample):
    summary = compute_report(df_sample, start="2025-01-16", end="2025-12-31")

    assert summary.valor_total == 5.0
    assert summary.produto_mais_vendido == "B"
