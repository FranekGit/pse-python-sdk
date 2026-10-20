"""Build OData query parts for an endpoint from the generated registry."""

from __future__ import annotations

from pse_sdk._endpoint_spec import EndpointSpec
from pse_sdk._registry import REGISTRY
from pse_sdk._validate import validate_endpoint


def get_spec(endpoint: str) -> EndpointSpec:
    """Return the registry entry for *endpoint*.

    Raises:
        ValueError: If *endpoint* is not in the registry.
    """
    validate_endpoint(endpoint)
    return REGISTRY[endpoint]


def data_columns(spec: EndpointSpec) -> list[str]:
    """Return the non-meta columns of *spec* in API order."""
    return [c for c in spec.columns if c not in spec.meta_columns]


def build_select(spec: EndpointSpec, columns: list[str] | None) -> list[str] | None:
    """Return the ``$select`` columns for *columns* of *spec*.

    ``None`` selects all columns. Otherwise the meta and key columns are
    prepended so every row stays identifiable; duplicates are dropped.
    """
    if columns is None:
        return None
    return list(dict.fromkeys([*spec.meta_columns, *spec.keys, *columns]))


def date_clauses(column: str, start: str, end: str) -> list[str]:
    """Return ``$filter`` clauses limiting *column* to ``[start, end]``."""
    return [f"{column} ge '{start}'", f"{column} le '{end}'"]
