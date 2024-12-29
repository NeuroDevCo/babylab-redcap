"""Test email functions
"""

import pytest
from babylab.src import api, utils


@pytest.mark.skip(reason="Test doesn't work in Github Actions.")
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


def test_compose_email(appointment_record, token):
    """Validate composed email."""
    data_dict = api.get_data_dict(token=token)
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
        "The appointment 1:2 (ID: 1) from study mop-newborns has been created or modified. Here are the details:"  # pylint: disable=line-too-long
        in email["body"]
    )
    assert (
        "Appointment 1:2 (Scheduled) | mop-newborns (ID: 1) - 2024-12-31T14:09:00"
        in email["subject"]
    )
