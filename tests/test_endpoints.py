from unittest.mock import MagicMock

import pandas as pd
import pytest

from pse_sdk._endpoints import COMMON_COLUMNS, make_endpoint


class TestMakeEndpoint:
    def test_returns_callable(self):
        client = MagicMock()
        result = make_endpoint(client, "price-cost")
        assert callable(result)

    def test_select_with_columns(self):
        client = MagicMock()
        client.fetch_all.return_value = []
        fn = make_endpoint(client, "price-cost", columns=["cen_cost"])
        fn("2024-01-01", "2024-01-30")
        call_kwargs = client.fetch_all.call_args
        assert call_kwargs.kwargs["select"] == COMMON_COLUMNS + ["cen_cost"]

    def test_select_none_without_columns(self):
        client = MagicMock()
        client.fetch_all.return_value = []
        fn = make_endpoint(client, "price-cost")
        fn("2024-01-01", "2024-01-30")
        call_kwargs = client.fetch_all.call_args
        assert call_kwargs.kwargs["select"] is None

    def test_common_columns_not_mutated(self):
        original = list(COMMON_COLUMNS)
        client = MagicMock()
        make_endpoint(client, "price-cost", columns=["extra"])
        assert COMMON_COLUMNS == original


class TestEndpointFetch:
    def test_filter_expr_built_correctly(self):
        client = MagicMock()
        client.fetch_all.return_value = []
        fn = make_endpoint(client, "price-cost", columns=["cen_cost"])
        fn("2024-01-01", "2024-01-30")
        filter_expr = client.fetch_all.call_args.kwargs["filter_expr"]
        assert filter_expr == "business_date ge '2024-01-01' and business_date le '2024-01-30'"

    def test_dict_format_returns_list(self):
        client = MagicMock()
        client.fetch_all.return_value = [{"a": 1}]
        fn = make_endpoint(client, "price-cost")
        result = fn("2024-01-01", "2024-01-30", format="dict")
        assert isinstance(result, list)

    def test_dataframe_format_returns_df(self):
        client = MagicMock()
        client.fetch_all.return_value = [{"a": 1}]
        fn = make_endpoint(client, "price-cost")
        result = fn("2024-01-01", "2024-01-30", format="dataframe")
        assert isinstance(result, pd.DataFrame)

    def test_invalid_dates_propagate(self):
        client = MagicMock()
        fn = make_endpoint(client, "price-cost")
        with pytest.raises(ValueError):
            fn("2024-02-01", "2024-01-01")


class TestChunkedFetch:
    def test_short_range_single_call(self):
        client = MagicMock()
        client.fetch_all.return_value = [{"a": 1}]
        fn = make_endpoint(client, "price-cost", columns=["cen_cost"])
        fn("2024-01-01", "2024-01-15")
        assert client.fetch_all.call_count == 1

    def test_long_range_multiple_calls(self):
        client = MagicMock()
        client.fetch_all.return_value = []
        fn = make_endpoint(client, "price-cost", columns=["cen_cost"])
        fn("2024-01-01", "2024-02-29")
        assert client.fetch_all.call_count == 2
        filters = [c.kwargs["filter_expr"] for c in client.fetch_all.call_args_list]
        assert filters[0] == "business_date ge '2024-01-01' and business_date le '2024-01-30'"
        assert filters[1] == "business_date ge '2024-01-31' and business_date le '2024-02-29'"

    def test_chunked_results_combined(self):
        client = MagicMock()
        client.fetch_all.side_effect = [[{"a": 1}], [{"a": 2}]]
        fn = make_endpoint(client, "price-cost")
        result = fn("2024-01-01", "2024-02-29")
        assert result == [{"a": 1}, {"a": 2}]

    def test_chunked_results_combined_dataframe(self):
        client = MagicMock()
        client.fetch_all.side_effect = [[{"a": 1}], [{"a": 2}]]
        fn = make_endpoint(client, "price-cost")
        result = fn("2024-01-01", "2024-02-29", format="dataframe")
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
