"""Test API."""

import os
from datetime import datetime
import pytest
from babylab.src import api

IS_GIHTUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def test_post_request(token):
    """Test ``post_request``."""
    assert api.post_request(
        fields={
            "content": "version",
        },
        token=token,
    ).ok


def test_redcap_version(token):
    """Test ``redcap_version``."""
    version = api.get_redcap_version(token=token)
    assert version
    assert isinstance(version, str)
    assert len(version.split(".")) == 3
    with pytest.raises(TypeError):
        api.get_redcap_version()
    with pytest.raises(TypeError):
        api.get_redcap_version(token)  # pylint: disable=too-many-function-args
    assert not api.get_redcap_version(token="wrongtoken")
    assert not api.get_redcap_version(token="bad#token")


def test_datetimes_to_str():
    """Test ``test_datetimes_to_str`` function."""
    data = {
        "date_now": datetime(2024, 10, 24, 8, 48, 34, 685496),
        "date_today": datetime(2024, 10, 24, 8, 48),
        "date_str": "2024-05-12T5:12",
    }
    result = api.datetimes_to_strings(data)
    assert result["date_now"] == "2024-10-24T08:48:34.685496"
    assert result["date_today"] == "2024-10-24T08:48:00"
    assert result["date_str"] == data["date_str"]


def test_strings_to_datetimes():
    """Test ``test_datetimes_to_str`` function."""
    data = {
        "date_now": "2024-05-12 05:34:15",
        "date_today": "2024-05-12 05:34",
    }
    result = api.strings_to_datetimes(data)
    assert result["date_now"] == datetime(2024, 5, 12, 5, 34, 15)
    assert result["date_today"] == datetime(2024, 5, 12, 5, 34)


def test_get_data_dict(benchmark, token):
    """Test ``get_records``."""
    data_dict = api.get_data_dict(token=token)

    assert isinstance(data_dict, dict)
    assert all(isinstance(v, dict) for v in data_dict.values())
    with pytest.raises(TypeError):
        api.get_data_dict()

    def _get_data_dict():
        api.get_data_dict(token=token)

    benchmark(_get_data_dict)


def test_make_id():
    """Test ``make_id``"""
    assert api.make_id(1, 2) == "1:2"
    assert api.make_id(1) == "1"
    assert api.make_id("1", "2") == "1:2"
    assert api.make_id("1") == "1"
    with pytest.raises(ValueError):
        api.make_id(1, "a")
    with pytest.raises(ValueError):
        api.make_id(1, "1 ")
    with pytest.raises(ValueError):
        api.make_id("a")
    with pytest.raises(ValueError):
        api.make_id("1 ")
    with pytest.raises(ValueError):
        api.make_id("1:1")


def test_get_participant(benchmark, ppt_record_mod, token):
    """Test ``get_participant``."""
    ppt_id = ppt_record_mod["record_id"]
    ppt = api.get_participant(ppt_id, token=token)

    assert isinstance(ppt, api.Participant)
    with pytest.raises(api.RecordNotFound):
        api.get_participant("BADID", token=token)

    def _get_participant():
        api.get_participant(ppt_id, token=token)

    benchmark(_get_participant)


def test_get_appointment(benchmark, apt_record_mod, token):
    """Test ``get_participant``."""
    ppt_id = apt_record_mod["record_id"]
    repeat_id = apt_record_mod["redcap_repeat_instance"]
    apt_id = api.make_id(ppt_id, repeat_id)
    apt = api.get_appointment(apt_id, token=token)
    assert isinstance(apt, api.Appointment)
    with pytest.raises(api.RecordNotFound):
        api.get_appointment("f{ppt_id}:BADID", token=token)

    def _get_appointment():
        api.get_appointment(apt_id, token=token)

    benchmark(_get_appointment)


def test_get_questionnaire(benchmark, que_record_mod, token):
    """Test ``get_participant``."""
    ppt_id = que_record_mod["record_id"]
    repeat_id = que_record_mod["redcap_repeat_instance"]
    que_id = api.make_id(ppt_id, repeat_id)
    que = api.get_questionnaire(que_id, token=token)
    assert isinstance(que, api.Questionnaire)
    with pytest.raises(api.RecordNotFound):
        api.get_questionnaire("f{que_id}:BADID", token=token)

    def _get_questionnaire():
        api.get_questionnaire(que_id, token=token)

    benchmark(_get_questionnaire)


def test_get_records(benchmark, token):
    """Test ``get_records``."""
    records = api.get_records(token=token)
    assert isinstance(records, list)
    assert all(isinstance(r, dict) for r in records)
    with pytest.raises(TypeError):
        api.get_records()

    def _get_records():
        api.get_records(token=token)

    benchmark(_get_records)


def test_add_participant(ppt_record, token):
    """Test ``add_participant``."""
    api.add_participant(ppt_record, token=token)
    with pytest.raises(TypeError):
        api.add_participant(ppt_record)


def test_add_participant_modifying(ppt_record_mod, token):
    """Test ``add_participant`` with ``modifying=True``."""
    api.add_participant(ppt_record_mod, token=token)
    with pytest.raises(TypeError):
        api.add_participant(ppt_record_mod)


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Only local testing")
def test_delete_participant(ppt_record_mod, token):
    """Test ``add_participant``."""
    api.delete_participant(ppt_record_mod, token=token)
    recs = api.Records(token=token)
    assert ppt_record_mod["record_id"] not in recs.appointments.records
    api.delete_participant(ppt_record_mod, token=token)
    with pytest.raises(TypeError):
        api.delete_participant(ppt_record_mod)


def test_add_appointment(apt_record, token):
    """Test ``add_appointment`` ."""
    api.add_appointment(apt_record, token=token)
    with pytest.raises(TypeError):
        api.add_appointment(apt_record)


def test_add_appointment_modifying(apt_record_mod, token):
    """Test ``add_appointment`` with ``modifying=True``."""
    api.add_appointment(apt_record_mod, token=token)
    with pytest.raises(TypeError):
        api.add_participant(apt_record_mod)


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Only local testing")
def test_delete_appointment(apt_record_mod, token):
    """Test ``add_appointment`` ."""
    apt_id = api.make_id(
        apt_record_mod["record_id"], apt_record_mod["redcap_repeat_instance"]
    )
    api.delete_appointment(apt_record_mod, token=token)
    recs = api.Records(token=token)
    assert apt_id not in recs.appointments.records
    with pytest.raises(TypeError):
        api.delete_appointment(apt_record_mod)


def test_add_questionnaire(que_record, token):
    """Test ``add_appointment``."""
    api.add_questionnaire(que_record, token=token)
    with pytest.raises(TypeError):
        api.add_questionnaire(que_record)


def test_add_questionnaire_mod(que_record_mod, token):
    """Test ``add_questionaire`` with ``modifying=True``."""
    api.add_questionnaire(que_record_mod, token=token)
    with pytest.raises(TypeError):
        api.add_questionnaire(que_record_mod)


@pytest.mark.skipif(IS_GIHTUB_ACTIONS, reason="Only local testing")
def test_delete_questionnaire(que_record_mod, token):
    """Test ``delete_questionnaire``."""
    que_id = api.make_id(
        que_record_mod["record_id"], que_record_mod["redcap_repeat_instance"]
    )
    api.delete_questionnaire(que_record_mod, token=token)
    recs = api.Records(token=token)
    assert que_id not in recs.questionnaires.records
    with pytest.raises(TypeError):
        api.delete_questionnaire(que_record_mod)


def test_redcap_backup(benchmark, token, tmp_path) -> dict:
    """Test ``redcap_backup``."""
    tmp_dir = tmp_path / "tmp"
    file = api.redcap_backup(dirpath=tmp_dir, token=token)
    assert os.path.exists(file)
    with pytest.raises(TypeError):
        api.redcap_backup(dirpath=tmp_dir)

    def _redcap_backup():
        api.redcap_backup(dirpath=tmp_dir, token=token)

    benchmark(_redcap_backup)


def get_next_id(benchmark, token, records: api.Records = None) -> str:
    """Test ``get_next_id``."""
    if records is None:
        records = api.Records(token=token)
    next_id = api.get_next_id(token=token)
    assert next_id not in list(records.participants.records.keys())

    def _get_next_id():
        api.get_next_id(token=token)

    benchmark(_get_next_id)
