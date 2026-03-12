import responses

from pse_sdk import PSEClient
from tests.conftest import BASE_URL, make_page, make_record


class TestPSERegistration:
    def test_has_main_method(self, pse):
        assert hasattr(pse, "get_price_cost")
        assert callable(pse.get_price_cost)

    def test_has_split_methods(self, pse):
        for name in ["get_cen", "get_ckoeb", "get_ceb_sr", "get_cor_pp",
                      "get_imb_energy", "get_contracting"]:
            assert hasattr(pse, name), f"Missing method: {name}"
            assert callable(getattr(pse, name))


class TestPSEIntegration:
    @responses.activate
    def test_get_cen_returns_list_of_dicts(self, pse):
        responses.add(
            responses.GET,
            f"{BASE_URL}/price-cost",
            json=make_page([{
                "dtime": "2024-01-01T00:00:00",
                "period": 1,
                "business_date": "2024-01-01",
                "publication_ts": "2024-01-01T12:00:00",
                "cen_cost": 150.5,
            }]),
        )
        result = pse.get_cen("2024-01-01", "2024-01-01")
        assert isinstance(result, list)
        assert len(result) == 1
        assert "cen_cost" in result[0]

    @responses.activate
    def test_get_cen_dataframe_via_partial(self, pse):
        responses.add(
            responses.GET,
            f"{BASE_URL}/price-cost",
            json=make_page([{
                "dtime": "2024-01-01T00:00:00",
                "period": 1,
                "business_date": "2024-01-01",
                "publication_ts": "2024-01-01T12:00:00",
                "cen_cost": 150.5,
            }]),
        )
        df = pse.get_cen("2024-01-01", "2024-01-01", format="dataframe")
        assert len(df) == 1
        assert "cen_cost" in df.columns

    @responses.activate
    def test_get_price_cost_returns_all_columns(self, pse):
        responses.add(
            responses.GET,
            f"{BASE_URL}/price-cost",
            json=make_page([make_record()]),
        )
        result = pse.get_price_cost("2024-01-01", "2024-01-01")
        assert isinstance(result, list)
        assert len(result) == 1
        assert "cen_cost" in result[0]
        assert "ckoeb_cost" in result[0]

    @responses.activate
    def test_pagination_end_to_end(self, pse):
        next_url = f"{BASE_URL}/price-cost?$after=token1"
        responses.add(
            responses.GET,
            f"{BASE_URL}/price-cost",
            json=make_page(
                [make_record(period=1)],
                next_link=next_url,
            ),
        )
        responses.add(
            responses.GET,
            next_url,
            json=make_page([make_record(period=2)]),
        )
        result = pse.get_price_cost("2024-01-01", "2024-01-01")
        assert len(result) == 2
