from __future__ import annotations

import functools

from pse._base import BaseEndpoint
from pse._client import PSEClient
from pse.endpoints import ALL_ENDPOINTS


class PSE:
    """Main entry point for the PSE API.

    Usage::

        from pse import PSE
        pse = PSE()
        df = pse.get_cen("2024-01-01", "2024-01-31")
    """

    def __init__(
        self,
        base_url: str = "https://api.raporty.pse.pl/api",
        page_size: int = 100,
        timeout: int = 30,
    ):
        self.client = PSEClient(base_url=base_url, page_size=page_size, timeout=timeout)
        self._register_endpoints()

    def _register_endpoints(self):
        for endpoint_cls in ALL_ENDPOINTS:
            endpoint: BaseEndpoint = endpoint_cls(self.client)

            # Register main query method
            method = functools.partial(endpoint.query)
            method.__doc__ = endpoint.doc
            setattr(self, endpoint.method_name, method)

            # Register split methods
            for split in endpoint.splits:
                split_method = functools.partial(endpoint.query_split, split.value_columns)
                split_method.__doc__ = split.doc
                setattr(self, split.method_name, split_method)
