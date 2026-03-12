from __future__ import annotations

from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from pse_sdk._client import HTTPClient

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]
DATETIME_COLUMNS = ["dtime", "publication_ts"]


def _validate_format(fmt: str) -> None:
    if fmt not in ("dict", "dataframe"):
        raise ValueError(f"format must be 'dict' or 'dataframe', got {fmt!r}")


def _build_date_filter(date_field: str, start: str, end: str) -> str:
    return f"{date_field} ge '{start}' and {date_field} le '{end}'"


def _to_dataframe(records: list[dict]):
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for format='dataframe'. "
            "Install it with: pip install pse-sdk[pandas]"
        ) from None
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    for col in DATETIME_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df


def _fetch_and_format(client, path, date_field, start, end, columns, fmt):
    _validate_format(fmt)
    filter_expr = _build_date_filter(date_field, start, end)
    records = client.fetch_all(path, select=columns, filter_expr=filter_expr)
    return _to_dataframe(records) if fmt == "dataframe" else records


class EndpointQuery:
    """Callable for full-endpoint queries."""

    def __init__(self, client: HTTPClient, path: str,
                 date_field: str) -> None:
        self._client = client
        self._path = path
        self._date_field = date_field

    def __call__(
        self,
        start: str,
        end: str,
        columns: list[str] | None = None,
        format: Literal["dict", "dataframe"] = "dict",
    ) -> list[dict]:
        return _fetch_and_format(
            self._client, self._path, self._date_field,
            start, end, columns, format,
        )


class EndpointSplitQuery:
    """Callable for split-endpoint queries."""

    def __init__(self, client: HTTPClient, path: str,
                 date_field: str, value_columns: list[str]) -> None:
        self._client = client
        self._path = path
        self._date_field = date_field
        self._value_columns = value_columns

    def __call__(
        self,
        start: str,
        end: str,
        format: Literal["dict", "dataframe"] = "dict",
    ) -> list[dict]:
        columns = list(COMMON_COLUMNS) + self._value_columns
        return _fetch_and_format(
            self._client, self._path, self._date_field,
            start, end, columns, format,
        )


class _BaseDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = f"_bound_{name}"

    def __get__(self, obj: object, objtype: type | None = None):
        if obj is None:
            return self
        bound = getattr(obj, self._attr, None)
        if bound is None:
            bound = self._make_query(obj)
            setattr(obj, self._attr, bound)
        return bound

    def _make_query(self, obj):
        raise NotImplementedError


class Endpoint(_BaseDescriptor):
    """Descriptor for full-endpoint methods on PSEClient."""

    def __init__(self, path: str, *, date_field: str = "business_date") -> None:
        self.path = path
        self.date_field = date_field

    def _make_query(self, obj) -> EndpointQuery:
        return EndpointQuery(obj.client, self.path, self.date_field)


class EndpointSplit(_BaseDescriptor):
    """Descriptor for split-endpoint methods on PSEClient."""

    def __init__(self, path: str, value_columns: list[str], *,
                 date_field: str = "business_date") -> None:
        self.path = path
        self.value_columns = value_columns
        self.date_field = date_field

    def _make_query(self, obj) -> EndpointSplitQuery:
        return EndpointSplitQuery(
            obj.client, self.path, self.date_field,
            self.value_columns,
        )
