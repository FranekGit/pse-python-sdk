from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from pse._client import PSEClient

COMMON_COLUMNS = ["dtime", "period", "business_date", "publication_ts"]
DATETIME_COLUMNS = ["dtime", "publication_ts"]


@dataclass
class SplitMethod:
    method_name: str
    value_columns: list[str]
    doc: str = ""


class BaseEndpoint:
    path: str = ""
    method_name: str = ""
    doc: str = ""
    date_field: str = "business_date"
    split_columns: list[str] = COMMON_COLUMNS
    splits: list[SplitMethod] = field(default_factory=list)

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, "splits") or not isinstance(cls.__dict__.get("splits"), list):
            cls.splits = []

    def __init__(self, client: PSEClient):
        self.client = client

    def _build_date_filter(self, start: str, end: str) -> str:
        return f"{self.date_field} ge '{start}' and {self.date_field} le '{end}'"

    def _to_dataframe(self, records: list[dict]) -> pd.DataFrame:
        if not records:
            return pd.DataFrame()
        df = pd.DataFrame(records)
        for col in DATETIME_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        return df

    def query(
        self,
        start: str,
        end: str,
        columns: list[str] | None = None,
    ) -> pd.DataFrame:
        """Query the endpoint for a date range, return a DataFrame."""
        filter_expr = self._build_date_filter(start, end)
        records = self.client.fetch_all(
            self.path,
            select=columns,
            filter_expr=filter_expr,
        )
        return self._to_dataframe(records)

    def query_split(
        self,
        value_columns: list[str],
        start: str,
        end: str,
    ) -> pd.DataFrame:
        """Query with only split_columns + value_columns selected."""
        columns = list(self.split_columns) + value_columns
        return self.query(start, end, columns=columns)
