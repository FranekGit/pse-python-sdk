from unittest.mock import MagicMock, patch

from pse_sdk._client import PSEClient


class TestPSEClient:
    @patch("pse_sdk._client.make_endpoint", return_value=MagicMock())
    @patch("pse_sdk._client.HTTPClient")
    def test_default_timeout(self, mock_http, mock_make):
        PSEClient()
        mock_http.assert_called_once_with(
            base_url="https://api.raporty.pse.pl/api",
            page_size=100,
            timeout=30,
        )

    @patch("pse_sdk._client.make_endpoint", return_value=MagicMock())
    @patch("pse_sdk._client.HTTPClient")
    def test_custom_timeout(self, mock_http, mock_make):
        PSEClient(timeout=60)
        mock_http.assert_called_once_with(
            base_url="https://api.raporty.pse.pl/api",
            page_size=100,
            timeout=60,
        )

    @patch("pse_sdk._client.make_endpoint", return_value=MagicMock())
    @patch("pse_sdk._client.HTTPClient")
    def test_all_endpoints_created(self, mock_http, mock_make):
        pse = PSEClient()
        for attr in ("get_cen", "get_ckoeb", "get_ceb_sr", "get_cor_pp", "get_imb_energy", "get_contracting"):
            assert callable(getattr(pse, attr))

    @patch("pse_sdk._client.make_endpoint", return_value=MagicMock())
    @patch("pse_sdk._client.HTTPClient")
    def test_make_endpoint_called_six_times(self, mock_http, mock_make):
        PSEClient()
        assert mock_make.call_count == 6

    @patch("pse_sdk._client.make_endpoint", return_value=MagicMock())
    @patch("pse_sdk._client.HTTPClient")
    def test_endpoint_paths_all_price_cost(self, mock_http, mock_make):
        PSEClient()
        for call in mock_make.call_args_list:
            assert call.kwargs["path"] == "price-cost"

    @patch("pse_sdk._client.make_endpoint", return_value=MagicMock())
    @patch("pse_sdk._client.HTTPClient")
    def test_endpoint_columns(self, mock_http, mock_make):
        PSEClient()
        columns = [call.kwargs["columns"] for call in mock_make.call_args_list]
        assert columns == [
            ["cen_cost"],
            ["ckoeb_cost"],
            ["ceb_sr_cost"],
            ["cor_pp_cost"],
            ["imb_energy"],
            ["contracting"],
        ]
