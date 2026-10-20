from __future__ import annotations

from collections.abc import Callable

from pse_sdk._format import OutputFormat

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]


def make_endpoint(
    fetch: Callable[..., list[dict]], path: str, columns: list[str] | None = None
):
    """Create a callable that fetches *columns* of *path* via *fetch*."""
    select = list(COMMON_COLUMNS) + columns if columns else None

    def get(start: str, end: str, format: OutputFormat = "dict") -> list[dict]:
        """Query PSE data for a date range.

        Args:
            start: Begin of range (``YYYY-MM-DD``, ``YYYY/MM/DD``, or ``YYYYMMDD``).
            end: End of range (``YYYY-MM-DD``, ``YYYY/MM/DD``, or ``YYYYMMDD``).
            format: Output format — ``"dict"`` (default) or ``"dataframe"``.

        Raises:
            TypeError: If *start* or *end* is not a string.
            ValueError: If a date string cannot be parsed, or *start* is
                after *end*.
        """
        return fetch(path, start, end, select=select, format=format)

    return get
