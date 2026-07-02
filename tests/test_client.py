from pse_sdk._client import PSEClient

EXPECTED_ENDPOINTS = [
    ("get_cen", "price-cost", ["cen_cost"]),
    ("get_ckoeb", "price-cost", ["ckoeb_cost"]),
    ("get_ceb_sr", "price-cost", ["ceb_sr_cost"]),
    ("get_cor_pp", "price-cost", ["cor_pp_cost"]),
    ("get_imb_energy", "price-cost", ["imb_energy"]),
    ("get_contracting", "price-cost", ["contracting"]),
    ("get_csdac", "csdac-pln", ["csdac_pln"]),
    ("get_kb", "krb-rozl", ["kb"]),
    ("get_ko", "krb-rozl", ["ko"]),
    ("get_kcz", "krb-rozl", ["kcz"]),
    ("get_kmb", "kmb-kro-rozl", ["kmb"]),
    ("get_kro", "kmb-kro-rozl", ["kro"]),
    ("get_sk_d1_fcst", "sk", ["sk_d1_fcst"]),
    ("get_sk_d_fcst", "sk", ["sk_d_fcst"]),
    ("get_sk_cost", "sk", ["sk_cost"]),
    ("get_demand", "his-wlk-cal", ["demand"]),
    ("get_swm_p", "his-wlk-cal", ["swm_p"]),
    ("get_swm_np", "his-wlk-cal", ["swm_np"]),
    ("get_jg", "his-wlk-cal", ["jg"]),
    ("get_jgw1", "his-wlk-cal", ["jgw1"]),
    ("get_jgw2", "his-wlk-cal", ["jgw2"]),
    ("get_jgm1", "his-wlk-cal", ["jgm1"]),
    ("get_jgm2", "his-wlk-cal", ["jgm2"]),
    ("get_jgz1", "his-wlk-cal", ["jgz1"]),
    ("get_jgz2", "his-wlk-cal", ["jgz2"]),
    ("get_jgz3", "his-wlk-cal", ["jgz3"]),
    ("get_jga", "his-wlk-cal", ["jga"]),
    ("get_jgo", "his-wlk-cal", ["jgo"]),
    ("get_jnwrb", "his-wlk-cal", ["jnwrb"]),
    ("get_jgm", "his-wlk-cal", ["jgm"]),
    ("get_wi", "his-wlk-cal", ["wi"]),
    ("get_pv", "his-wlk-cal", ["pv"]),
]


class TestPSEClient:
    def test_default_timeout(self, mock_client):
        mock_http, mock_make = mock_client
        PSEClient()
        mock_http.assert_called_once_with(
            base_url="https://api.raporty.pse.pl/api",
            page_size=100,
            timeout=30,
        )

    def test_custom_timeout(self, mock_client):
        mock_http, mock_make = mock_client
        PSEClient(timeout=60)
        mock_http.assert_called_once_with(
            base_url="https://api.raporty.pse.pl/api",
            page_size=100,
            timeout=60,
        )

    def test_all_endpoints_created(self, mock_client):
        pse = PSEClient()
        for name, _, _ in EXPECTED_ENDPOINTS:
            assert callable(getattr(pse, name))

    def test_make_endpoint_call_count(self, mock_client):
        _, mock_make = mock_client
        PSEClient()
        assert mock_make.call_count == len(EXPECTED_ENDPOINTS)

    def test_endpoint_paths(self, mock_client):
        _, mock_make = mock_client
        PSEClient()
        paths = [call.kwargs["path"] for call in mock_make.call_args_list]
        assert paths == [path for _, path, _ in EXPECTED_ENDPOINTS]

    def test_endpoint_columns(self, mock_client):
        _, mock_make = mock_client
        PSEClient()
        columns = [call.kwargs["columns"] for call in mock_make.call_args_list]
        assert columns == [cols for _, _, cols in EXPECTED_ENDPOINTS]
