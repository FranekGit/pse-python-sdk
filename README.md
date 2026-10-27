<p align="center">
  <img src="https://raw.githubusercontent.com/FranekGit/pse-python-sdk/main/assets/pse_logo.png" alt="PSE Logo">
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
