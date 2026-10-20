from gen_docs import HEADER, KEYS_HEADER, OUTPUT, natural_key, render
from pse_sdk._endpoint_spec import EndpointSpec
from pse_sdk._registry import REGISTRY

SPEC = {
    "price-cost": EndpointSpec(
        columns={
            "cen_cost": "number",
            "contracting": "string",
            "dtime": "string",
            "business_date": "string",
        },
        date_column="business_date",
        meta_columns=("dtime", "business_date"),
        keys=("dtime",),
    ),
    "csire-kpi10": EndpointSpec(
        columns={"kpi": "number"}, date_column="business_date", meta_columns=(), keys=()
    ),
    "csire-kpi2": EndpointSpec(
        columns={"kpi": "number"}, date_column="business_date", meta_columns=(), keys=()
    ),
}


def _rows(source: str) -> list[str]:
    return source.removeprefix(HEADER).split(KEYS_HEADER)[0].splitlines()


def _key_rows(source: str) -> list[str]:
    return source.split(KEYS_HEADER)[1].splitlines()


class TestNaturalKey:
    def test_digits_compared_numerically(self):
        names = ["csire-kpi10", "csire-kpi2", "csire-kpi1"]
        assert sorted(names, key=natural_key) == [
            "csire-kpi1",
            "csire-kpi2",
            "csire-kpi10",
        ]

    def test_otherwise_alphabetical(self):
        names = ["ogr-d1-head", "ogr-b", "ogr-d1", "cor-q-1", "cor"]
        assert sorted(names, key=natural_key) == sorted(names)


class TestRender:
    def test_header(self):
        assert render(SPEC).startswith(HEADER)

    def test_endpoints_natural_order(self):
        endpoints = [row.split("`")[1] for row in _rows(render(SPEC))]
        assert list(dict.fromkeys(endpoints)) == [
            "csire-kpi2",
            "csire-kpi10",
            "price-cost",
        ]

    def test_data_columns_only_in_api_order(self):
        rows = _rows(render({"price-cost": SPEC["price-cost"]}))
        assert rows == [
            "| `price-cost` | `cen_cost` | number |",
            "| `price-cost` | `contracting` | string |",
        ]

    def test_key_rows(self):
        assert _key_rows(render(SPEC)) == [
            "| `csire-kpi2` | `business_date` | - |",
            "| `csire-kpi10` | `business_date` | - |",
            "| `price-cost` | `business_date` | `dtime` |",
        ]


class TestCommittedDocs:
    def test_up_to_date(self):
        assert OUTPUT.read_text(encoding="utf-8") == render(REGISTRY)

    def test_all_endpoints_listed(self):
        endpoints = {row.split("`")[1] for row in _rows(render(REGISTRY))}
        assert endpoints == set(REGISTRY)

    def test_all_endpoints_in_key_table(self):
        endpoints = [row.split("`")[1] for row in _key_rows(render(REGISTRY))]
        assert sorted(endpoints) == sorted(REGISTRY)
