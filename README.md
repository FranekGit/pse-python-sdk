<p align="center">
  <img src="assets/pse_logo.png" alt="PSE Logo">
</p>

# pse-python-sdk

Python SDK for the PSE (Polskie Sieci Elektroenergetyczne) public reporting API.

## Release Status

Current Version: 0.1.0

## Installation

```bash
pip install git+https://github.com/FranekGit/pse-python-sdk.git
```

## Quick Start

```python
from pse_sdk import PSEClient

pse = PSEClient()

# Returns list[dict]
records = pse.get_cen(start="2024-01-01", end="2024-01-31")

# Returns pd.DataFrame (requires pandas)
df = pse.get_cen(start="2024-01-01", end="2024-01-31", format="dataframe")
```

## Date Formats

Accepted formats: `YYYY-MM-DD`, `YYYY/MM/DD`, `YYYYMMDD`.

## Output Formats

- `"dict"` (default) — returns `list[dict]`
- `"dataframe"` — returns `pd.DataFrame` (requires `pse-sdk[pandas]`)

## Documentation

See [docs/endpoints.md](docs/endpoints.md) for available endpoints.
