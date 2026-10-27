from __future__ import annotations

import difflib
from collections.abc import Iterable

from pse_sdk._registry import REGISTRY


def suggest(name: str, choices: Iterable[str]) -> str | None:
    """Return the closest match to *name* in *choices*, or ``None``.

    *name* is lowercased first, so case is ignored (registry names are all
    lowercase). A non-string *name* has no match.
    """
    if not isinstance(name, str):
        return None
    matches = difflib.get_close_matches(name.lower(), choices, n=1)
    return matches[0] if matches else None


def validate_endpoint(endpoint: str) -> None:
    """Raise ``ValueError`` if *endpoint* is not in the registry.

    A non-string *endpoint* is unknown; the message names its type.
    """
    if isinstance(endpoint, str):
        if endpoint in REGISTRY:
            return
        match = suggest(endpoint, REGISTRY)
        hint = f"Did you mean {match!r}?" if match else "See PSEClient.endpoints()."
    else:
        hint = f"Endpoint must be a str, got {type(endpoint).__name__}."
    raise ValueError(f"Unknown endpoint {endpoint!r}. {hint}")


def validate_columns(endpoint: str, columns: list[str] | None) -> None:
    """Raise if any of *columns* is not a column of *endpoint*.

    Meta columns count, so requesting them explicitly is fine. ``None``
    (all columns) always passes. *endpoint* must already be validated.

    Raises:
        TypeError: If *columns* is not a list or tuple, or holds a non-string.
        ValueError: If a column is unknown. The message names every unknown
            column with a hint.
    """
    if columns is None:
        return
    _check_types(columns)
    known = REGISTRY[endpoint].columns
    unknown = list(dict.fromkeys(c for c in columns if c not in known))
    if unknown:
        raise ValueError(_unknown_columns_message(endpoint, unknown))


def _check_types(columns: list[str]) -> None:
    """Raise ``TypeError`` unless *columns* is a list or tuple of strings."""
    if not isinstance(columns, (list, tuple)):
        raise TypeError(
            f"columns must be a list of column names, got {type(columns).__name__}"
        )
    for column in columns:
        if not isinstance(column, str):
            raise TypeError(f"column names must be str, got {type(column).__name__}")


def _unknown_columns_message(endpoint: str, unknown: list[str]) -> str:
    hints = [_column_hint(endpoint, column) for column in unknown]
    items = ", ".join(
        f"{column!r} ({hint})" if hint else repr(column)
        for column, hint in zip(unknown, hints)
    )
    noun = "column" if len(unknown) == 1 else "columns"
    message = f"Unknown {noun} for endpoint {endpoint!r}: {items}."
    if None in hints:
        message += f" See PSEClient.columns({endpoint!r})."
    return message


def _column_hint(endpoint: str, column: str) -> str | None:
    """Return a hint for unknown *column* of *endpoint*, or ``None``.

    Other endpoints with the exact column (as a data column) win over a close
    match in *endpoint*.
    """
    elsewhere = [
        name
        for name, spec in REGISTRY.items()
        if column in spec.columns and column not in spec.meta_columns
    ]
    if elsewhere:
        return f"found in: {', '.join(elsewhere)}"
    match = suggest(column, REGISTRY[endpoint].columns)
    return f"did you mean {match!r}?" if match else None
