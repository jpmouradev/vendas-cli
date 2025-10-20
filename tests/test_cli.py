import sys

import pytest

from vendas_cli.cli import main


def test_cli_invalid_date_range(monkeypatch, capsys, tmp_path):
    csv_path = tmp_path / "fake.csv"
    csv_path.write_text("produto,quantidade,preco_unitario,data\nA,1,10,2025-01-10")

    monkeypatch.setattr(
        sys,
        "argv",
        ["vendas-cli", str(csv_path), "--start", "2025-12-31", "--end", "2025-01-01"],
    )

    with pytest.raises(SystemExit) as exc:
        main()

    captured = capsys.readouterr()

    assert exc.value.code == 2
    assert "cannot be greater" in captured.err or "cannot be greater" in captured.out


def test_cli_missing_args(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["vendas-cli"])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code != 0


def test_cli_success(monkeypatch, capsys, tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("produto,quantidade,preco_unitario,data\nA,2,10,2025-01-10")

    monkeypatch.setattr(sys, "argv", ["vendas-cli", str(csv_path), "--format", "text"])

    with pytest.raises(SystemExit) as exc:
        main()

    output = capsys.readouterr().out
    assert "TOTAL SALES:" in output
    assert "A" in output
    assert exc.value.code == 0
