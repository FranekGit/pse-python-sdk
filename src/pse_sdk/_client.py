from __future__ import annotations

from pse_sdk._dates import normalize_date_range, split_date_range
from pse_sdk._format import OutputFormat, convert, validate_format
from pse_sdk._http import HTTPClient
from pse_sdk._query import build_select, data_columns, date_clauses, get_spec
from pse_sdk._registry import REGISTRY, Endpoint


class PSEClient:
    """Client for the PSE (Polskie Sieci Elektroenergetyczne) reporting API.

    Args:
        timeout: HTTP timeout in seconds.

    Usage::

        from pse_sdk import PSEClient
        pse = PSEClient()
        pse.endpoints()  # ["afrr-status", "cmbp-tp", ...]
        pse.columns("price-cost")  # ["cen_cost", "ckoeb_cost", ...]
        records = pse.fetch("price-cost", "2024-01-01", "2024-01-31")
        df = pse.fetch(
            "price-cost",
            "2024-01-01",
            "2024-01-31",
            columns=["cen_cost", "ckoeb_cost"],
            format="dataframe",
        )
    """

    _BASE_URL = "https://api.raporty.pse.pl/api"
    _PAGE_SIZE = 100

    def __init__(self, timeout: int = 30) -> None:
        self.client: HTTPClient = HTTPClient(
            base_url=self._BASE_URL,
            page_size=self._PAGE_SIZE,
            timeout=timeout,
        )

    @staticmethod
    def endpoints() -> list[Endpoint]:
        """Return the names of all endpoints, sorted alphabetically."""
        return list(REGISTRY)

    @staticmethod
    def columns(endpoint: Endpoint) -> list[str]:
        """Return the data columns of *endpoint* in API order.

        These are the names accepted by ``fetch(columns=...)``. Meta columns
        (``dtime``, ``period``, ``business_date``, ``publication_ts`` and their
        ``*_utc`` variants) are left out; ``fetch()`` always returns them.

        Raises:
            ValueError: If *endpoint* is unknown.
        """
        return data_columns(get_spec(endpoint))

    def fetch(
        self,
        endpoint: Endpoint,
        start: str,
        end: str,
        *,
        columns: list[str] | None = None,
        format: OutputFormat = "dict",
    ):
        """Query *endpoint* for a date range.

        The range is fetched in 30-day chunks.

        Args:
            endpoint: Endpoint name, e.g. ``"price-cost"``.
            start: Begin of range (``YYYY-MM-DD``, ``YYYY/MM/DD``, or ``YYYYMMDD``).
            end: End of range (``YYYY-MM-DD``, ``YYYY/MM/DD``, or ``YYYYMMDD``).
            columns: Data columns to return. The endpoint's meta and key
                columns are always included. ``None`` (default) returns all
                columns.
            format: Output format — ``"dict"`` (default) or ``"dataframe"``.

        Raises:
            TypeError: If *start* or *end* is not a string.
            ValueError: If *endpoint* is unknown or has no date column,
                *format* is not supported, a date string cannot be parsed,
                or *start* is after *end*.
        """
        spec = get_spec(endpoint)
        validate_format(format)
        if spec.date_column is None:
            raise ValueError(
                f"Endpoint {endpoint!r} has no date column and is not supported yet"
            )
        start_str, end_str = normalize_date_range(start, end)
        select = build_select(spec, columns)

        records: list[dict] = []
        for chunk_start, chunk_end in split_date_range(start_str, end_str):
            filter_expr = " and ".join(
                date_clauses(spec.date_column, chunk_start, chunk_end)
            )
            records.extend(
                self.client.fetch_all(endpoint, select=select, filter_expr=filter_expr)
            )

        return convert(records, format)
