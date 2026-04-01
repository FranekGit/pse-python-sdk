from __future__ import annotations

import logging
import time

import requests

logger = logging.getLogger(__name__)


class HTTPClient:
    """Low-level HTTP client for the PSE API with OData pagination."""

    _RETRY_STATUSES = (500, 502, 503, 504)
    _MAX_RETRIES = 3
    _BACKOFF_BASE = 1

    def __init__(
        self,
        base_url: str,
        page_size: int,
        timeout: int,
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

    def _request_with_retry(self, url: str) -> dict:
        """GET *url* with retries on transient server errors."""
        for attempt in range(self._MAX_RETRIES + 1):
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code not in self._RETRY_STATUSES or attempt == self._MAX_RETRIES:
                resp.raise_for_status()
                return resp.json()
            delay = self._BACKOFF_BASE * (2 ** attempt)
            logger.warning(
                "HTTP %s from %s, retrying in %ss (%d/%d)",
                resp.status_code, url, delay, attempt + 1, self._MAX_RETRIES,
            )
            time.sleep(delay)

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
            data = self._request_with_retry(data["nextLink"])
            records.extend(data.get("value", []))

        return records
