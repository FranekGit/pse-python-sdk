from __future__ import annotations

from pse_sdk._client import HTTPClient
from pse_sdk._endpoint_factory import make_endpoint


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

        self.get_cen = make_endpoint(
            client=self.client, path="price-cost", columns=["cen_cost"]
        )
        self.get_ckoeb = make_endpoint(
            client=self.client, path="price-cost", columns=["ckoeb_cost"]
        )
        self.get_ceb_sr = make_endpoint(
            client=self.client, path="price-cost", columns=["ceb_sr_cost"]
        )
        self.get_cor_pp = make_endpoint(
            client=self.client, path="price-cost", columns=["cor_pp_cost"]
        )
        self.get_imb_energy = make_endpoint(
            client=self.client, path="price-cost", columns=["imb_energy"]
        )
        self.get_contracting = make_endpoint(
            client=self.client, path="price-cost", columns=["contracting"]
        )
