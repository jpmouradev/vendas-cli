# vendas-cli — Advanced Sales Report Generator

A Python CLI tool for processing sales CSV files with robust data validation, date filtering, text or JSON output, clear logging, and unit tests with coverage above 80%.

---

## Installation

Clone the project and install locally on Linux:

```bash
python -m venv .venv
source .venv/bin/activate   
pip install .
```

This will automatically register the global command `vendas-cli` (via the entrypoint in `pyproject.toml`).

For development mode:

```bash
pip install --editable .
```

---

## Usage

### Help Command

```bash
vendas-cli --help
```

### Basic Command

```bash
vendas-cli data_test/vendas.csv --format text
```

### JSON Output with Date Filter

```bash
vendas-cli data_test/vendas.csv --format json --start 2025-01-01 --end 2025-03-31
```

---

## CLI Parameters

| Parameter              | Description |
|----------------------|-----------|
| `csv_path`           | Path to the `.csv` file |
| `--format`           | Defines the output format (`text` or `json`) |
| `--start YYYY-MM-DD` | Start date for filtering (must be used together with `--end`) |
| `--end YYYY-MM-DD`   | End date for filtering (must be used together with `--start`) |

> The flags `--start` and `--end` must be used together. If only one is provided, the CLI will exit with a friendly error message.

---

## Project Structure

```
vendas_cli/
 ├── cli.py                  → Main CLI entrypoint
 ├── parser.py               → CSV loading and initial validation
 ├── core.py                 → Report computation logic
 ├── output.py               → Rendering output in text or JSON
 ├── helpers.py              → Utility functions
 ├── validators/validation.py → Pandera schema for data validation
 ├── schemas.py              → Pydantic models for structured output
 ├── logger.py               → Logging configuration
 ├── typing.py               → Custom CLIArgs and OutputFormat types
```

---

## Features

- CSV reading with automatic encoding fallback (`utf-8` → `latin1`)
- Strong data validation using Pandera + Pydantic
- Date range filtering with integrity checks (`--start <= --end`)
- Per-product aggregation and total sales calculation
- Identification of the top-selling product
- CLI-friendly formatted table output or JSON mode
- Clear error handling with human-friendly messaging and logs
- Modular architecture with strong typing
- Installable via `pip install .`
- Automated tests with `pytest`
- **Pre-commit hooks for formatting, linting, and type checking**

---

## Development & Code Quality

### Install development dependencies:

```bash
pip install '.[dev]'
```

### Use pre-commit

Run on all files manually:

```bash
pre-commit run --all-files
```

> This ensures `ruff`, `mypy` and basic validations run before each commit, enforcing consistent code quality.

---

## Testing & Coverage

Run tests:

```bash
pytest
```

`pytest.ini` is already configured with:

```
--cov=vendas_cli --cov-report=term-missing --cov-fail-under=80
```

---

## Output Examples

### Text Mode


```
TOTAL SALES: 1599.90
TOP PRODUCT: Notebook Gamer

PRODUCT                       QTY       TOTAL VALUE
---------------------------------------------------
Mouse Bluetooth               10        499.90
Notebook Gamer                3         1100.00

FILTER APPLIED: 2025-01-01 : 2025-03-31
```

---

### JSON Mode

```json
{
  "valor_total": 1599.9,
  "produto_mais_vendido": "Notebook Gamer",
  "totais_por_produto": [
    { "produto": "Mouse Bluetooth", "quantidade_total": 10, "total_vendas": 499.9 },
    { "produto": "Notebook Gamer", "quantidade_total": 3, "total_vendas": 1100.0 }
  ],
  "filtros": { "start": "2025-01-01", "end": "2025-03-31" }
}
```

---
