"""Test appointments endpoints."""

from babylab.src import api


def test_apt_all(client):
    """Test apt_all endpoint."""
    response = client.get("/appointments/")
    assert response.status_code == 200


def test_apt(client, apt_record_mod):
    """Test apt_all endpoint."""
    apt_id = api.make_id(
        apt_record_mod["record_id"], apt_record_mod["redcap_repeat_instance"]
    )
    response = client.get("/appointments/" + apt_id)
    assert response.status_code == 200


def test_apt_new(client, apt_finput):
    """Test apt_new endpoint."""
    ppt_id = apt_finput["inputId"]
    response = client.get(f"/appointments/appointment_new?ppt_id={ppt_id}")
    assert response.status_code == 200


def test_apt_new_post(client, apt_finput, token):
    """Test apt_new endpoint."""
    ppt_id = apt_finput["inputId"]
    ppt = api.get_participant(ppt_id, token=token)
    apt_ids = list(ppt.appointments.records.keys())
    last_apt_id = apt_ids[-1].split(":")[1]
    next_apt_id = str(int(last_apt_id) + 1)
    assert api.make_id(ppt_id, next_apt_id) not in apt_ids
    url = f"/appointments/appointment_new?ppt_id={ppt_id}"
    response = client.post(url, data=apt_finput)
    assert response.status_code == 302
    ppt = api.get_participant(ppt_id, token=token)
    apt_ids = list(ppt.appointments.records.keys())
    last_apt_id = apt_ids[-1].split(":")[1]
    assert api.make_id(ppt_id, last_apt_id) in apt_ids


def test_apt_mod(client, apt_finput_mod):
    """Test apt_all endpoint."""
    apt_id = apt_finput_mod["inputAptId"]
    url = f"/appointments/{apt_id}/appointment_modify"
    response = client.get(url)
    assert response.status_code == 200


def test_apt_mod_post(client, apt_finput_mod, token):
    """Test apt_all endpoint."""
    apt_id = apt_finput_mod["inputAptId"]
    apt = api.get_appointment(apt_id, token=token)

    url = f"/appointments/{apt_id}/appointment_modify"
    response = client.post(url, data=apt_finput_mod)
    assert response.status_code == 302
    new_apt = api.get_appointment(apt_id, token=token)
    assert new_apt.data != apt.data
