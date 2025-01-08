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


def test_compose_email(appointment_record, data_dict: dict):
    """Validate composed email."""
    email_data = {
        "record_id": "1",
        "appointment_id": "1:2",
        "status": "1",
        "date": appointment_record["appointment_date"].isoformat(),
        "study": "1",
        "taxi_address": appointment_record["appointment_taxi_address"],
        "taxi_isbooked": appointment_record["appointment_taxi_isbooked"],
        "comments": appointment_record["appointment_comments"],
    }
    data = utils.replace_labels(email_data, data_dict)
    email = api.compose_email(data)
    assert all(k in email for k in ["body", "subject"])
    assert "<table" in email["body"]
    assert "</table" in email["body"]
    assert (
        "The appointment 1:2 (ID: 1) from study mop_newborns_1_nirs has been created or modified. Here are the details:"  # pylint: disable=line-too-long
        in email["body"]
    )
    assert (
        "Appointment 1:2 (Scheduled) | mop_newborns_1_nirs (ID: 1) - 2024-12-31T14:09:00"
        in email["subject"]
    )


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_send_email(data_dict: dict):
    """Test that en email is received."""
    record = {
        "record_id": "1",
        "redcap_repeat_instrument": "appointments",
        "redcap_repeat_instance": "1",
        "appointment_study": "1",
        "appointment_date_created": "2024-12-14 12:08:00",
        "appointment_date_updated": "2024-12-14 12:08:00",
        "appointment_date": "2024-12-14T12:08",
        "appointment_taxi_address": "lkfnsdklfnsd",
        "appointment_taxi_isbooked": "1",
        "appointment_status": "2",
        "appointment_comments": "sdldkfndskln",
        "appointments_complete": "2",
        "appointment_id": "1:1",
    }

    email_data = utils.prepare_email(
        apt_id=record["appointment_id"],
        ppt_id=record["record_id"],
        data=record,
        data_dict=data_dict,
    )
    api.send_email(data=email_data)
    time.sleep(20)
    email = tutils.check_email_received()
    assert email
    assert email["subject"] == email_data["subject"]
