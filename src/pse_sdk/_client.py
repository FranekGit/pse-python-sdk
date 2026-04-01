from __future__ import annotations

from pse_sdk._endpoints import make_endpoint
from pse_sdk._http import HTTPClient


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

        # price-cost
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

        # csdac-pln
        self.get_csdac = make_endpoint(
            client=self.client, path="csdac-pln", columns=["csdac_pln"]
        )

        # krb-rozl
        self.get_kb = make_endpoint(client=self.client, path="krb-rozl", columns=["kb"])
        self.get_ko = make_endpoint(client=self.client, path="krb-rozl", columns=["ko"])
        self.get_kcz = make_endpoint(
            client=self.client, path="krb-rozl", columns=["kcz"]
        )

        # kmb-kro-rozl
        self.get_kb = make_endpoint(client=self.client, path="krb-rozl", columns=["kb"])
        self.get_ko = make_endpoint(client=self.client, path="krb-rozl", columns=["ko"])
