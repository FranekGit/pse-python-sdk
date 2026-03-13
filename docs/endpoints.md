# Endpoints

All endpoints share the same signature:

```python
(start: str, end: str, format: OutputFormat = "dict")
```

## Common Response Columns

Every endpoint returns these columns plus one endpoint-specific column:

- `dtime` — timestamp
- `period` — period identifier
- `business_date` — business date
- `publication_ts` — publication timestamp

## Available Endpoints

| Method | Column | Description |
|---|---|---|
| `get_cen()` | `cen_cost` | CEN cost |
| `get_ckoeb()` | `ckoeb_cost` | CKOeB cost |
| `get_ceb_sr()` | `ceb_sr_cost` | CEB SR cost |
| `get_cor_pp()` | `cor_pp_cost` | COR PP cost |
| `get_imb_energy()` | `imb_energy` | Imbalance energy |
| `get_contracting()` | `contracting` | Contracting |
