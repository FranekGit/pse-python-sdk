from __future__ import annotations

from pse_sdk._client import HTTPClient
from pse_sdk._converter import OutputFormat, to_dataframe, validate_format

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]


def _build_date_filter(date_field: str, start: str, end: str) -> str:
    return f"{date_field} ge '{start}' and {date_field} le '{end}'"


def _fetch_and_format(client, path, date_field, start, end, select_columns, output_format):
    validate_format(output_format)
    filter_expr = _build_date_filter(date_field, start, end)
    records = client.fetch_all(path, select=select_columns, filter_expr=filter_expr)
    if output_format == "dataframe":
        return to_dataframe(records)
    return records


class EndpointQuery:
    """Callable for full-endpoint queries."""

    def __init__(self, client: HTTPClient, path: str, date_field: str) -> None:
        self._client = client
        self._path = path
        self._date_field = date_field

    def __call__(
        self,
        start: str,
        end: str,
        columns: list[str] | None = None,
        format: OutputFormat = "dict",
    ) -> list[dict]:
        return _fetch_and_format(
            self._client,
            self._path,
            self._date_field,
            start,
            end,
            select_columns=columns,
            output_format=format,
        )


class EndpointSplitQuery:
    """Callable for split-endpoint queries."""

    def __init__(
        self, client: HTTPClient, path: str, date_field: str, value_columns: list[str]
    ) -> None:
        self._client = client
        self._path = path
        self._date_field = date_field
        self._value_columns = value_columns

    def __call__(
        self,
        start: str,
        end: str,
        format: OutputFormat = "dict",
    ) -> list[dict]:
        select_columns = list(COMMON_COLUMNS) + self._value_columns
        return _fetch_and_format(
            self._client,
            self._path,
            self._date_field,
            start,
            end,
            select_columns,
            output_format=format,
        )


class _BaseDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self._cache_attr = f"_bound_{name}"

    def __get__(self, instance: object, owner_type: type | None = None):
        if instance is None:
            return self
        cached_query = getattr(instance, self._cache_attr, None)
        if cached_query is None:
            cached_query = self._make_query(instance)
            setattr(instance, self._cache_attr, cached_query)
        return cached_query

    def _make_query(self, instance):
        raise NotImplementedError


class Endpoint(_BaseDescriptor):
    """Descriptor for full-endpoint methods on PSEClient."""

    def __init__(self, path: str, *, date_field: str = "business_date") -> None:
        self.path = path
        self.date_field = date_field

    def _make_query(self, instance) -> EndpointQuery:
        return EndpointQuery(instance.client, self.path, self.date_field)


class EndpointSplit(_BaseDescriptor):
    """Descriptor for split-endpoint methods on PSEClient."""

    def __init__(
        self, path: str, value_columns: list[str], *, date_field: str = "business_date"
    ) -> None:
        self.path = path
        self.value_columns = value_columns
        self.date_field = date_field

    def _make_query(self, instance) -> EndpointSplitQuery:
        return EndpointSplitQuery(
            instance.client,
            self.path,
            self.date_field,
            self.value_columns,
        )
