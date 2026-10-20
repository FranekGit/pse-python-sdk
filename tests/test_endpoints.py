from unittest.mock import MagicMock

from pse_sdk._endpoints import COMMON_COLUMNS, make_endpoint


class TestMakeEndpoint:
    def test_returns_callable(self):
        result = make_endpoint(MagicMock(), "price-cost")
        assert callable(result)

    def test_select_with_columns(self):
        fetch = MagicMock()
        fn = make_endpoint(fetch, "price-cost", columns=["cen_cost"])
        fn("2024-01-01", "2024-01-30")
        assert fetch.call_args.kwargs["select"] == COMMON_COLUMNS + ["cen_cost"]

    def test_select_none_without_columns(self):
        fetch = MagicMock()
        fn = make_endpoint(fetch, "price-cost")
        fn("2024-01-01", "2024-01-30")
        assert fetch.call_args.kwargs["select"] is None

    def test_common_columns_not_mutated(self):
        original = list(COMMON_COLUMNS)
        make_endpoint(MagicMock(), "price-cost", columns=["extra"])
        assert COMMON_COLUMNS == original


class TestEndpointCall:
    def test_forwards_arguments(self):
        fetch = MagicMock()
        fn = make_endpoint(fetch, "price-cost", columns=["cen_cost"])
        fn("2024-01-01", "2024-01-30", format="dataframe")
        fetch.assert_called_once_with(
            "price-cost",
            "2024-01-01",
            "2024-01-30",
            select=COMMON_COLUMNS + ["cen_cost"],
            format="dataframe",
        )

    def test_positional_format(self):
        fetch = MagicMock()
        fn = make_endpoint(fetch, "price-cost")
        fn("2024-01-01", "2024-01-30", "dataframe")
        assert fetch.call_args.kwargs["format"] == "dataframe"

    def test_default_format_dict(self):
        fetch = MagicMock()
        fn = make_endpoint(fetch, "price-cost")
        fn("2024-01-01", "2024-01-30")
        assert fetch.call_args.kwargs["format"] == "dict"

    def test_returns_fetch_result(self):
        fetch = MagicMock(return_value=[{"a": 1}])
        fn = make_endpoint(fetch, "price-cost")
        assert fn("2024-01-01", "2024-01-30") == [{"a": 1}]
