from __future__ import annotations

from pse._client import PSEClient
from pse._endpoints import Endpoint, Split


class PSE:
    """Main entry point for the PSE API.

    Usage::

        from pse import PSE
        pse = PSE()
        records = pse.get_cen("2024-01-01", "2024-01-31")
    """

    # -- price-cost (split endpoint) --
    get_price_cost = Endpoint("price-cost", doc="Price and cost data from the PSE balancing market.")
    get_cen = Split("price-cost", ["cen_cost"], doc="CEN — settlement imbalance price")
    get_ckoeb = Split("price-cost", ["ckoeb_cost"], doc="CKOeB — balancing energy cost")
    get_ceb_sr = Split("price-cost", ["ceb_sr_cost"], doc="CEB_SR — avg balancing energy price")
    get_cor_pp = Split("price-cost", ["cor_pp_cost"], doc="COR_PP — premium price correction")
    get_imb_energy = Split("price-cost", ["imb_energy"], doc="Imbalance energy volume")
    get_contracting = Split("price-cost", ["contracting"], doc="Contracting direction (long/short)")

    def __init__(
        self,
        base_url: str = "https://api.raporty.pse.pl/api",
        page_size: int = 100,
        timeout: int = 30,
    ):
        self.client = PSEClient(base_url=base_url, page_size=page_size, timeout=timeout)
