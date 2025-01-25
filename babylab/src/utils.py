"""
Util functions for the app.
"""

import os
import datetime
import shutil
from pandas import DataFrame
from flask import flash, render_template
from babylab.src import api

if os.name == "nt":
    from babylab.src import outlook


def format_ppt_id(ppt_id: str) -> str:
    """Format appointment ID.

    Args:
        ppt_id (str): Participant ID.

    Returns:
        str: Formated participant ID.
    """
    return f"<a href=/participants/{ppt_id}>{ppt_id}</a>"


def format_apt_id(apt_id: str) -> str:
    """Format appointment ID.

    Args:
        apt_id (str): Appointment ID.

    Returns:
        str: Formated appointment ID.
    """
    return f"<a href=/appointments/{apt_id}>{apt_id}</a>"


def format_que_id(que_id: str, ppt_id: str) -> str:
    """Format questionnaire ID.

    Args:
        apt_id (str): Questionnaire ID.
        ppt_id (str): Participant ID.

    Returns:
        str: Formated questionnaire ID.
    """
    return f"<a href=/participants/{ppt_id}/questionnaires/{que_id}>{que_id}</a>"


def format_isestimated(isestimated: str) -> str:
    """Format ``isestimated`` variable.

    Args:
        isestimated (str): Value of ``isestimated`` variable.

    Returns:
        str: Formatted ``isestimated`` value.
    """
    return "Estimated" if isestimated == "1" else "Calculated"


def format_percentage(x: float | int) -> str:
    """Format number into percentage.

    Args:
        x (float | int): Number to format. Must be higher than or equal to zero, and lower than or equal to one.

    Raises:
        ValueError: If number is not higher than or equal to zero, and lower than or equal to one.

    Returns:
        str: Formatted percentage.
    """  # pylint: disable=line-too-long
    if x > 100 or x < 0:
        raise ValueError(
            "`x` higher than or equal to zero, and lower than or equal to one"
        )
    return str(int(float(x))) if x else ""


def format_taxi_isbooked(address: str, isbooked: str) -> str:
    """Format ``taxi_isbooked`` variable to HTML.

    Args:
        address (str): ``taxi_address`` value.
        isbooked (str): ``taxi_isbooked`` value.

    Raises:
        ValueError: If ``isbooked`` is not "0" or "1".

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    if isbooked not in ["0", "1"]:
        raise ValueError("`is_booked` must be one of '0' or '1'")
    if not address:
        return ""
    if int(isbooked):
        return "<p style='color: green;'>Yes</p>"
    return "<p style='color: red;'>No</p>"


def format_modify_button(ppt_id: str, apt_id: str = None, ques_id: str = None):
    """Add modify button.

    Args:
        ppt_id (str): Participant ID.
        apt_id (str, optional): Appointment ID. Defaults to None.
        ques_id (str, optional): Questionnaire ID. Defaults to None.

    Returns:
        str: Formatted HTML string.
    """  # pylint: disable=line-too-long
    if apt_id:
        return f'<a href="/participants/{ppt_id}/{apt_id}/appointment_modify"><button type="button" class="btn btn-warning">Modify</button></a>'  # pylint: disable=line-too-long

    if ques_id:
        return f'<a href="/participants/{ppt_id}/questionnaires/{ques_id}/questionnaire_modify"><button type="button" class="btn btn-warning">Modify</button></a>'  # pylint: disable=line-too-long

    return f'<a href="/participants/{ppt_id}/participant_modify"><button type="button" class="btn btn-warning">Modify</button></a>'  # pylint: disable=line-too-long


def format_df(
    x: DataFrame,
    data_dict: dict,
    prefixes: list[str] = None,
) -> DataFrame:
    """Reformat dataframe.

    Args:
        x (DataFrame): Dataframe to reformat.
        data_dict (dict): Data dictionary to labels to use, as returned by ``api.get_data_dict``.
        prefixes (list[str]): List of prefixes to look for in variable names.

    Returns:
        DataFrame: A reformated Dataframe.
    """
    if prefixes is None:
        prefixes = ["participant", "appointment", "language"]
    for col_name, col_values in x.items():
        kdict = [x + "_" + col_name for x in prefixes]
        for k in kdict:
            if k in data_dict:
                x[col_name] = [data_dict[k][v] if v else "" for v in col_values]
        if "lang" in col_name:
            x[col_name] = ["" if v == "None" else v for v in x[col_name]]
        if "exp" in col_name:
            x[col_name] = [format_percentage(v) for v in col_values]
        if "taxi_isbooked" in col_name:
            pairs = zip(x["taxi_address"], x[col_name])
            x[col_name] = [format_taxi_isbooked(a, i) for a, i in pairs]
        if "isestimated" in col_name:
            x[col_name] = [format_isestimated(x) for x in x[col_name]]
    return x


def format_dict(x: dict, data_dict: dict) -> dict:
    """Reformat dictionary.

    Args:
        x (dict): dictionary to reformat.
        data_dict (dict): Data dictionary to labels to use, as returned by ``api.get_data_dict``.

    Returns:
        dict: A reformatted dictionary.
    """
    fields = ["participant_", "appointment_", "language_"]
    y = dict(x)
    for k, v in y.items():
        for f in fields:
            kdict = f + k
            if kdict in data_dict and v:
                y[k] = data_dict[kdict][v]
        if "exp" in k:
            y[k] = round(float(v), None) if v else ""
        if "taxi_isbooked" in k:
            y[k] = format_taxi_isbooked(y["taxi_address"], y[k])

    return y


def replace_labels(x: DataFrame | dict, data_dict: dict) -> DataFrame:
    """Replace field values with labels.

    Args:
        x (DataFrame): Pandas DataFrame in which to replace values with labels.
        data_dict (dict): Data dictionary as returned by ``get_data_dictionary``.

    Returns:
        DataFrame: A Pandas DataFrame with replaced labels.
    """  # pylint: disable=line-too-long
    if isinstance(x, DataFrame):
        return format_df(x, data_dict)
    if isinstance(x, dict):
        return format_dict(x, data_dict)
    return None


def get_age_timestamp(
    apt_records: dict, ppt_records: dict, timestamp: str = "date"
) -> tuple[str, str]:
    """Get age at timestamp in months and days.

    Args:
        apt_records (dict): Appointment records.
        ppt_records (dict): Participant records.
        timestamp (str, optional): Timestamp at which to calculate age. Defaults to "date".

    Raises:
        ValueError: If tiemstamp is not "date" or "date_created".

    Returns:
        tuple[str, str]: Age at timestamp in months and days.
    """
    if timestamp not in ["date", "date_created"]:
        raise ValueError("timestamp must be 'date' or 'date_created'")
    date_format = "%Y-%m-%d %H:%M" if timestamp == "date" else "%Y-%m-%d %H:%M:%S"
    months_new = []
    days_new = []
    for v in apt_records.values():
        if timestamp == "date_created":
            t = datetime.datetime.strptime(
                ppt_records[v.record_id].data[timestamp],
                date_format,
            )
        else:
            t = datetime.datetime.strptime(
                v.data["date"],
                "%Y-%m-%d %H:%M",
            )
        months = ppt_records[v.record_id].data["age_now_months"]
        days = ppt_records[v.record_id].data["age_now_days"]
        age_now = api.get_age(
            birth_date=api.get_birth_date(age=f"{months}:{days}"),
            timestamp=t,
        )
        months_new.append(int(age_now[0]))
        days_new.append(int(age_now[1]))
    return months_new, days_new


def get_participants_table(
    records: api.Records, data_dict: dict, n: int = None
) -> DataFrame:
    """Get participants table

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict, optional): Data dictionary as returned by ``api.get_data_dictionary``.
        n (int, optional): Number of records to show. Defaults to None (all records are shown).

    Returns:
        DataFrame: Table of partcicipants.
    """  # pylint: disable=line-too-long
    cols = [
        "record_id",
        "date_created",
        "date_updated",
        "source",
        "name",
        "age_now_months",
        "age_now_days",
        "days_since_last_appointment",
        "sex",
        "twin",
        "parent1_name",
        "parent1_surname",
        "email1",
        "phone1",
        "parent2_name",
        "parent2_surname",
        "email2",
        "phone2",
        "address",
        "city",
        "postcode",
        "birth_type",
        "gest_weeks",
        "birth_weight",
        "head_circumference",
        "apgar1",
        "apgar2",
        "apgar3",
        "hearing",
        "diagnoses",
        "comments",
    ]
    if not records.participants.records:
        return DataFrame([], columns=cols)

    new_age_months = []
    new_age_days = []
    for _, v in records.participants.records.items():
        age = api.get_age(
            birth_date=api.get_birth_date(
                age=f"{v.data['age_now_months']}:{v.data['age_now_days']}"
            )
        )
        new_age_months.append(int(age[0]))
        new_age_days.append(int(age[1]))

    df = records.participants.to_df()
    df["age_now_months"] = new_age_months
    df["age_now_days"] = new_age_days
    if n:
        df = df.tail(n)
    return replace_labels(df, data_dict)


def get_appointments_table(
    records: api.Records,
    data_dict: dict = None,
    ppt_id: str = None,
    study: str = None,
    n: int = None,
) -> DataFrame:
    """Get appointments table.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        ppt_id (str, optional): Participant ID. Defaults to None.
        study (str, optional): Study to filter for. Defaults to None.
        n (int, optional): Number of records to show. Defaults to None (all records are shown).

    Returns:
        DataFrame: Table of appointments.
    """  # pylint: disable=line-too-long
    apts = (
        records.participants.records[ppt_id].appointments
        if ppt_id
        else records.appointments
    )

    if study:
        apts.records = {
            k: v for k, v in apts.records.items() if v.data["study"] == study
        }

    if not apts.records:
        return DataFrame(
            [],
            columns=[
                "appointment_id",
                "record_id",
                "study",
                "status",
                "date",
                "date_created",
                "date_updated",
                "taxi_address",
                "taxi_isbooked",
            ],
        )
    apt_records = apts.records
    ppt_records = records.participants.records

    df = apts.to_df()
    df["appointment_id"] = df["id"]

    # get current age
    age_now = get_age_timestamp(apt_records, ppt_records, "date_created")[:n]
    df["age_now_months"] = age_now[0]
    df["age_now_days"] = age_now[1]

    # get age at appointment
    age_apt = get_age_timestamp(apt_records, ppt_records, "date")[:n]
    df["age_apt_months"] = age_apt[0]
    df["age_apt_days"] = age_apt[1]
    if n:
        df = df.tail(n)
    return replace_labels(df, data_dict)


def get_questionnaires_table(
    records: api.Records,
    data_dict: dict,
    ppt_id: str = None,
    n: int = None,
) -> DataFrame:
    """Get questionnaires table.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        ppt_id (str, optional): Participant ID. Defaults to None.
        study (str, optional): Study to filter for. Defaults to None.
        n (int, optional): Number of records to show. Defaults to None (all records are shown).

    Returns:
        DataFrame: A formated Pandas DataFrame.
    """  # pylint: disable=line-too-long
    if ppt_id is None:
        quest = records.questionnaires
    else:
        quest = records.participants.records[ppt_id].questionnaires

    if not quest.records:
        return DataFrame(
            [],
            columns=[
                "record_id",
                "questionnaire_id",
                "isestimated",
                "date_created",
                "date_updated",
                "lang1",
                "lang1_exp",
                "lang2",
                "lang2_exp",
                "lang3",
                "lang3_exp",
                "lang4",
                "lang4_exp",
            ],
        )
    df = quest.to_df()
    df["questionnaire_id"] = [
        str(p) + ":" + str(q) for p, q in zip(df.index, df["redcap_repeat_instance"])
    ]
    df = replace_labels(df, data_dict)
    if n:
        df = df.tail(n)
    return df


def count_col(
    x: DataFrame,
    col: str,
    values_sort: bool = False,
    cumulative: bool = False,
    missing_label: str = "Missing",
) -> dict:
    """Count frequencies of column in DataFrame.

    Args:
        x (DataFrame): DataFrame containing the target column.
        col (str): Name of the column.
        values_sort (str, optional): Should the resulting dict be ordered by values? Defaults to False.
        cumulative (bool, optional): Should the counts be cumulative? Defaults to False.
        missing_label (str, optional): Label to associate with missing values. Defaults to "Missing".

    Returns:
        dict: Counts of each category, sorted in descending order.
    """  # pylint: disable=line-too-long
    counts = x[col].value_counts().to_dict()
    counts = {missing_label if not k else k: v for k, v in counts.items()}
    counts = dict(sorted(counts.items()))
    if values_sort:
        counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    if cumulative:
        for idx, (k, v) in enumerate(counts.items()):
            if idx > 0:
                counts[k] = v + list(counts.values())[idx - 1]
    return counts


def clean_tmp(path: str = "tmp"):
    """Clean temporal directory

    Args:
        path (str, optional): Path to the temporal directory. Defaults to "tmp".
    """
    if os.path.exists(path):
        shutil.rmtree(path)


def prepare_email(ppt_id: str, apt_id: str, data: dict, data_dict: dict) -> dict:
    """Prepare email to send.

    Args:
        ppt_id (str): Participant ID.
        apt_id (str): Appointment ID.
        data (dict): Appointment data.

    Returns:
        dict: Email data.
    """
    email = {
        "record_id": ppt_id,
        "id": apt_id,
        "status": data["status"],
        "date": datetime.datetime.strptime(data["date"], "%Y-%m-%d %H:%M").isoformat(),
        "study": data["study"],
        "taxi_address": data["taxi_address"],
        "taxi_isbooked": data["taxi_isbooked"],
        "comments": data["comments"],
    }
    return replace_labels(email, data_dict)


if os.name == "nt":

    def send_email_or_exception(email_from: str, **kwargs) -> None:
        """Try sending an email or catch the exception.

        Args:
            **kwargs: Arguments passed to ``prepare_email``.
        """
        try:
            data = prepare_email(**kwargs)
            outlook.send_email(data=data, email_from=email_from)
        except outlook.MailDomainException as e:
            flash(f"Appointment modified, but e-mail was not sent: {e}", "warning")
            return render_template("apt_new.html", **kwargs)
        except outlook.MailAddressException as e:
            flash(f"Appointment modified, but e-mail was not sent: {e}", "warning")
            return render_template("apt_new.html", **kwargs)
        return None

    def create_event_or_exception(account: str, calendar_name: str, **kwargs) -> None:
        """Try creating and email or catch the exception.

        Args:
            **kwargs: Arguments passed to ``prepare_email``.
        """
        try:
            data = prepare_email(**kwargs)
            outlook.create_event(
                data=data, account=account, calendar_name=calendar_name
            )
        except outlook.MailDomainException as e:
            flash(f"Appointment created, but event was not created: {e}", "warning")
            return render_template("apt_new.html", **kwargs)
        except outlook.MailAddressException as e:
            flash(f"Appointment created, but event was not created: {e}", "warning")
            return render_template("apt_new.html", **kwargs)
        return None

    def modify_event_or_exception(account: str, calendar_name: str, **kwargs) -> None:
        """Try modifying and email or catch the exception.

        Args:
            **kwargs: Arguments passed to ``prepare_email``.
        """
        try:
            data = prepare_email(**kwargs)
            outlook.modify_event(
                data=data, account=account, calendar_name=calendar_name
            )
        except outlook.MailDomainException as e:
            flash(f"Appointment modified, but event was not created: {e}", "warning")
            return render_template("apt_new.html", **kwargs)
        except outlook.MailAddressException as e:
            flash(f"Appointment modified, but event was not created: {e}", "warning")
            return render_template("apt_new.html", **kwargs)
        return None
