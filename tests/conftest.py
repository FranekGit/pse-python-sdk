from urllib.parse import parse_qs, urlparse

import pytest

from pse import PSEClient
from pse._client import HTTPClient

BASE_URL = "https://api.raporty.pse.pl/api"


@pytest.fixture
def client():
    return HTTPClient(base_url=BASE_URL, page_size=2, timeout=5)


@pytest.fixture
def pse():
    return PSEClient(base_url=BASE_URL, page_size=2, timeout=5)


def make_record(period=1, business_date="2024-01-01", cen_cost=100.0, **extra):
    return {
        "dtime": "2024-01-01T00:00:00",
        "period": period,
        "business_date": business_date,
        "publication_ts": "2024-01-01T12:00:00",
        "cen_cost": cen_cost,
        "ckoeb_cost": 50.0,
        "ceb_sr_cost": 75.0,
        "cor_pp_cost": 10.0,
        "imb_energy": 200.0,
        "contracting": "long",
        **extra,
    }


def make_page(records, next_link=None):
    result = {"value": records}
    if next_link:
        result["nextLink"] = next_link
    return result


def parse_params(url: str) -> dict[str, str]:
    """Parse URL query params into {key: value} dict (decoded, single-value)."""
    qs = parse_qs(urlparse(url).query)
    return {k: v[0] for k, v in qs.items()}
