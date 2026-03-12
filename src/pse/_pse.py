from __future__ import annotations

from pse._client import HTTPClient
from pse._endpoints import Endpoint, Split


class PSEClient:
    """Main entry point for the PSE API.

    Usage::

        from pse import PSEClient
        pse = PSEClient()
        records = pse.get_cen("2024-01-01", "2024-01-31")
    """

    # -- price-cost (split endpoint) --
    get_price_cost = Endpoint("price-cost")
    get_cen = Split("price-cost", ["cen_cost"])
    get_ckoeb = Split("price-cost", ["ckoeb_cost"])
    get_ceb_sr = Split("price-cost", ["ceb_sr_cost"])
    get_cor_pp = Split("price-cost", ["cor_pp_cost"])
    get_imb_energy = Split("price-cost", ["imb_energy"])
    get_contracting = Split("price-cost", ["contracting"])

    def __init__(
        self,
        base_url: str = "https://api.raporty.pse.pl/api",
        page_size: int = 100,
        timeout: int = 30,
    ):
        self.client = HTTPClient(base_url=base_url, page_size=page_size, timeout=timeout)
