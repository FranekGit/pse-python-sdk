# Usage

How `fetch()` picks columns and rows. Per-endpoint data, date and key columns
are listed in [endpoints.md](endpoints.md).

## Columns

- `columns=None` returns all columns.
- `columns=[...]` returns these columns plus the endpoint's meta columns
  (`dtime`, `period`, `business_date`, `publication_ts` and their `*_utc`
  variants, where present) and key columns (e.g. `resource_code` on `gen-jw`),
  so every row stays identifiable.
- `client.columns(endpoint)` lists the names accepted by `columns=`. Meta
  columns are not listed there, but are always returned.

## Date filter

`start` and `end` are inclusive. Rows are filtered on the endpoint's date
column: `business_date` for most endpoints, `period` (plan date) for
`ogr-d1-head`, `ogr-d2-head`, `ogr-d39-head`, `ogr-m-head`, `ogr-oper-head` and
`ogr-r-head`.

On `ogr-d39-head`, `ogr-m-head` and `ogr-r-head`, `period` is the plan's first
day, so a range returns plans starting in it, not plans active in it. Their
`from_period` and `to_period` columns give the plan's span.

## Requests

The range is fetched in 30-day chunks, and each chunk follows the API's pages.
Long ranges take several requests.
