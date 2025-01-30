"""Test questionnaires endpoints."""


def test_ques_all(client):
    """Test que_all endpoint."""
    response = client.get("/questionnaires/")
    assert response.status_code == 200


def test_que(client, que_record_mod):
    """Test que endpoint."""
    ppt_id = que_record_mod["record_id"]
    que_id = ppt_id + ":" + que_record_mod["redcap_repeat_instance"]
    response = client.get(f"/questionnaires/{que_id}")
    assert response.status_code == 200


def test_que_new(client, que_finput):
    """Test que_new endpoint."""
    ppt_id = que_finput["inputId"]
    response = client.get(f"/questionnaires/questionnaire_new?ppt_id={ppt_id}")
    assert response.status_code == 200


def test_que_new_post(client, que_finput):
    """Test que_new endpoint."""
    ppt_id = que_finput["inputId"]
    url = f"/questionnaires/questionnaire_new?ppt_id={ppt_id}"
    response = client.post(url, data=que_finput)
    assert response.status_code == 302


def test_que_mod(client, que_finput_mod):
    """Test que_mod endpoint."""
    que_id = que_finput_mod["inputQueId"]
    response = client.get(f"/questionnaires/{que_id}/questionnaire_modify")
    assert response.status_code == 200


def test_que_mod_post(client, que_finput_mod):
    """Test que_mod endpoint."""
    que_id = que_finput_mod["inputQueId"]
    url = f"/questionnaires/{que_id}/questionnaire_modify"
    response = client.post(url, data=que_finput_mod)
    assert response.status_code == 302
