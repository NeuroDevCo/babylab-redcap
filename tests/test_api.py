"""Test api.py"""

from babylab import api

URL = "https://run.mocky.io/v3/b5cf9465-0e94-40f6-a2ea-caf7e48700c9"
TOKEN = "90F230F9J239F0JMXM1Z"


def test_login(url: str = URL, token: str = TOKEN):
    """Given some URL and API token, test that URL and API token are returned correctly.

    Args:
        url (str): API URL.
        token (str): API token.
    """
    creds = api.redcap_login(url=url, token=token)
    assert isinstance(creds, dict)
    assert len(creds) == 2
    assert all(k in ["API_URL", "API_KEY"] for k in creds)
    assert isinstance(creds["API_URL"], str)
    assert isinstance(creds["API_KEY"], str)
    assert creds["API_URL"] == url
    assert creds["API_KEY"] == token
