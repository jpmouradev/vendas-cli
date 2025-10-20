from vendas_cli.parser import load_csv


def test_load_csv_utf8(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "produto,quantidade,preco_unitario,data\nA,2,10,2025-01-10", encoding="utf-8"
    )

    df = load_csv(str(csv_path), encoding="utf-8")
    assert not df.empty
    assert list(df.columns) == ["produto", "quantidade", "preco_unitario", "data"]


def test_load_csv_fallback_latin(tmp_path, caplog):
    csv_path = tmp_path / "data_latin.csv"
    csv_path.write_bytes(
        "produto,quantidade,preco_unitario,data\nÁ,1,10,2025-01-10".encode("latin1")
    )

    with caplog.at_level("WARNING"):
        try:
            _ = load_csv(str(csv_path), encoding="utf-8")
        except UnicodeDecodeError:
            pass

    assert any("falling back to latin1" in message for message in caplog.messages)
