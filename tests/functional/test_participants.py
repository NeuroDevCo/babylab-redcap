"""Test participants endpoints."""


def test_ppt_all(client):
    """Test ppt_all endpoint."""
    response = client.get("/participants/")
    assert response.status_code == 200


def test_ppt_all_post(client):
    """Test ppt_all endpoint."""
    response = client.post("/participants/", data={"inputPptId": "1"})
    assert response.status_code == 200


def test_ppt(client):
    """Test ppt_all endpoint."""
    response = client.get("/participants/1")
    assert response.status_code == 200


def test_ppt_new(client):
    """Test ppt_all endpoint."""
    response = client.get("/participant_new")
    assert response.status_code == 200


def test_ppt_new_post(client, participant_finput):
    """Test ppt_all endpoint."""

    response = client.post("/participant_new", data=participant_finput)
    assert response.status_code == 302


def test_ppt_mod(client, participant_finput_mod):
    """Test ppt_all endpoint."""
    response = client.get(
        f"participants/{participant_finput_mod['record_id']}/participant_modify"
    )
    assert response.status_code == 200


def test_ppt_mod_post(client, participant_finput_mod):
    """Test ppt_all endpoint."""

    response = client.post(
        f"/participants/{participant_finput_mod['record_id']}/participant_modify",
        data=participant_finput_mod,
    )
    assert response.status_code == 302
