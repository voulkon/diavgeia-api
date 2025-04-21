import requests
import pytest
from diavgeia_api.client import DiavgeiaClient
from diavgeia_api._config import BASE_URL


def test_default_headers():
    c = DiavgeiaClient()
    assert c.session.headers["Accept"] == "application/json"


def test_base_url_override():
    c = DiavgeiaClient(base_url="http://example.com")
    assert c._build_url("foo") == "http://example.com/foo"


def test_basic_auth():
    c = DiavgeiaClient(username="bob", password="bob")
    assert isinstance(c.session.auth, requests.auth.HTTPBasicAuth)


def test__build_url_helper():
    c = DiavgeiaClient()
    assert c._build_url("decisions", "ADA123") == f"{BASE_URL}/decisions/ADA123"
