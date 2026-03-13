<p align="center">
  <img src="assets/pse_logo.png" alt="PSE Logo">
</p>

# pse-python-sdk

Python SDK for the PSE (Polskie Sieci Elektroenergetyczne) public reporting API.

> API page: https://api.raporty.pse.pl/app/home

## Release Status

Current Version: 0.1.0

## Installation

```bash
pip install git+https://github.com/FranekGit/pse-python-sdk.git
```

## Quick Start

```python
from pse_sdk import PSEClient

client = PSEClient()

# Returns list[dict]
records = client.get_cen(start="2024-01-01", end="2024-01-31")

# Returns pd.DataFrame (requires pandas)
df = client.get_cen(start="2024-01-01", end="2024-01-31", format="dataframe")
```

## Date Formats

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

See [docs/endpoints.md](docs/endpoints.md) for available endpoints.

