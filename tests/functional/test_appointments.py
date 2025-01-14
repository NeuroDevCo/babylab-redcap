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


def test_apt(client):
    """Test apt_all endpoint."""
    response = client.get("/appointments/1:1")
    assert response.status_code == 200


def test_apt_new(client):
    """Test apt_new endpoint."""
    response = client.get("/participants/1/appointment_new")
    assert response.status_code == 200


def test_apt_new_post(client, appointment_finput):
    """Test apt_new endpoint."""
    response = client.post("/participants/1/appointment_new", data=appointment_finput)
    assert response.status_code == 302


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_apt_new_post_email(app, appointment_finput):
    """Test apt_new endpoint with email."""
    app.config["EMAIL"] = "gonzalo.garcia@sjd.es"
    client = app.test_client()
    response = client.post("/participants/1/appointment_new", data=appointment_finput)
    assert response.status_code == 302

    # check that email has been sent
    time.sleep(20)
    email = tutils.check_email_received()
    assert email
    assert "Appointment 1:" in email["subject"]

    # check that event has been created
    event = tutils.check_event_created(apt_id="1:1")
    assert event
    assert "1:1" in event["subject"]


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
    assert "Appointment 1:" in email["subject"]

    # check that event has been created
    event = tutils.check_event_created(apt_id=apt_id)
    assert event
    assert apt_id in event["subject"]
