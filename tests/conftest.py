"""
Fixtures for testing
"""

from string import digits, ascii_lowercase
from random import choice, choices
import datetime
import pytest
from babylab.src import api
from babylab.app import create_app
from babylab.app import config as conf


@pytest.fixture
def app():
    """App factory for testing."""
    yield create_app(env="test")


@pytest.fixture
def client(app):  # pylint: disable=redefined-outer-name
    """Testing client."""
    return app.test_client()


@pytest.fixture
def token():
    """API test token.

    Returns:
        str: API test token.
    """
    return conf.get_api_key()


@pytest.fixture
def records():
    """REDCap records database."""
    return api.Records(token=conf.get_api_key())


def generate_str(n: str = 7) -> str:
    """Generate random string of ASCII characters.

    Args:
        nchar (str, optional): Number of characters in the string. Defaults to 7.

    Returns:
        str: Random string of characters of length ``n``.
    """
    return "".join(choices(ascii_lowercase + digits, k=n))


def generate_phone() -> str:
    """Generate random phone number (no prefix).

    Returns:
        str: Random phone number.
    """
    return "".join([str(x) for x in choices(range(9), k=9)])


def generate_email() -> str:
    """Generate random e-mail address.

    Returns:
        str: Random e-mail address.
    """
    return generate_str() + "@" + generate_str() + ".com"


def generate_lang_exp():
    """Create vector of language exposures.

    Returns:
        list[float]: Vector of language exposures that adds up to 100.
    """
    nlangs = choice(range(1, 4))
    exp = [0] * 4
    for l in range(1, nlangs):
        exp[l] = choice(range(100 - sum(exp)))
    exp[-1] = 100 - sum(exp[:-1])
    exp.sort(reverse=True)
    return exp


def get_data_dict() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return api.get_data_dict(token=conf.get_api_key())


def create_finput_participant(is_new: bool = True) -> dict:
    """Simulate form input to test POST request in participants.

    Args:
        is_new (bool, optional): Should a new record be created? Defaults to True.

    Returns:
        dict: Simulated form input.
    """
    data = {
        "record_id": "new" if is_new else "1",
        "inputName": generate_str(),
        "inputParent1Name": generate_str(),
        "inputSex": choice(range(1, 6)),
        "inputParent1Surname": generate_str(),
        "inputParent2Name": generate_str(),
        "inputParent2Surname": generate_str(),
        "inputAgeMonths": choice(range(12)),
        "inputAgeDays": choice(range(31)),
        "inputNormalHearing": choice(["1", "2"]),
        "inputTwinID": "",
        "inputComments": " ".join([generate_str(25) for _ in range(3)]),
        "inputEmail1": generate_email(),
        "inputPhone1": generate_phone(),
        "inputEmail2": generate_email(),
        "inputPhone2": generate_phone(),
        "inputAddress": generate_str(),
        "inputCity": generate_str(),
        "inputPostcode": "".join([str(x) for x in choices(range(9), k=5)]),
        "inputBirthWeight": choice(range(2700, 4500)),
        "inputDeliveryType": choice(["1", "2"]),
        "inputGestationalWeeks": choice(range(34, 43)),
        "inputHeadCircumference": choice(range(32, 38)),
        "inputApgar1": choice(range(10)),
        "inputApgar2": choice(range(10)),
        "inputApgar3": choice(range(10)),
        "inputDiagnoses": generate_str(50),
    }
    data = {k: str(v) for k, v in data.items()}
    return data


def create_finput_appointment(is_new: bool = True) -> dict:
    """Simulate form input to test POST request in appointments.

    Args:
        is_new (bool, optional): Should a new record be created? Defaults to True.

    Returns:
        dict: Simulated form input.
    """
    recs = api.Records(token=conf.get_api_key())
    data_dict = api.get_data_dict(token=conf.get_api_key())
    ppt_id = choice(list(recs.participants.records.keys()))
    apt_choices = list(recs.participants.records[ppt_id].appointments.records.keys())
    if apt_choices:
        apt_id = choice(apt_choices)
    else:
        ppt_id = "1"
        apt_id = "1:1"
    data = {
        "inputId": ppt_id,
        "inputAptId": "new" if is_new else apt_id,
        "inputStudy": choice(list(data_dict["appointment_study"].keys())),
        "inputStatus": choice(list(data_dict["appointment_status"].keys())),
        "inputDate": "2024-12-31T14:09",
        "inputTaxiAddress": generate_str(),
        "inputComments": ". ".join([generate_str(25) for _ in range(3)]),
    }
    data = {k: str(v) for k, v in data.items()}
    return data


def create_finput_questionnaire(is_new: bool = True) -> dict:
    """Simulate form input to test POST request in questionnaires.

    Args:
        is_new (bool, optional): Should a new record be created? Defaults to True.

    Returns:
        dict: Simulated form input.
    """
    recs = api.Records(token=conf.get_api_key())
    data_dict = api.get_data_dict(token=conf.get_api_key())
    lang_exp = generate_lang_exp()
    ppt_id = choice(list(recs.participants.records.keys()))
    que_choices = list(recs.participants.records[ppt_id].questionnaires.records.keys())

    if que_choices:
        que_id = choice(que_choices)
    else:
        ppt_id = "1"
        que_id = "1:1"

    data = {
        "inputId": ppt_id,
        "inputQueId": "new" if is_new else que_id,
        "inputIsEstimated": choice(["0", "1"]),
        "inputLang1": choice(list(data_dict["language_lang1"].keys())),
        "inputLang1Exp": lang_exp[0],
        "inputLang2": choice(list(data_dict["language_lang1"].keys())),
        "inputLang2Exp": lang_exp[1],
        "inputLang3": choice(list(data_dict["language_lang1"].keys())),
        "inputLang3Exp": lang_exp[2],
        "inputLang4": choice(list(data_dict["language_lang1"].keys())),
        "inputLang4Exp": lang_exp[3],
        "inputComments": ". ".join([generate_str(25) for _ in range(3)]),
    }

    data = {k: str(v) for k, v in data.items()}
    return data


def create_record_participant(is_new: bool = True) -> dict:
    """Create a REDCap participant record.

    Args:
        is_new (bool): Should a new record be created? Defaults to True.

    Returns:
        dict: A REDCap record.
    """
    recs = api.Records(token=conf.get_api_key())
    ppt_id = choice(list(recs.participants.records.keys()))
    return {
        "record_id": "0" if is_new else ppt_id,
        "participant_date_created": datetime.datetime.strptime(
            "2024-12-16 11:13:00", "%Y-%m-%d %H:%M:%S"
        ),
        "participant_date_updated": datetime.datetime.strptime(
            "2024-12-16 11:13:00", "%Y-%m-%d %H:%M:%S"
        ),
        "participant_name": generate_str(),
        "participant_age_now_months": choice(range(12)),
        "participant_age_now_days": choice(range(31)),
        "participant_days_since_last_appointment": "",
        "participant_sex": str(choice(range(1, 6))),
        "participant_twin": "",
        "participant_parent1_name": generate_str(),
        "participant_parent1_surname": generate_str(),
        "participant_email1": generate_email(),
        "participant_phone1": generate_phone(),
        "participant_parent2_name": generate_str(),
        "participant_parent2_surname": generate_str(),
        "participant_email2": generate_email(),
        "participant_phone2": generate_str(),
        "participant_address": generate_str(),
        "participant_city": generate_str(),
        "participant_postcode": "".join([str(x) for x in choices(range(9), k=5)]),
        "participant_birth_type": choice(["1", "2"]),
        "participant_gest_weeks": str(choice(range(34, 43))),
        "participant_birth_weight": str(choice(range(2700, 4500))),
        "participant_head_circumference": str(choice(range(32, 38))),
        "participant_apgar1": str(choice(range(10))),
        "participant_apgar2": str(choice(range(10))),
        "participant_apgar3": str(choice(range(10))),
        "participant_hearing": choice(["1", "2"]),
        "participant_diagnoses": generate_str(50),
        "participant_comments": " ".join([generate_str(25) for _ in range(3)]),
        "participants_complete": "2",
    }


def create_record_appointment(is_new: bool = True) -> dict:
    """Create a REDCap appointment record.

    Args:
        is_new (bool): Should a new record be created? Defaults to True.

    Returns:
        dict: A REDCap record.
    """
    data_dict = get_data_dict()
    recs = api.Records(token=conf.get_api_key())
    ppt_id = choice(list(recs.participants.records.keys()))
    apt_choices = list(recs.participants.records[ppt_id].appointments.records.keys())
    if apt_choices:
        apt_id = choice(apt_choices)
    else:
        ppt_id = "1"
        apt_id = "1:1"

    return {
        "record_id": ppt_id,
        "redcap_repeat_instrument": "appointments",
        "redcap_repeat_instance": "new" if is_new else apt_id.split(":")[1],
        "appointment_study": choice(list(data_dict["appointment_study"].keys())),
        "appointment_date_created": datetime.datetime.strptime(
            "2024-12-12 14:09:00", "%Y-%m-%d %H:%M:%S"
        ),
        "appointment_date_updated": datetime.datetime.strptime(
            "2024-12-14 12:08:00", "%Y-%m-%d %H:%M:%S"
        ),
        "appointment_date": datetime.datetime.strptime(
            "2024-12-31 14:09", "%Y-%m-%d %H:%M"
        ),
        "appointment_taxi_address": generate_str(),
        "appointment_taxi_isbooked": choice(["0", "1"]),
        "appointment_status": choice(list(data_dict["appointment_status"].keys())),
        "appointment_comments": ". ".join([generate_str(25) for _ in range(3)]),
        "appointments_complete": "2",
    }


def create_record_questionnaire(is_new: bool = True) -> dict:
    """Create a REDCap questionnaire record.

    Args:
        is_new (bool): Should a new record be created? Defaults to True.

    Returns:
        dict: A REDCap record.
    """
    data_dict = get_data_dict()
    recs = api.Records(token=conf.get_api_key())
    ppt_id = choice(list(recs.participants.records.keys()))
    lang_exp = generate_lang_exp()
    que_choices = list(recs.participants.records[ppt_id].questionnaires.records.keys())

    if que_choices:
        que_id = choice(que_choices)
    else:
        ppt_id = "1"
        que_id = "1:1"

    return {
        "record_id": ppt_id,
        "redcap_repeat_instrument": "language",
        "redcap_repeat_instance": "new" if is_new else que_id.split(":")[1],
        "language_date_created": datetime.datetime.strptime(
            "2024-12-12 14:24:00", "%Y-%m-%d %H:%M:%S"
        ),
        "language_date_updated": datetime.datetime.strptime(
            "2024-12-12 14:24:00", "%Y-%m-%d %H:%M:%S"
        ),
        "language_isestimated": choice(["0", "1"]),
        "language_lang1": choice(list(data_dict["language_lang1"].keys())),
        "language_lang1_exp": lang_exp[0],
        "language_lang2": choice(list(data_dict["language_lang2"].keys())),
        "language_lang2_exp": lang_exp[1],
        "language_lang3": choice(list(data_dict["language_lang3"].keys())),
        "language_lang3_exp": lang_exp[2],
        "language_lang4": choice(list(data_dict["language_lang4"].keys())),
        "language_lang4_exp": lang_exp[3],
        "language_comments": "",
        "language_complete": "2",
    }


@pytest.fixture
def participant_finput() -> dict:
    """Form input for participant."""
    return create_finput_participant()


@pytest.fixture
def participant_finput_mod() -> dict:
    """Form input for participant."""
    return create_finput_participant(is_new=False)


@pytest.fixture
def appointment_finput() -> dict:
    """Form input for appointment."""
    return create_finput_appointment()


@pytest.fixture
def appointment_finput_mod() -> dict:
    """Form input for appointment."""
    return create_finput_appointment(is_new=False)


@pytest.fixture
def questionnaire_finput() -> dict:
    """Form input for questionnaire."""
    return create_finput_questionnaire()


@pytest.fixture
def questionnaire_finput_mod() -> dict:
    """Form input for questionnaire."""
    return create_finput_questionnaire(is_new=False)


@pytest.fixture
def participant_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return create_record_participant()


@pytest.fixture
def participant_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return create_record_participant(is_new=False)


@pytest.fixture
def appointment_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return create_record_appointment()


@pytest.fixture
def appointment_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDcap record fixture.
    """
    return create_record_appointment(is_new=False)


@pytest.fixture
def questionnaire_record() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDCap record fixture.
    """
    return create_record_questionnaire()


@pytest.fixture
def questionnaire_record_mod() -> dict:
    """Create REDcap record fixture.

    Returns:
        dict: A REDCap record fixture.
    """
    return create_record_questionnaire(is_new=False)
