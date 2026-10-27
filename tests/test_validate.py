import pytest

from pse_sdk._registry import REGISTRY
from pse_sdk._validate import suggest, validate_columns, validate_endpoint


def error(func, *args) -> str:
    with pytest.raises(ValueError) as exc:
        func(*args)
    return str(exc.value)


class TestSuggest:
    def test_typo(self):
        assert suggest("price-cots", REGISTRY) == "price-cost"

    def test_ignores_case(self):
        assert suggest("CEN_COST", REGISTRY["price-cost"].columns) == "cen_cost"

    def test_no_match(self):
        assert suggest("xyz", REGISTRY) is None


class TestValidateEndpoint:
    def test_known(self):
        validate_endpoint("price-cost")

    def test_typo_suggests(self):
        assert error(validate_endpoint, "price-cots") == (
            "Unknown endpoint 'price-cots'. Did you mean 'price-cost'?"
        )

    def test_no_match_points_to_endpoints(self):
        assert error(validate_endpoint, "xyz") == (
            "Unknown endpoint 'xyz'. See PSEClient.endpoints()."
        )

    @pytest.mark.parametrize(
        ("endpoint", "type_name"),
        [
            (None, "NoneType"),
            (5, "int"),
            (["price-cost"], "list"),
            ({"price-cost": 1}, "dict"),
        ],
    )
    def test_non_str(self, endpoint, type_name):
        assert error(validate_endpoint, endpoint) == (
            f"Unknown endpoint {endpoint!r}. Endpoint must be a str, got {type_name}."
        )


class TestValidateColumns:
    def test_none_passes(self):
        validate_columns("price-cost", None)

    def test_empty_passes(self):
        validate_columns("price-cost", [])

    def test_data_columns_pass(self):
        validate_columns("price-cost", ["cen_cost", "ckoeb_cost"])

    def test_meta_column_passes(self):
        validate_columns("price-cost", ["dtime_utc"])

    def test_tuple_passes(self):
        validate_columns("price-cost", ("cen_cost",))

    def test_typo_suggests(self):
        assert error(validate_columns, "price-cost", ["cen_cots"]) == (
            "Unknown column for endpoint 'price-cost': "
            "'cen_cots' (did you mean 'cen_cost'?)."
        )

    def test_typo_ignores_case(self):
        assert error(validate_columns, "price-cost", ["CEN_COST"]).endswith(
            "(did you mean 'cen_cost'?)."
        )

    def test_column_of_other_endpoints(self):
        assert error(validate_columns, "kse-load", ["cen_cost"]) == (
            "Unknown column for endpoint 'kse-load': "
            "'cen_cost' (found in: crb-rozl, energy-prices, price-cost)."
        )

    def test_no_match_points_to_columns(self):
        assert error(validate_columns, "price-cost", ["foo"]) == (
            "Unknown column for endpoint 'price-cost': 'foo'. "
            "See PSEClient.columns('price-cost')."
        )

    def test_all_unknown_named_once(self):
        assert error(
            validate_columns, "price-cost", ["cen_cots", "foo", "cen_cost", "foo"]
        ) == (
            "Unknown columns for endpoint 'price-cost': "
            "'cen_cots' (did you mean 'cen_cost'?), 'foo'. "
            "See PSEClient.columns('price-cost')."
        )

    def test_all_unknown_hinted(self):
        assert error(validate_columns, "price-cost", ["cen_cots", "ckoeb_cots"]) == (
            "Unknown columns for endpoint 'price-cost': "
            "'cen_cots' (did you mean 'cen_cost'?), "
            "'ckoeb_cots' (did you mean 'ckoeb_cost'?)."
        )

    def test_meta_column_missing_on_endpoint(self):
        message = error(validate_columns, "rcco2", ["dtime"])
        assert message.startswith("Unknown column for endpoint 'rcco2': 'dtime'")
        assert "found in" not in message

    @pytest.mark.parametrize("columns", ["cen_cost", {"cen_cost"}, iter(["cen_cost"])])
    def test_not_list_raises(self, columns):
        with pytest.raises(TypeError, match="columns must be a list of column names"):
            validate_columns("price-cost", columns)

    def test_non_str_column_raises(self):
        with pytest.raises(TypeError, match="column names must be str, got int"):
            validate_columns("price-cost", ["cen_cost", 1])


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_registry_own_columns_pass(name):
    validate_columns(name, list(REGISTRY[name].columns))
