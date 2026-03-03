import responses

from pse._client import PSEClient
from pse.endpoints.price_cost import PriceCost
from tests.conftest import BASE_URL, make_page, make_record, parse_params


@responses.activate
def test_query_returns_dataframe_with_parsed_datetimes():
    client = PSEClient(base_url=BASE_URL, page_size=100, timeout=5)
    ep = PriceCost(client)

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([make_record()]),
    )
    df = ep.query("2024-01-01", "2024-01-01")
    assert len(df) == 1
    assert "datetime64" in str(df["dtime"].dtype)
    assert "datetime64" in str(df["publication_ts"].dtype)
    assert df["cen_cost"].iloc[0] == 100.0


@responses.activate
def test_query_split_selects_correct_columns():
    client = PSEClient(base_url=BASE_URL, page_size=100, timeout=5)
    ep = PriceCost(client)

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([{
            "dtime": "2024-01-01T00:00:00",
            "period": 1,
            "business_date": "2024-01-01",
            "publication_ts": "2024-01-01T12:00:00",
            "cen_cost": 100.0,
        }]),
    )
    df = ep.query_split(["cen_cost"], "2024-01-01", "2024-01-01")
    assert "cen_cost" in df.columns

    params = parse_params(responses.calls[0].request.url)
    select_cols = params["$select"].split(",")
    assert "cen_cost" in select_cols
    assert "dtime" in select_cols
    assert "business_date" in select_cols


@responses.activate
def test_query_empty_returns_empty_dataframe():
    client = PSEClient(base_url=BASE_URL, page_size=100, timeout=5)
    ep = PriceCost(client)

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([]),
    )
    df = ep.query("2024-01-01", "2024-01-01")
    assert len(df) == 0


@responses.activate
def test_date_filter_format():
    client = PSEClient(base_url=BASE_URL, page_size=100, timeout=5)
    ep = PriceCost(client)

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([]),
    )
    ep.query("2024-06-01", "2024-06-30")

    params = parse_params(responses.calls[0].request.url)
    assert params["$filter"] == "business_date ge '2024-06-01' and business_date le '2024-06-30'"


def test_price_cost_has_correct_splits():
    assert PriceCost.path == "price-cost"
    assert PriceCost.method_name == "get_price_cost"
    assert len(PriceCost.splits) == 6
    names = [s.method_name for s in PriceCost.splits]
    assert "get_cen" in names
    assert "get_ckoeb" in names
