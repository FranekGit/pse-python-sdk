from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture()
def mock_client():
    with (
        patch("pse_sdk._client.HTTPClient") as mock_http,
        patch("pse_sdk._client.make_endpoint", return_value=MagicMock()) as mock_make,
    ):
        yield mock_http, mock_make
