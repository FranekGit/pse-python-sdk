"""Format converters for query output."""

from __future__ import annotations

from typing import Literal

from pse_sdk._formats._converter import to_dataframe, validate_format

OutputFormat = Literal["dict", "dataframe"]

__all__ = ["OutputFormat", "to_dataframe", "validate_format"]
