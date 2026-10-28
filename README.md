<p align="center">
  <img src="https://raw.githubusercontent.com/FranekGit/pse-python-sdk/main/assets/pse_logo.png" alt="PSE Logo">
</p>

# pse-python-sdk

[![PyPI](https://img.shields.io/pypi/v/pse-sdk)](https://pypi.org/project/pse-sdk/)

Community-maintained Python SDK for the PSE (Polskie Sieci Elektroenergetyczne) public reporting API.

> API reference: https://api.raporty.pse.pl/app/home

## Installation

```bash
pip install pse-sdk
```

## Quick Start

```python
from pse_sdk import PSEClient

client = PSEClient()

# list[dict] with all columns
rows = client.fetch("price-cost", start="2025-10-01", end="2025-10-31")

# pd.DataFrame (requires pandas) with selected columns
df = client.fetch(
    "price-cost",
    start="2025-10-01",
    end="2025-10-31",
    columns=["cen_cost", "ckoeb_cost"],
    format="dataframe",
)
```

## Documentation

- [docs/usage.md](https://github.com/FranekGit/pse-python-sdk/blob/main/docs/usage.md): finding endpoints, date ranges, columns and
  output formats
- [docs/endpoints.md](https://github.com/FranekGit/pse-python-sdk/blob/main/docs/endpoints.md): all endpoints, their columns and
  types
