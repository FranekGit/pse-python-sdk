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
        self.get_kmb = make_endpoint(
            client=self.client, path="kmb-kro-rozl", columns=["kmb"]
        )
        self.get_kro = make_endpoint(
            client=self.client, path="kmb-kro-rozl", columns=["kro"]
        )

        # sk
        self.get_sk_d1_fcst = make_endpoint(
            client=self.client, path="sk", columns=["sk_d1_fcst"]
        )
        self.get_sk_d_fcst = make_endpoint(
            client=self.client, path="sk", columns=["sk_d_fcst"]
        )
        self.get_sk_cost = make_endpoint(
            client=self.client, path="sk", columns=["sk_cost"]
        )

        # his-wlk-cal
        self.get_demand = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["demand"]
        )
        self.get_swm_p = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["swm_p"]
        )
        self.get_swm_np = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["swm_np"]
        )
        self.get_jg = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jg"]
        )
        self.get_jgw1 = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgw1"]
        )
        self.get_jgw2 = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgw2"]
        )
        self.get_jgm1 = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgm1"]
        )
        self.get_jgm2 = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgm2"]
        )
        self.get_jgz1 = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgz1"]
        )
        self.get_jgz2 = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgz2"]
        )
        self.get_jgz3 = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgz3"]
        )
        self.get_jga = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jga"]
        )
        self.get_jgo = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgo"]
        )
        self.get_jnwrb = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jnwrb"]
        )
        self.get_jgm = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["jgm"]
        )
        self.get_wi = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["wi"]
        )
        self.get_pv = make_endpoint(
            client=self.client, path="his-wlk-cal", columns=["pv"]
        )
