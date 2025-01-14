"""Test email functions
"""

import os
import time
import pytest
from babylab.src import api, utils
from tests import utils as tutils

IS_GIHTUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_email_validation():
    """Validate email addresses."""
    try:
        api.check_email_domain("iodsf@sjd.es")
    except (api.MailDomainException, api.MailAddressException) as e:
        pytest.fail(str(e))
    with pytest.raises(api.MailDomainException):
        api.check_email_domain("iodsf@sjd.com")
    with pytest.raises(api.MailAddressException):
        api.check_email_address("iodsf@opdofsn.com")


def test_compose_outlook(appointment_record_mod, data_dict: dict):
    """Validate composed outlook."""
    apt_id = (
        appointment_record_mod["record_id"]
        + ":"
        + appointment_record_mod["redcap_repeat_instance"]
    )
    email_data = {
        "record_id": appointment_record_mod["record_id"],
        "id": apt_id,
        "status": "1",
        "date": appointment_record_mod["appointment_date"].isoformat(),
        "study": "1",
        "taxi_address": appointment_record_mod["appointment_taxi_address"],
        "taxi_isbooked": appointment_record_mod["appointment_taxi_isbooked"],
        "comments": appointment_record_mod["appointment_comments"],
    }
    data = utils.replace_labels(email_data, data_dict)
    email = api.compose_outlook(data)
    assert all(k in email for k in ["body", "subject"])
    assert appointment_record_mod["appointment_study"] in email["body"]
    assert appointment_record_mod["appointment_study"] in email["subject"]
    assert appointment_record_mod["appointment_status"] in email["body"]
    assert appointment_record_mod["appointment_status"] in email["subject"]
    assert "Here are the details:" in email["body"]
    assert f"Appointment {apt_id}" in email["subject"]


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_send_email(data_dict: dict):
    """Test that en email is received."""
    record = {
        "record_id": "1",
        "redcap_repeat_instrument": "appointments",
        "redcap_repeat_instance": "1",
        "study": "1",
        "date_created": "2024-12-31 12:08:00",
        "date_updated": "2024-12-31 12:08:00",
        "date": "2024-12-14 12:08",
        "taxi_address": "lkfnsdklfnsd",
        "taxi_isbooked": "1",
        "status": "2",
        "comments": "sdldkfndskln",
        "appointments_complete": "2",
        "id": "1:1",
    }

    email_data = utils.prepare_email(
        apt_id=record["id"],
        ppt_id=record["record_id"],
        data=record,
        data_dict=data_dict,
    )
    api.send_email(data=email_data)
    time.sleep(20)
    email = tutils.check_email_received()
    assert email
    assert email["subject"] == email_data["subject"]


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_create_event(data_dict: dict):
    """Test that en email is received."""
    record = {
        "record_id": "1",
        "redcap_repeat_instrument": "appointments",
        "redcap_repeat_instance": "1",
        "study": "1",
        "date_created": "2024-12-31 12:08:00",
        "date_updated": "2024-12-31 12:08:00",
        "date": "2024-12-31 12:08",
        "taxi_address": "lkfnsdklfnsd",
        "taxi_isbooked": "1",
        "status": "2",
        "comments": "sdldkfndskln",
        "appointments_complete": "2",
        "id": "1:1",
    }

    event_data = utils.prepare_email(
        apt_id=record["id"],
        ppt_id=record["record_id"],
        data=record,
        data_dict=data_dict,
    )
    api.create_event(data=event_data, calendar_name="Appointments - Test")
    time.sleep(20)
    event = tutils.check_event_created(ppt_id=record["record_id"])
    assert event
    assert "1:1" in event["subject"]
