import pandas as pd
import pytest

from pse_sdk._client import PSEClient
from pse_sdk._registry import REGISTRY


class TestPSEClient:
    def test_default_timeout(self, mock_http):
        PSEClient()
        mock_http.assert_called_once_with(
            base_url="https://api.raporty.pse.pl/api",
            page_size=100,
            timeout=30,
        )

    def test_custom_timeout(self, mock_http):
        PSEClient(timeout=60)
        mock_http.assert_called_once_with(
            base_url="https://api.raporty.pse.pl/api",
            page_size=100,
            timeout=60,
        )


@pytest.fixture()
def pse(mock_http):
    client = PSEClient()
    client.client.fetch_all.return_value = []
    return client


class TestFetch:
    def test_select_meta_keys_and_columns(self, pse):
        pse.fetch("price-cost", "2024-01-01", "2024-01-15", columns=["cen_cost", "ckoeb_cost"])
        assert pse.client.fetch_all.call_count == 1
        assert pse.client.fetch_all.call_args.args == ("price-cost",)
        assert pse.client.fetch_all.call_args.kwargs["select"] == [
            *REGISTRY["price-cost"].meta_columns,
            "cen_cost",
            "ckoeb_cost",
        ]

    def test_select_includes_keys(self, pse):
        pse.fetch("gen-jw", "2024-01-01", "2024-01-15", columns=[])
        select = pse.client.fetch_all.call_args.kwargs["select"]
        assert {"resource_code", "operating_mode"} <= set(select)

    def test_columns_none_selects_all(self, pse):
        pse.fetch("price-cost", "2024-01-01", "2024-01-15")
        assert pse.client.fetch_all.call_args.kwargs["select"] is None

    def test_filter_on_date_column(self, pse):
        pse.fetch("price-cost", "2024-01-01", "2024-01-30")
        filter_expr = pse.client.fetch_all.call_args.kwargs["filter_expr"]
        assert filter_expr == "business_date ge '2024-01-01' and business_date le '2024-01-30'"

    def test_long_range_chunked(self, pse):
        pse.fetch("price-cost", "2024-01-01", "2024-02-29")
        filters = [c.kwargs["filter_expr"] for c in pse.client.fetch_all.call_args_list]
        assert filters == [
            "business_date ge '2024-01-01' and business_date le '2024-01-30'",
            "business_date ge '2024-01-31' and business_date le '2024-02-29'",
        ]

    def test_chunked_results_combined(self, pse):
        pse.client.fetch_all.side_effect = [[{"a": 1}], [{"a": 2}]]
        result = pse.fetch("price-cost", "2024-01-01", "2024-02-29")
        assert result == [{"a": 1}, {"a": 2}]

    def test_dataframe_format(self, pse):
        pse.client.fetch_all.side_effect = [[{"a": 1}], [{"a": 2}]]
        result = pse.fetch("price-cost", "2024-01-01", "2024-02-29", format="dataframe")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2

    def test_invalid_format_raises_before_request(self, pse):
        with pytest.raises(ValueError, match="format must be"):
            pse.fetch("price-cost", "2024-01-01", "2024-01-30", format="df")
        pse.client.fetch_all.assert_not_called()

    def test_no_date_column_raises_before_request(self, pse):
        with pytest.raises(ValueError, match="'ogr-d1-head' has no date column"):
            pse.fetch("ogr-d1-head", "2024-01-01", "2024-01-30")
        pse.client.fetch_all.assert_not_called()

    def test_unknown_endpoint_raises_before_request(self, pse):
        with pytest.raises(ValueError, match="Unknown endpoint 'nope'"):
            pse.fetch("nope", "2024-01-01", "2024-01-30")
        pse.client.fetch_all.assert_not_called()

    def test_invalid_date_range_raises_before_request(self, pse):
        with pytest.raises(ValueError, match="must not be after"):
            pse.fetch("price-cost", "2024-02-01", "2024-01-01")
        pse.client.fetch_all.assert_not_called()
