import typing

import pytest

from gen_registry import build_registry, parse_keys, render
from pse_sdk._registry import REGISTRY, Endpoint


def _props(**types):
    return {col: {"type": type_, "format": ""} for col, type_ in types.items()}


SPEC = {
    "info": {"version": "1.0"},
    "paths": {
        "/price-cost": {},
        "/price-cost/dtime_utc/{dtime_utc}": {},
        "/unav-pk5l": {},
        "/unav-pk5l/unit_code/{unit_code}/start_dtime_utc/{start_dtime_utc}": {},
        "/ogr-d1-head": {},
        "/ogr-d1-head/period/{period}": {},
    },
    "components": {
        "schemas": {
            "price-cost": {
                "type": "object",
                "properties": _props(
                    cen_cost="number",
                    contracting="string",
                    publication_ts="string",
                    business_date="string",
                    dtime_utc="string",
                    dtime="string",
                ),
            },
            "unav-pk5l": {
                "type": "object",
                "properties": _props(
                    unit_code="string",
                    start_dtime_utc="string",
                    business_date="string",
                ),
            },
            "ogr-d1-head": {
                "type": "object",
                "properties": _props(title="string", period="string"),
            },
        }
    },
}


class TestParseKeys:
    def test_single_key(self):
        assert parse_keys(SPEC["paths"])["price-cost"] == ("dtime_utc",)

    def test_composite_key(self):
        keys = parse_keys(SPEC["paths"])
        assert keys["unav-pk5l"] == ("unit_code", "start_dtime_utc")

    def test_collection_paths_ignored(self):
        assert set(parse_keys(SPEC["paths"])) == {
            "price-cost",
            "unav-pk5l",
            "ogr-d1-head",
        }


class TestBuildRegistry:
    def test_endpoints_sorted(self):
        assert list(build_registry(SPEC)) == ["ogr-d1-head", "price-cost", "unav-pk5l"]

    def test_columns_keep_spec_order_and_types(self):
        columns = build_registry(SPEC)["price-cost"]["columns"]
        assert list(columns) == [
            "cen_cost",
            "contracting",
            "publication_ts",
            "business_date",
            "dtime_utc",
            "dtime",
        ]
        assert columns["cen_cost"] == "number"
        assert columns["contracting"] == "string"

    def test_date_column_business_date(self):
        assert build_registry(SPEC)["price-cost"]["date_column"] == "business_date"

    def test_date_column_none_without_business_date(self):
        assert build_registry(SPEC)["ogr-d1-head"]["date_column"] is None

    def test_meta_columns_fixed_order(self):
        assert build_registry(SPEC)["price-cost"]["meta_columns"] == (
            "dtime",
            "dtime_utc",
            "business_date",
            "publication_ts",
        )

    def test_utc_data_columns_not_meta(self):
        meta = build_registry(SPEC)["unav-pk5l"]["meta_columns"]
        assert meta == ("business_date",)

    def test_keys(self):
        assert build_registry(SPEC)["unav-pk5l"]["keys"] == (
            "unit_code",
            "start_dtime_utc",
        )


class TestRender:
    def test_round_trip(self):
        registry = build_registry(SPEC)
        namespace: dict = {}
        exec(render(registry, "1.0"), namespace)
        spec_cls = namespace["EndpointSpec"]
        assert namespace["REGISTRY"] == {
            name: spec_cls(**entry) for name, entry in registry.items()
        }

    def test_endpoint_literal(self):
        namespace: dict = {}
        exec(render(build_registry(SPEC), "1.0"), namespace)
        assert typing.get_args(namespace["Endpoint"]) == (
            "ogr-d1-head",
            "price-cost",
            "unav-pk5l",
        )

    def test_header_has_spec_version(self):
        assert "(spec version 1.0)" in render(build_registry(SPEC), "1.0")


class TestCommittedRegistry:
    def test_endpoint_literal_matches_registry(self):
        assert typing.get_args(Endpoint) == tuple(REGISTRY)

    def test_contains_client_endpoints(self):
        used = {
            "price-cost",
            "csdac-pln",
            "krb-rozl",
            "kmb-kro-rozl",
            "sk",
            "his-wlk-cal",
        }
        assert used <= set(REGISTRY)

    def test_price_cost(self):
        spec = REGISTRY["price-cost"]
        assert spec.columns["cen_cost"] == "number"
        assert spec.date_column == "business_date"
        assert spec.keys == ("dtime_utc",)

    def test_rcco2_has_no_dtime(self):
        assert "dtime" not in REGISTRY["rcco2"].meta_columns

    @pytest.mark.parametrize(
        "name",
        [
            "ogr-oper-head",
            "ogr-d1-head",
            "ogr-d2-head",
            "ogr-d39-head",
            "ogr-m-head",
            "ogr-r-head",
        ],
    )
    def test_head_endpoints_have_no_date_column(self, name):
        assert REGISTRY[name].date_column is None


@pytest.mark.parametrize("name", REGISTRY)
class TestRegistryInvariants:
    def test_meta_columns_are_columns(self, name):
        spec = REGISTRY[name]
        assert set(spec.meta_columns) <= set(spec.columns)

    def test_keys_are_columns(self, name):
        spec = REGISTRY[name]
        assert set(spec.keys) <= set(spec.columns)

    def test_date_column_is_column(self, name):
        spec = REGISTRY[name]
        assert spec.date_column is None or spec.date_column in spec.columns
