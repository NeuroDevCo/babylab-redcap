"""Participants routes."""

import datetime
import requests
from flask import flash, redirect, render_template, url_for, request
from babylab.src import api, utils
from babylab.app import config as conf


def prepare_participants(records: api.Records, data_dict: dict, **kwargs) -> dict:
    """Prepare data for participants page.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        data_dict (dict): Data dictionary as returned by ``api.get_data_dictionary``.
        **kwargs: Extra arguments passed to ``get_participants_table``.

    Returns:
        dict: Parameters for the participants endpoint.
    """  # pylint: disable=line-too-long
    df = utils.get_participants_table(records, data_dict=data_dict, **kwargs)
    classes = "table table-hover table-responsive"
    df["record_id"] = [utils.format_ppt_id(i) for i in df.index]
    df.index = df.index.astype(int)
    df = df.sort_index(ascending=False)
    df["modify_button"] = [utils.format_modify_button(p) for p in df.index]
    df = df[
        [
            "record_id",
            "name",
            "age_now_months",
            "age_now_days",
            "sex",
            "source",
            "email1",
            "email2",
            "phone1",
            "phone2",
            "date_created",
            "date_updated",
            "comments",
            "modify_button",
        ]
    ]
    df = df.rename(
        columns={
            "record_id": "Participant",
            "name": "Name",
            "age_now_months": "Age (months)",
            "age_now_days": "Age (days)",
            "sex": "Sex",
            "source": "Source",
            "phone1": "Phone 1",
            "phone2": "Phone 2",
            "email1": "E-mail 1",
            "email2": "E-mail 2",
            "date_created": "Added on",
            "date_updated": "Last updated",
            "comments": "Comments",
            "modify_button": "",
        }
    )
    return {
        "table": df.to_html(
            classes=f'{classes}" id = "ppttable',
            escape=False,
            justify="left",
            index=False,
            bold_rows=True,
        )
    }


def prepare_record_id(
    records: api.Records, data_dict: dict, ppt_id: str, **kwargs
) -> dict:
    """Prepare record ID page.

    Args:
        records (api.Records): REDCap records, as returned by ``api.Records``.
        ppt_id (str, optional): Participant ID. Defaults to None.
        **kwargs: Extra arguments passed to ``get_participants_table``, ``get_appointments_table``, and ``get_questionnaires_table``

    Returns:
        dict: Parameters for the participants endpoint.
    """  # pylint: disable=line-too-long
    data = records.participants.records[ppt_id].data
    for k, v in data.items():
        kdict = "participant_" + k
        if kdict in data_dict:
            data[k] = data_dict[kdict][v] if v else ""
    data["age_now_months"] = (
        str(data["age_now_months"]) if data["age_now_months"] else ""
    )
    data["age_now_days"] = str(data["age_now_days"]) if data["age_now_days"] else ""
    data["parent1"] = data["parent1_name"] + " " + data["parent1_surname"]
    data["parent2"] = data["parent2_name"] + " " + data["parent2_surname"]

    classes = "table table-hover table-responsive"

    # prepare participants table
    df_appt = utils.get_appointments_table(
        records, data_dict=data_dict, ppt_id=ppt_id, **kwargs
    )
    df_appt["record_id"] = [utils.format_ppt_id(i) for i in df_appt.index]
    df_appt["appointment_id"] = [
        utils.format_apt_id(i) for i in df_appt["appointment_id"]
    ]
    df_appt = df_appt.sort_values(by="date", ascending=False)
    df_appt = df_appt[
        [
            "record_id",
            "appointment_id",
            "study",
            "date",
            "date_created",
            "date_updated",
            "taxi_address",
            "taxi_isbooked",
            "status",
        ]
    ]
    df_appt = df_appt.rename(
        columns={
            "record_id": "Participant",
            "appointment_id": "Appointment",
            "study": "Study",
            "date": "Date",
            "date_created": "Made on the",
            "date_updated": "Last update",
            "taxi_address": "Taxi address",
            "taxi_isbooked": "Taxi booked",
            "status": "Status",
        }
    )
    table_appt = df_appt.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    # prepare language questionnaires table
    df_quest = utils.get_questionnaires_table(
        records, data_dict=data_dict, ppt_id=ppt_id
    )
    df_quest["questionnaire_id"] = [
        utils.format_que_id(p, q)
        for p, q in zip(df_quest.index, df_quest["questionnaire_id"])
    ]
    df_quest["record_id"] = [utils.format_ppt_id(i) for i in df_quest.index]
    df_quest = df_quest[
        [
            "questionnaire_id",
            "record_id",
            "lang1",
            "lang1_exp",
            "lang2",
            "lang2_exp",
            "lang3",
            "lang3_exp",
            "lang4",
            "lang4_exp",
            "date_created",
            "date_updated",
        ]
    ]
    df_quest = df_quest.sort_values("date_created", ascending=False)
    df_quest = df_quest.rename(
        columns={
            "record_id": "ID",
            "questionnaire_id": "Questionnaire",
            "date_updated": "Last updated",
            "date_created": "Created on the:",
            "lang1": "L1",
            "lang1_exp": "%",
            "lang2": "L2",
            "lang2_exp": "%",
            "lang3": "L3",
            "lang3_exp": "%",
            "lang4": "L4",
            "lang4_exp": "%",
        }
    )

    table_quest = df_quest.to_html(
        classes=classes,
        escape=False,
        justify="left",
        index=False,
        bold_rows=True,
    )

    return {
        "data": data,
        "table_appointments": table_appt,
        "table_questionnaires": table_quest,
    }


def participants_routes(app):
    """Participants routes."""

    @app.route("/participants/")
    @conf.token_required
    def ppt_all(
        ppt_options: list[str] = None,
        data_ppt: dict = None,
        records: api.Records = None,
        n: int = None,
    ):
        """Participants database"""
        token = app.config["API_KEY"]
        if records is None:
            records = conf.get_records_or_index(token=token)
        data_dict = api.get_data_dict(token=token)
        data = prepare_participants(records, data_dict=data_dict, n=n)
        if ppt_options is None:
            ppt_options = list(records.participants.to_df().index)
            ppt_options = [int(x) for x in ppt_options]
            ppt_options.sort(reverse=True)
            ppt_options = [str(x) for x in ppt_options]

        return render_template(
            "ppt_all.html",
            ppt_options=ppt_options,
            data=data,
            data_dict=data_dict,
            data_ppt=data_ppt,
            n_ppt=len(records.participants.records),
            records=records,
        )

    @app.route("/participants/<string:ppt_id>", methods=["GET", "POST"])
    @conf.token_required
    def ppt(ppt_id: str, records: api.Records = None):
        """Show the ppt_id for that participant"""
        token = app.config["API_KEY"]
        data_dict = api.get_data_dict(token=token)
        if records is None:
            records = conf.get_records_or_index(token=token)
        data = prepare_record_id(records, data_dict, ppt_id)
        if request.method == "POST":
            try:
                api.delete_participant(
                    data={"record_id": ppt_id},
                    token=app.config["API_KEY"],
                )
                flash("Participant deleted!", "success")
                records = conf.get_records_or_index(token=token)
                return redirect(url_for("ppt_all", records=records))
            except requests.exceptions.HTTPError as e:
                flash(f"Something went wrong! {e}", "error")
                return redirect(url_for("ppt_all"))
        return render_template(
            "ppt.html",
            ppt_id=ppt_id,
            data=data,
        )

    @app.route("/participant_new", methods=["GET", "POST"])
    @conf.token_required
    def ppt_new():
        """New participant page"""
        data_dict = api.get_data_dict(token=app.config["API_KEY"])
        if request.method == "POST":
            finput = request.form
            date_now = datetime.datetime.strftime(
                datetime.datetime.now(), "%Y-%m-%d %H:%M"
            )
            data = {
                "record_id": "0",
                "participant_date_created": date_now,
                "participant_date_updated": date_now,
                "participant_source": finput["inputSource"],
                "participant_name": finput["inputName"],
                "participant_age_now_months": finput["inputAgeMonths"],
                "participant_age_now_days": finput["inputAgeDays"],
                "participant_sex": finput["inputSex"],
                "participant_twin": finput["inputTwinID"],
                "participant_parent1_name": finput["inputParent1Name"],
                "participant_parent1_surname": finput["inputParent1Surname"],
                "participant_parent2_name": finput["inputParent2Name"],
                "participant_parent2_surname": finput["inputParent2Surname"],
                "participant_email1": finput["inputEmail1"],
                "participant_phone1": finput["inputPhone1"],
                "participant_email2": finput["inputEmail2"],
                "participant_phone2": finput["inputPhone2"],
                "participant_address": finput["inputAddress"],
                "participant_city": finput["inputCity"],
                "participant_postcode": finput["inputPostcode"],
                "participant_birth_type": finput["inputDeliveryType"],
                "participant_gest_weeks": finput["inputGestationalWeeks"],
                "participant_birth_weight": finput["inputBirthWeight"],
                "participant_head_circumference": finput["inputHeadCircumference"],
                "participant_apgar1": finput["inputApgar1"],
                "participant_apgar2": finput["inputApgar2"],
                "participant_apgar3": finput["inputApgar3"],
                "participant_hearing": finput["inputNormalHearing"],
                "participant_diagnoses": finput["inputDiagnoses"],
                "participant_comments": finput["inputComments"],
                "participants_complete": "2",
            }
            try:
                api.add_participant(
                    data,
                    modifying=False,
                    token=app.config["API_KEY"],
                )
                flash("Participant added!", "success")
                records = conf.get_records_or_index(token=app.config["API_KEY"])
                return redirect(url_for("ppt_all", records=records))
            except requests.exceptions.HTTPError as e:
                flash(f"Something went wrong! {e}", "error")
                return redirect(url_for("ppt_new", data_dict=data_dict))
        return render_template("ppt_new.html", data_dict=data_dict)

    @app.route(
        "/participants/<string:ppt_id>/participant_modify", methods=["GET", "POST"]
    )
    @conf.token_required
    def ppt_modify(
        ppt_id: str,
        data: dict = None,
    ):
        """Modify participant page"""
        data_dict = api.get_data_dict(token=app.config["API_KEY"])
        data = (
            api.Records(token=app.config["API_KEY"]).participants.records[ppt_id].data
        )
        if request.method == "POST":
            finput = request.form
            date_now = datetime.datetime.strftime(
                datetime.datetime.now(), "%Y-%m-%d %H:%M"
            )
            data = {
                "record_id": ppt_id,
                "participant_date_updated": date_now,
                "participant_name": finput["inputName"],
                "participant_age_now_months": finput["inputAgeMonths"],
                "participant_age_now_days": finput["inputAgeDays"],
                "participant_sex": finput["inputSex"],
                "participant_source": finput["inputSource"],
                "participant_twin": finput["inputTwinID"],
                "participant_parent1_name": finput["inputParent1Name"],
                "participant_parent1_surname": finput["inputParent1Surname"],
                "participant_parent2_name": finput["inputParent2Name"],
                "participant_parent2_surname": finput["inputParent2Surname"],
                "participant_email1": finput["inputEmail1"],
                "participant_phone1": finput["inputPhone1"],
                "participant_email2": finput["inputEmail2"],
                "participant_phone2": finput["inputPhone2"],
                "participant_address": finput["inputAddress"],
                "participant_city": finput["inputCity"],
                "participant_postcode": finput["inputPostcode"],
                "participant_birth_type": finput["inputDeliveryType"],
                "participant_gest_weeks": finput["inputGestationalWeeks"],
                "participant_birth_weight": finput["inputBirthWeight"],
                "participant_head_circumference": finput["inputHeadCircumference"],
                "participant_apgar1": finput["inputApgar1"],
                "participant_apgar2": finput["inputApgar2"],
                "participant_apgar3": finput["inputApgar3"],
                "participant_hearing": finput["inputNormalHearing"],
                "participant_diagnoses": finput["inputDiagnoses"],
                "participant_comments": finput["inputComments"],
                "participants_complete": "2",
            }
            try:
                api.add_participant(
                    data,
                    modifying=True,
                    token=app.config["API_KEY"],
                )
                flash("Participant modified!", "success")
                return redirect(url_for("ppt", ppt_id=ppt_id))
            except requests.exceptions.HTTPError as e:
                flash(f"Something went wrong! {e}", "error")
                return render_template(
                    "ppt_modify.html", ppt_id=ppt_id, data=data, data_dict=data_dict
                )
        return render_template(
            "ppt_modify.html", ppt_id=ppt_id, data=data, data_dict=data_dict
        )
