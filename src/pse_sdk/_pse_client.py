from __future__ import annotations

from pse_sdk._client import HTTPClient
from pse_sdk._endpoints import Endpoint


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

    get_price_cost = Endpoint("price-cost")
    get_cen = Endpoint("price-cost", ["cen_cost"])
    get_ckoeb = Endpoint("price-cost", ["ckoeb_cost"])
    get_ceb_sr = Endpoint("price-cost", ["ceb_sr_cost"])
    get_cor_pp = Endpoint("price-cost", ["cor_pp_cost"])
    get_imb_energy = Endpoint("price-cost", ["imb_energy"])
    get_contracting = Endpoint("price-cost", ["contracting"])

    def __init__(
        self,
        base_url: str = "https://api.raporty.pse.pl/api",
        page_size: int = 100,
        timeout: int = 30,
    ):
        self.client = HTTPClient(
            base_url=base_url,
            page_size=page_size,
            timeout=timeout,
        )
