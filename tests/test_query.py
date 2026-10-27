import pytest

from pse_sdk._endpoint_spec import EndpointSpec
from pse_sdk._query import build_select, data_columns, date_clauses, get_spec
from pse_sdk._registry import REGISTRY

SPEC = EndpointSpec(
    columns={
        "node": "string",
        "value": "number",
        "other": "number",
        "dtime": "string",
        "dtime_utc": "string",
        "business_date": "string",
    },
    date_column="business_date",
    meta_columns=("dtime", "dtime_utc", "business_date"),
    keys=("dtime_utc", "node"),
)


class TestGetSpec:
    def test_known_endpoint(self):
        assert get_spec("price-cost") is REGISTRY["price-cost"]

    def test_unknown_endpoint_raises(self):
        with pytest.raises(ValueError, match="Unknown endpoint 'nope'"):
            get_spec("nope")


class TestDataColumns:
    def test_meta_dropped_api_order_kept(self):
        assert data_columns(SPEC) == ["node", "value", "other"]


class TestBuildSelect:
    def test_none_selects_all(self):
        assert build_select(SPEC, None) is None

    def test_meta_then_keys_then_columns(self):
        assert build_select(SPEC, ["value", "other"]) == [
            "dtime",
            "dtime_utc",
            "business_date",
            "node",
            "value",
            "other",
        ]

    def test_duplicates_dropped(self):
        assert build_select(SPEC, ["node", "business_date", "value", "value"]) == [
            "dtime",
            "dtime_utc",
            "business_date",
            "node",
            "value",
        ]

    def test_empty_columns_selects_meta_and_keys(self):
        assert build_select(SPEC, []) == ["dtime", "dtime_utc", "business_date", "node"]

    def test_unknown_column_passed_through(self):
        assert build_select(SPEC, ["typo"])[-1] == "typo"

    def test_columns_not_mutated(self):
        columns = ["value"]
        build_select(SPEC, columns)
        assert columns == ["value"]


@pytest.mark.parametrize("name", REGISTRY)
def test_registry_select_only_existing_columns(name):
    spec = REGISTRY[name]
    assert set(build_select(spec, [])) <= set(spec.columns)


def test_date_clauses():
    assert date_clauses("business_date", "2024-01-01", "2024-01-30") == [
        "business_date ge '2024-01-01'",
        "business_date le '2024-01-30'",
    ]
