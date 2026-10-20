"""Check endpoint and column names against the registry before any request.

Typos fail fast with a suggestion instead of an HTTP 400/404 from the API.
"""

from __future__ import annotations

import difflib
from collections.abc import Iterable

from pse_sdk._registry import REGISTRY


def _build_column_index() -> dict[str, tuple[str, ...]]:
    """Map each data column to the endpoints that have it (meta columns left out)."""
    index: dict[str, list[str]] = {}
    for name, spec in REGISTRY.items():
        for column in spec.columns:
            if column not in spec.meta_columns:
                index.setdefault(column, []).append(name)
    return {column: tuple(names) for column, names in index.items()}


_COLUMN_ENDPOINTS = _build_column_index()


def suggest(name: str, choices: Iterable[str]) -> str | None:
    """Return the closest match to *name* in *choices*, or ``None``.

    *name* is lowercased first, so case is ignored (registry names are all
    lowercase).
    """
    matches = difflib.get_close_matches(name.lower(), choices, n=1)
    return matches[0] if matches else None


def validate_endpoint(endpoint: str) -> None:
    """Raise ``ValueError`` if *endpoint* is not in the registry."""
    if endpoint in REGISTRY:
        return
    match = suggest(endpoint, REGISTRY) if isinstance(endpoint, str) else None
    hint = f"Did you mean {match!r}?" if match else "See PSEClient.endpoints()."
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
    if not isinstance(columns, (list, tuple)):
        raise TypeError(
            f"columns must be a list of column names, got {type(columns).__name__}"
        )
    for column in columns:
        if not isinstance(column, str):
            raise TypeError(f"column names must be str, got {type(column).__name__}")

    known = REGISTRY[endpoint].columns
    unknown = list(dict.fromkeys(c for c in columns if c not in known))
    if unknown:
        raise ValueError(_unknown_columns_message(endpoint, unknown))


def _column_hint(endpoint: str, column: str) -> str | None:
    """Return a hint for unknown *column* of *endpoint*, or ``None``.

    Other endpoints with the exact column win over a close match in
    *endpoint*.
    """
    elsewhere = _COLUMN_ENDPOINTS.get(column)
    if elsewhere:
        return f"found in: {', '.join(elsewhere)}"
    match = suggest(column, REGISTRY[endpoint].columns)
    return f"did you mean {match!r}?" if match else None


def _sentence(hint: str) -> str:
    """Capitalize *hint* and end it with a period unless it is a question."""
    return hint[0].upper() + hint[1:] + ("" if hint.endswith("?") else ".")


def _unknown_columns_message(endpoint: str, unknown: list[str]) -> str:
    hints = [_column_hint(endpoint, column) for column in unknown]
    see = f"See PSEClient.columns({endpoint!r})."
    if len(unknown) == 1:
        tail = _sentence(hints[0]) if hints[0] else see
        return f"Unknown column {unknown[0]!r} for endpoint {endpoint!r}. {tail}"
    items = ", ".join(
        f"{column!r} ({hint})" if hint else repr(column)
        for column, hint in zip(unknown, hints)
    )
    message = f"Unknown columns for endpoint {endpoint!r}: {items}."
    return f"{message} {see}" if None in hints else message
