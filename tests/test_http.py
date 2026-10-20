from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

import pytest
import requests.exceptions
import responses

from pse_sdk._http import HTTPClient

BASE_URL = "https://api.example.com/api"


class TestInit:
    def test_trailing_slash_stripped(self):
        c = HTTPClient("https://x.com/api/", 10, 5)
        assert c.base_url == "https://x.com/api"


class TestFetch:
    @responses.activate
    def test_basic_fetch(self):
        responses.get(f"{BASE_URL}/data", json={"value": [{"a": 1}]})
        c = HTTPClient(BASE_URL, 10, 5)
        result = c.fetch("data")
        assert result == {"value": [{"a": 1}]}

    @responses.activate
    def test_select_params(self):
        responses.get(f"{BASE_URL}/data", json={"value": []})
        c = HTTPClient(BASE_URL, 10, 5)
        c.fetch("data", select=["a", "b"])
        params = parse_qs(urlparse(responses.calls[0].request.url).query)
        assert params["$select"] == ["a,b"]

    @responses.activate
    def test_filter_param(self):
        responses.get(f"{BASE_URL}/data", json={"value": []})
        c = HTTPClient(BASE_URL, 10, 5)
        c.fetch("data", filter_expr="x eq 1")
        params = parse_qs(urlparse(responses.calls[0].request.url).query)
        assert params["$filter"] == ["x eq 1"]

    @responses.activate
    def test_orderby_param(self):
        responses.get(f"{BASE_URL}/data", json={"value": []})
        c = HTTPClient(BASE_URL, 10, 5)
        c.fetch("data", order_by="col asc")
        params = parse_qs(urlparse(responses.calls[0].request.url).query)
        assert params["$orderby"] == ["col asc"]

    @responses.activate
    def test_first_and_after_params(self):
        responses.get(f"{BASE_URL}/data", json={"value": []})
        c = HTTPClient(BASE_URL, 10, 5)
        c.fetch("data", first=50, after="token123")
        params = parse_qs(urlparse(responses.calls[0].request.url).query)
        assert params["$first"] == ["50"]
        assert params["$after"] == ["token123"]

    @responses.activate
    def test_http_error_raises(self):
        responses.get(f"{BASE_URL}/data", status=404)
        c = HTTPClient(BASE_URL, 10, 5)
        with pytest.raises(requests.exceptions.HTTPError):
            c.fetch("data")
        assert len(responses.calls) == 1

    @responses.activate
    def test_http_error_includes_api_message(self):
        responses.get(
            f"{BASE_URL}/data",
            status=400,
            json={
                "error": {
                    "code": "BadRequest",
                    "message": "Invalid field to be returned requested: x",
                    "status": 400,
                }
            },
        )
        c = HTTPClient(BASE_URL, 10, 5)
        with pytest.raises(requests.exceptions.HTTPError) as exc:
            c.fetch("data")
        assert str(exc.value) == (
            f"400 Client Error: Bad Request for url: {BASE_URL}/data: "
            "Invalid field to be returned requested: x"
        )
        assert exc.value.response.status_code == 400

    @responses.activate
    @pytest.mark.parametrize(
        "body", [{"body": "<html>Bad Request</html>"}, {"json": {"detail": "x"}}]
    )
    def test_http_error_without_api_message_unchanged(self, body):
        responses.get(f"{BASE_URL}/data", status=400, **body)
        c = HTTPClient(BASE_URL, 10, 5)
        with pytest.raises(requests.exceptions.HTTPError) as exc:
            c.fetch("data")
        assert str(exc.value) == f"400 Client Error: Bad Request for url: {BASE_URL}/data"


class TestFetchAll:
    @responses.activate
    def test_single_page(self):
        responses.get(f"{BASE_URL}/data", json={"value": [{"a": 1}]})
        c = HTTPClient(BASE_URL, 10, 5)
        result = c.fetch_all("data")
        assert result == [{"a": 1}]

    @responses.activate
    def test_two_pages(self):
        responses.get(
            f"{BASE_URL}/data",
            json={"value": [{"a": 1}], "nextLink": "https://api.example.com/page2"},
        )
        responses.get(
            "https://api.example.com/page2",
            json={"value": [{"a": 2}]},
        )
        c = HTTPClient(BASE_URL, 10, 5)
        result = c.fetch_all("data")
        assert result == [{"a": 1}, {"a": 2}]

    @responses.activate
    def test_three_pages(self):
        responses.get(
            f"{BASE_URL}/data",
            json={"value": [{"a": 1}], "nextLink": "https://api.example.com/p2"},
        )
        responses.get(
            "https://api.example.com/p2",
            json={"value": [{"a": 2}], "nextLink": "https://api.example.com/p3"},
        )
        responses.get(
            "https://api.example.com/p3",
            json={"value": [{"a": 3}]},
        )
        c = HTTPClient(BASE_URL, 10, 5)
        result = c.fetch_all("data")
        assert result == [{"a": 1}, {"a": 2}, {"a": 3}]

    @responses.activate
    def test_empty_response(self):
        responses.get(f"{BASE_URL}/data", json={"value": []})
        c = HTTPClient(BASE_URL, 10, 5)
        assert c.fetch_all("data") == []

    @responses.activate
    def test_page_size_passed_as_first(self):
        responses.get(f"{BASE_URL}/data", json={"value": []})
        c = HTTPClient(BASE_URL, 25, 5)
        c.fetch_all("data")
        params = parse_qs(urlparse(responses.calls[0].request.url).query)
        assert params["$first"] == ["25"]


class TestRetry:
    @responses.activate
    @patch("pse_sdk._http.time.sleep")
    def test_retry_on_500_then_success(self, mock_sleep):
        responses.get(
            f"{BASE_URL}/data",
            json={"value": [{"a": 1}], "nextLink": "https://api.example.com/p2"},
        )
        responses.get("https://api.example.com/p2", status=500)
        responses.get("https://api.example.com/p2", json={"value": [{"a": 2}]})

        c = HTTPClient(BASE_URL, 10, 5)
        result = c.fetch_all("data")
        assert result == [{"a": 1}, {"a": 2}]
        mock_sleep.assert_called_once_with(1)

    @responses.activate
    @patch("pse_sdk._http.time.sleep")
    def test_retry_exhaustion_raises(self, mock_sleep):
        responses.get(
            f"{BASE_URL}/data",
            json={"value": [{"a": 1}], "nextLink": "https://api.example.com/p2"},
        )
        for _ in range(4):
            responses.get("https://api.example.com/p2", status=500)

        c = HTTPClient(BASE_URL, 10, 5)
        with pytest.raises(requests.exceptions.HTTPError):
            c.fetch_all("data")
        assert mock_sleep.call_count == 3

    @responses.activate
    @patch("pse_sdk._http.time.sleep")
    def test_no_retry_on_4xx(self, mock_sleep):
        responses.get(
            f"{BASE_URL}/data",
            json={"value": [{"a": 1}], "nextLink": "https://api.example.com/p2"},
        )
        responses.get("https://api.example.com/p2", status=404)

        c = HTTPClient(BASE_URL, 10, 5)
        with pytest.raises(requests.exceptions.HTTPError):
            c.fetch_all("data")
        mock_sleep.assert_not_called()

    @responses.activate
    @patch("pse_sdk._http.time.sleep")
    @pytest.mark.parametrize("status", [502, 503, 504])
    def test_retry_on_other_server_errors(self, mock_sleep, status):
        responses.get(
            f"{BASE_URL}/data",
            json={"value": [{"a": 1}], "nextLink": "https://api.example.com/p2"},
        )
        responses.get("https://api.example.com/p2", status=status)
        responses.get("https://api.example.com/p2", json={"value": [{"a": 2}]})

        c = HTTPClient(BASE_URL, 10, 5)
        result = c.fetch_all("data")
        assert result == [{"a": 1}, {"a": 2}]

    @responses.activate
    @patch("pse_sdk._http.time.sleep")
    def test_first_page_retry_on_503_then_success(self, mock_sleep):
        responses.get(f"{BASE_URL}/data", status=503)
        responses.get(f"{BASE_URL}/data", json={"value": [{"a": 1}]})

        c = HTTPClient(BASE_URL, 10, 5)
        result = c.fetch_all("data")
        assert result == [{"a": 1}]
        mock_sleep.assert_called_once_with(1)

    @responses.activate
    @patch("pse_sdk._http.time.sleep")
    def test_first_page_retry_exhaustion_raises(self, mock_sleep):
        for _ in range(4):
            responses.get(f"{BASE_URL}/data", status=500)

        c = HTTPClient(BASE_URL, 10, 5)
        with pytest.raises(requests.exceptions.HTTPError):
            c.fetch_all("data")
        assert mock_sleep.call_count == 3

    @responses.activate
    @patch("pse_sdk._http.time.sleep")
    def test_retry_exhaustion_includes_api_message(self, mock_sleep):
        for _ in range(4):
            responses.get(
                f"{BASE_URL}/data",
                status=500,
                json={"error": {"message": "DatabaseOperationFailed"}},
            )

        c = HTTPClient(BASE_URL, 10, 5)
        with pytest.raises(
            requests.exceptions.HTTPError, match=r"^500 Server Error.*: DatabaseOperationFailed$"
        ):
            c.fetch_all("data")
        assert mock_sleep.call_count == 3

    @responses.activate
    @patch("pse_sdk._http.time.sleep")
    def test_first_page_retry_keeps_query_params(self, mock_sleep):
        responses.get(f"{BASE_URL}/data", status=503)
        responses.get(f"{BASE_URL}/data", json={"value": []})

        c = HTTPClient(BASE_URL, 25, 5)
        c.fetch_all("data", select=["a", "b"], filter_expr="x eq 1")
        assert len(responses.calls) == 2
        params = parse_qs(urlparse(responses.calls[1].request.url).query)
        assert params["$first"] == ["25"]
        assert params["$select"] == ["a,b"]
        assert params["$filter"] == ["x eq 1"]
