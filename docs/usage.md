# Usage

How to find an endpoint, fetch a date range, pick columns and choose an
output format. All endpoints and their columns are listed in
[endpoints.md](endpoints.md).

## Find an endpoint

```python
from pse_sdk import PSEClient

client = PSEClient()

client.endpoints()            # ["afrr-status", "cmbp-tp", ...]
client.columns("price-cost")  # ["cen_cost", "ckoeb_cost", ...]
```

## Fetch a date range

```python
rows = client.fetch("price-cost", "2025-10-01", "2025-10-31")
```

`start` and `end` are inclusive and accept these formats:

| Format       | Example      |
|--------------|--------------|
| `YYYY-MM-DD` | `2025-10-01` |
| `YYYY/MM/DD` | `2025/10/01` |
| `YYYYMMDD`   | `20251001`   |

## Pick columns

`columns=None` (the default) returns all columns. Pass a list to get only
some of them:

```python
rows = client.fetch("price-cost", "2025-10-01", "2025-10-01", columns=["cen_cost"])
rows[0]
```

```python
{
    "dtime": "2025-10-01 00:15:00",
    "period": "00:00 - 00:15",
    "cen_cost": 449.02,
    "dtime_utc": "2025-09-30 22:15:00",
    "period_utc": "22:00 - 22:15",
    "business_date": "2025-10-01",
    "publication_ts": "2026-06-16 12:11:18.607",
    "publication_ts_utc": "2026-06-16 10:11:18.607",
}
```

## Choose an output format

| `format`            | Returns        |
|---------------------|----------------|
| `"dict"` (default)  | `list[dict]`   |
| `"dataframe"`       | `pd.DataFrame` |

`"dataframe"` requires pandas