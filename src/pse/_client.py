from __future__ import annotations

import requests


class PSEClient:
    """Low-level HTTP client for the PSE API with OData pagination."""

    def __init__(
        self,
        base_url: str = "https://api.raporty.pse.pl/api",
        page_size: int = 100,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.page_size = page_size
        self.timeout = timeout
        self.session = requests.Session()

    def fetch(
        self,
        path: str,
        *,
        select: list[str] | None = None,
        filter_expr: str | None = None,
        order_by: str | None = None,
        first: int | None = None,
        after: str | None = None,
    ) -> dict:
        """Fetch a single page from the API."""
        url = f"{self.base_url}/{path}"
        params: dict[str, str] = {}
        if select:
            params["$select"] = ",".join(select)
        if filter_expr:
            params["$filter"] = filter_expr
        if order_by:
            params["$orderby"] = order_by
        if first is not None:
            params["$first"] = str(first)
        if after:
            params["$after"] = after

        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def fetch_all(
        self,
        path: str,
        *,
        select: list[str] | None = None,
        filter_expr: str | None = None,
        order_by: str | None = None,
    ) -> list[dict]:
        """Fetch all pages, auto-paginating via nextLink."""
        data = self.fetch(
            path,
            select=select,
            filter_expr=filter_expr,
            order_by=order_by,
            first=self.page_size,
        )
        records: list[dict] = data.get("value", [])

        while "nextLink" in data:
            resp = self.session.get(data["nextLink"], timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            records.extend(data.get("value", []))

        return records
