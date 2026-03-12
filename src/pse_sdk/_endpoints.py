from __future__ import annotations

from pse_sdk._client import HTTPClient
from pse_sdk._converter import OutputFormat, to_dataframe, validate_format

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]


class Endpoint:
    """Callable that fetches and formats endpoint data."""

    def __init__(
        self,
        client: HTTPClient,
        path: str,
        value_columns: list[str] | None = None,
    ) -> None:
        self._client = client
        self._path = path
        self._value_columns = value_columns

    def __call__(
        self,
        start: str,
        end: str,
        columns: list[str] | None = None,
        format: OutputFormat = "dict",
    ) -> list[dict]:
        validate_format(format)
        if self._value_columns:
            columns = list(COMMON_COLUMNS) + self._value_columns
        filter_expr = f"business_date ge '{start}' and business_date le '{end}'"
        records = self._client.fetch_all(self._path, select=columns, filter_expr=filter_expr)
        if format == "dataframe":
            return to_dataframe(records)
        return records
