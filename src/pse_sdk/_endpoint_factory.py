from __future__ import annotations

from pse_sdk._client import HTTPClient
from pse_sdk._converter import OutputFormat, convert
from pse_sdk._date import DateLike, normalize_date, validate_date_range

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]


def make_endpoint(client: HTTPClient, path: str, columns: list[str] | None = None):
    """Create a callable that fetches and formats endpoint data."""
    select = list(COMMON_COLUMNS) + columns if columns else None

    def fetch(start: DateLike, end: DateLike, format: OutputFormat = "dict") -> list[dict]:
        """Query PSE data for a date range.

        Args:
            start: Start date (inclusive). Accepts ``str``, ``datetime.date``,
                or ``datetime.datetime``. Strings may use ``YYYY-MM-DD``,
                ``YYYY/MM/DD``, or ``YYYYMMDD`` format.
            end: End date (inclusive). Same types as *start*.
            format: ``"dict"`` for list of dicts, ``"dataframe"`` for pandas DataFrame.
        """
        start_str = normalize_date(start, "start")
        end_str = normalize_date(end, "end")
        validate_date_range(start_str, end_str)
        filter_expr = f"business_date ge '{start_str}' and business_date le '{end_str}'"
        records = client.fetch_all(path, select=select, filter_expr=filter_expr)
        return convert(records, format)

    return fetch
