from __future__ import annotations

from pse_sdk._client import HTTPClient
from pse_sdk._converter import OutputFormat, convert

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]


def make_endpoint(client: HTTPClient, path: str, columns: list[str] | None = None):
    """Create a callable that fetches and formats endpoint data."""
    select = list(COMMON_COLUMNS) + columns if columns else None

    def fetch(start: str, end: str, format: OutputFormat = "dict") -> list[dict]:
        """Query PSE data for a date range.

        Args:
            start: Start date (inclusive), e.g. ``"2024-01-01"``.
            end: End date (inclusive), e.g. ``"2024-01-31"``.
            format: ``"dict"`` for list of dicts, ``"dataframe"`` for pandas DataFrame.
        """
        filter_expr = f"business_date ge '{start}' and business_date le '{end}'"
        records = client.fetch_all(path, select=select, filter_expr=filter_expr)
        return convert(records, format)

    return fetch
