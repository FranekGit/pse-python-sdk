from __future__ import annotations

import datetime
from typing import Union

DateLike = Union[str, datetime.date, datetime.datetime]

DATE_FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]


def normalize_date(value: DateLike, param_name: str) -> str:
    """Convert *value* to a ``YYYY-MM-DD`` string.

    Accepts ``datetime.datetime``, ``datetime.date``, or a string in one of:
    ``YYYY-MM-DD``, ``YYYY/MM/DD``, ``YYYYMMDD``.

    Raises:
        TypeError: If *value* is not a supported type.
        ValueError: If a string cannot be parsed.
    """
    if isinstance(value, datetime.datetime):
        return value.date().isoformat()
    if isinstance(value, datetime.date):
        return value.isoformat()
    if not isinstance(value, str):
        raise TypeError(
            f"{param_name} must be a str, datetime.date, or datetime.datetime, "
            f"got {type(value).__name__}"
        )

    value = value.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue

    accepted = ", ".join(f"'{f}'" for f in DATE_FORMATS)
    raise ValueError(
        f"{param_name}: unable to parse date {value!r}. "
        f"Accepted formats: {accepted}"
    )


def validate_date_range(start: str, end: str) -> None:
    """Raise ``ValueError`` if *start* is after *end*."""
    if start > end:
        raise ValueError(f"start date ({start}) must not be after end date ({end})")


def normalize_date_range(start: DateLike, end: DateLike) -> tuple[str, str]:
    """Normalize *start* and *end* to ``YYYY-MM-DD`` and validate the range."""
    start_str = normalize_date(start, "start")
    end_str = normalize_date(end, "end")
    validate_date_range(start_str, end_str)
    return start_str, end_str
