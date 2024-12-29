"""Test appointments endpoints."""


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
