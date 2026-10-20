from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ColumnType = Literal["string", "number", "integer", "boolean"]


@dataclass(frozen=True)
class EndpointSpec:
    """Schema of one PSE API endpoint."""

    columns: dict[str, ColumnType]  # all columns in API order -> JSON type
    date_column: str | None  # column for date-range filtering, None = no filter
    meta_columns: tuple[str, ...]  # dtime/period/business_date/publication_ts (+ _utc)
    keys: tuple[str, ...]  # primary key columns
