import responses

from tests.conftest import BASE_URL, make_page, make_record, parse_params


class TestPSEClientFetch:
    @responses.activate
    def test_fetch_builds_odata_params(self, client):
        responses.add(
            responses.GET,
            f"{BASE_URL}/price-cost",
            json=make_page([make_record()]),
        )
        result = client.fetch(
            "price-cost",
            select=["cen_cost", "dtime"],
            filter_expr="business_date ge '2024-01-01'",
            order_by="dtime",
            first=10,
        )
        assert result["value"][0]["cen_cost"] == 100.0

        params = parse_params(responses.calls[0].request.url)
        assert params["$select"] == "cen_cost,dtime"
        assert params["$filter"] == "business_date ge '2024-01-01'"
        assert params["$orderby"] == "dtime"
        assert params["$first"] == "10"

    @responses.activate
    def test_fetch_raises_on_http_error(self, client):
        responses.add(responses.GET, f"{BASE_URL}/bad", status=404)
        import pytest
        with pytest.raises(Exception):
            client.fetch("bad")


class TestPSEClientFetchAll:
    @responses.activate
    def test_single_page(self, client):
        responses.add(
            responses.GET,
            f"{BASE_URL}/price-cost",
            json=make_page([make_record(period=1), make_record(period=2)]),
        )
        records = client.fetch_all("price-cost")
        assert len(records) == 2

    @responses.activate
    def test_pagination_follows_next_link(self, client):
        next_url = f"{BASE_URL}/price-cost?$after=abc123"
        responses.add(
            responses.GET,
            f"{BASE_URL}/price-cost",
            json=make_page([make_record(period=1)], next_link=next_url),
        )
        responses.add(
            responses.GET,
            next_url,
            json=make_page([make_record(period=2)]),
        )
        records = client.fetch_all("price-cost")
        assert len(records) == 2
        assert records[0]["period"] == 1
        assert records[1]["period"] == 2

    @responses.activate
    def test_empty_response(self, client):
        responses.add(
            responses.GET,
            f"{BASE_URL}/price-cost",
            json=make_page([]),
        )
        records = client.fetch_all("price-cost")
        assert records == []
