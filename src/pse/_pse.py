from __future__ import annotations

from pse._client import HTTPClient
from pse._endpoints import Endpoint, EndpointSplit


class PSEClient:
    """Client for the PSE (Polskie Sieci Elektoenergetyczne) reporting API.

    Args:
        timeout: HTTP timeout in seconds.

    Usage::

        from pse import PSEClient
        pse = PSEClient()
        records = pse.get_cen("2024-01-01", "2024-01-31")
        df = pse.get_price_cost("2024-01-01", "2024-01-31", format="dataframe")
    """

    # -- price-cost (full endpoint) --
    get_price_cost = Endpoint("price-cost")

    # -- price-cost column slices --
    get_cen = EndpointSplit("price-cost", ["cen_cost"])
    get_ckoeb = EndpointSplit("price-cost", ["ckoeb_cost"])
    get_ceb_sr = EndpointSplit("price-cost", ["ceb_sr_cost"])
    get_cor_pp = EndpointSplit("price-cost", ["cor_pp_cost"])
    get_imb_energy = EndpointSplit("price-cost", ["imb_energy"])
    get_contracting = EndpointSplit("price-cost", ["contracting"])

    _BASE_URL = "https://api.raporty.pse.pl/api"
    _PAGE_SIZE = 100

    def __init__(self, timeout: int = 30):
        self.client = HTTPClient(
            base_url=self._BASE_URL,
            page_size=self._PAGE_SIZE,
            timeout=timeout,
        )
