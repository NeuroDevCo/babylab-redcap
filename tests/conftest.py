"""
Fixtures for testing
"""

import os
import pytest
import win32com as win
from babylab.src import api
from babylab.app import create_app
from babylab.app import config as conf
from tests import utils as tutils

IS_GIHTUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.fixture
def app():
    """App factory for testing."""
    yield create_app(env="test")


@pytest.fixture
def client(app):  # pylint: disable=redefined-outer-name
    """Testing client."""
    return app.test_client()


@pytest.fixture
def token():
    """API test token.

    Returns:
        str: API test token.
    """
    return conf.get_api_key()


@pytest.fixture
def records():
    """REDCap records database."""
    return api.Records(token=conf.get_api_key())


@pytest.fixture
def data_dict():
    """REDCap data dictionary.."""
    return api.get_data_dict(token=conf.get_api_key())


@pytest.fixture
def participant_finput() -> dict:
    """Form input for participant."""
    return tutils.create_finput_participant()


@pytest.fixture
def participant_finput_mod() -> dict:
    """Form input for participant."""
    return tutils.create_finput_participant(is_new=False)


@pytest.fixture
def appointment_finput() -> dict:
    """Form input for appointment."""
    return tutils.create_finput_appointment()


@pytest.fixture
def appointment_finput_mod() -> dict:
    """Form input for appointment."""
    return tutils.create_finput_appointment(is_new=False)


@pytest.fixture
def questionnaire_finput() -> dict:
    """Form input for questionnaire."""
    return tutils.create_finput_questionnaire()


@pytest.fixture
def questionnaire_finput_mod() -> dict:
    """Form input for questionnaire."""
    return tutils.create_finput_questionnaire(is_new=False)


@pytest.fixture
def participant_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return tutils.create_record_participant()


@pytest.fixture
def participant_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return tutils.create_record_participant(is_new=False)


@pytest.fixture
def appointment_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return tutils.create_record_appointment()


@pytest.fixture
def appointment_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return tutils.create_record_appointment(is_new=False)


@pytest.fixture
def questionnaire_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDCap record fixture.
    """
    return tutils.create_record_questionnaire()


@pytest.fixture
def questionnaire_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDCap record fixture.
    """
    return tutils.create_record_questionnaire(is_new=False)


def pytest_sessionfinish(account: str = "gonzalo.garcia@sjd.es"):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    if not IS_GIHTUB_ACTIONS:
        api.check_email_address(account)
        outlook = win.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        recipient = outlook.createRecipient(account)
        shared_cal = outlook.GetSharedDefaultFolder(recipient, 9).Folders(
            "Appointments - Test"
        )
        for e in shared_cal.Items:
            e.Delete()
