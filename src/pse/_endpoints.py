from __future__ import annotations

from typing import Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from pse._client import PSEClient

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
            "Install it with: pip install pse-python-sdk[pandas]"
        ) from None
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    for col in DATETIME_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df


class BoundEndpoint:
    """Callable for full-endpoint queries."""

    def __init__(self, client: PSEClient, path: str,
                 date_field: str, doc: str) -> None:
        self._client = client
        self._path = path
        self._date_field = date_field
        self.__doc__ = doc

    def __call__(
        self,
        start: str,
        end: str,
        columns: list[str] | None = None,
        format: Literal["dict", "dataframe"] = "dict",
    ) -> list[dict]:
        _validate_format(format)
        filter_expr = _build_date_filter(self._date_field, start, end)
        records = self._client.fetch_all(
            self._path, select=columns, filter_expr=filter_expr,
        )
        if format == "dataframe":
            return _to_dataframe(records)
        return records


class BoundSplit:
    """Callable for split-endpoint queries."""

    def __init__(self, client: PSEClient, path: str,
                 date_field: str, value_columns: list[str],
                 doc: str) -> None:
        self._client = client
        self._path = path
        self._date_field = date_field
        self._value_columns = value_columns
        self.__doc__ = doc

    def __call__(
        self,
        start: str,
        end: str,
        format: Literal["dict", "dataframe"] = "dict",
    ) -> list[dict]:
        _validate_format(format)
        columns = list(COMMON_COLUMNS) + self._value_columns
        filter_expr = _build_date_filter(self._date_field, start, end)
        records = self._client.fetch_all(
            self._path, select=columns, filter_expr=filter_expr,
        )
        if format == "dataframe":
            return _to_dataframe(records)
        return records


class Endpoint:
    """Descriptor for full-endpoint methods on PSE."""

    def __init__(self, path: str, *, date_field: str = "business_date",
                 doc: str = "") -> None:
        self.path = path
        self.date_field = date_field
        self.doc = doc

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = f"_bound_{name}"

    def __get__(self, obj: object, objtype: type | None = None) -> BoundEndpoint:
        if obj is None:
            return self  # type: ignore[return-value]
        bound = getattr(obj, self._attr, None)
        if bound is None:
            bound = BoundEndpoint(obj.client, self.path, self.date_field, self.doc)
            setattr(obj, self._attr, bound)
        return bound


class Split:
    """Descriptor for split-endpoint methods on PSE."""

    def __init__(self, path: str, value_columns: list[str], *,
                 date_field: str = "business_date", doc: str = "") -> None:
        self.path = path
        self.value_columns = value_columns
        self.date_field = date_field
        self.doc = doc

    def __set_name__(self, owner: type, name: str) -> None:
        self._attr = f"_bound_{name}"

    def __get__(self, obj: object, objtype: type | None = None) -> BoundSplit:
        if obj is None:
            return self  # type: ignore[return-value]
        bound = getattr(obj, self._attr, None)
        if bound is None:
            bound = BoundSplit(
                obj.client, self.path, self.date_field,
                self.value_columns, self.doc,
            )
            setattr(obj, self._attr, bound)
        return bound
