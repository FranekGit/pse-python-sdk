from __future__ import annotations

from pse_sdk._http import HTTPClient
from pse_sdk._endpoints import _make_endpoint


class PSEClient:
    """Client for the PSE (Polskie Sieci Elektoenergetyczne) reporting API.

    Args:
        timeout: HTTP timeout in seconds.

    Usage::

        from pse_sdk import PSEClient
        pse = PSEClient()
        records = pse.get_cen("2024-01-01", "2024-01-31")
        df = pse.get_price_cost("2024-01-01", "2024-01-31", format="dataframe")
    """

    _BASE_URL = "https://api.raporty.pse.pl/api"
    _PAGE_SIZE = 100

    def __init__(self, timeout: int = 30) -> None:
        self.client: HTTPClient = HTTPClient(
            base_url=self._BASE_URL,
            page_size=self._PAGE_SIZE,
            timeout=timeout,
        )

        self.get_cen = _make_endpoint(
            client=self.client, path="price-cost", columns=["cen_cost"]
        )
        self.get_ckoeb = _make_endpoint(
            client=self.client, path="price-cost", columns=["ckoeb_cost"]
        )
        self.get_ceb_sr = _make_endpoint(
            client=self.client, path="price-cost", columns=["ceb_sr_cost"]
        )
        self.get_cor_pp = _make_endpoint(
            client=self.client, path="price-cost", columns=["cor_pp_cost"]
        )
        self.get_imb_energy = _make_endpoint(
            client=self.client, path="price-cost", columns=["imb_energy"]
        )
        self.get_contracting = _make_endpoint(
            client=self.client, path="price-cost", columns=["contracting"]
        )
