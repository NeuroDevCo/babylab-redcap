"""Test questionnaires endpoints."""


def test_ques_all(client):
    """Test que_all endpoint."""
    response = client.get("/questionnaires/")
    assert response.status_code == 200


def test_que(client):
    """Test que endpoint."""
    response = client.get("/participants/1/questionnaires/1:1")
    assert response.status_code == 200


def test_que_new(client):
    """Test que_new endpoint."""
    response = client.get("/participants/1/questionnaires/questionnaire_new")
    assert response.status_code == 200


def test_que_new_post(client, questionnaire_finput):
    """Test que_new endpoint."""
    response = client.post(
        "/participants/1/questionnaires/questionnaire_new", data=questionnaire_finput
    )
    assert response.status_code == 302


def test_que_mod(client, questionnaire_finput_mod):
    """Test que_mod endpoint."""
    ppt_id = questionnaire_finput_mod["inputId"]
    que_id = questionnaire_finput_mod["inputQueId"]
    response = client.get(
        f"/participants/{ppt_id}/questionnaires/{que_id}/questionnaire_modify"
    )
    assert response.status_code == 200


def test_que_mod_post(client, questionnaire_finput_mod):
    """Test que_mod endpoint."""
    ppt_id = questionnaire_finput_mod["inputId"]
    que_id = questionnaire_finput_mod["inputQueId"]
    response = client.post(
        f"/participants/{ppt_id}/questionnaires/{que_id}/questionnaire_modify",
        data=questionnaire_finput_mod,
    )
    assert response.status_code == 302
