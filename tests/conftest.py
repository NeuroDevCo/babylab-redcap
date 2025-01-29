"""
Fixtures for testing
"""

import os
import pytest
import win32com as win
from babylab.src import api, outlook
from babylab.app import create_app
from babylab.app import config as conf
from tests import utils as tutils

IS_GIHTUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.fixture
def app():
    """App factory for testing."""
    yield create_app(env="test")


@pytest.fixture
def token():
    """API test token.

    Returns:
        str: API test token.
    """
    return conf.get_api_key()


@pytest.fixture
def client(app, token):  # pylint: disable=redefined-outer-name
    """Testing client."""
    app.config["RECORDS"] = api.Records(token=token)
    return app.test_client()


@pytest.fixture
def records():
    """REDCap records database."""
    return api.Records(token=conf.get_api_key())


@pytest.fixture
def data_dict():
    """REDCap data dictionary.."""
    return api.get_data_dict(token=conf.get_api_key())


@pytest.fixture
def ppt_finput() -> dict:
    """Form input for participant."""
    return tutils.create_finput_ppt()


@pytest.fixture
def ppt_finput_mod() -> dict:
    """Form input for participant."""
    return tutils.create_finput_ppt(is_new=False)


@pytest.fixture
def apt_finput() -> dict:
    """Form input for appointment."""
    return tutils.create_finput_apt()


@pytest.fixture
def apt_finput_mod() -> dict:
    """Form input for appointment."""
    return tutils.create_finput_apt(is_new=False)


@pytest.fixture
def que_finput() -> dict:
    """Form input for questionnaire."""
    return tutils.create_finput_que()


@pytest.fixture
def que_finput_mod() -> dict:
    """Form input for questionnaire."""
    return tutils.create_finput_que(is_new=False)


@pytest.fixture
def ppt_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return tutils.create_record_ppt()


@pytest.fixture
def ppt_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return tutils.create_record_ppt(is_new=False)


@pytest.fixture
def apt_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return tutils.create_record_apt()


@pytest.fixture
def apt_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return tutils.create_record_apt(is_new=False)


@pytest.fixture
def que_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDCap record fixture.
    """
    return tutils.create_record_que()


@pytest.fixture
def que_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDCap record fixture.
    """
    return tutils.create_record_que(is_new=False)


def pytest_sessionfinish(account: str = "gonzalo.garcia@sjd.es"):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    if not IS_GIHTUB_ACTIONS:
        outlook.check_email_address(account)
        ol = win.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        recipient = ol.createRecipient(account)
        shared_cal = ol.GetSharedDefaultFolder(recipient, 9).Folders(
            "Appointments - Test"
        )
        for e in shared_cal.Items:
            e.Delete()
