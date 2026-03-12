from __future__ import annotations

from pse_sdk._client import HTTPClient
from pse_sdk._converter import OutputFormat, convert

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]


class Endpoint:
    """Callable that fetches and formats endpoint data."""

    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    def __call__(
        self,
        path: str,
        start: str,
        end: str,
        columns: list[str] | None = None,
        format: OutputFormat = "dict",
    ) -> list[dict]:
        select = list(COMMON_COLUMNS) + columns if columns else None
        filter_expr = f"business_date ge '{start}' and business_date le '{end}'"

        records = self._client.fetch_all(
            path, select=select, filter_expr=filter_expr
        )

        return convert(records, format)

    def query(self, path: str, columns: list[str] | None = None):
        """Create a PSE query method for *path*, optionally selecting *columns*."""
        endpoint = self

        def method(start: str, end: str, format: OutputFormat = "dict"):
            """Query PSE data for a date range.

            Args:
                start: Start date (inclusive), e.g. ``"2024-01-01"``.
                end: End date (inclusive), e.g. ``"2024-01-31"``.
                format: ``"dict"`` for list of dicts, ``"dataframe"`` for pandas DataFrame.
            """
            return endpoint(path, start, end, columns=columns, format=format)

        return method
