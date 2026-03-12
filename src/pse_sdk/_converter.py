"""Format conversion logic."""

from __future__ import annotations

from typing import Literal

OutputFormat = Literal["dict", "dataframe"]

def to_dataframe(records: list[dict]):
    """Convert records to a pandas DataFrame."""
    try:
        import pandas as pd
    except ImportError:
        raise ImportError(
            "pandas is required for format='dataframe'. "
            "Install it with: pip install pse-sdk[pandas]"
        ) from None
    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records)


def validate_format(fmt: str) -> None:
    """Raise ValueError if *fmt* is not a supported format."""
    if fmt not in ("dict", "dataframe"):
        raise ValueError(
            f"format must be 'dict' or 'dataframe', got {fmt!r}"
        )
