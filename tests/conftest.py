from unittest.mock import patch

import pytest


@pytest.fixture()
def mock_http():
    with patch("pse_sdk._client.HTTPClient") as mock_http:
        yield mock_http
