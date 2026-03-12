from __future__ import annotations

from pse_sdk._client import HTTPClient
from pse_sdk._converter import OutputFormat, to_dataframe, validate_format

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]


class EndpointQuery:
    """Callable that fetches and formats endpoint data."""

    def __init__(
        self,
        client: HTTPClient,
        path: str,
        date_field: str,
        value_columns: list[str] | None = None,
    ) -> None:
        self._client = client
        self._path = path
        self._date_field = date_field
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
        filter_expr = f"{self._date_field} ge '{start}' and {self._date_field} le '{end}'"
        records = self._client.fetch_all(self._path, select=columns, filter_expr=filter_expr)
        if format == "dataframe":
            return to_dataframe(records)
        return records


class Endpoint:
    """Descriptor that binds an EndpointQuery to a PSEClient instance."""

    def __init__(
        self,
        path: str,
        value_columns: list[str] | None = None,
        *,
        date_field: str = "business_date",
    ) -> None:
        self.path = path
        self.value_columns = value_columns
        self.date_field = date_field

    def __set_name__(self, owner: type, name: str) -> None:
        self._cache_attr = f"_bound_{name}"

    def __get__(self, instance: object, owner_type: type | None = None):
        if instance is None:
            return self
        cached_query = getattr(instance, self._cache_attr, None)
        if cached_query is None:
            cached_query = EndpointQuery(
                instance.client, self.path, self.date_field, self.value_columns
            )
            setattr(instance, self._cache_attr, cached_query)
        return cached_query
