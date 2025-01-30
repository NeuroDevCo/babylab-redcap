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


def test_apt(client, apt_record_mod):
    """Test apt_all endpoint."""
    apt_id = (
        apt_record_mod["record_id"] + ":" + apt_record_mod["redcap_repeat_instance"]
    )
    response = client.get("/appointments/" + apt_id)
    assert response.status_code == 200


def test_apt_new(client, apt_finput):
    """Test apt_new endpoint."""
    ppt_id = apt_finput["inputId"]
    response = client.get(f"/appointments/appointment_new?ppt_id={ppt_id}")
    assert response.status_code == 200


def test_apt_new_post(client, apt_finput):
    """Test apt_new endpoint."""
    ppt_id = apt_finput["inputId"]
    url = f"/appointments/appointment_new?ppt_id={ppt_id}"
    response = client.post(url, data=apt_finput)
    assert response.status_code == 302


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_apt_new_post_email(app, apt_finput):
    """Test apt_new endpoint with email."""
    app.config["EMAIL"] = "gonzalo.garcia@sjd.es"
    ppt_id = apt_finput["inputId"]
    with app.test_client() as client:
        url = f"/appointments/appointment_new?ppt_id={ppt_id}"
        response = client.post(url, data=apt_finput)
        assert response.status_code == 302

    # check that email has been sent
    time.sleep(20)
    email = tutils.check_email_received()
    assert email
    assert f"{ppt_id}:" in email["subject"]

    # check that event has been created
    event = tutils.check_event_created(ppt_id=ppt_id)
    assert event
    assert f"{ppt_id}:" in event["subject"]


def test_apt_mod(client, apt_finput_mod):
    """Test apt_all endpoint."""
    apt_id = apt_finput_mod["inputAptId"]
    url = f"/appointments/{apt_id}/appointment_modify"
    response = client.get(url)
    assert response.status_code == 200


def test_apt_mod_post(client, apt_finput_mod):
    """Test apt_all endpoint."""
    apt_id = apt_finput_mod["inputAptId"]
    url = f"/appointments/{apt_id}/appointment_modify"
    response = client.post(url, data=apt_finput_mod)
    assert response.status_code == 302


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Test doesn't work in Github Actions.")
def test_apt_mod_post_email(app, apt_finput_mod):
    """Test apt_post endpoint with email."""
    app.config["EMAIL"] = "gonzalo.garcia@sjd.es"
    apt_id = apt_finput_mod["inputAptId"]
    url = f"/appointments/{apt_id}/appointment_modify"
    with app.test_client() as client:
        response = client.post(url, data=apt_finput_mod)
    assert response.status_code == 302

    # check that email has been sent
    time.sleep(20)
    email = tutils.check_email_received()
    assert email
    assert f"{apt_id}" in email["subject"]

    # check that event has been created
    ppt_id = apt_id.split(":")[0]
    event = tutils.check_event_created(ppt_id=ppt_id)
    assert event
    assert ppt_id in event["subject"]
