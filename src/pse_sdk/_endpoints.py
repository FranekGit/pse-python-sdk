from __future__ import annotations

from pse_sdk._http import HTTPClient
from pse_sdk._format import OutputFormat, convert
from pse_sdk._dates import DateLike, normalize_date_range

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]


def _make_endpoint(client: HTTPClient, path: str, columns: list[str] | None = None):
    """Create a callable that fetches and formats endpoint data."""
    select = list(COMMON_COLUMNS) + columns if columns else None

    def fetch(
        start: DateLike, end: DateLike, format: OutputFormat = "dict"
    ) -> list[dict]:
        """Query PSE data for a date range.

        Args:
            start: Begin of range (``str``, ``date``, or ``datetime``).
            end: End of range (``str``, ``date``, or ``datetime``).
            format: Output format — ``"dict"`` (default) or ``"dataframe"``.

        Raises:
            TypeError: If *start* or *end* is not a supported type.
            ValueError: If a date string cannot be parsed, or *start* is
                after *end*.
        """
        start_str, end_str = normalize_date_range(start, end)
        filter_expr = f"business_date ge '{start_str}' and business_date le '{end_str}'"

        records = client.fetch_all(path, select=select, filter_expr=filter_expr)

        return convert(records, format)

    return fetch
