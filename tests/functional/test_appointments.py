"""Test appointments endpoints."""

import os
import time
import pytest
from tests import utils as tutils

IS_GIHTUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def test_apt_all(client):
    """Test apt_all endpoint."""
    response = client.get("/appointments/")
    assert response.status_code == 200


def test_apt(client, appointment_record_mod):
    """Test apt_all endpoint."""
    apt_id = (
        appointment_record_mod["record_id"]
        + ":"
        + appointment_record_mod["redcap_repeat_instance"]
    )
    response = client.get("/appointments/" + apt_id)
    assert response.status_code == 200


def test_apt_new(client, appointment_finput):
    """Test apt_new endpoint."""
    ppt_id = appointment_finput["inputId"]
    response = client.get(f"/participants/{ppt_id}/appointment_new")
    assert response.status_code == 200


def test_apt_new_post(client, appointment_finput):
    """Test apt_new endpoint."""
    ppt_id = appointment_finput["inputId"]
    response = client.post(
        f"/participants/{ppt_id}/appointment_new", data=appointment_finput
    )
    assert response.status_code == 302


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_apt_new_post_email(app, appointment_finput):
    """Test apt_new endpoint with email."""
    app.config["EMAIL"] = "gonzalo.garcia@sjd.es"
    client = app.test_client()
    ppt_id = appointment_finput["inputId"]
    response = client.post(
        f"/participants/{ppt_id}/appointment_new", data=appointment_finput
    )
    assert response.status_code == 302

    # check that email has been sent
    time.sleep(20)
    email = tutils.check_email_received()
    assert email
    assert f"Appointment {ppt_id}:" in email["subject"]

    # check that event has been created
    event = tutils.check_event_created(ppt_id=ppt_id)
    assert event
    assert ppt_id in event["subject"]


def test_apt_mod(client, appointment_finput_mod):
    """Test apt_all endpoint."""
    ppt_id = appointment_finput_mod["inputId"]
    apt_id = appointment_finput_mod["inputAptId"]
    response = client.get(f"/participants/{ppt_id}/{apt_id}/appointment_modify")
    assert response.status_code == 200


def test_apt_mod_post(client, appointment_finput_mod):
    """Test apt_all endpoint."""
    ppt_id = appointment_finput_mod["inputId"]
    apt_id = appointment_finput_mod["inputAptId"]
    response = client.post(
        f"/participants/{ppt_id}/{apt_id}/appointment_modify",
        data=appointment_finput_mod,
    )
    assert response.status_code == 302


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_apt_mod_post_email(app, appointment_finput_mod):
    """Test apt_post endpoint with email."""
    app.config["EMAIL"] = "gonzalo.garcia@sjd.es"
    client = app.test_client()
    ppt_id = appointment_finput_mod["inputId"]
    apt_id = appointment_finput_mod["inputAptId"]
    response = client.post(
        f"/participants/{ppt_id}/{apt_id}/appointment_modify",
        data=appointment_finput_mod,
    )
    assert response.status_code == 302

    # check that email has been sent
    time.sleep(20)
    email = tutils.check_email_received()
    assert email
    assert f"Appointment {ppt_id}:" in email["subject"]

    # check that event has been created
    event = tutils.check_event_created(ppt_id=ppt_id)
    assert event
    assert ppt_id in event["subject"]
