"""Test questionnaires endpoints."""

from babylab.src import api


def test_ques_all(client):
    """Test que_all endpoint."""
    response = client.get("/questionnaires/")
    assert response.status_code == 200


def test_que(client, que_record_mod):
    """Test que endpoint."""
    ppt_id = que_record_mod["record_id"]
    que_id = api.make_id(ppt_id, que_record_mod["redcap_repeat_instance"])
    response = client.get(f"/questionnaires/{que_id}")
    assert response.status_code == 200


def test_que_new(client, que_finput):
    """Test que_new endpoint."""
    ppt_id = que_finput["inputId"]
    response = client.get(f"/questionnaires/questionnaire_new?ppt_id={ppt_id}")
    assert response.status_code == 200


def test_que_new_post(client, que_finput, token_fixture):
    """Test que_new endpoint."""
    ppt_id = que_finput["inputId"]
    ppt = api.get_participant(ppt_id, token=token_fixture)
    que_ids = list(ppt.questionnaires.records.keys())
    last_que_id = que_ids[-1].split(":")[1]
    next_que_id = str(int(last_que_id) + 1)
    assert api.make_id(ppt_id, next_que_id) not in que_ids
    url = f"/questionnaires/questionnaire_new?ppt_id={ppt_id}"
    response = client.post(url, data=que_finput)
    assert response.status_code == 302
    ppt = api.get_participant(ppt_id, token=token_fixture)
    que_ids = list(ppt.questionnaires.records.keys())
    last_que_id = que_ids[-1].split(":")[1]
    assert api.make_id(ppt_id, last_que_id) in que_ids


def test_que_mod(client, que_finput_mod):
    """Test que_mod endpoint."""
    que_id = que_finput_mod["inputQueId"]
    response = client.get(f"/questionnaires/{que_id}/questionnaire_modify")
    assert response.status_code == 200


def test_que_mod_post(client, que_finput_mod, token_fixture):
    """Test que_mod endpoint."""
    que_id = que_finput_mod["inputQueId"]
    que = api.get_questionnaire(que_id, token=token_fixture)

    url = f"/questionnaires/{que_id}/questionnaire_modify"
    response = client.post(url, data=que_finput_mod)
    assert response.status_code == 302

    new_que = api.get_questionnaire(que_id, token=token_fixture)
    assert new_que.data != que.data
