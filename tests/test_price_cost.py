import pytest
import responses

from pse_sdk._client import HTTPClient
from pse_sdk._endpoints import EndpointQuery, EndpointSplitQuery
from tests.conftest import BASE_URL, make_page, make_record, parse_params


def _make_endpoint():
    client = HTTPClient(base_url=BASE_URL, page_size=100, timeout=5)
    return client, EndpointQuery(client, "price-cost", "business_date")


def _make_split(value_columns=None):
    client = HTTPClient(base_url=BASE_URL, page_size=100, timeout=5)
    return client, EndpointSplitQuery(
        client, "price-cost", "business_date",
        value_columns or ["cen_cost"],
    )


@responses.activate
def test_query_returns_list_of_dicts():
    _, ep = _make_endpoint()

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([make_record()]),
    )
    result = ep("2024-01-01", "2024-01-01")
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["cen_cost"] == 100.0


@responses.activate
def test_query_dataframe_returns_dataframe_with_parsed_datetimes():
    _, ep = _make_endpoint()

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([make_record()]),
    )
    df = ep("2024-01-01", "2024-01-01", format="dataframe")
    assert len(df) == 1
    assert "datetime64" in str(df["dtime"].dtype)
    assert "datetime64" in str(df["publication_ts"].dtype)
    assert df["cen_cost"].iloc[0] == 100.0


@responses.activate
def test_query_split_selects_correct_columns():
    _, split = _make_split(["cen_cost"])

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
    result = split("2024-01-01", "2024-01-01")
    assert isinstance(result, list)
    assert "cen_cost" in result[0]

    params = parse_params(responses.calls[0].request.url)
    select_cols = params["$select"].split(",")
    assert "cen_cost" in select_cols
    assert "dtime" in select_cols
    assert "business_date" in select_cols


@responses.activate
def test_query_split_dataframe():
    _, split = _make_split(["cen_cost"])

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
    df = split("2024-01-01", "2024-01-01", format="dataframe")
    assert "cen_cost" in df.columns


@responses.activate
def test_query_empty_returns_empty_list():
    _, ep = _make_endpoint()

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([]),
    )
    result = ep("2024-01-01", "2024-01-01")
    assert result == []


@responses.activate
def test_query_empty_dataframe():
    _, ep = _make_endpoint()

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([]),
    )
    df = ep("2024-01-01", "2024-01-01", format="dataframe")
    assert len(df) == 0


def test_query_invalid_format_raises_value_error():
    _, ep = _make_endpoint()

    with pytest.raises(ValueError, match="format must be"):
        ep("2024-01-01", "2024-01-01", format="csv")


@responses.activate
def test_date_filter_format():
    _, ep = _make_endpoint()

    responses.add(
        responses.GET,
        f"{BASE_URL}/price-cost",
        json=make_page([]),
    )
    ep("2024-06-01", "2024-06-30")

    params = parse_params(responses.calls[0].request.url)
    assert params["$filter"] == "business_date ge '2024-06-01' and business_date le '2024-06-30'"
