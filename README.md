<p align="center">
  <img src="assets/pse_logo.png" alt="PSE Logo">
</p>

# pse-python-sdk

![Version](https://img.shields.io/badge/version-v1.5.1-blue)

Python SDK for the PSE (Polskie Sieci Elektroenergetyczne) public reporting API.

> API reference: https://api.raporty.pse.pl/app/home


## Installation

```bash
pip install git+https://github.com/FranekGit/pse-python-sdk.git
```

## Quick Start

```python
from pse_sdk import PSEClient

client = PSEClient()

# Returns list[dict] with all columns
records = client.fetch("price-cost", start="2024-01-01", end="2024-01-31")

# Returns pd.DataFrame (requires pandas) with selected columns
df = client.fetch(
    "price-cost",
    start="2024-01-01",
    end="2024-01-31",
    columns=["cen_cost", "ckoeb_cost"],
    format="dataframe",
)
```

## Columns

- `columns=None` returns all columns.
- `columns=[...]` returns these columns plus the endpoint's meta columns
  (`dtime`, `period`, `business_date`, `publication_ts` and their `*_utc`
  variants, where present) and key columns (e.g. `resource_code` on `gen-jw`),
  so every row stays identifiable.

## Date Formats

Rows are filtered on `business_date`. `ogr-*-head` endpoints have no date
column and are not supported yet.

| Format       | Example      |
|--------------|--------------|
| `YYYY-MM-DD` | `2024-01-01` |
| `YYYY/MM/DD` | `2024/01/01` |
| `YYYYMMDD`   | `20240101`   |

## Output Formats

| Format        | Return Type    | 
|---------------|----------------|
| `"dict"`      | `list[dict]`   |
| `"dataframe"` | `pd.DataFrame` |

## Endpoints

See [docs/endpoints.md](docs/endpoints.md) for available endpoints and their columns.

